---
subject: cn
unit: 5
topic: electronic-mail
syllabus_ref: CSM3103 Unit-V
status: draft
---
# Electronic Mail

## Overview

**Electronic mail (email)** is a store-and-forward application that carries messages between users through a network of mail servers. A sender's mail user agent submits a message to a mail server. The server stores and relays it, possibly over several hops, until it reaches the recipient's mailbox. A mail-reading protocol then lets the recipient access it.

SMTP handles submission and transfer between mail servers, while IMAP and POP3 are common protocols for retrieving mail. MIME extends the basic mail format to carry attachments, non-ASCII text, images, audio, and other media. Real email also needs DNS, authentication, encryption, spam filtering, retries, and delivery reporting.

Email is store-and-forward rather than a direct connection between two people. A sender and recipient do not have to be online at the same time. This makes email robust, but it creates queues, delayed delivery, duplicate handling, security, and privacy issues.

## Explanation

### 1. Email architecture

The main components are:

- **Mail user agent (MUA):** the application used to compose, read, and manage mail, such as a mail client.
- **Submission agent (MTA/MTA client):** the server that accepts a message from the MUA and begins relay.
- **Mail transfer agent (MTA):** routes and relays a message toward the destination.
- **Mail delivery agent (MDA):** places a delivered message in a mailbox.
- **Mail store:** server-side storage of messages and folders.
- **Mail access protocol:** retrieves or synchronises messages, commonly IMAP or POP3.
- **DNS:** finds the destination mail servers through MX, A, and AAAA records.
- **MIME:** represents rich content and attachments.
- **Security services:** TLS, authentication, anti-abuse controls, and possibly signed/encrypted mail.

A single host may run several of these functions. The conceptual roles remain useful for troubleshooting.

### 2. Store-and-forward delivery

A user composes a message addressed to `user@example.org`. The MUA submits it to a local mail server using SMTP. The server looks up the recipient domain's MX record, selects an exchanger, and relays the message. If the destination is offline, the server queues the message and retries later.

The recipient's server eventually stores the message in a mailbox. The user's client retrieves it with IMAP or POP3. At no point must the sender and recipient be online simultaneously.

Store-and-forward supports long outages, but it requires policies for:

- queue lifetime and retries;
- delivery failure and bounce messages;
- duplicate suppression;
- mailbox quotas;
- message expiry;
- virus and spam scanning;
- authentication and rate limits.

### 3. Message envelope and content

An email has two related but distinct layers:

- **content/message data:** headers and body intended for the user;
- **SMTP envelope:** source and recipient addresses used for actual delivery.

A message may have a visible `From:` header that differs from the SMTP `MAIL FROM` envelope sender. This difference is used for bounces and anti-spoofing analysis, but it can also be abused. A `Reply-To:` header controls where a reply is directed and is not necessarily the transport source.

The envelope may include multiple recipients, and a message can be copied to recipients not listed in `To`/`Cc`. Servers should verify the intended recipients and policy.

### 4. Message headers and body

Common headers include:

- `From`, `To`, `Cc`, `Bcc`;
- `Date`;
- `Subject`;
- `Message-ID`;
- `In-Reply-To` and `References`;
- `MIME-Version` and content-type fields;
- authentication and routing information added by servers.

The body can be plain text, HTML, or a MIME multipart structure. Headers describe the message and are needed by clients, servers, and verification systems. A header is not proof that the visible sender is honest.

A `Message-ID` is useful for threading and duplicate detection, but it is not globally guaranteed to be unique by every client. `Bcc` recipients are normally hidden from other visible recipients, but delivery systems may still process them.

### 5. SMTP submission and relay

SMTP is used to submit a message from a client to a mail server and to relay messages between mail servers. The client usually connects to port 25 for server-to-server transfer or to a submission port such as 587 when authenticated client submission is required. A secure deployment commonly uses TLS.

The server may authenticate the submitting user, reject unauthorised relaying, scan the message, and add trace headers. Open relays are dangerous because they allow spammers to send through the server.

Mail servers route based on domain and MX records. A domain may have several exchangers with priorities. If one is unavailable, the sender tries another according to its delivery policy.

### 6. Mail user agents and access

An MUA gives the user a mailbox interface to read, compose, search, and organise messages. A local mail client can synchronise with a server or download messages to the device. The choice of IMAP or POP3 affects multi-device behaviour, storage, privacy, and state.

A webmail interface is also an MUA-like client: the browser accesses a server-side mailbox. The browser does not make SMTP the reading protocol; SMTP remains used for submission and transfer.

### 7. Delivery status and retries

A server queues a message if the destination is temporarily unavailable. It retries at intervals, records failures, and eventually generates a delivery-status notification or bounce message. Retry policy must distinguish a temporary failure (network unavailable) from a permanent failure (invalid address or rejected policy).

A bounce can itself be delayed or lost. A successful SMTP transaction means the receiving server accepted responsibility, not that the user has read the message. Read receipts, if supported, are separate and not guaranteed.

### 8. DNS and email routing

The sender's server queries DNS for the recipient domain's MX record. MX identifies a mail exchanger and preference. The server then resolves the exchanger's A or AAAA address. The mail is sent to the exchanger's SMTP service, not directly to the user's workstation.

If no MX exists, a domain may have an implicit fallback depending on the server's rules, and that behaviour should be managed explicitly. A domain with a mail server can also publish other DNS records for policy and authentication.

### 9. MIME

MIME is covered in a separate file. In the overall mail flow, an MUA creates a MIME message, SMTP transports the encoded message, the delivery server preserves its structure, and IMAP/POP3 retrieves it. SMTP was originally designed mainly for text; MIME supplies a common representation for richer content and attachments.

MIME provides format and transfer encoding, not necessarily confidentiality or authentication. An attachment can still be malicious, and an encoded message can be modified by a server unless integrity/authentication is added.

### 10. Email security

Email security addresses several threats:

- **spoofing:** forged From or envelope sender;
- **phishing:** misleading content and links;
- **malware:** malicious attachments or links;
- **interception:** reading mail in transit;
- **replay:** resending an old message;
- **spam and abuse:** unsolicited bulk mail.

TLS protects a connection between selected SMTP or mail-access endpoints but does not automatically protect every stored message or hop. DKIM signs domain/header information, SPF authorises sending hosts, and DMARC aligns policies and reports. End-to-end encryption may protect message content but can reduce server-side search and abuse controls.

Authentication of the envelope sender can help with bounces, but it is not the same as reading authentication. A mail client should display the verified identity carefully and avoid trusting display names alone.

## Worked examples

### Example 1: Normal delivery

A MUA sends a message to a submission server using SMTP. The server queries MX for `example.org`, connects to the exchanger, and relays the message. The exchanger stores it in `user@example.org`'s mailbox. The user later reads it with IMAP. The sender and recipient need not be online together.

### Example 2: Destination offline

The recipient's mail server is unavailable. The sender's server queues the message and retries. The sender receives no immediate failure. After a configured period, the server may issue a bounce. This is store-and-forward behaviour.

### Example 3: Envelope versus header

A marketing system sends a message with a visible `From: announcements@example.net` and an envelope `MAIL FROM:<bounces@example.net>` for bounce handling. The visible address does not necessarily match the transport sender. Authentication policies should inspect the relevant fields.

### Example 4: Attachment

A user sends a PDF and a text note in one message. MIME multipart/mixed gives each part a content type and boundary. SMTP carries the encoded structure. The receiving client renders the text and offers the PDF as an attachment.

## Key terms & formulas

- **Email:** store-and-forward electronic message service.
- **MUA:** mail user agent.
- **MTA:** mail transfer agent.
- **MDA:** mail delivery agent.
- **SMTP:** mail submission/transfer protocol.
- **IMAP/POP3:** mail access protocols.
- **MIME:** multipurpose mail extensions.
- **MX:** DNS mail exchanger record.
- **Envelope sender:** SMTP `MAIL FROM` address.
- **Header sender:** visible `From` field.
- **Bounce:** delivery-failure notification.
- **Queue:** messages awaiting retry or delivery.
- **Store-and-forward:** server stores and later relays.
- **Mailbox:** server-side or client-side message store.
- **Bcc:** blind carbon copy.
- **Message-ID:** message identifier used for threading/duplicate handling.
- **Ports:** SMTP 25 typical, submission commonly 587, secure variants 465.

## Common mistakes

1. **SMTP is not usually the reading protocol.** IMAP or POP3 retrieves mail.
2. **Email is not a direct connection between sender and receiver.** It uses store-and-forward servers.
3. **The From header is not the envelope sender.** They can differ.
4. **A successful SMTP transaction does not mean the user read the message.** It means the server accepted responsibility.
5. **MX is not an address of the user's workstation.** It identifies a mail server.
6. **MIME does not encrypt mail.** It encodes content and attachments.
7. **POP3 and IMAP are not identical.** IMAP keeps more state on the server; POP3 traditionally downloads.
8. **TLS on one hop does not protect every stored copy.** End-to-end and at-rest controls may be needed.
9. **A mail server must not be an open relay.** Authentication and relay policy prevent abuse.
10. **Bcc is hidden from visible recipients, not from the delivery system.** The server still processes it.

## Exam prep

### Likely 2-mark questions

1. **Name the main components of electronic mail.**  
   Hint: MUA, MTA, MDA, mail store, DNS, and access protocol.
2. **What is store-and-forward?**  
   Hint: servers store a message and relay it when a route/contact is available.
3. **How does SMTP differ from IMAP/POP3?**  
   Hint: SMTP sends/relays; IMAP/POP3 retrieve/synchronise.
4. **Distinguish envelope sender and From header.**  
   Hint: SMTP delivery identity versus displayed content header.
5. **State the role of MX.**  
   Hint: identify a mail exchanger and priority for a domain.
6. **Why are retries and queues used?**  
   Hint: recipient/server may be temporarily unavailable.

### Likely long-answer questions

1. **Trace an email from composition to reading, including DNS, SMTP, queueing, and IMAP.**  
   Answer hint: MUA, submission, MX lookup, relay, mailbox, access, and failure handling.
2. **Explain email headers, envelope fields, bounces, and recipient privacy.**  
   Answer hint: From/To/Cc/Bcc, `MAIL FROM`, RCPT TO, delivery reports, and anti-spoofing limits.
3. **Discuss store-and-forward reliability and its costs.**  
   Answer hint: offline delivery, queues, retries, duplicates, expiry, latency, and storage.
4. **Explain how MIME, SMTP, IMAP, and DNS cooperate.**  
   Answer hint: MIME encodes content, SMTP transports, IMAP retrieves, DNS finds mail servers.
5. **Describe email security threats and controls.**  
   Answer hint: SPF/DKIM/DMARC, TLS, authentication, malware/phishing controls, and end-to-end limits.

### Short-answer revision checklist

Be able to name MUA/MTA/MDA, explain store-and-forward, distinguish SMTP from IMAP, describe envelope versus header, and trace MX lookup.
