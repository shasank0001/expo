---
subject: cn
unit: 4
topic: tcp-connection-management
syllabus_ref: CSM3103 Unit-IV
status: draft
---
# TCP Connection Management

## Overview

A TCP connection is a stateful relationship between two sockets. Before application data is sent, the endpoints normally establish state and agree on initial sequence numbers. When the exchange ends, each direction is closed and the protocol protects against old duplicate segments.

The **three-way handshake** uses SYN, SYN+ACK, and ACK. **Graceful termination** uses FIN and ACK, normally in both directions. A reset can abort a connection. State timers and sequence numbers help recover from lost or duplicate control segments.

Connection management is the control foundation for TCP reliability, ordered data, retransmission, and flow/congestion control. It adds a round-trip setup cost and endpoint state, which is why real-time applications sometimes choose UDP.

## Explanation

### 1. Why connection state is needed

TCP must know where one byte stream begins, which bytes have been received, and which endpoint is permitted to send. The initial sequence number and acknowledgement state identify the connection's byte space. Options such as MSS, window scaling, SACK, and timestamps can be negotiated during establishment.

A connection is identified by the local and remote IP addresses and ports plus the protocol. Multiple applications can use different source ports, and several connections can share the same server port.

### 2. Three-way handshake

Assume the client chooses initial sequence number `x` and the server chooses `y`.

1. **Client -> server: SYN, seq=x.** The client requests a connection and announces its starting sequence number.
2. **Server -> client: SYN+ACK, seq=y, ack=x+1.** The server acknowledges the client's SYN and supplies its own starting sequence number.
3. **Client -> server: ACK, ack=y+1.** The client acknowledges the server's SYN.

After the third ACK, both endpoints can send application data. The handshake synchronises sequence numbers, confirms that both sides can communicate, and exchanges options. It takes one round trip before ordinary data can begin.

The SYN may carry options such as maximum segment size, window scale, timestamps, and SACK permission. The two endpoints do not necessarily have identical resources; the negotiated values govern later behaviour.

### 3. SYN synchronisation and old duplicates

A delayed or duplicated SYN must not accidentally create a new connection. TCP's sequence-number space and the acknowledgement of the SYN help the receiver associate a request with a live socket. The handshake also prevents a blind old duplicate from being treated as a fresh data stream in the normal way.

A SYN flood is a different attack: many forged SYNs consume half-open state. SYN cookies, firewalls, rate limits, and monitoring can mitigate it. A connection protocol does not guarantee protection against malicious control traffic.

### 4. Connection states

A simplified state model is:

- **CLOSED:** no connection exists.
- **LISTEN:** server waits for a SYN.
- **SYN-SENT:** client has sent SYN and waits.
- **SYN-RECEIVED:** server has received SYN and sent SYN+ACK.
- **ESTABLISHED:** handshake complete; data can flow.
- **FIN-WAIT-1/2:** local side initiated close.
- **CLOSE-WAIT:** peer requested close, but local application may still send.
- **LAST-ACK:** local side has closed and waits for final ACK.
- **TIME-WAIT:** wait for old segments to expire.
- **CLOSING:** simultaneous close.

A real implementation can have additional states, retransmission behaviour, and error paths. The names are useful for explaining setup and teardown.

### 5. Data during an established connection

Once established, both sides can send data simultaneously. Each direction has its own sequence and acknowledgement state. A segment can contain data, an ACK-only update, or both. TCP can send several segments in flight up to its send window.

The application need not wait for a connection to send every message after establishment, although the initial setup is complete. A connection can carry requests and responses in either direction.

### 6. Graceful close

A TCP endpoint closes its sending direction by sending a FIN. The receiver ACKs the FIN. Because TCP is full duplex, the receiver may continue sending data in the opposite direction until it also sends a FIN.

A common sequence is:

1. A sends `FIN`.
2. B sends `ACK`.
3. B finishes its remaining data and sends `FIN`.
4. A sends `ACK`.
5. A waits in `TIME-WAIT` before fully closing/reusing the tuple.

FIN consumes one sequence number. A FIN is not a request to destroy all state immediately; it indicates that no more data will be sent in that direction.

### 7. TIME_WAIT

TIME_WAIT protects the connection from delayed duplicate segments from an earlier incarnation of the same four-tuple. It also allows the final ACK to be retransmitted if lost and gives the network time to clear old packets.

TIME_WAIT can consume a port or connection state for a period, especially on servers that make many short connections. It is a correctness mechanism, not an error state. TCP can use connection reuse strategies, but the protection remains important.

### 8. Abrupt close and reset

A **reset (RST)** immediately abandons state and usually causes an application to receive an error. It is used for some error conditions and by protocols that do not want a graceful exchange. A reset can be caused by a port with no listener, an invalid sequence, or a deliberate abort.

A reset does not provide a reliable delivery report for data already sent. Data may be lost, and the application must handle the failure.

### 9. Timers and connection failures

A connection can fail if a path breaks, a peer crashes, a firewall drops state, or a sequence of packets is lost. Retransmission timers, keepalive mechanisms, and idle timeouts allow TCP to detect some failures. Application-level heartbeats may be needed for long idle connections.

A retransmission timer is not a connection-establishment timer. Setup, data, and close exchanges can have different timers and state transitions.

### 10. Connection security

TCP itself authenticates the tuple, not a user's identity. A malicious or misconfigured endpoint can use a valid address. Applications use TLS, SSH, certificates, passwords, or other authentication and encryption protocols after TCP establishes the byte stream.

TCP sequence numbers are not secrets against an attacker who can observe or inject traffic. Security must be added above the transport layer.

## Worked examples

### Example 1: Handshake with numbers

Client sends `SYN seq=4000`; server replies `SYN+ACK seq=7000 ack=4001`; client sends `ACK ack=7001`. The first application byte from the client is sequence 4001. The server's first application byte is sequence 7001.

### Example 2: Lost SYN

The client's first SYN is lost. No server reply arrives, so the client retransmits. If the original SYN reached the server but its SYN+ACK was lost, the server may retain a half-open state. The retransmitted SYN is handled according to TCP state and sequence rules.

### Example 3: Lost final ACK

B receives A's FIN and ACKs it, then sends its own FIN. If the final ACK is lost, A retransmits the ACK or appropriate segment while B is in LAST-ACK. The connection eventually closes.

### Example 4: Simultaneous close

Both applications send FIN at nearly the same time. Each ACKs the other's FIN. TCP uses states such as CLOSING and TIME-WAIT to finish safely rather than assuming a strict client/server order.

### Example 5: One direction closes

A sends all of its data and FIN. B ACKs and continues sending data in the reverse direction. A can still receive B's data until B sends its own FIN. This is why FIN is a half-close signal.

## Key terms & formulas

- **Connection:** stateful TCP relationship between two sockets.
- **Three-way handshake:** SYN -> SYN+ACK -> ACK.
- **SYN:** synchronise sequence numbers and request connection.
- **SYN+ACK:** acknowledge SYN and supply server sequence number.
- **Initial sequence number (ISN):** starting byte sequence selected by an endpoint.
- **FIN:** graceful close of one direction.
- **RST:** reset/abrupt error.
- **TIME_WAIT:** protection after close for old duplicates and safe tuple reuse.
- **Half-close:** one direction closed while the other remains usable.
- **ESTABLISHED:** handshake-complete state.
- **Connection tuple:** source/destination address and port plus protocol.
- **FIN sequence:** FIN consumes one sequence number.
- **SYN consumption:** SYN consumes one sequence number.
- **Handshake RTT:** roughly one round trip before ordinary data.

## Common mistakes

1. **The three-way handshake is not data transfer.** It establishes state and sequence synchronisation.
2. **SYN, SYN-ACK, and ACK are not three data segments.** They are control segments with sequence/ACK information.
3. **A SYN+ACK acknowledges the client's SYN with `ISN+1`.** Do not use the client's initial number without adding one.
4. **TCP close is full duplex.** A FIN closes only one direction.
5. **TIME_WAIT is not a failure state.** It protects correct reuse and old duplicates.
6. **A reset is not graceful closure.** It abandons state and may report an error.
7. **A connection is not a physical circuit.** It is endpoint state and a logical byte stream.
8. **The server's listening port does not identify one connection alone.** The four-tuple is needed.
9. **TCP does not authenticate the user.** TLS or application security is separate.
10. **The handshake cannot prevent a SYN flood.** Resource protection and filtering are needed.

## Exam prep

### Likely 2-mark questions

1. **List the three segments of a TCP handshake.**  
   Hint: SYN, SYN+ACK, ACK.
2. **Why is it called a three-way handshake?**  
   Hint: both sides send control segments and acknowledge each other's sequence numbers.
3. **What does FIN mean?**  
   Hint: graceful close of one sending direction.
4. **What is TIME_WAIT?**  
   Hint: post-close protection against old duplicates and unsafe tuple reuse.
5. **Differentiate FIN and RST.**  
   Hint: graceful direction close versus abrupt reset.
6. **What is a half-close?**  
   Hint: one direction is closed while the other can still send.

### Likely long-answer questions

1. **Draw and explain the TCP three-way handshake.**  
   Answer hint: client/server roles, ISNs, ACK values, options, states, and round-trip cost.
2. **Explain graceful TCP termination and TIME_WAIT.**  
   Answer hint: independent FIN directions, ACKs, retransmission, old duplicates, and port reuse.
3. **Discuss lost SYN, lost ACK, and simultaneous close cases.**  
   Answer hint: timers, duplicate handling, state machines, and final stable state.
4. **Compare connection-oriented TCP with connectionless UDP for a chosen application.**  
   Answer hint: setup, state, reliability, delay, message boundaries, and recovery.

### Short-answer revision checklist

Be able to write the handshake with sequence numbers, list simplified TCP states, explain a half-close, and state why TIME_WAIT exists.
