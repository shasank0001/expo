---
subject: cn
unit: 4
topic: tcp-flow-control
syllabus_ref: CSM3103 Unit-IV
status: draft
---
# TCP Flow Control

## Overview

TCP **flow control** protects a receiver from being overwhelmed by a sender. The receiver advertises a **receive window (`rwnd`)** describing how much data it is willing to accept. The sender limits unacknowledged data to that window and adjusts as the receiver consumes data.

Flow control is different from congestion control. Flow control protects the endpoint's buffer; congestion control protects the routers and links inside the network. TCP's effective sending limit is normally the smaller of the receiver window and the congestion window.

The syllabus includes TCP flow control implicitly through transport elements and TCP, so this file covers advertised windows, sequence-space arithmetic, ACKs, zero windows, window scaling, buffer management, fairness, and worked examples.

## Explanation

### 1. Receiver protection

A receiver has limited memory and application processing capacity. A fast sender can fill the receive buffer and cause memory pressure, packet loss, or application stalls. The receiver therefore advertises how much additional data it can accept.

The receive window is not simply the total buffer size. It can be reduced as the buffer fills, based on available space and protocol policy. The sender must not send beyond the advertised allowance.

### 2. Advertised window

In a TCP header, the window field advertises a window relative to the acknowledgement number. The exact scaling rules depend on the negotiated window-scale option and sequence arithmetic. Conceptually, if the receiver has acknowledged data through byte `ACK` and advertises `W` bytes, the sender can have up to `W` bytes outstanding beyond the acknowledged position.

The window moves as ACKs arrive and the receiver reads data. It is a sliding window rather than a fixed lifetime quota.

### 3. `rwnd` and sender state

The receiver window is often written `rwnd`. The sender tracks:

- the highest byte sent;
- the oldest unacknowledged byte;
- the current effective send limit;
- the receiver's advertised window.

A simplified byte-accounting form is:

`usable send window = advertised rwnd - bytes already sent but not acknowledged`

The protocol must use sequence-number arithmetic and handle wrap-around. An application should not treat the field as a simple unsigned integer without considering the TCP state.

### 4. Flow control and congestion control

TCP sender has two major limits:

- `rwnd`: receiver capacity;
- `cwnd`: network congestion estimate.

The effective limit is:

`send limit = min(rwnd, cwnd)`

If `rwnd` is 16 KB and `cwnd` is 8 KB, the sender is congestion-limited even though the receiver has more space. If `cwnd` is 32 KB and `rwnd` is 16 KB, the sender is receiver-limited.

A common mistake is to call `cwnd` flow control or `rwnd` congestion control. Their goals and inputs are different.

### 5. Acknowledgements and window updates

A receiver sends ACKs as data arrives. The ACK advances the left edge of the sender's outstanding window. The receiver may also send a window update when its application reads buffered data and more space becomes available.

ACK frequency is a trade-off. Every segment acknowledged gives quick feedback but adds overhead. Delayed ACKs can reduce traffic but make the sender wait longer. Window scaling allows a large window without requiring a huge 16-bit window field.

### 6. Zero window

A **zero window** means the receiver cannot currently accept new data. A sender should stop normal transmission, but it cannot simply wait forever because the window-update ACK could be lost.

TCP uses window probes or persist timers to send small probes until the receiver responds with a non-zero window. A zero window does not mean the TCP connection is closed; it means the application or buffer is temporarily not ready.

### 7. Window scaling

The TCP window field is limited to 16 bits. **Window scaling**, negotiated during the three-way handshake, interprets the advertised value with a scale factor so a high-bandwidth/high-delay path can keep enough data in flight.

For example, a scale factor of 7 multiplies the 16-bit field by 128, allowing a much larger effective window. The scale factor is meaningful only when both endpoints negotiated it and sequence/window calculations use the same rules.

### 8. Receiver buffer and application speed

The receiver's advertised window depends on:

- receive buffer size;
- bytes already buffered;
- how quickly the application reads data;
- memory and scheduling constraints;
- protocol limits and implementation policy.

A fast network feed with a slow application can produce a small or zero window. The sender is then correctly limited by receiver processing, not by the physical link.

### 9. Flow-control fairness

One connection should not consume all receiver buffer space. Receivers can use per-connection buffers, shared-buffer limits, and fair allocation. A scheduler may reserve space for interactive flows or apply a minimum window.

A receiver's policy is part of TCP performance. It must avoid a state where a connection is starved while another grows without limit. An overly small window can reduce throughput; an overly large window can make loss recovery slow.

### 10. Silly-window syndrome and delayed ACKs

**Silly-window syndrome** occurs when a receiver advertises a tiny window and the sender sends tiny segments, wasting capacity. Delaying ACKs can also interact with a receiver's window-update policy. Nagle's algorithm at the sender and ACK/window handling at the receiver can reduce unnecessary small transmissions.

These are performance mechanisms, not reliability guarantees. A protocol should not create a deadlock or allow one side to wait forever for a window update.

### 11. Connection failure while blocked

A sender in a zero-window or persist state may eventually detect a failed connection through retransmission limits, keepalive, or a reset. It cannot assume that a missing window update is temporary. A timeout should eventually report failure or close the connection, subject to the application's desired retry policy.

### 12. Security and resource exhaustion

An attacker can open many connections and advertise small windows, consuming server state. TCP flow control is not access control. Connection limits, authentication, rate limits, and resource allocation are needed to prevent denial of service.

## Worked examples

### Example 1: Receiver-limited

A receiver advertises `rwnd=16 KB`; the sender's `cwnd=64 KB`. The sender can send only 16 KB beyond the ACKed position. As the application reads data, the receiver advertises a larger window. The sender is limited by the receiver, not the path.

### Example 2: Congestion-limited

The receiver advertises `rwnd=64 KB`, but the sender's congestion window is 12 KB. The effective limit is 12 KB. Increasing the receiver window will not improve throughput until the network window grows.

### Example 3: Zero-window probe

A receiver advertises zero because its application is busy. The sender stops bulk data and sends a window probe after a persist timer. The receiver reads data and returns a non-zero window. The sender resumes from the correct sequence number.

### Example 4: Lost window update

The receiver's window update is lost. A persist probe prompts another update. This prevents a healthy connection from being blocked forever by one lost control segment.

### Example 5: BDP requirement

A 100-Mbit/s path has 50-ms RTT. Its bandwidth-delay product is:

`100,000,000 bit/s x 0.05 s = 5,000,000 bits = 625,000 bytes`

A receive window substantially below 625,000 bytes may leave the path idle. Window scaling can represent such a window, but congestion and buffers still limit actual throughput.

## Key terms & formulas

- **Flow control:** receiver protection.
- **Receive window `rwnd`:** advertised additional capacity.
- **Sender outstanding bytes:** sent but not ACKed.
- **Effective limit:** `min(rwnd, cwnd)`.
- **Zero window:** receiver temporarily advertises no capacity.
- **Window update:** increase advertised capacity.
- **Window probe:** query a receiver after zero window.
- **Window scaling:** scale the 16-bit TCP window field.
- **BDP:** `R x RTT`.
- **MSS:** maximum TCP payload per segment, not the receive window.
- **Silly-window syndrome:** tiny windows/segments reduce efficiency.
- **Buffer:** receiver storage for out-of-order or unconsumed data.
- **Fairness:** sharing receiver capacity among connections.

## Common mistakes

1. **Flow control and congestion control are different.** One protects the receiver; the other the network.
2. **`rwnd` is not always the physical buffer size.** It is an advertised allowance based on available space and policy.
3. **A zero window does not close the connection.** It pauses new data until space opens.
4. **TCP must use window probes.** A lost window update should not block forever.
5. **The 16-bit window field is not the whole receive capacity.** Window scaling extends it.
6. **BDP is a capacity estimate, not a guarantee.** Loss, protocol overhead, and congestion reduce throughput.
7. **A large receive window requires memory.** It can also hold data during a long round trip.
8. **ACKs and window updates are not identical.** An ACK confirms data; a window update advertises capacity.
9. **Flow control is not access control.** Many connections can exhaust server resources.
10. **Silly-window syndrome is a performance problem, not data corruption.** Tiny transmissions waste capacity.

## Exam prep

### Likely 2-mark questions

1. **Define TCP flow control.**  
   Hint: protect a receiver by limiting the sender to its advertised capacity.
2. **What is `rwnd`?**  
   Hint: receiver's advertised window for additional data.
3. **State the effective TCP sending limit.**  
   Hint: `min(rwnd, cwnd)`.
4. **What is a zero window?**  
   Hint: receiver temporarily cannot accept new data.
5. **Why are window probes used?**  
   Hint: recover if a zero-window update is lost.
6. **Define window scaling.**  
   Hint: negotiate a scale factor so a large window can be represented.

### Likely long-answer questions

1. **Explain TCP flow control with an advertised-window example.**  
   Answer hint: receiver buffer, ACK, window update, sender limit, and effective `rwnd/cwnd`.
2. **Trace a zero-window condition and recovery.**  
   Answer hint: application slowdown, zero advertisement, sender pause, probe, lost update, and reopening.
3. **Explain why a high-bandwidth path needs a sufficiently large window.**  
   Answer hint: BDP calculation, in-flight data, RTT, throughput, and memory trade-off.
4. **Compare flow control and congestion control with a bottleneck example.**  
   Answer hint: receiver buffer versus router queue, separate windows, loss/delay signals, and common limit.

### Short-answer revision checklist

Be able to define `rwnd`, state `min(rwnd, cwnd)`, explain a zero window and probe, calculate a BDP, and distinguish a window update from an ACK.
