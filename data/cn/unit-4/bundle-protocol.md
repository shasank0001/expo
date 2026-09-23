---
subject: cn
unit: 4
topic: bundle-protocol
syllabus_ref: CSM3103 Unit-IV
status: draft
---
# Bundle Protocol

## Overview

The **Bundle Protocol** is the main overlay protocol used in Delay-Tolerant Networking. It carries an application payload and delivery information as a durable **bundle**. Unlike an IP packet, a bundle may be large, stored for a long time, fragmented, replicated, and forwarded through intermittent links.

A bundle header identifies the source, destination, creation time, lifetime, service requirements, and processing flags. The protocol defines fragmentation and reassembly, custody transfer, delivery reporting, duplicate handling, and security options so a message can progress through a store-carry-forward network.

The syllabus includes the Bundle Protocol after DTN architecture. This file explains bundle structure, header fields, endpoint identifiers, fragmentation, custody, delivery options, security, congestion/resource issues, and worked examples.

## Explanation

### 1. Bundle concept

A bundle is a protocol data unit for DTN. It contains:

- a bundle header;
- optional extension blocks and security fields;
- an application payload;
- optional previous-hop or custody information;
- integrity information.

A bundle is not required to fit in one IP packet or one radio contact. A node can store it until a suitable opportunity, transfer custody to a relay, and fragment it if a link can carry only a small unit.

A bundle has a lifecycle and identity. It is created by an application, routed through a DTN overlay, delivered to an endpoint, and eventually deleted or expired according to policy.

### 2. Bundle header

A conceptual header contains the following types of information:

- **version:** protocol format;
- **creation timestamp:** when the bundle was created;
- **sequence number:** creation order at the source;
- **lifetime:** how long the bundle should remain useful;
- **destination endpoint identifier:** where it should be delivered;
- **source endpoint identifier:** where it originated;
- **priority:** relative service or handling importance;
- **flags:** delivery, custody, fragmentation, and processing options;
- **service class:** requested handling behaviour.

The exact wire format and field encodings depend on the protocol version. An exam answer should explain the purpose of each field rather than pretend every implementation has identical bit positions.

### 3. Endpoint identifiers and naming

An endpoint identifier names a DTN endpoint, such as a node, application, or group. It may be expressed as a URI-like name such as:

`dtn://region/node/application`

The name is resolved by a delay-tolerant naming service. It need not be a currently reachable IP address. A destination can be offline when the bundle is created and receive it much later.

A group endpoint can be used for multicast or broadcast-like delivery, but membership, authorisation, and duplicate handling become more complex.

### 4. Bundle creation and delivery options

The source application creates a bundle and requests options such as:

- delivery notification;
- return receipt;
- custody transfer;
- delete after delivery;
- priority;
- expiration/lifetime;
- end-to-end encryption;
- application-level processing flags.

Options affect the protocol's state and resource use. A request for a delivery report creates an acknowledgement that may itself wait for a future contact. A long lifetime increases storage and forwarding probability but also keeps sensitive data longer.

### 5. Fragmentation

A bundle can be larger than the maximum transmission unit of a DTN contact. **Fragmentation** divides a bundle into smaller **fragment bundles**, each of which carries a fragment identifier and a reassembly rule. A fragment may itself be fragmented if necessary.

The destination or an intermediate bundle-protocol agent collects fragments, identifies the parent bundle, waits until all required fragments arrive, verifies integrity, and reassembles the payload. Missing fragments can be requested when a reverse opportunity exists.

Fragmentation has costs: additional headers, storage, reassembly memory, and vulnerability to losing one fragment. A protocol may duplicate or prioritise fragments, but a large bundle over a fragile link can be inefficient.

### 6. Reassembly and duplicate detection

Every bundle has an identifier, often derived from source endpoint and creation information. A fragment also carries a parent identifier and fragment sequence or offset. A receiver can distinguish:

- a new bundle;
- a fragment of a known bundle;
- a duplicate of a previously received fragment;
- a fragment that belongs to a different source or version.

Duplicate suppression avoids applying a payload twice. If delivery reports are lost, retransmission may create duplicates even when the original payload arrived.

### 7. Custody transfer

**Custody transfer** is a core Bundle Protocol mechanism. A sender or relay holding a bundle can transfer custody to the next node. The receiving node accepts responsibility for storing and forwarding it.

A custody transfer may be acknowledged to confirm that the next node has assumed responsibility. If custody is not accepted, the current node may retain a copy and try another route. Custody is not the same as a route reservation; it is a protocol-level responsibility handoff.

Custody helps ensure that a bundle is not simply copied into a volatile mobile contact and lost when the node moves. It also creates a possible resource burden: a node that accepts custody must store the bundle until it can forward or deliver it.

### 8. Store, carry, and forward

The protocol is used in a store-carry-forward network:

1. A node receives a bundle and checks its header and integrity.
2. It stores the bundle durably.
3. It waits for a contact or route opportunity.
4. It may fragment the bundle and transfer custody.
5. The next node repeats the process.
6. A destination or gateway delivers the payload and optionally reports success.

Because contacts are intermittent, forwarding decisions may be made from expected next-contact information, energy, priority, and storage. A node can use multiple routes or retain a copy for reliability.

### 9. Delivery report and acknowledgement

A delivery report can confirm that a bundle reached a gateway or destination. Reports are themselves bundles and may have to wait for a future opportunity. If a report is lost, the source may resend the payload or request the report again. The destination uses bundle identifiers to recognise duplicates.

A custody acknowledgement says a relay has accepted responsibility; a delivery report says the payload reached its intended delivery point. They answer different questions and should not be conflated.

### 10. Security blocks

The Bundle Protocol can carry security-related information, such as:

- source authentication;
- payload integrity;
- destination or intermediary authentication;
- encryption of the payload;
- signatures over selected blocks;
- certificates or key metadata;
- replay counters or timestamps.

A signature can protect authenticity and integrity, while encryption protects confidentiality. Encrypting only the payload can leave routing headers readable, which may be desirable for forwarding but exposes metadata. A long-lived bundle may need key updates or revocation handling.

### 11. Congestion and resource control

DTN nodes can experience **bundle congestion** when more bundles are stored than the node can retain or forward. The protocol may use:

- priority and lifetime;
- storage quotas;
- bundle dropping;
- replication policies;
- forward-error or erasure coding;
- admission control;
- selective delivery;
- delegation of custody.

A high-priority emergency bundle may displace a large scientific bundle. A node must balance durability, energy, and future opportunity. Ordinary IP congestion control is not automatically sufficient because links are intermittent and storage is persistent.

### 12. Bundle versus IP packet

| Property | Bundle | IP packet |
|---|---|---|
| Lifetime | Can wait for long periods | Usually short forwarding state |
| Size | May be large and fragmented | Usually bounded by path MTU |
| Unit of forwarding | Bundle/fragment with custody | Packet |
| Storage | Persistent often required | Router buffer normally temporary |
| Destination | DTN endpoint identifier | IP address/prefix |
| Delivery options | Custody/report/priority | Best effort by default |
| Failure assumption | Intermittent link acceptable | Route generally expected |

The Bundle Protocol is an overlay; it can run over IP but changes the persistence and delivery model.

## Worked examples

### Example 1: Header and custody

A rover creates a bundle addressed to a ground application, with a 30-day lifetime and a delivery report requested. The rover stores it until a satellite contact. It transfers custody to a relay; the relay ACKs custody and stores the bundle until the next contact to the ground gateway.

### Example 2: Fragmentation

A 100-kilobyte scientific bundle encounters a narrow link with a 5-kilobyte maximum. The relay fragments it into 20 or more bundle fragments, each with a parent identifier. The destination stores fragments, detects one missing fragment, and requests it when a return contact becomes available.

### Example 3: Duplicate delivery

The destination receives and processes a bundle, but its report is lost. The source later retransmits it. The destination sees the same bundle identifier, recognises the duplicate, and suppresses a second application action.

### Example 4: Security

A medical bundle contains encrypted patient data and a source signature. A relay can verify that the source signed the payload and that it was not modified, but cannot read the patient data unless authorised. The encryption and signature add headers, so the bundle may need more fragments.

### Example 5: Storage pressure

A low-priority weather bundle fills a sensor's storage. A later high-priority alert arrives. The node keeps the alert, drops or compresses the old bundle according to policy, and forwards the alert at the next contact. A protocol-specific congestion policy is needed.

## Key terms & formulas

- **Bundle Protocol:** DTN overlay protocol.
- **Bundle:** durable DTN protocol data unit.
- **Endpoint identifier:** logical source/destination name.
- **Creation timestamp:** time bundle was created.
- **Lifetime:** expiry duration.
- **Sequence number:** source creation order.
- **Priority:** relative handling/service importance.
- **Fragment:** smaller bundle carrying part of a parent.
- **Parent identifier:** identifies the original bundle for reassembly.
- **Custody transfer:** transfer responsibility for storing/forwarding.
- **Custody ACK:** confirms custody acceptance.
- **Delivery report:** confirms delivery to a target/gateway.
- **Duplicate suppression:** prevent repeated bundle application.
- **Security block:** signature, encryption, or authentication metadata.
- **Bundle congestion:** persistent storage/forwarding overload.
- **Store-carry-forward:** wait, retain, and send at a later opportunity.
- **Fragment count:** approximately `ceil(bundle payload / maximum fragment payload)`, excluding headers.
- **Bundle TTL example:** creation time + lifetime defines expiry.

## Common mistakes

1. **A bundle is not an IP packet.** It may be persistent, large, delayed, and fragmented.
2. **A bundle header does more than contain source/destination.** It includes lifetime, sequence, priority, and options.
3. **Custody is not delivery.** It transfers responsibility, not necessarily arrival at the final endpoint.
4. **Fragmentation is not ordinary IP fragmentation.** Bundle fragments carry DTN identity and reassembly information.
5. **Reassembly requires all required fragments.** A missing fragment can block the parent payload.
6. **A delivery report is itself delayed.** It may wait for a future DTN opportunity.
7. **A duplicate can be caused by a lost report.** Identity fields are needed to suppress it.
8. **A signature is not encryption.** One authenticates/integrity-protects; the other provides confidentiality.
9. **DTN congestion is not only link congestion.** Persistent storage and energy can be bottlenecks.
10. **Bundle protocol does not guarantee every bundle arrives.** Lifetime, storage, contacts, and failure determine delivery.
11. **Endpoint identifiers are not necessarily IP addresses.** They can name offline DTN applications or groups.

## Exam prep

### Likely 2-mark questions

1. **What is a bundle?**  
   Hint: durable DTN message containing payload, header, and delivery/control information.
2. **List four bundle-header fields and their purposes.**  
   Hint: source, destination, creation time, lifetime, sequence, priority, or flags.
3. **Why is fragmentation needed?**  
   Hint: a bundle may exceed the capacity of an intermittent link or contact.
4. **Define custody transfer.**  
   Hint: hand responsibility for storing/forwarding a bundle to another node.
5. **Differentiate a delivery report from a custody ACK.**  
   Hint: delivery confirmation versus responsibility-transfer confirmation.
6. **What is a DTN endpoint identifier?**  
   Hint: a logical name for a possibly offline source or destination.

### Likely long-answer questions

1. **Explain the Bundle Protocol header and lifecycle.**  
   Answer hint: create, identify, store, route, custody, deliver, report, and delete/expire.
2. **How does fragmentation and reassembly work?**  
   Answer hint: parent ID, fragment sequence/offset, size limit, missing fragment, reassembly, and duplicate handling.
3. **Compare Bundle Protocol with IP packet forwarding.**  
   Answer hint: persistent state, intermittent links, custody, endpoint naming, and fragmentation.
4. **Explain security and resource management for bundles.**  
   Answer hint: signature/encryption, metadata, storage quotas, priority, lifetime, and energy.
5. **Trace a bundle from a rover through a satellite relay to a gateway.**  
   Answer hint: store, wait, custody, contact, forward, report, and destination delivery.

### Short-answer revision checklist

Be able to name at least eight header fields, explain fragmentation and reassembly, distinguish custody from delivery, and contrast a bundle with an IP packet.
