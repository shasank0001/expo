---
subject: cn
unit: 4
topic: dtn-architecture
syllabus_ref: CSM3103 Unit-IV
status: draft
---
# Delay-Tolerant Networking Architecture

## Overview

**Delay-tolerant networking (DTN)** supports communication over links that are slow, intermittent, expensive, or frequently unavailable. Ordinary Internet protocols usually assume that an end-to-end route is available and that losses are temporary. A DTN instead allows a node to store a message, wait for an opportunity, carry it across a disconnected network, and deliver it later.

The central operation is **store-carry-forward**: receive and store a bundle, carry it physically or logically, then forward it when a link becomes available. DTN gateways connect unlike network technologies, and custody rules specify which node is responsible for a bundle at a time.

DTN is useful in deep-space communication, sensor networks, disaster response, military networks, remote monitoring, and intermittent mobile links. It trades delay and storage for reachability. The syllabus includes DTN architecture and the Bundle Protocol, so this file explains the architecture, gateways, naming, custody, security, resources, and delivery semantics.

## Explanation

### 1. Why ordinary Internet assumptions fail

IP forwarding is designed for a connected path and short-lived packet state. A router normally forwards a packet immediately or discards it if there is no usable route. It does not promise to wait hours for a satellite, mobile device, or damaged link to come back.

DTN relaxes these assumptions:

- links may be unavailable for long periods;
- nodes may be offline or have limited energy;
- messages may be large or require long lifetimes;
- network topology and opportunity can change;
- a path may consist of several disconnected segments;
- delivery may be delayed more than ordinary latency budgets allow.

A DTN is therefore an **opportunistic** network: a node uses whatever communication opportunity is currently available.

### 2. Store-carry-forward

The **store-carry-forward** model has three actions:

1. **Store:** a node receives a bundle and keeps it durably.
2. **Carry:** the node retains the bundle while moving or waiting.
3. **Forward:** when a contact or usable link appears, the node sends the bundle onward.

Store-and-forward is different from simply copying a packet. A node assumes responsibility for preserving data until a later opportunity, may need power management, and may need to decide when to delete or regenerate a copy.

A rover can store a report in nonvolatile memory, drive to a location with a satellite contact, and send the report to a gateway. The gateway forwards it over the Internet when the rover is offline.

### 3. DTN architecture components

A DTN architecture can include:

- **source and destination applications;**
- **DTN nodes or routers;**
- **gateways** between DTN and conventional networks;
- **bundle protocol;**
- **custody transfer and delivery mechanisms;**
- **delay-tolerant naming;**
- **storage, energy, and scheduling policy;**
- **security services;**
- **opportunistic contact scheduling.**

The Bundle Protocol is the main data-unit protocol specified by the DTN architecture. Other components may use it as an overlay over IP, Ethernet, serial links, or other transports.

### 4. Gateways

A **gateway** connects a DTN to an ordinary IP network or to another DTN technology. It can translate between a bundle and a conventional packet, route bundles across heterogeneous links, and act as an application endpoint.

A gateway may have an always-on connection to the Internet while the remote sensor has only intermittent contact. The gateway stores incoming bundles, forwards them over the available DTN link, and delivers ordinary IP traffic to the appropriate host.

A gateway is not necessarily a router in the ordinary IP sense. It may need persistent storage, application protocols, delay-tolerant naming, and a different delivery model.

### 5. Delay-tolerant naming

An end-to-end name identifies a destination that may be temporarily unreachable. A DTN can use an endpoint identifier such as `dtn://region/node/application` and resolve it through a naming or directory service.

The name need not be an IP address. It may identify a logical application or a group and can be resolved when the destination becomes reachable. Naming must support uniqueness, delegation, security, and possibly late binding.

A bundle can be addressed to an individual node or a named group. Custody and delivery reports are associated with the bundle and its endpoint.

### 6. Custody transfer

**Custody transfer** moves responsibility for a bundle from one node to another. A sender can transfer custody to a relay; the relay becomes responsible for storing and forwarding it. The previous node may retain a record or delete its copy according to the protocol and policy.

Custody supports reliable progress in a disconnected network, but it needs transfer rules, acknowledgements, and protection against conflicting custody. A node must know whether it is responsible for a bundle, how long it must retain it, and how to report a transfer.

### 7. Bundle delivery lifecycle

A typical lifecycle is:

1. An application creates a bundle with an endpoint, lifetime, payload, and delivery options.
2. A source DTN router stores it and waits for a route/contact.
3. Custody is transferred to a relay.
4. The relay waits for a next opportunity and forwards the bundle.
5. A gateway or destination stores and delivers it.
6. A delivery report may be returned when possible.

Delivery can be duplicated if reports are lost. Bundle identifiers, custody, and duplicate-delivery policies help the destination recognise a repeated bundle.

### 8. Storage and resource management

DTN nodes may have limited storage, energy, bandwidth, and duty cycles. A node must decide:

- which bundles to retain;
- which bundle to forward first;
- when to delete a delivered or expired bundle;
- whether to keep a copy after custody transfer;
- how to handle a very large bundle;
- how to survive reboot or power loss.

Storage durability matters because the next contact may be hours or days away. A bundle can be lost if a node fails before forwarding it. Replication can improve reliability but consumes storage and energy.

### 9. Intermittent connectivity and contacts

DTN opportunities can be described by:

- contact duration;
- expected next contact;
- bandwidth;
- latency;
- energy cost;
- probability of success;
- directionality.

A node may schedule a large scientific bundle for a long, high-bandwidth satellite contact and use short, low-rate radio contacts for small urgent messages. The routing algorithm can be store-and-forward and opportunity-aware.

A contact may be scheduled in advance or discovered opportunistically. A DTN can use satellite, Wi-Fi, cellular, acoustic, or other links as long as the bundle protocol can run over them.

### 10. Security and privacy

A bundle may contain sensitive scientific, medical, military, or personal information. Security can include:

- source authentication;
- integrity protection;
- encryption;
- endpoint and custody authorisation;
- replay protection;
- secure storage;
- gateway access control.

Encryption can increase size, processing, and key-management cost. DTN delay means a revocation or key update may arrive after a bundle has been stored. Security policy must account for long lifetimes and disconnected operation.

### 11. Quality of service and delivery options

Different bundles need different delivery guarantees. A DTN can support options such as:

- best effort;
- delivery notification;
- custody transfer;
- delete-after-delivery;
- priority;
- lifetime/expiry;
- group destination;
- return receipt.

A scientific measurement may prefer reliable custody and a report. A low-priority environmental reading may tolerate loss to save energy. The protocol should not promise a delivery time when the next contact is unknown.

### 12. DTN versus ordinary IP

| Property | Ordinary IP | DTN |
|---|---|---|
| Basic unit | Packet/datagram | Bundle/message |
| Basic operation | Forward immediately | Store, carry, forward |
| Connectivity | Assumes a route | Accepts intermittent links |
| State | Short-lived | Persistent and durable |
| Addressing | Usually IP prefix | DTN endpoint naming |
| Delivery | Best effort | Custody/notification options |
| Long delay | Usually exception | Normal operating condition |

DTN is not a faster replacement for IP. It is an overlay or architecture for environments where IP's assumptions do not fit.

## Worked examples

### Example 1: Deep-space rover

The rover generates a scientific bundle, stores it while moving, and waits for a scheduled satellite contact. It transfers custody to a gateway and the gateway forwards the bundle to a ground station over the Internet. The rover need not remain continuously connected.

### Example 2: Disaster relay

A sensor in a damaged area has intermittent contact with a drone. The drone stores a bundle, carries it to a reachable base station, and forwards it when a link opens. A different drone can relay the bundle if the first loses power.

### Example 3: Opportunistic routing

A mobile device has contacts with Wi-Fi at home, cellular at work, and an intermittent satellite link. It sends a large bundle over the faster available contact and waits for a small acknowledgement over a later opportunity.

### Example 4: Delivery duplicate

A destination receives a bundle but the delivery report is lost. The sender retransmits during the next contact. The destination uses the bundle identifier to recognise the duplicate and avoids applying the payload twice.

### Example 5: Resource choice

A battery-powered node receives a large image and a short alert. It stores the alert and forwards it during a short radio contact. It retains the image until a high-bandwidth link or a later contact, because a large bundle may not fit the low-rate opportunity.

## Key terms & formulas

- **DTN:** Delay-Tolerant Networking.
- **Store-carry-forward:** store a bundle, carry it, forward when possible.
- **Bundle:** DTN protocol data unit.
- **Gateway:** bridge between DTN and another network.
- **Custody transfer:** transfer responsibility for a bundle.
- **DTN endpoint identifier:** logical destination name.
- **Intermittent link:** available only during some opportunities.
- **Contact:** a period when two nodes can communicate.
- **Delivery report:** confirmation returned when possible.
- **Bundle lifetime:** period before expiry.
- **Persistent storage:** durable storage for delayed forwarding.
- **Duplicate delivery:** repeated arrival of the same bundle.
- **Opportunistic routing:** choose among available future contacts.
- **DTN overlay:** runs over one or more ordinary networks.
- **Bundle size:** may exceed a single network packet and require fragmentation.

## Common mistakes

1. **DTN is not ordinary IP with a longer delay.** It changes the basic unit and forwarding process.
2. **Store-and-forward is not immediate forwarding.** A node may wait for a future contact.
3. **Carry means more than copying.** The node retains the bundle while moving or waiting.
4. **A DTN does not require a continuously connected end-to-end path.** That is its defining assumption.
5. **Custody is not the same as delivery.** Custody is responsibility; delivery is arrival at the destination.
6. **A gateway is not automatically an IP router.** It may translate protocols and store data durably.
7. **DTN endpoint names are not necessarily IP addresses.** They can identify offline or logical destinations.
8. **DTN does not guarantee delivery.** Link opportunity, storage, lifetime, and failure matter.
9. **Long delay makes security and power management harder.** Revocation and durable storage need planning.
10. **A bundle can be larger than an IP packet.** Fragmentation and reassembly are often needed.

## Exam prep

### Likely 2-mark questions

1. **Explain store-carry-forward.**  
   Hint: store a bundle, retain it while waiting/moving, and forward at a later opportunity.
2. **What is a DTN gateway?**  
   Hint: bridge between a DTN and a conventional or different network.
3. **What is custody transfer?**  
   Hint: transfer responsibility for storage/forwarding a bundle to another node.
4. **Give one situation where DTN is useful.**  
   Hint: satellite, sensor, disaster, or intermittent mobile link.
5. **What is a DTN endpoint identifier?**  
   Hint: a logical name for a possibly offline destination.
6. **Differentiate DTN from ordinary IP forwarding.**  
   Hint: persistent bundle storage/waiting versus immediate best-effort packet forwarding.

### Likely long-answer questions

1. **Explain the DTN architecture and its store-carry-forward operation.**  
   Answer hint: bundles, storage, contacts, gateways, naming, custody, delivery, and intermittent links.
2. **Compare DTN and ordinary Internet architecture.**  
   Answer hint: assumptions, unit, forwarding, state, addressing, delay, and delivery options.
3. **Explain resource management and security in a battery-powered DTN.**  
   Answer hint: storage, energy, contact scheduling, encryption, authentication, and long lifetimes.
4. **Trace a bundle from a rover to an application through a gateway.**  
   Answer hint: create, store, custody, satellite contact, forward, deliver, and report.

### Short-answer revision checklist

Be ready to define DTN, store-carry-forward, bundle, gateway, custody, and endpoint identifier, and give one contrast with IP.
