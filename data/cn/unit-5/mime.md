---
subject: cn
unit: 5
topic: mime
syllabus_ref: CSM3103 Unit-V
status: draft
---
# Multipurpose Internet Mail Extensions (MIME)

## Overview

**Multipurpose Internet Mail Extensions (MIME)** extends basic electronic mail so it can carry text in different character sets, HTML, images, audio, video, and arbitrary files. Basic SMTP was designed mainly for a simple text message; MIME adds headers and a structured body format while remaining compatible with mail transport and retrieval protocols.

A MIME message declares its content type and, for multipart messages, uses boundary strings to separate parts. A transfer encoding such as Base64 makes binary data safe to pass through a text-oriented transport. MIME is a representation and encoding standard, not encryption or malware protection.

The syllabus lists MIME under electronic mail. This file covers MIME headers, media types, multipart structures, boundaries, encodings, base64/Quoted-Printable, message disposition, attachments, nested multiparts, and a worked message.

## Explanation

### 1. Why MIME exists

Early email systems assumed a simple text body and US-ASCII-like text transport. Real users needed:

- non-English text and many character encodings;
- binary files such as PDFs, images, and archives;
- alternative plain-text and HTML versions;
- images embedded in HTML;
- structured alternative and related content;
- metadata describing how to interpret a body part.

MIME does not change the basic email route. SMTP still transports the message, and IMAP/POP3 still retrieve it. MIME supplies a standard way for the sender and receiver to describe and encode the content.

### 2. MIME headers

Important headers include:

- `MIME-Version`: version of the MIME standard, commonly `1.0`.
- `Content-Type`: media type and optional parameters, such as `text/plain`, `application/pdf`, or `multipart/mixed`.
- `Content-Transfer-Encoding`: how body bytes are represented, such as `7bit`, `8bit`, `binary`, Quoted-Printable, or Base64.
- `Content-Disposition`: how a client should present the part, commonly `inline` or `attachment`.
- `Content-ID` and `Content-Location`: identifiers/links useful for related HTML and images.
- `Content-Description`: optional human-readable description.

Headers apply to the entire message or to an individual MIME part. A multipart message has headers at the top and headers for each child part.

### 3. Media types

A media type has a **type** and **subtype**, written as `type/subtype`. Examples:

- `text/plain`;
- `text/html`;
- `text/calendar`;
- `image/jpeg`;
- `image/png`;
- `audio/mpeg`;
- `video/mp4`;
- `application/pdf`;
- `application/zip`;
- `message/rfc822` for an attached email.

Parameters provide extra information, such as `charset=UTF-8`, filename, size, or creation date. A receiver uses the type to decide how to render or process the content.

The media type is a declaration, not a guarantee that the bytes are safe. A file named `.pdf` can be malicious, and a declared image can be malformed.

### 4. Multipart messages

A multipart body contains several parts separated by boundary lines. The top-level header says which multipart subtype it uses.

#### Multipart/mixed

`multipart/mixed` is common for a message with a main body and one or more attachments. The first part may be plain text or HTML; later parts are files.

#### Multipart/alternative

`multipart/alternative` contains alternative representations of the same content, such as plain text and HTML. A client chooses or renders the best supported representation. Parts are ordered from least to most preferred in common practice; the exact preference rules are part of the MIME model and should be handled carefully.

#### Multipart/related

`multipart/related` groups a main document, such as HTML, with resources referenced by it, such as images. A `start` parameter identifies the root part. The parts share a relationship rather than simply offering alternatives.

#### Multipart/signed and encrypted

MIME can also describe cryptographically signed or encrypted content using appropriate media types/parameters. A digital signature provides authenticity/integrity; encryption provides confidentiality. These controls require keys and secure handling and are not the same as Base64 encoding.

### 5. MIME boundaries

A multipart message includes a `boundary` parameter containing a unique string. The body uses lines:

```text
--boundary
Content-Type: text/plain

This is the text part.
--boundary
Content-Type: application/pdf
Content-Transfer-Encoding: base64
...
--boundary--
```

The initial boundary separates the headers from the body. Each subsequent boundary separates parts, and the closing boundary `--boundary--` marks the end. The receiver finds exact boundary lines rather than searching for the string everywhere in a part.

Boundary values should be chosen so they do not occur accidentally in the content. If a part contains a line that looks like a boundary, the encoder must alter or encode it. A corrupt boundary can make a message undecodable or create security ambiguity.

### 6. Transfer encodings

#### 7bit and 8bit

`7bit` represents data using seven-bit US-ASCII lines. `8bit` allows eight-bit bytes but still assumes the transport can carry them. Some old mail paths cannot safely carry arbitrary 8-bit data, so another encoding may be needed.

#### Binary

`binary` indicates arbitrary binary data and requires a transport capable of preserving it. Many traditional SMTP systems do not handle this safely as a message body, so Base64 or another encoding is more portable.

#### Quoted-Printable

Quoted-Printable is designed for mostly text data with a few non-ASCII or special bytes. It uses printable ASCII and `=XX` hexadecimal escapes for problematic bytes. It is usually more compact than Base64 for text and keeps line lengths manageable.

#### Base64

Base64 encodes arbitrary bytes using a 6-bit alphabet and groups them into characters. It is robust for binary files through a text-oriented path. It increases size by roughly one third (four output characters for every three input bytes, ignoring padding/line breaks).

Base64 is **not encryption**: anyone can decode it, and it does not prove the sender's identity. It also does not detect malicious content.

### 7. Attachments and disposition

An attachment is usually a MIME part with a non-text media type and `Content-Disposition: attachment; filename="report.pdf"`. A filename can be displayed or used to suggest a local name, but clients must sanitise it to avoid path traversal and dangerous extensions. The binary content is encoded for transport and decoded by the client.

A MIME attachment is not necessarily safe. Recipients should scan it, verify its type/signature where appropriate, and apply updates and access controls. A mail server may reject or rewrite executable content according to policy.

### 8. Character sets and text

`text/plain` and `text/html` can include a `charset` parameter such as `UTF-8`. The sender encodes the original characters into the declared format, and the client decodes them. A wrong charset can produce garbled text or, in some cases, create a security risk if content is interpreted as a different type.

HTML in email is not identical to HTML in a browser. Mail clients may disable scripts, external images, forms, or remote content for security. A multipart/alternative message can include a plain-text fallback.

### 9. Nested multipart

Multipart structures can be nested. A `multipart/mixed` message may contain a text body and a `multipart/alternative` HTML/text part, plus a PDF. The receiver walks the tree using each part's headers and boundary. A client should not assume there is only one body or one attachment.

A Content-ID can link an HTML body to an image part in a `multipart/related` structure. A remote image URL may be blocked or replaced for privacy; inline CID resources are often included in the message.

### 10. MIME and email security

MIME provides structure and encoding, not trust. Security concerns include:

- malicious attachments;
- spoofed filenames and types;
- scripts or active content in HTML;
- hidden tracking images;
- oversized encoded messages;
- boundary manipulation;
- content-type confusion.

Mail clients should use a safe renderer, scan attachments, avoid automatically launching files, and respect user controls for external content. SMTP/TLS protects transport to the extent configured, while end-to-end encryption is separate.

### 11. MIME processing example

A message contains:

1. a `text/plain` part with a report summary;
2. a `text/html` alternative;
3. a `application/pdf` attachment.

A webmail client can display the HTML or plain text and offer a PDF link. A command-line client can save the decoded PDF. A mobile client can download only the text and fetch or stream the PDF later.

## Worked examples

### Example 1: Multipart/mixed

```text
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="abc123"

--abc123
Content-Type: text/plain; charset="UTF-8"

Please find the report attached.
--abc123
Content-Type: application/pdf
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename="report.pdf"

JVBERi0xLjQK...
--abc123--
```

The client separates parts on the boundary lines and decodes Base64 for the PDF.

### Example 2: Multipart/alternative

A message contains a plain-text part followed by an HTML part. A rich client renders HTML; a limited client chooses the plain-text alternative. The parts represent alternatives, not two independent messages.

### Example 3: Base64 size

A 3-byte input becomes four Base64 characters. A 3,000,000-byte file therefore needs about 4,000,000 Base64 characters, plus line breaks and headers. Base64 is an encoding, so the receiver can recover the original file.

### Example 4: HTML with image

An HTML part references `cid:image1@example`. A `multipart/related` message includes a matching `image/png` part with `Content-ID: image1@example`. A client can display the image without fetching a remote URL.

### Example 5: Security check

A message declares an attachment as `report.pdf`, but the bytes fail a malware scan or signature check. The client should warn or block it. The MIME `Content-Type` is a hint about interpretation, not a safety guarantee.

## Key terms & formulas

- **MIME:** Multipurpose Internet Mail Extensions.
- **Media type:** `type/subtype`, such as `text/plain`.
- **Content-Type:** describes body/part media type and parameters.
- **Multipart:** body with multiple MIME parts.
- **Boundary:** unique delimiter between parts.
- **Closing boundary:** boundary followed by `--`.
- **Content-Transfer-Encoding:** representation such as Base64.
- **Quoted-Printable:** text-friendly `=XX` encoding.
- **Base64:** six-bit text encoding; roughly 4/3 size expansion.
- **Multipart/mixed:** body plus attachments.
- **Multipart/alternative:** alternative representations.
- **Multipart/related:** related resources such as inline images.
- **Content-Disposition:** `inline` or `attachment` presentation.
- **Content-ID:** identifier linking related parts.
- **Charset:** character encoding such as UTF-8.
- **MIME security:** scan/render safely; encoding is not encryption.

## Common mistakes

1. **MIME is not encryption.** It encodes and structures content.
2. **Base64 does not compress or protect a file.** It expands size and is reversible by anyone.
3. **A boundary separates parts; it is not a MIME command.** It is a delimiter in the body.
4. **`multipart/mixed` and `multipart/alternative` have different meanings.** Mixed commonly carries attachments; alternative offers versions of one message.
5. **A filename does not prove the file type.** The client should inspect and scan content.
6. **A Content-Type is not a security label.** A receiver must validate and safely handle bytes.
7. **MIME does not replace SMTP.** SMTP transports the structured message.
8. **Quoted-Printable is not always smaller than Base64.** Text often compresses better with it.
9. **HTML email is not a normal browser page.** Scripts and remote content may be disabled.
10. **A message can be nested multipart.** Parsing must be recursive.
11. **Transfer encoding does not prevent header injection.** Headers and boundaries need validation.

## Exam prep

### Likely 2-mark questions

1. **State two tasks performed by MIME.**  
   Hint: carry non-ASCII text and attachments/rich media; describe/transfer-encode parts.
2. **What is a MIME boundary?**  
   Hint: delimiter marking the beginning/end of a multipart part.
3. **Distinguish multipart/mixed and multipart/alternative.**  
   Hint: attachments versus alternate representations.
4. **Why is Base64 used?**  
   Hint: represent arbitrary binary data safely in a text transport.
5. **Is Base64 encryption?**  
   Hint: no; it is reversible encoding.
6. **Name two important MIME headers.**  
   Hint: Content-Type, Content-Transfer-Encoding, Content-Disposition, MIME-Version.

### Likely long-answer questions

1. **Explain MIME headers, media types, boundaries, and transfer encodings.**  
   Answer hint: top-level and part headers, multipart structure, 7bit/QP/Base64, and size overhead.
2. **Compare multipart/mixed, alternative, and related with examples.**  
   Answer hint: attachment-bearing, alternate representations, and HTML/resources.
3. **Explain how a mail client processes a MIME message with an attachment.**  
   Answer hint: parse headers, find boundaries, select part, decode, scan, and display/save.
4. **Discuss MIME security and why a declared content type is not trusted.**  
   Answer hint: malware, HTML, tracking, filenames, boundary validation, and safe rendering.
5. **Calculate Base64 expansion and design a mail message for text plus PDF.**  
   Answer hint: 3 bytes -> 4 characters, show headers/boundaries/encoding, and mention recipient handling.

### Short-answer revision checklist

Be able to write a multipart boundary structure, distinguish the three multipart types, define QP/Base64, state that Base64 is not encryption, and name MIME security risks.
