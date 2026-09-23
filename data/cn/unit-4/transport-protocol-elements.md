---
subject: cn
unit: 4
topic: transport-protocol-elements
syllabus_ref: CSM3103 Unit-IV
status: draft
---
# Elements of Transport Protocols

## Overview

A transport protocol coordinates communication between application processes across an internetwork. Its design is made from several elements: connection management, segmentation and reassembly, multiplexing, error control, sequencing, flow control, congestion control, and sometimes state or service management.

No single element solves every problem. Sequence numbers identify data, acknowledgements confirm receipt, retransmission recovers loss, flow control protects a receiver, and congestion control protects shared routers. Their interaction determines latency, throughput, reliability, and complexity.

The syllabus explicitly lists elements of transport protocols before TCP and UDP. This file explains each element, the relationship between them, connection modes, and design trade-offs. TCP and UDP receive more detailed treatment in their own files.

## Explanation

### 1. Connection management

Connection management covers:

- establishing a connection and agreeing on initial state;
- authenticating or identifying the peer where required;
- negotiating options such as maximum segment size or window scaling;
- maintaining state while data is transferred;
- detecting a failed peer;
- closing each direction gracefully or resetting the connection.

A connection-oriented protocol has setup and teardown cost, but state can support reliable sequence and recovery. A connectionless protocol sends units without setup. It is simpler and often faster for short or delay-sensitive exchanges.

A robust protocol must handle a lost setup message, a duplicate setup, a reset, and an idle peer. A connection should not remain half-open indefinitely.

### 2. Multiplexing and demultiplexing

**Multiplexing** allows many application processes to share a host's network interface. **Demultiplexing** uses an address or port to deliver a received unit to the correct process.

A TCP or UDP endpoint is identified by source/destination IP addresses and ports, plus the transport protocol. Multiplexing improves efficiency because one host need not use a separate physical network for every application. It also creates security concerns: a port must not be treated as proof of identity.

### 3. Segmentation and reassembly

Applications can send messages larger than the maximum transport unit. **Segmentation** divides data into segments or datagrams; **reassembly** rebuilds a stream or message at the receiver. The protocol may add a length, sequence number, and checksum.

TCP provides a byte stream: an application write can be combined with or split among reads. UDP preserves each datagram boundary, but the datagram must fit within transport and path limits. Segmentation affects header overhead, latency, buffer requirements, and loss recovery.

### 4. Sequence numbers and ordering

Sequence numbers identify positions in a byte stream or numbered units. They allow the receiver to:

- order data;
- detect missing data;
- recognise duplicates;
- acknowledge a precise position;
- place retransmitted data correctly.

The sequence-number space may wrap. A protocol must compare numbers with modular arithmetic, not ordinary greater-than/less-than always. Sequence numbers do not themselves prove that a byte arrived; they work with checksums and acknowledgements.

### 5. Acknowledgement

An **acknowledgement (ACK)** tells the sender that data up to a position or within a set of ranges has been received. It can be cumulative or selective, immediate or delayed.

An ACK reduces the sender's uncertainty, but it may be delayed or lost. The sender therefore uses timers and duplicate information to infer loss. Acknowledgements also carry window updates and can affect the sender's rate of transmission.

### 6. Error control

Error control can include:

- checksum for accidental corruption;
- sequence number for loss/duplication/order;
- ACK for receipt;
- retransmission for missing data;
- duplicate suppression;
- reset or error notification.

A checksum alone cannot correct a payload. A transport protocol can detect damage and discard a segment, while the receiver asks for a retransmission. A cryptographic authentication mechanism is needed when protection from deliberate modification is required.

### 7. Retransmission and recovery

When a sender does not receive the required acknowledgement before a timeout, it may retransmit. A duplicate ACK or fast-retransmit signal can trigger an earlier retry. The receiver uses sequence numbers to discard duplicates and deliver only the appropriate data.

Retransmission adds traffic and can worsen congestion. A good transport protocol combines recovery with a rate-control mechanism. It may limit retries, use exponential backoff, or report a failure when recovery is not useful.

### 8. Flow control

Flow control protects the receiver. The receiver advertises a window based on available buffer. The sender must limit outstanding data to that window. A zero window pauses normal transmission; window probes help detect when the receiver's application has made space.

The window is a bound on data in flight, not a guarantee that the network is uncongested. A receiver can have plenty of memory while a router in the path is full.

### 9. Congestion control

Congestion control protects the network and reacts to loss, delay, or an explicit signal. A sender maintains a congestion window and increases it gradually, reducing it when the network appears overloaded. TCP's congestion-control variants use different growth and loss-recovery rules.

The effective sending allowance is generally the smaller of the receiver window and congestion window:

`send limit = min(rwnd, cwnd)`

This formula makes the two controls distinct: one is a receiver limit, the other a network limit.

### 10. Full-duplex and independent directions

Many transport connections allow both endpoints to send data simultaneously. Each direction has its own sequence space, ACK state, and buffer, while the connection shares negotiated parameters. Closing one direction does not necessarily close the other immediately.

A half-duplex protocol must coordinate turns. Full duplex improves efficiency but can make state and fairness more complex.

### 11. Service guarantees and QoS

A transport protocol may offer different services to applications: reliable ordered stream, reliable message, unreliable datagram, real-time stream, or multicast. It can use priority, deadlines, or traffic classes. A guarantee requires resources and enforcement; a header field alone is not enough.

### 12. Protocol element interactions

Elements are interdependent:

- segmentation chooses a size that fits a path and buffer;
- sequence numbers identify segments after segmentation;
- ACKs free sequence space and update flow control;
- retransmission uses sequence numbers and timers;
- congestion control limits the amount and rate of new data;
- multiplexing uses ports to separate applications;
- connection management stores all of this state.

A change to one element can affect the others. A larger receive window can improve a high-bandwidth path but require more memory. A faster timeout can recover loss sooner but cause unnecessary retransmissions.

## Worked examples

### Example 1: Loss recovery

A TCP segment is lost. Later segments arrive and produce duplicate ACKs. The sender fast-retransmits the missing sequence range. The receiver's sequence numbers and checksum prevent duplicate or damaged bytes from being delivered. The congestion window may then be reduced because loss is a congestion signal.

### Example 2: Flow-control protection

The receiver's buffer is 4 KB and it advertises a 4-KB window. The sender's congestion window is 64 KB, so its effective limit is only 4 KB. As the application reads 2 KB, the receiver advertises a larger window. This is receiver protection, not proof that the network is uncongested.

### Example 3: Multiplexing

A laptop opens two TCP connections from the same IP address using different source ports, one to a web server and one to a file server. The receiver's port identifies the correct application. A firewall can inspect and control each flow.

### Example 4: UDP segmentation

A voice application sends a 160-byte datagram every 20 ms. UDP adds a header and passes the datagram to IP. If the path MTU is too small, IP may fragment it; modern applications normally choose a datagram size that avoids fragmentation. UDP itself has no segmentation/reassembly protocol above IP.

### Example 5: Connection teardown

One endpoint sends FIN for its sending direction. The peer ACKs it but may still send data in the other direction. Later the peer sends its own FIN. TIME_WAIT protects against old duplicate segments when addresses are reused.

## Key terms & formulas

- **Connection management:** establish, maintain, and terminate state.
- **Multiplexing:** share one host/network among processes.
- **Demultiplexing:** deliver a flow to the correct process.
- **Segmentation:** divide application data into transport units.
- **Reassembly:** rebuild data at the receiver.
- **Sequence number:** position/identity of data.
- **Cumulative ACK:** ACK through a position.
- **Checksum:** detect accidental corruption.
- **Retransmission:** resend missing data.
- **Duplicate suppression:** discard already received sequence positions.
- **Flow-control window `rwnd`:** receiver's advertised capacity.
- **Congestion window `cwnd`:** sender's network-load estimate.
- **Effective limit:** `min(rwnd, cwnd)`.
- **Timeout:** recovery timer for missing ACK/data.
- **Full duplex:** simultaneous bidirectional data.
- **Transport PDU:** TCP segment or UDP datagram.

## Common mistakes

1. **Sequence numbers do not correct data.** They identify/order it; recovery needs ACK and retransmission.
2. **An ACK is not necessarily immediate.** It can be cumulative or delayed.
3. **Retransmission is not congestion control.** It can increase congestion unless rate is reduced.
4. **Flow control and congestion control are different.** One is `rwnd`, the other `cwnd`.
5. **Multiplexing is not segmentation.** One combines flows; the other divides data.
6. **TCP segmentation is not message preservation.** TCP is a byte stream.
7. **UDP has a checksum but no reliable recovery.** It does not automatically retransmit.
8. **A connection is not a physical circuit.** It is protocol state between endpoints.
9. **A larger window requires more state and memory.** It is not automatically better.
10. **A FIN closes one direction, not necessarily both immediately.** TCP is full duplex.

## Exam prep

### Likely 2-mark questions

1. **List four elements of a transport protocol.**  
   Hint: connection management, segmentation, multiplexing, error control, sequence, flow/congestion control.
2. **Define multiplexing and demultiplexing.**  
   Hint: sharing and delivery to the right process.
3. **Differentiate flow control and congestion control.**  
   Hint: receiver versus network; `rwnd` versus `cwnd`.
4. **What is a sequence number used for?**  
   Hint: ordering, loss detection, duplicate recognition, and ACKs.
5. **What is the role of segmentation?**  
   Hint: fit data into manageable units and control overhead.
6. **State the TCP effective sending limit.**  
   Hint: `min(rwnd, cwnd)`.

### Likely long-answer questions

1. **Explain all elements of a transport protocol and their interactions.**  
   Answer hint: connection, ports, segmentation, sequence, ACK, recovery, flow/congestion, and teardown.
2. **Compare error control, flow control, and congestion control with a loss scenario.**  
   Answer hint: checksum/ACK/retransmission, receiver window, and network window.
3. **Explain why transport protocols multiplex and how a four-tuple identifies a connection.**  
   Answer hint: many applications per host, addresses/ports/protocol, and demultiplexing.
4. **Discuss the trade-offs of larger transport windows and shorter timers.**  
   Answer hint: bandwidth-delay, memory, loss, retransmission, and responsiveness.

### Short-answer revision checklist

Be ready to list at least eight protocol elements, explain `min(rwnd, cwnd)`, draw a four-tuple, and trace a lost segment through ACK/retransmission.
