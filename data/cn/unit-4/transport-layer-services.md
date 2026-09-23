---
subject: cn
unit: 4
topic: transport-layer-services
syllabus_ref: CSM3103 Unit-IV
status: draft
---
# Transport-Layer Services

## Overview

The **transport layer** provides end-to-end communication between application processes across one or more networks. The network layer moves packets between hosts; the transport layer identifies the source and destination processes, divides data into manageable units, and can add reliability, ordering, flow control, and congestion control.

The syllabus names transport services, elements of transport protocols, TCP, and UDP. This file explains the purpose and scope of the transport layer, connection-oriented and connectionless services, process addressing, multiplexing, segmentation/reassembly, reliability, error control, QoS, and the relationship between network and transport layers.

## Explanation

### 1. Network layer versus transport layer

The network layer provides **host-to-host** delivery. If a server has several applications, its IP address alone does not tell which application should receive a packet. The transport layer adds a port number for each endpoint and therefore provides **process-to-process** communication.

A transport segment travels inside IP packets. The network layer routes it through routers, but routers normally do not examine the transport port or provide end-to-end reliability. The destination host's transport layer examines the port and delivers the data to the correct process.

A common example is a web server at `192.0.2.10` listening on port 443. Another service on the same host can listen on port 53. Both use the same IP interface, but the ports distinguish the services.

### 2. Transport-layer services

A transport protocol may provide:

- **connection management:** establish, maintain, and close communication state;
- **multiplexing:** many applications share one host/network;
- **segmentation and reassembly:** divide data and rebuild it;
- **error control:** detect damaged, lost, or duplicate data;
- **sequence/order:** arrange data in a usable order;
- **acknowledgement:** confirm receipt;
- **retransmission:** recover missing data;
- **flow control:** protect a receiver;
- **congestion control:** protect the network;
- **connection reset or error reporting:** signal failures.

Not every protocol provides all services. UDP supplies a small connectionless service and leaves reliability to the application. TCP supplies a reliable, ordered, connection-oriented byte stream. Other transport protocols can provide different trade-offs.

### 3. Connection-oriented service

A **connection-oriented** service establishes a logical connection before data transfer. The endpoints agree on state and parameters, exchange data, and release the connection. It can provide ordered delivery, acknowledgements, retransmission, flow control, and congestion control.

TCP uses a three-way handshake for establishment and a FIN exchange for graceful closure. Connection setup costs time and router/endpoint state, but it supports reliable stateful communication. A connection is normally identified by the two endpoint addresses and ports, along with protocol information.

### 4. Connectionless service

A **connectionless** service sends each message without first establishing connection state. There is no setup handshake and no built-in guarantee of delivery, ordering, duplicate suppression, or flow control.

UDP is the standard example. It is useful for short requests, real-time traffic, broadcast/multicast, and applications that prefer low delay or can tolerate loss. A connectionless protocol can still provide an error check; the absence of connection does not mean the absence of any control field.

### 5. Multiplexing and demultiplexing

**Multiplexing** combines data from many application processes so that one host/network can carry multiple flows. **Demultiplexing** examines the destination port and delivers a segment to the correct process.

A transport connection is normally identified by:

- source IP address and source port;
- destination IP address and destination port;
- transport protocol and address family.

A server can listen on one port and accept many simultaneous connections. The server's operating system uses the four-tuple to keep their state separate.

### 6. Segmentation and reassembly

Applications may write a large file or a small control message. The transport layer divides application data into transport units—TCP segments or UDP datagrams—and the receiver reassembles or delivers them according to the protocol. Each unit carries a length and control fields.

TCP provides a byte stream: the receiver can deliver bytes to the application without preserving the boundaries of every application write. UDP preserves the boundary of each datagram, subject to maximum size and the network's ability to deliver it. Segmentation affects headers, timing, loss recovery, and buffer requirements.

### 7. Error control

Transport error control can detect corruption using a checksum, identify missing or duplicate data with sequence numbers, confirm receipt with acknowledgements, and recover with retransmission. A checksum detects errors but cannot repair a packet by itself. A retransmission request requires a protocol policy and, normally, a return path.

Reliability is end-to-end: it covers the entire path, not only one cable. It can therefore detect a loss caused by a congested queue several hops away. A link-layer FCS is still useful locally, but TCP provides path-wide recovery.

### 8. Flow control

Flow control protects a receiver from a fast sender. The receiver advertises how much data it can accept, usually through a window. The sender must not send beyond that amount until the window advances.

The receiver's application reads buffered data, then advertises more space. A zero window tells the sender to stop new data until a probe or update indicates that space is available. Flow control protects the receiver's buffer; it does not automatically protect an intermediate router.

### 9. Congestion control

Congestion control protects shared network resources. A sender reduces its rate when it detects loss, delay, or an explicit congestion signal. TCP maintains a congestion window in addition to the receiver window.

The effective sending limit is commonly the smaller of the receiver window and congestion window. This separates the question “how much can the receiver take?” from “how much can the network sustain?” Congestion control is not a guaranteed delay or bandwidth promise.

### 10. Connection establishment and teardown

A connection-oriented protocol needs to agree on initial sequence numbers and options. TCP uses SYN, SYN-ACK, and ACK. During data transfer, both endpoints can send simultaneously. A graceful close uses FIN and ACK for each direction, followed by a state such as TIME_WAIT.

A reset is an abrupt teardown. A half-open connection is one side believes it is established while the peer has lost state. Timers and sequence numbers help detect and recover from such failures.

### 11. Ports and well-known services

Port numbers are 16 bits and range from 0 to 65,535. Some are reserved or assigned by standards. Familiar examples include:

- 20/21: FTP data/control;
- 25: SMTP;
- 53: DNS;
- 67/68: DHCP;
- 80: HTTP;
- 110: POP3;
- 143: IMAP;
- 443: HTTPS;
- 161/162: SNMP requests/notifications.

A port is meaningful with a transport protocol and address family. TCP port 443 and UDP port 443 are different endpoints.

### 12. QoS and application requirements

Different applications prefer different transport services. File transfer and web downloads value reliability and throughput. Voice and video value delay and jitter, and may prefer a late packet to a retransmitted one. Gaming and telemetry may use UDP with application-level recovery. A transport service should match these needs rather than maximise reliability for every application.

## Worked examples

### Example 1: Two services on one host

A laptop sends an IP packet to `192.0.2.10:53` and another to `192.0.2.10:443`. The IP address is the same, but the destination port selects DNS or HTTPS. This is process-to-process delivery.

### Example 2: Connection-oriented transfer

A TCP client opens a connection, exchanges data, receives ACKs, retransmits a lost segment, and closes gracefully. The handshake and FIN exchange add setup/teardown work but give a reliable ordered service.

### Example 3: Connectionless voice

A voice application sends a datagram every 20 ms. If one is lost or arrives late, the application may conceal or skip it rather than wait for retransmission. The low-overhead service matches the real-time requirement.

### Example 4: Segmentation

An application writes 10,000 bytes. TCP may segment them according to the maximum segment size and congestion window. The receiver supplies bytes to the application in order. A UDP application sending a 10,000-byte message would need fragmentation at the IP layer and has a larger datagram limit.

### Example 5: Flow control

A receiver has only 8 KB of buffer and advertises an 8-KB window. A sender with a much larger congestion window can send only 8 KB before waiting. As the application reads data, the advertised window grows.

## Key terms & formulas

- **Transport layer:** Layer 4, process-to-process communication.
- **Port:** 16-bit process endpoint number, 0–65,535.
- **Socket/connection four-tuple:** `(source IP, source port, destination IP, destination port)`, plus protocol/family.
- **Multiplexing:** combine application flows.
- **Demultiplexing:** direct a flow to its destination process.
- **Segment:** TCP transport PDU.
- **Datagram:** UDP transport PDU.
- **Connection-oriented:** establish state before data.
- **Connectionless:** no setup; independent units.
- **Reliability:** error detection, ordering, ACK, and retransmission.
- **Flow control:** receiver protection.
- **Congestion control:** network protection.
- **Effective TCP limit:** approximately `min(rwnd, cwnd)`.
- **MSS:** maximum TCP payload in a segment, excluding headers.
- **Port examples:** DNS 53, HTTP 80, HTTPS 443, SMTP 25, SNMP 161/162.

## Common mistakes

1. **The transport layer identifies processes, not routes.** Ports deliver data; routers choose paths.
2. **A connectionless protocol is not necessarily unreliable by accident.** UDP deliberately provides no reliability guarantee.
3. **Connection-oriented does not mean only one packet.** After setup, many segments can flow.
4. **A port is not a physical address.** It is a logical endpoint number.
5. **TCP port 443 and UDP port 443 are different.** Ports are interpreted with the transport protocol.
6. **Multiplexing and demultiplexing are opposite operations.** One combines; one separates.
7. **A checksum does not retransmit data.** Recovery needs a protocol policy.
8. **Flow control and congestion control use different limits.** `rwnd` protects the receiver; `cwnd` protects the network.
9. **TCP is a byte stream, not a message service.** Application write boundaries are not necessarily preserved.
10. **UDP datagram boundaries are important.** A datagram is delivered as a unit, if it arrives at all.
11. **A four-tuple alone is not universally sufficient.** Protocol and address family may also be needed.

## Exam prep

### Likely 2-mark questions

1. **State the purpose of the transport layer.**  
   Hint: end-to-end communication between application processes across networks.
2. **Define multiplexing and demultiplexing.**  
   Hint: combine many flows and direct each to the right process.
3. **Differentiate connection-oriented and connectionless services.**  
   Hint: setup/state/reliability versus independent low-overhead messages.
4. **Why are ports needed?**  
   Hint: multiple applications share one host/IP address.
5. **Differentiate flow control and congestion control.**  
   Hint: receiver versus shared-network protection.
6. **Name two functions of TCP and one limitation of UDP.**  
   Hint: reliability/ordering/flow/congestion versus no ACK/retransmission/order.

### Likely long-answer questions

1. **Explain the services provided by the transport layer.**  
   Answer hint: process addressing, multiplex, segmentation, connection management, reliability, flow/congestion, and QoS.
2. **Compare TCP and UDP from the transport-service perspective.**  
   Answer hint: setup, PDU, reliability, order, headers, latency, and applications.
3. **Trace a TCP connection from setup through data and close.**  
   Answer hint: three-way handshake, byte stream, ACKs, FIN directions, and TIME_WAIT.
4. **Explain flow control and congestion control with a `min(rwnd, cwnd)` example.**  
   Answer hint: receiver buffer versus network bottleneck, windows, ACK feedback, and adaptation.
5. **Explain segmentation and message boundaries in TCP and UDP.**  
   Answer hint: TCP byte stream, MSS, reassembly, UDP datagram boundary, IP fragmentation, and application implications.

### Short-answer revision checklist

Be ready to state the four-tuple, explain the transport/network-layer distinction, compare connection modes, and list the services that TCP adds over UDP.
