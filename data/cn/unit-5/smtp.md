---
subject: cn
unit: 5
topic: smtp
syllabus_ref: CSM3103 Unit-V
status: draft
---
# Simple Mail Transfer Protocol (SMTP)

## Overview

**Simple Mail Transfer Protocol (SMTP)** is a connection-oriented, push-based protocol used to submit and relay electronic mail. A client opens a TCP connection to a mail server, identifies itself, names the envelope sender and recipients, sends message data, and receives status responses.

SMTP is store-and-forward: a server accepts responsibility for a message and relays it toward the destination. It normally uses TCP port 25 for server-to-server transfer, while authenticated client submission commonly uses port 587 (or implicit TLS on 465). SMTP was originally designed mainly for plain text; MIME supplies a common way to carry richer content and attachments.

The syllabus includes SMTP under electronic mail. This file explains commands, replies, transaction phases, relays, extensions, authentication, security, errors, and a worked session.

## Explanation

### 1. SMTP role

SMTP defines how a **submitting client** hands a message to a **mail transfer agent** and how mail servers relay it. It is a push protocol: the sender sends data actively; the receiving server does not pull the message.

SMTP is not normally used to:

- read a user's mailbox (IMAP/POP3 do that);
- resolve the recipient's IP address (DNS does that);
- define rich media formats (MIME does that);
- provide end-to-end confidentiality by itself (TLS and other controls are needed).

### 2. SMTP transaction structure

A simple SMTP transaction has phases:

1. **Connection establishment:** TCP connects to the server.
2. **Greeting:** server sends a 220 service-ready response.
3. **EHLO/HELO:** client identifies itself and discovers extensions.
4. **MAIL FROM:** client identifies the envelope sender.
5. **RCPT TO:** client identifies one or more recipients.
6. **DATA:** client sends message headers/body.
7. **Message terminator:** a line containing only `.` ends data.
8. **Server response:** server accepts, defers, or rejects.
9. **QUIT:** client closes the session cleanly.

A server can accept several messages over one connection using the same transaction structure. The connection is not necessarily the same as a mailbox session.

### 3. SMTP commands

Common commands include:

- `HELO domain`: identify the client and enter the transaction.
- `EHLO domain`: extended hello, usually preferred; server returns capabilities.
- `MAIL FROM:<address>`: start a new message and specify the reverse-path/envelope sender.
- `RCPT TO:<address>`: specify an envelope recipient; can be repeated.
- `DATA`: begin message content.
- `RSET`: reset the current transaction.
- `NOOP`: test liveness without changing state.
- `VRFY`: verify a mailbox, often disabled for privacy.
- `EXPN`: expand a mailing list, often disabled.
- `HELP`: request command help.
- `QUIT`: end the SMTP session.

Modern SMTP may also use `AUTH`, `STARTTLS`, `BDAT`, and other extensions. Not every server permits every command.

### 4. EHLO and capability discovery

The client sends `EHLO client.example.org`. The server replies with a multiline 250 response listing extensions such as:

- `250-PIPELINING`
- `250-SIZE`
- `250-STARTTLS`
- `250-AUTH ...`

`EHLO` is an SMTP extension introduced for this exchange. `HELO` is the older basic form and does not provide the same capability list. A client should not assume that STARTTLS, authentication, or a particular size limit is available.

### 5. MAIL FROM and RCPT TO

`MAIL FROM:<alice@example.org>` identifies the envelope sender. `RCPT TO:<bob@example.net>` identifies an envelope recipient. Multiple `RCPT TO` commands can create multiple recipients for one message. The server can accept some recipients and reject others, returning a separate reply for each.

The envelope is used for delivery, bounces, and policy. It is not necessarily the visible `From:` header. A client must not let arbitrary users use the server as an open relay; the server may authenticate the client or restrict permitted source/destination relationships.

### 6. DATA and message termination

After a successful `MAIL FROM` and at least one `RCPT TO`, the client sends `DATA`. The server responds with a 354 intermediate reply, after which the client sends headers, a blank line, and body. A line containing only a period (`.`) ends the data.

Because the period line can occur naturally in some text contexts, SMTP uses dot-stuffing: a line beginning with a period is transmitted with an extra period, and the receiver removes the extra one. MIME content and attachments are encoded so they remain compatible with the mail transport.

After the terminator, the server returns a final 250 if it accepts responsibility for the message, or a 4xx/5xx code if it defers or rejects it.

### 7. Reply codes

SMTP replies are three-digit codes followed by text. The first digit has a broad meaning:

- **1xx:** preliminary, the command is accepted and more reply follows.
- **2xx:** command completed successfully.
- **3xx:** next stage is needed, such as starting TLS or entering DATA.
- **4xx:** temporary failure; retry later.
- **5xx:** permanent failure; do not retry unchanged.

Examples:

- `220` server ready;
- `250` command accepted/message queued;
- `354` start mail input;
- `421` service not available/closing;
- `450` mailbox temporarily unavailable;
- `550` mailbox or command rejected;
- `553` mailbox name not allowed.

A client should parse the code and text, not assume that all non-2xx replies mean the same thing. It should distinguish temporary from permanent failures and obey retry guidance.

### 8. Relay and DNS routing

An SMTP server receives a message for `bob@example.org`. It queries DNS for the domain's MX records, chooses an exchanger by priority and policy, resolves its A/AAAA address, connects over TCP, and repeats the SMTP transaction. The receiving server may relay to another server or deliver locally.

A message can cross several administrative domains. Each relay may add Received trace information, check authentication, scan content, apply rate limits, and queue for retry. The sender's acceptance of the message does not guarantee final delivery or reading.

### 9. Store-and-forward and queueing

After a server accepts a message, it stores it in a queue while waiting for the next relay attempt. The queue contains the message, envelope recipients, attempts, timestamps, and status. The server retries temporary failures with backoff.

If all attempts fail permanently, it creates a bounce or delivery-status notification, usually using the envelope sender. The queue must be protected against tampering and resource exhaustion. Mailbox limits and message size limits can reject a message before it enters a long queue.

### 10. MIME and SMTP

SMTP can carry a line-oriented text stream. MIME defines headers and encoding for non-ASCII characters, attachments, HTML, images, audio, and multipart structures. A MIME message is passed through SMTP as encoded text; the receiving client decodes or renders it.

MIME transfer encodings such as Base64 make binary data safe for a text-oriented transport, but they increase size and do not encrypt it. MIME boundaries and content types are not SMTP commands.

### 11. Authentication and relay security

An SMTP server can require `AUTH` after TLS so that a user proves identity before submission. Authentication helps prevent unauthorised relay, but it is not the same as end-toend sender identity. SPF, DKIM, and DMARC operate at the DNS/message-policy level.

Open or weakly authenticated relays can be abused for spam. A server should require authentication for submission, restrict unauthenticated relay, apply rate limits, and monitor unusual volume. A client should not send credentials over plaintext SMTP.

### 12. TLS and encryption

`STARTTLS` upgrades a plaintext SMTP connection to TLS after the client and server agree. Implicit TLS starts with TLS on a dedicated port such as 465. TLS protects confidentiality and integrity between the two endpoints for that session, but it does not automatically encrypt mail while it is stored or between every relay unless every hop is protected appropriately.

Certificate validation and hostname verification matter. A client should not silently continue after a TLS failure when the connection is supposed to be secure. End-to-end message encryption is a separate application choice and can interfere with server-side scanning.

### 13. Multiple recipients and partial failure

A client can issue:

```text
MAIL FROM:<sender@example.org>
RCPT TO:<first@example.net>
RCPT TO:<second@example.net>
DATA
```

The server may accept the first recipient and reject the second. The client should track partial delivery and report it correctly. A rejected recipient should not be hidden from the sender's delivery-status information.

### 14. Error recovery

If a client receives a temporary error before DATA, it can retry the command or connection according to policy. If a connection drops during DATA, the transaction state may be unknown, and the client must avoid blindly creating a duplicate message. SMTP has no universal end-to-end transaction identifier; `Message-ID` and queue policy help but do not fully replace reliable application design.

If a message is rejected permanently, retrying the identical transaction will not help. A client should report an error, preserve a draft if appropriate, and avoid a retry loop that blocks the mail server.

## Worked examples

### Example 1: Basic SMTP session

```text
S: 220 mail.example.org ESMTP ready
C: EHLO client.example.org
S: 250-mail.example.org
S: 250-SIZE 52428800
S: 250 AUTH PLAIN
C: MAIL FROM:<alice@example.org>
S: 250 2.1.0 Sender accepted
C: RCPT TO:<bob@example.net>
S: 250 2.1.5 Recipient accepted
C: DATA
S: 354 End data with <CRLF>.<CRLF>
C: From: Alice <alice@example.org>
C: To: Bob <bob@example.net>
C: Subject: Test
C:
C: Hello
C: .
S: 250 2.0.0 Queued as 12345
C: QUIT
S: 221 2.0.0 Closing connection
```

### Example 2: Temporary failure

`450 4.2.1 Mailbox temporarily busy` is a 4xx reply. The server is willing to accept the message later, so the sender queues and retries. `550 5.1.1 User unknown` is permanent; repeated identical attempts should stop and a bounce may be generated.

### Example 3: Dot stuffing

A body line begins with `.` followed by text. The client sends an extra leading period. The server removes one period on receipt, so the recipient sees the original line. A line with only `.` still terminates DATA.

### Example 4: Relay route

The sender's server queries `example.net` MX, obtains `mx1.example.net`, resolves its A record, connects to port 25, and repeats the envelope transaction. It may add a Received header. The destination server then places the message in a mailbox.

### Example 5: STARTTLS and AUTH

A submission client connects to port 587, issues EHLO, starts TLS, authenticates, and then issues MAIL FROM/RCPT TO/DATA. This prevents credentials from being sent in clear text and restricts submission to authorised users.

## Key terms & formulas

- **SMTP:** Simple Mail Transfer Protocol.
- **MUA:** mail user agent.
- **MTA:** mail transfer agent.
- **MAIL FROM:** envelope sender command.
- **RCPT TO:** envelope recipient command.
- **DATA:** begin message content.
- **Dot:** line with only `.` terminates data.
- **Reply code:** three-digit SMTP response.
- **1xx/2xx/3xx/4xx/5xx:** preliminary/success/next/temporary/permanent.
- **EHLO:** extended hello/capability exchange.
- **HELO:** basic hello.
- **STARTTLS:** upgrade a connection to TLS.
- **AUTH:** SMTP authentication extension.
- **SMTP port:** usually 25; submission commonly 587, implicit TLS 465.
- **Queue:** accepted messages awaiting relay.
- **Relay:** server forwarding a message toward the destination.
- **Bounce:** permanent failure notification.
- **SPF/DKIM/DMARC:** DNS/message sender-authentication policies.
- **MIME:** rich content and attachment representation carried through SMTP.

## Common mistakes

1. **SMTP is not a mail-reading protocol.** IMAP/POP3 retrieve messages.
2. **SMTP is not connectionless.** The transaction uses a TCP connection and explicit commands.
3. **`MAIL FROM` is not necessarily the From header.** One is envelope information.
4. **A 250 response does not mean the recipient read the message.** It means the server accepted/queued responsibility.
5. **A 4xx error is temporary; a 5xx error is permanent.** Do not retry a 5xx unchanged.
6. **DATA does not end at a blank line.** The final line is a period.
7. **EHLO is not the same as HELO.** EHLO discovers extensions.
8. **STARTTLS does not encrypt every mail hop automatically.** Each connection and storage location needs protection.
9. **MIME does not replace SMTP.** MIME provides content structure; SMTP transports it.
10. **A mail server should not be an open relay.** Authentication and policy are essential.
11. **A partial RCPT acceptance must be handled.** The sender may have delivered to only some recipients.

## Exam prep

### Likely 2-mark questions

1. **List the main SMTP commands.**  
   Hint: EHLO/HELO, MAIL FROM, RCPT TO, DATA, QUIT, plus AUTH/RSET.
2. **What is the purpose of `MAIL FROM` and `RCPT TO`?**  
   Hint: envelope sender and recipient for delivery.
3. **How does a client terminate DATA?**  
   Hint: a line containing only a period.
4. **What do 250 and 550 mean?**  
   Hint: successful acceptance versus permanent rejection.
5. **Why does SMTP use TCP?**  
   Hint: reliable ordered byte stream and connection for a complete transaction.
6. **What is STARTTLS?**  
   Hint: command to upgrade an SMTP connection to TLS.

### Likely long-answer questions

1. **Explain an SMTP transaction from connection to QUIT.**  
   Answer hint: greeting, EHLO, TLS, MAIL FROM, RCPT TO, DATA, response, and close.
2. **Compare SMTP reply-code classes and retry behaviour.**  
   Answer hint: 1xx–5xx, temporary versus permanent, queue/backoff, and bounce.
3. **Explain envelope fields and partial recipient delivery.**  
   Answer hint: MAIL FROM/RCPT TO, multiple RCPT commands, accepted/rejected recipients, and bounce.
4. **Discuss SMTP security: relay abuse, authentication, TLS, SPF, DKIM, and DMARC.**  
   Answer hint: open relay, AUTH, STARTTLS, certificate validation, and DNS policies.
5. **Explain how SMTP, DNS MX, and MIME cooperate in email delivery.**  
   Answer hint: route by MX, relay by SMTP, preserve rich content through MIME, and retrieve with IMAP/POP3.

### Short-answer revision checklist

Be able to write the command sequence, explain dot-stuffing, distinguish 4xx from 5xx, state the default port, and explain why `MAIL FROM` differs from the From header.
