---
subject: cn
unit: 4
topic: tcp
syllabus_ref: CSM3103 Unit-IV
status: draft
---
# Transmission Control Protocol (TCP)

## Overview

**Transmission Control Protocol (TCP)** is a connection-oriented, reliable, ordered transport protocol that provides a **byte-stream** service between application processes. TCP sits above IP, which itself is best effort, and adds connection state, sequence numbers, acknowledgements, retransmission, checksums, flow control, and congestion control.

TCP is used when complete and correctly ordered delivery is more important than minimum startup time or per-byte overhead. HTTP, SSH, SMTP, and many other protocols use TCP. A browser can recover a lost web segment, whereas an application using UDP may choose to skip a lost datagram.

TCP does not preserve application message boundaries. One application write may be read as several reads, and several writes may be read together. It also does not provide a real-time deadline guarantee; congestion and retransmission can increase delay.

## Explanation

### 1. TCP service

TCP offers a reliable, connection-oriented, full-duplex byte stream. The service is implemented between a source socket and a destination socket. Applications write a stream of bytes; TCP sends segments, numbers the bytes, detects loss, and makes the stream available in order at the receiver.

A TCP segment contains a header and payload. The minimum header is 20 bytes, with optional fields making it longer. The payload is normally limited by the maximum segment size and path conditions.

TCP provides:

- connection establishment and termination;
- byte ordering;
- duplicate detection;
- error detection;
- acknowledgements;
- retransmission of missing bytes;
- receive-window flow control;
- congestion-window control;
- full-duplex operation.

TCP does not guarantee that every application write becomes exactly one received write, nor does it guarantee a fixed delay or bandwidth.

### 2. Connection establishment

TCP normally uses a **three-way handshake**:

1. The client sends `SYN` with an initial sequence number `x`.
2. The server sends `SYN, ACK`, acknowledges `x + 1`, and chooses its own initial sequence number `y`.
3. The client sends `ACK`, acknowledging `y + 1`.

After the third ACK, both sides enter the established state. The handshake synchronises sequence numbers and allows options such as maximum segment size, window scaling, and timestamps to be negotiated.

The handshake also prevents an old duplicate connection request from being silently accepted as a new connection in the normal sequence space, though it adds round-trip setup time.

### 3. Sequence numbers and ACKs

TCP numbers bytes, not individual application messages. A sequence number identifies the first byte or the position associated with a segment. An ACK indicates the next sequence number the receiver expects, often written `ack = x` to mean all bytes below `x` have been received in order.

If a receiver receives bytes 1001–1500 while expecting 1001, it accepts them and ACKs 1501. If it receives a later range first, out-of-order data can be buffered, but the ACK and delivery rules depend on the implementation and options. A gap triggers duplicate ACKs or a timer.

TCP acknowledgements are cumulative: an ACK for a later byte normally also confirms earlier bytes. SACK options can report blocks received out of order so that a receiver can request only missing data.

### 4. Reliability and retransmission

If a segment is lost, the receiver does not receive the missing byte range. A timeout or duplicate ACK signals the sender. The sender retransmits the missing data. The receiver's sequence numbers and checksum prevent a corrupted or duplicate segment from being delivered incorrectly.

Retransmission is not a guarantee of immediate recovery. If the link is down, the receiver never acknowledges the segment, and the connection may eventually fail. A sender uses repeated timers and limits retries to avoid infinite resource use.

TCP's reliability is end-to-end: it covers the whole path, not just one link. IP can lose a packet at any hop, and TCP supplies recovery above it.

### 5. Checksums

The TCP checksum covers the header and data and uses a pseudo-header containing source/destination addresses, protocol, and length. It detects many accidental errors. If the checksum fails, the receiver silently discards the segment; it normally does not send a negative acknowledgement for a corrupted segment.

A checksum is not authentication. An attacker can modify data and recompute the checksum. Applications that need integrity against deliberate modification require cryptographic protection such as TLS or an authenticated message mechanism.

### 6. Full-duplex byte stream

TCP connections are full duplex: both endpoints can send segments at the same time. Each direction has sequence and acknowledgement state. A connection can be closed in one direction with a FIN while the other direction continues briefly.

The byte-stream model means TCP does not insert message boundaries. An application may call `write("A")` and `write("B")`, while the receiver may read `"AB"`, `"A"`, or another available combination. Applications that need message boundaries must add their own framing.

### 7. Sliding windows

TCP maintains a sender window of bytes that may be sent before an acknowledgement is required. As ACKs arrive, the window moves forward. The window is controlled by:

- `rwnd`, the receiver's advertised receive window;
- `cwnd`, the congestion window.

The effective sending limit is normally:

`send limit = min(rwnd, cwnd)`

The window lets a high-bandwidth path remain busy and also bounds the amount of unacknowledged data. A large window can improve bandwidth-delay utilisation but requires buffers and can increase loss or latency under congestion.

### 8. Flow control

The receiver advertises how much data it can accept. If its application is slow, the window shrinks or becomes zero. The sender must not send beyond the advertised amount and uses window probes or persist behaviour to learn when space opens.

Flow control is receiver protection. It can work correctly even when the network is congested, and it cannot by itself prevent a router queue from filling.

### 9. Congestion control

TCP maintains a congestion window based on observed network conditions. It generally increases the window gradually and reduces it after loss, excessive delay, or an explicit congestion signal. Slow start, congestion avoidance, fast retransmit, fast recovery, and different loss-signalling variants appear in modern TCP.

The sender's rate is not fixed. It depends on the path's round-trip time, loss, receive window, congestion window, and application behaviour. Congestion control aims for stable high utilisation, not a guaranteed maximum rate.

### 10. TCP header

The minimum TCP header contains:

- source and destination ports;
- sequence number;
- acknowledgement number;
- data offset/header length;
- reserved/control bits such as SYN, ACK, FIN, RST, and PSH;
- window size;
- checksum;
- urgent pointer.

Options may include MSS, window scale, timestamps, selective acknowledgement, and padding. The data-offset field tells the receiver how many 32-bit words the header occupies.

TCP port numbers identify the application endpoints. IP addresses identify the interfaces. A TCP segment is encapsulated in an IP packet, which is encapsulated in a link frame.

### 11. Connection states and teardown

A simplified TCP state progression is:

`CLOSED -> SYN-SENT -> ESTABLISHED -> FIN-WAIT/CLOSE-WAIT -> CLOSED`

The exact states depend on who initiates the close and how the exchange proceeds. A graceful close sends FIN in one direction, receives an ACK, and later exchanges FIN/ACK for the other direction. A reset immediately tears down state.

TIME_WAIT protects against old duplicate segments and allows a safe reuse of the four-tuple. It can temporarily keep a port unavailable after a rapid close/reopen sequence.

### 12. Checksum, MSS, and performance

The **maximum segment size (MSS)** is the largest TCP payload a device expects to receive in one segment, negotiated during the handshake or discovered through PMTUD. It is different from the path MTU because TCP and IP headers consume space.

Throughput is limited by the smaller of the available path capacity and the sender's window/rate. A high-bandwidth path needs a large enough window:

`bytes in flight >= bandwidth x RTT`

If the window is too small, the sender waits even though the link could carry more. If it is too large, queues and loss may increase.

## Worked examples

### Example 1: Three-way handshake

Client sends `SYN, seq=1000`. Server replies `SYN, ACK, seq=5000, ack=1001`. Client sends `ACK, ack=5001`. Both then use sequence numbers from `1001` and `5001`.

### Example 2: Lost segment and duplicate ACK

The client sends segments 1000–1999, 2000–2999, and 3000–3999. The second is lost. The receiver repeatedly ACKs 2000 when later segments arrive. After enough duplicate ACKs, the sender fast-retransmits bytes beginning at 2000. It may also reduce its congestion window.

### Example 3: Zero receive window

The receiver's buffer is full and advertises `rwnd=0`. The sender stops normal data. A window probe eventually reaches the receiver. After the application reads data, the receiver advertises a positive window and transmission resumes.

### Example 4: Congestion control

The sender has `cwnd=10 MSS` and `rwnd=20 MSS`. It can send at most 10 MSS before the next ACK. If congestion is detected, `cwnd` may fall and the effective rate decreases. If the receiver window is smaller, it becomes the limiting control.

### Example 5: Stream boundary

A client writes `HELLO` and `WORLD` separately. The network may combine them in one segment, and the server may read one or both in one or two reads. The application must add a delimiter or length field if message boundaries matter.

### Example 6: Graceful close

The client sends FIN, the server ACKs it. The server may still send remaining data, then sends its own FIN. The client ACKs the server FIN and enters TIME_WAIT. Both directions are eventually closed.

## Key terms & formulas

- **TCP:** connection-oriented reliable byte-stream transport protocol.
- **Segment:** TCP transport PDU.
- **Byte stream:** ordered stream without preserved application message boundaries.
- **SYN:** synchronise sequence numbers/open connection.
- **ACK:** acknowledge received bytes/control state.
- **FIN:** graceful close of one direction.
- **RST:** abrupt reset.
- **Sequence number:** byte position in the stream.
- **Cumulative ACK:** ACK through a byte position.
- **SACK:** selective acknowledgement option for out-of-order blocks.
- **Checksum:** error detection over TCP header/data.
- **MSS:** maximum TCP payload per segment.
- **RTT:** round-trip time.
- **BDP:** `R x RTT`.
- **rwnd:** receiver flow-control window.
- **cwnd:** congestion window.
- **Effective limit:** `min(rwnd, cwnd)`.
- **Header minimum:** 20 bytes.
- **Port range:** 16 bits, 0–65,535.
- **TIME_WAIT:** state protecting old duplicates and tuple reuse.

## Common mistakes

1. **TCP is not message-oriented.** It provides a byte stream.
2. **TCP is not simply IP with a guarantee on every segment.** It recovers missing data at the endpoints.
3. **An ACK number usually means the next expected byte.** Do not always interpret it as the last byte received.
4. **A checksum does not repair a segment.** It usually causes silent discard.
5. **Sequence numbers and ACKs do not prevent congestion.** They support recovery; `cwnd` controls load.
6. **rwnd and cwnd are not the same.** One protects the receiver, the other the network.
7. **TCP is not always faster than UDP.** It has setup and retransmission overhead.
8. **FIN closes one direction.** TCP is full duplex; both directions must close.
9. **The MSS is not the IP MTU.** It describes TCP payload and excludes headers.
10. **A large TCP window requires memory and can worsen loss.** It is not always better.
11. **TCP's checksum is not cryptographic authentication.** Use TLS for hostile-network security.

## Exam prep

### Likely 2-mark questions

1. **List four features of TCP.**  
   Hint: connection-oriented, reliable byte stream, ordering, ACK/retransmission, flow/congestion control, checksum.
2. **Why does TCP use both sequence numbers and ACKs?**  
   Hint: identify/order and confirm receipt/recover loss.
3. **What is the minimum TCP header size?**  
   Hint: 20 bytes, excluding optional fields and payload.
4. **State the effective sending limit.**  
   Hint: `min(rwnd, cwnd)`.
5. **Differentiate TCP from UDP in two ways.**  
   Hint: connection/reliability versus low-overhead datagrams.
6. **What does TIME_WAIT protect?**  
   Hint: old duplicate segments and safe four-tuple reuse.

### Likely long-answer questions

1. **Explain TCP's reliable byte-stream service.**  
   Answer hint: connection, segmentation, sequence, checksum, ACK, loss detection, retransmission, ordering, duplicate suppression, and flow/congestion control.
2. **Draw and explain the three-way handshake and graceful close.**  
   Answer hint: SYN/SYN-ACK/ACK, sequence agreement, options, FIN/ACK per direction, TIME_WAIT.
3. **Explain TCP sliding windows and the difference between `rwnd` and `cwnd`.**  
   Answer hint: effective limit, receiver buffer, network congestion, BDP, and zero window.
4. **Trace a lost TCP segment and explain fast retransmit/recovery.**  
   Answer hint: duplicate ACKs, missing sequence range, retransmission, congestion response, SACK possibility.
5. **Compare TCP and UDP for file transfer, voice, DNS, and email.**  
   Answer hint: reliability, delay, message boundaries, header/setup overhead, and application recovery.

### Short-answer revision checklist

Be able to draw a TCP header from memory, write a four-tuple, explain the three-way handshake, calculate BDP, and trace a loss through ACKs and retransmission.
