---
subject: cn
unit: 5
topic: imap
syllabus_ref: CSM3103 Unit-V
status: draft
---
# Internet Message Access Protocol (IMAP)

## Overview

**Internet Message Access Protocol (IMAP)** gives an email client organised access to messages and mailbox state stored on a mail server. Unlike traditional POP3, which often downloads messages and removes them from the server, IMAP is designed around server-based mailboxes, folders, message flags, and synchronisation across multiple devices.

A user can read or mark a message on a phone, laptop, and web interface while seeing consistent server-side state. IMAP supports multiple mailboxes, subfolders, searches, partial message fetching, and flags such as seen, answered, flagged, and deleted. Secure IMAP commonly runs over TLS on port 993.

The syllabus includes IMAP under electronic mail. This file explains IMAP's client/server model, state, commands, folders, flags, synchronisation, partial fetch, security, comparison with POP3, and a worked session.

## Explanation

### 1. IMAP purpose

SMTP is used to submit and relay mail; IMAP is used by a recipient's client to access a mailbox on a server. IMAP does not normally send a message from the user to another recipient. A mail client can use SMTP for submission and IMAP for retrieval/synchronisation.

IMAP is designed for a **server-resident mailbox model**:

- the server stores messages;
- clients identify mailboxes and message states;
- flags and folders are server state;
- multiple clients can synchronise;
- only requested parts or messages need to be transferred.

This model is useful when a user has several devices or wants server-side search and organisation.

### 2. IMAP client/server model

The user agent opens a TCP connection to an IMAP server, authenticates, and enters a selected mailbox. It can issue commands to list folders, search messages, fetch headers or bodies, change flags, move or copy messages, and create or delete folders.

The server maintains session state, mailbox state, message identifiers, and flags. A client may use a persistent connection or reconnect and use state information to discover changes.

Typical secure IMAP uses TLS from the beginning on port 993. Unencrypted IMAP commonly used port 143, but plaintext credentials and message contents are unsafe on an untrusted network.

### 3. Mailboxes, folders, and hierarchy

IMAP supports a hierarchy of mailboxes. Common special-use names include:

- `INBOX` for the primary mailbox;
- `Sent` for sent messages;
- `Drafts` for drafts;
- `Trash` or `Deleted` for deleted items;
- `Archive` or custom folders.

A user can create folders, subscribe to them, rename or move messages, and search within them. Folder names are often encoded in UTF-7 or another modified representation because the original IMAP syntax has restrictions; clients hide most of this complexity from users.

IMAP folder state is server-side. Creating a folder on one device makes it available to another synchronised client.

### 4. Message identifiers and sequence numbers

IMAP can refer to messages in several ways:

- **message sequence number:** position in a mailbox, which can change when messages are removed;
- **UID:** a mailbox-assigned identifier intended to remain stable within that mailbox;
- **UIDVALIDITY:** identifies a new incarnation of a mailbox's UID numbering;
- **UIDNEXT:** predicts the next assigned UID within limits.

A client should not permanently cache a sequence number across mailbox changes. UIDs and UIDVALIDITY are more stable, but a mailbox reset or move to another mailbox can change the context. A correct client detects the change and refreshes state.

### 5. Flags and message state

IMAP flags represent mailbox state, including:

- `\Seen`: message has been read;
- `\Answered`: marked as answered;
- `\Flagged`: marked for follow-up;
- `\Deleted`: marked for removal;
- `\Draft`: draft state;
- `\Recent`: newly arrived in the session, depending on server state.

Flags can be changed explicitly, or a client can use **implicit flags** such as automatically setting `\Seen` when a message is fetched with a body. A flag is server state, not a property permanently embedded in the message. Another synchronised client sees the updated flag.

### 6. Fetching and partial retrieval

IMAP can retrieve:

- a mailbox summary;
- selected headers;
- a full message;
- a body part;
- an attachment;
- message flags without downloading the entire message.

This saves bandwidth and time, especially on mobile links. A client can first list headers, inspect sizes and subjects, and fetch only what the user opens. MIME multipart structure helps identify parts.

Partial fetching does not necessarily mean the message is incomplete after retrieval; the client has requested a particular representation and can fetch other parts later.

### 7. Search

IMAP search criteria can include sender, recipient, date, subject, header, body text, size, flags, and other fields. A client can search server-side without downloading every message.

For example:

```text
A SEARCH UNSEEN FROM "alice@example.org" SINCE 1-Jan-2026
```

The exact command syntax and date format depend on the IMAP version and server. Search results are mailbox state and may change while the user is acting on them.

### 8. Mailbox synchronisation

An IMAP client can record the last known state, including message UIDs and flags, and ask the server what changed. A typical process is:

1. Select the mailbox.
2. Re-establish session and mailbox state.
3. Fetch changed UIDs or flags.
4. Download only new or changed message parts.
5. Apply local updates and send flag changes.
6. Handle conflicts if another client changes the same message.

A server may send unsolicited `EXPUNGE`, `FETCH`, `RECENT`, or other notifications while a session is active. Clients need robust error handling and resynchronisation after a connection failure.

### 9. Basic IMAP commands

Common commands include:

- `CAPABILITY`: list supported features.
- `LOGIN` or `AUTHENTICATE`: authenticate.
- `SELECT` or `EXAMINE`: open a mailbox, read-only or read-write.
- `LIST`/`LSUB`: discover mailboxes.
- `STATUS`: obtain counts and state.
- `SEARCH`: find messages.
- `FETCH`: retrieve flags, headers, body, or parts.
- `STORE`: change flags.
- `COPY`/`MOVE`: copy or move messages.
- `APPEND`: upload a message to a mailbox.
- `EXPUNGE`: permanently remove messages marked deleted.
- `CLOSE`/`LOGOUT`: close mailbox/session.

Commands have tagged responses and untagged status/data responses. A client matches the tag to the command and handles asynchronous state changes.

### 10. IMAP state and connection lifecycle

A session may go through states such as not authenticated, authenticated, selected, and logout. A client usually sends `LOGIN`/`AUTHENTICATE`, selects a mailbox, performs operations, and then logs out. If a command is invalid for the current state, the server returns a `BAD` or `NO` response.

A connection can be lost at any point. A client reconnects, reauthenticates, selects the mailbox, and reconciles UIDs/flags. It should not assume an upload or flag update succeeded merely because the local command was sent.

### 11. IMAP versus POP3

Traditional POP3 often downloads messages to a local device and may delete them from the server. POP3 has `USER`, `PASS`, `STAT`, `RETR`, `DELE`, `LIST`, `UIDL`, and `TOP` operations. It is simple and can be efficient for one device and limited storage.

IMAP is better when:

- the user has multiple devices;
- messages should remain on the server;
- folders and flags need synchronisation;
- partial fetching and server-side search are useful;
- the user wants access from a web or mobile interface.

POP3 can have extensions and a leave-on-server option, so the comparison is a design tendency rather than an absolute capability list. The key distinction is server-resident, synchronised state versus download-focused operation.

### 12. Security and privacy

IMAP credentials and message contents must be protected. Secure IMAP uses TLS, usually port 993. The client should validate the server certificate and hostname. Plaintext IMAP on port 143 should be used only inside a carefully protected environment or inside an encrypted tunnel.

IMAP itself is not end-to-end message encryption between all mail servers. It protects the client-to-server session and relies on the mail architecture for other hops. At-rest encryption and mailbox access controls may be needed.

Server-side search and synchronisation can expose metadata to the mail provider. A user should understand retention, access, and device-security policies.

## Worked examples

### Example 1: Multi-device flag synchronisation

A user marks a message `\Flagged` on a phone. The phone sends a `STORE` command. The server updates the message state. The laptop later selects the mailbox, compares UIDs/flags, and sees the message as flagged.

### Example 2: Partial fetch

A mobile client fetches only the sender, subject, date, and size for a large message. The user opens one message, and the client fetches its text body. It downloads a large attachment only when requested.

### Example 3: UID change

A client stores UID 1045 for a message. Another user deletes an earlier message, changing sequence numbers. UID 1045 can still identify the same message if the mailbox's UIDVALIDITY is unchanged. A sequence number would have shifted, so a UID-aware client avoids confusion.

### Example 4: Search

A client sends a search for unseen messages from a sender. The server returns matching sequence numbers or UIDs. The client fetches headers for the results, then downloads selected bodies.

### Example 5: Secure login

A client connects to port 993 with TLS, authenticates with `AUTHENTICATE`, selects `INBOX`, and fetches messages. It never sends the password in plaintext. If certificate validation fails, the client aborts rather than exposing credentials.

## Key terms & formulas

- **IMAP:** Internet Message Access Protocol.
- **MUA:** client accessing a server mailbox.
- **Mailbox/folder:** server-side named message collection.
- **Message sequence number:** current position in a mailbox.
- **UID:** mailbox-assigned stable message identifier within a validity context.
- **UIDVALIDITY:** identifier for a mailbox UID namespace.
- **UIDNEXT:** predicted next UID.
- **`\Seen`:** read flag.
- **`\Deleted`:** marked for removal flag.
- **EXPUNGE:** permanently remove messages marked deleted.
- **FETCH:** retrieve selected message data.
- **STORE:** modify flags.
- **SEARCH:** server-side query.
- **Implicit `\Seen`:** set when a body is fetched.
- **IMAP port:** 993 for implicit TLS; 143 traditionally plaintext.
- **Partial fetch:** download headers/body parts selectively.
- **Synchronisation:** reconcile server mailbox state across clients.

## Common mistakes

1. **IMAP is not normally the submission protocol.** SMTP is used to send and relay.
2. **IMAP is not just download-and-delete like basic POP3.** It manages server-side mailbox state.
3. **A flag is not embedded permanently in the message.** It is mailbox state stored by the server.
4. **Message sequence numbers are not stable identifiers.** UIDs are intended to be more stable within UIDVALIDITY.
5. **Opening a message may set `\Seen` implicitly.** A client can request a peek or alter flags.
6. **A search result is not a permanent promise.** The mailbox can change after the search.
7. **Secure IMAP is not plaintext port 143.** TLS protects credentials and content.
8. **IMAP does not guarantee end-to-end mail security across every server.** It protects the session to its server.
9. **IMAP does not make a malicious attachment safe.** The client must still scan and validate content.
10. **POP3 and IMAP are not completely mutually exclusive.** Deployments can support both and extensions vary.

## Exam prep

### Likely 2-mark questions

1. **State two IMAP features.**  
   Hint: server-side folders, multiple-device synchronisation, flags, search, partial fetch.
2. **Differentiate IMAP from basic POP3.**  
   Hint: server-resident state/synchronisation versus download-focused retrieval.
3. **What is a UID?**  
   Hint: mailbox-assigned message identifier more stable than a sequence number.
4. **What does `\Seen` mean?**  
   Hint: message has been marked/read on the server.
5. **Why is TLS used with IMAP?**  
   Hint: protect credentials and message contents from interception/tampering.
6. **Name two common IMAP commands.**  
   Hint: SELECT, FETCH, STORE, SEARCH, LIST, EXPUNGE, LOGIN.

### Likely long-answer questions

1. **Explain IMAP's client/server model and mailbox synchronisation.**  
   Answer hint: authenticate, select, UIDs/UIDVALIDITY, flags, changes, reconnect.
2. **Compare IMAP and POP3 for multi-device mail use.**  
   Answer hint: storage, flags, folders, partial fetch, privacy, and server state.
3. **Explain IMAP message identifiers and why sequence numbers can change.**  
   Answer hint: deletion, insertion, UIDs, UIDVALIDITY, and stale client state.
4. **Describe an IMAP session from login to search and partial fetch.**  
   Answer hint: TLS, AUTHENTICATE, SELECT, STATUS/SEARCH, FETCH headers/body, STORE flags.
5. **Discuss IMAP privacy, security, and failure recovery.**  
   Answer hint: TLS, certificate validation, metadata exposure, reconnects, UID reconciliation, and malware.

### Short-answer revision checklist

Be ready to state the secure port, define UID/UIDVALIDITY, name common flags and commands, and explain why IMAP suits a phone/laptop/web client better than basic POP3.
