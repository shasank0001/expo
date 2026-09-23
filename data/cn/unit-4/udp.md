---
subject: cn
unit: 4
topic: udp
syllabus_ref: CSM3103 Unit-IV
status: draft
---
# User Datagram Protocol (UDP)

## Overview

**User Datagram Protocol (UDP)** is a simple, connectionless transport protocol for process-to-process communication. It sends each datagram independently, without a handshake, sequence number, acknowledgement, retransmission, flow control, or built-in congestion control.

UDP provides low overhead and low setup delay. It is suitable for short request/response exchanges, real-time audio/video, gaming, broadcast, and telemetry when the application can tolerate loss, reordering, or duplication or has its own recovery mechanism. TCP is preferable when complete ordered delivery is essential.

UDP does not mean unreliable hardware or no error check. It has a checksum and ports, and IP still provides best-effort forwarding. The application must decide what to do when data is missing or damaged.

## Explanation

### 1. UDP service

UDP provides a **connectionless datagram** service. Each application message is placed in a datagram, normally with its own boundary. The sender does not first establish a connection or receive an ACK. The destination port identifies the receiving process.

A datagram may be:

- delivered;
- lost;
- duplicated;
- delivered out of order;
- delayed;
- corrupted and then discarded if the checksum detects the error.

UDP itself does not retransmit, reorder, duplicate-suppress, or control congestion. A protocol above UDP may add those functions.

### 2. UDP header

The UDP header is 8 bytes:

- **source port:** 16 bits;
- **destination port:** 16 bits;
- **length:** 16 bits, header plus data;
- **checksum:** 16 bits over the header, data, and an IP pseudo-header.

The header is much smaller than a TCP header. A zero source port has special meanings in some UDP applications, and a zero checksum is allowed only in special IPv4 cases under the relevant standards; normal IPv6 UDP requires checksum protection. Always follow the protocol specification for a particular exam or deployment.

### 3. Connectionless operation

A UDP client can send a datagram without a SYN or ACK exchange. A server receives it on a bound port, processes it, and sends a reply to the source port. The server does not maintain a TCP-like connection state, although it may maintain application-specific state.

A connected UDP socket can restrict communication to one peer and receive ICMP errors more readily, but it remains connectionless and unreliable. Connecting is not equivalent to TCP establishment.

### 4. Ports and multiplexing

The source and destination ports identify application endpoints. A process can bind a well-known port, such as DNS at 53, while clients use ephemeral ports. The operating system demultiplexes incoming datagrams by address family, protocol, address, and port.

UDP supports broadcast and multicast, which are useful for discovery, streaming, and local services. Multicast requires membership and routing support; a datagram sent to a multicast group is delivered to members according to the network's rules.

### 5. Error detection

The UDP checksum detects many accidental errors in the header and payload. The receiver normally discards a datagram with a bad checksum. Detection does not correct the data, and an error pattern can theoretically be missed.

A checksum protects against noise, not a malicious sender. An attacker can modify a datagram and compute a valid checksum. Applications needing authentication or tamper resistance must use an authenticated security mechanism.

### 6. No reliability or ordering

UDP provides no sequence number, so the receiver cannot know whether a datagram is missing or whether two arrived in the intended order. It provides no ACK or timer-based retransmission. A sender that needs reliable transfer must implement or use an upper-layer protocol.

An application can add reliability with its own sequence numbers, ACKs, timers, and retransmission, but then it is effectively using an application-level reliability mechanism. The header and connection overhead of TCP may still be preferable for general file or web transfer.

### 7. No flow or congestion control

UDP has no receive window or sender rate limit. A fast sender can overwhelm a receiver or an intermediate router. A UDP application should implement pacing, rate limits, or a congestion-control algorithm appropriate to its traffic.

This is a major operational responsibility. A real-time application may choose to drop late packets rather than retransmit, but it should still avoid sending more traffic than the network can carry.

### 8. Datagram size and fragmentation

A UDP datagram is carried in an IP packet. The combined UDP header, IP header, and payload must fit the path MTU. If not, IPv4 may fragment the IP packet; the IP fragments are reassembled before UDP is delivered. A lost fragment loses the entire datagram. IPv6 routers do not fragment, so the source uses path-MTU discovery or selects a smaller datagram.

UDP's length field describes the UDP header plus data, not the IP header or link overhead. A large UDP datagram can also be less efficient than several smaller application messages depending on the workload.

### 9. DNS example

A DNS client normally sends a query to UDP port 53. A DNS server sends a response to the client's source port. If the response is too large or truncated, DNS may use TCP. UDP is suitable because queries are usually small, the service is stateless from the transport perspective, and a lost query can be retried by the application.

A DNSSEC query or response has additional record data, but the transport choice remains an application decision.

### 10. Real-time voice and video

A voice application may send a datagram every 20 ms. If a datagram is lost, the application may conceal, interpolate, or skip the sample. If it arrives late, playing it can disrupt the next audio, so it may be discarded. Retransmitting a 100-ms-old voice packet would add more delay than the loss itself.

Video can use UDP for media and another protocol for control, or use a transport such as QUIC over UDP with its own reliability. The lesson is that UDP provides a building block, not a complete real-time service.

### 11. Broadcast, multicast, and discovery

UDP is well suited to one-to-many delivery because the transport does not require a separate connection for every receiver. A service can send to a broadcast address on a local link or a multicast group across a configured network. Network policy must restrict broadcast and multicast where necessary.

A discovery protocol can use a multicast group, collect responses from peers, and choose a suitable endpoint. Security and authorisation are necessary because broadcast/multicast can expose service information.

### 12. UDP versus TCP

| Property | UDP | TCP |
|---|---|---|
| Connection | None | Three-way handshake |
| Service | Datagram | Byte stream |
| Reliability | None built in | Retransmit/order/ACK |
| Flow control | None | `rwnd` |
| Congestion control | None built in | `cwnd` and adaptation |
| Header | 8 bytes | At least 20 bytes |
| Setup delay | Low | Higher |
| Message boundaries | Preserved per datagram | Not preserved |
| Common use | Voice, video, DNS, games | Web, email, file transfer, SSH |

A UDP application can be reliable if it implements reliability above UDP, but then the application—not UDP—owns the trade-offs.

## Worked examples

### Example 1: DNS query

A resolver sends a small DNS query to `198.51.100.53:53` from an ephemeral port. The server sends a response to the source port. If the response is lost, the resolver waits and retries according to its own timeout policy. UDP itself does not retransmit.

### Example 2: Lost voice datagram

A sender emits a 20-ms voice sample. The sample is lost. The receiver plays the next sample or uses concealment. It does not wait for TCP-like retransmission because a late voice packet would be less useful than a short gap.

### Example 3: Oversized datagram

A 1,500-byte payload plus UDP and IP headers exceeds a 1,500-byte path MTU. On IPv4, the packet may be fragmented; a lost fragment loses the datagram. On IPv6, the source receives Path MTU information and sends a smaller datagram.

### Example 4: Congestion responsibility

A UDP game sends an unbounded stream to a server. Queues grow and packets are dropped. Adding a pacing/rate-control mechanism or using a congestion-controlled transport can improve network behaviour even if the application still uses datagrams.

## Key terms & formulas

- **UDP:** connectionless transport protocol.
- **Datagram:** independent UDP message.
- **Header length:** 8 bytes.
- **Source port:** 16 bits.
- **Destination port:** 16 bits.
- **Length:** UDP header plus payload, 16 bits.
- **Checksum:** 16-bit error-detection field with pseudo-header.
- **Port range:** 0–65,535.
- **No ACK:** no built-in receipt confirmation.
- **No sequence number:** no built-in ordering/loss indication.
- **No retransmission:** no automatic recovery.
- **No flow control:** no built-in receiver window.
- **No congestion control:** application responsibility.
- **MTU condition:** `IP header + UDP header + payload <= path MTU`.
- **Datagram size:** maximum constrained by transport and IP/path limits.

## Common mistakes

1. **UDP is not always faster in every network.** Its design reduces overhead, but congestion can still delay packets.
2. **UDP has a checksum.** It detects many errors even though it does not correct them.
3. **UDP is not message-preserving at TCP level.** Each datagram has a boundary, subject to IP fragmentation and delivery.
4. **UDP has no reliability by design.** An application or upper protocol must recover if needed.
5. **UDP ports are separate from TCP ports.** UDP 53 and TCP 53 are different endpoints.
6. **No connection does not mean no state anywhere.** A server or application may maintain its own state.
7. **A UDP datagram is not guaranteed to fit one IP packet.** IPv4 may fragment it; IPv6 source PMTU is needed.
8. **A checksum is not authentication.** A malicious sender can create a valid one.
9. **UDP does not protect the receiver or network.** Rate control and congestion control are application duties.
10. **A lost real-time packet is not always worth retransmitting.** Latency may matter more than completeness.

## Exam prep

### Likely 2-mark questions

1. **State four services UDP does not provide.**  
   Hint: ACK, sequence/reordering, retransmission, flow control, and congestion control.
2. **What is the UDP header size and name its four fields.**  
   Hint: 8 bytes; source/destination port, length, checksum.
3. **Why is UDP suitable for voice?**  
   Hint: low overhead, low delay, and late loss can be preferable to retransmission.
4. **Distinguish UDP from TCP by connection and reliability.**  
   Hint: connectionless datagrams/no built-in recovery versus connected reliable byte stream.
5. **What is a UDP checksum for?**  
   Hint: detect accidental header/data errors, normally by discarding a bad datagram.
6. **What is the role of source and destination ports?**  
   Hint: identify the sending and receiving application endpoints.

### Likely long-answer questions

1. **Explain UDP's service, header, and operation.**  
   Answer hint: connectionless datagrams, ports, checksum, length, no setup, and demultiplexing.
2. **Compare UDP and TCP for a real-time voice call.**  
   Answer hint: delay, setup, loss recovery, header overhead, and application concealment.
3. **Explain why UDP needs application-level congestion and reliability mechanisms.**  
   Hint: no ACK/cwnd/rwnd/retransmission; give a game or custom protocol example.
4. **Discuss UDP, IP fragmentation, and MTU.**  
   Answer hint: header sizes, IPv4 fragmentation, IPv6 PMTU, and loss of a whole datagram.

### Short-answer revision checklist

Be ready to draw the 8-byte UDP header, state the four missing services, compare it with TCP in a table, and explain a real-time loss decision.
