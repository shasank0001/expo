---
subject: cn
unit: 4
topic: tcp-congestion-control
syllabus_ref: CSM3103 Unit-IV
status: draft
---
# TCP Congestion Control

## Overview

TCP congestion control prevents a sender, or a set of senders, from overwhelming routers and links in the shared network. IP does not provide this protection, so each TCP sender estimates the path's available capacity from feedback such as acknowledgements, loss, delay, and explicit congestion signals.

The sender maintains a **congestion window (`cwnd`)**. During slow start, it grows rapidly; during congestion avoidance, it grows more carefully. Loss or another congestion signal reduces the window. TCP also uses fast retransmit and fast recovery to respond to some losses without waiting for a timeout.

TCP congestion control is not a guaranteed throughput or fairness promise. It balances speed, delay, loss, recovery, and network stability. Modern variants differ in how they detect loss and how quickly they grow, but the goal of stable use of shared resources is common.

## Explanation

### 1. Congestion versus receiver capacity

A sender can be limited by two independent conditions:

- **receiver capacity:** the destination's buffer or `rwnd`;
- **network capacity:** routers/links along the path, represented by `cwnd`.

The effective sending window is normally:

`send limit = min(rwnd, cwnd)`

If the receiver is fast but a router is full, `cwnd` is limiting. If the path is free but the receiver application is slow, `rwnd` is limiting. This distinction is essential for diagnosing throughput and for designing TCP.

### 2. Congestion signals

TCP observes:

- **packet loss:** a retransmission timeout or duplicate ACKs;
- **increased RTT/queueing delay:** a possible early signal, though not universal;
- **explicit congestion notification (ECN):** routers mark packets instead of dropping them when possible;
- **ECN-CE and related feedback:** endpoints reduce rate;
- **application or transport-specific loss signals:** some variants use delay or bandwidth estimation.

Loss is not always congestion: it can be caused by radio interference, a bad link, or a policy drop. Delay can be caused by processing or route changes without severe congestion. TCP variants therefore differ in how aggressively they react.

### 3. Slow start

**Slow start** is the initial growth phase. The name does not mean the sender is intentionally slow; it means the congestion window grows exponentially from a conservative initial value.

For each ACK that acknowledges new data, a sender may increase `cwnd` by roughly one MSS or a corresponding amount. The window therefore approximately doubles per round-trip time while no loss occurs. The exact increase depends on the TCP variant, delayed ACKs, and implementation.

Slow start lets a connection quickly discover available capacity on a short path while avoiding a huge initial burst. It is ended when the window reaches a threshold, a loss occurs, or another congestion-control phase begins.

### 4. Congestion avoidance

When the exponential slow-start phase ends, **congestion avoidance** increases the window more slowly, often approximately linearly with time or ACK count. The algorithm tries to probe for additional capacity without creating repeated large bursts.

An increase per ACK can be expressed approximately as:

`cwnd += MSS^2 / cwnd`

for one common Reno-family formulation. The exact equation is not universal; a conceptual statement such as “add about one MSS per RTT” is usually safer for an introductory exam.

The goal is steady growth while keeping queues and loss under control. If loss occurs, the window is reduced and the algorithm may return to a cautious phase.

### 5. Loss detection and response

A **retransmission timeout (RTO)** is a strong loss signal but can be triggered by delay or a temporary outage. When it occurs, TCP typically reduces `cwnd` substantially, sometimes to one or a few MSS, and restarts cautious growth.

Three duplicate ACKs indicate that later segments arrived while one segment is missing. TCP can **fast retransmit** the missing segment before the timeout. Reno-style TCP also uses **fast recovery**, reducing the window less drastically and avoiding a full slow start. Modern variants such as CUBIC, BBR, and others use different loss signals and growth laws.

A single loss can therefore cause a major throughput dip even if the bottleneck is brief. Loss-based control is simple and widespread but may interpret ordinary wireless loss as congestion.

### 6. Timeout and duplicate-ACK behaviours

A timeout is expensive because the sender waits for a long timer and loses an RTT of opportunity. Three duplicate ACKs provide earlier evidence of a gap and support fast retransmit. A modern sender may retransmit only the missing ranges using SACK, reducing unnecessary data transfer.

The choice of loss response affects throughput, latency, and fairness. A conservative response protects the network but may waste capacity; an aggressive response recovers quickly but can cause repeated congestion and loss.

### 7. Congestion window growth summary

A simplified Reno-style pattern is:

1. Start with a small `cwnd`.
2. Grow exponentially during slow start.
3. On timeout, reduce `cwnd` sharply and restart slow start.
4. At a threshold, enter congestion avoidance.
5. On three duplicate ACKs, fast-retransmit and enter fast recovery.
6. Continue cautious additive growth.

The exact thresholds and formulas differ among variants. A table of variants should be read as an example, not a universal standard.

### 8. ECN

**Explicit Congestion Notification (ECN)** allows a router to mark an IP packet as experiencing congestion when it can avoid an immediate drop. The packet carries an ECN codepoint such as ECN-Congestion Experienced. A TCP receiver can return an ECN notification, and the sender reduces `cwnd` without treating the marked packet as lost.

ECN can reduce unnecessary packet loss and improve fairness when both endpoints and routers support it. A router must have sufficient queue capacity; if congestion is already severe, dropping may still be necessary. Spoofed or malformed signals require protection.

### 9. Fairness

Congestion control attempts to share capacity fairly among competing flows. A flow that sends more aggressively may obtain more throughput but can also cause loss. Additive increase and multiplicative decrease provide a simple reaction: increase slowly while safe and reduce substantially when congestion appears.

Fairness is not perfectly equal. Different RTTs, loss patterns, application limits, and TCP variants can produce different throughput. Newer algorithms may optimise bandwidth-delay performance rather than strict fairness.

### 10. Bufferbloat and delay

Large router buffers can hide packet loss while creating very high queueing delay. A loss-based TCP sender may fill the buffer and enjoy a high throughput measurement, but users experience latency and poor interactive response. This is called bufferbloat.

ECN, AQM, lower-latency congestion control, and active queue management can reduce the problem. Flow control cannot fix a bottleneck in the network; it only limits what the receiver accepts.

### 11. Interaction with applications and transport

The congestion window is measured in bytes, not packets. An application can limit its own sending rate, pause, or use UDP. A UDP application needs an application-level congestion-control scheme; UDP itself does not react to loss or delay.

The sender's actual rate also depends on RTT, ACK frequency, receiver window, path capacity, and CPU. `cwnd` is an estimate and controller, not a direct measurement of link bandwidth in every protocol.

### 12. TCP variants

- **Reno/NewReno:** loss-based slow start, congestion avoidance, fast recovery.
- **CUBIC:** uses a window-growth function based on the most recent congestion event, common in Linux and other systems.
- **BBR:** estimates bottleneck bandwidth and round-trip propagation time and can avoid relying only on loss.
- **ECN-enabled TCP:** reduces rate when routers mark congestion.
- **Delay/loss variants:** differ in sensitivity, fairness, and deployment.

A variant is not automatically better for every path. It may perform well on one network and be less suitable for another.

## Worked examples

### Example 1: Slow start

A new TCP connection starts with `cwnd = 1 MSS` or a small implementation-defined value. If ACKs arrive without loss, `cwnd` can approximately double each RTT: 1, 2, 4, 8 MSS, until a threshold or loss.

### Example 2: Congestion avoidance

After slow start, the sender increases `cwnd` by about one MSS per RTT rather than doubling. If `rwnd=32 MSS` and `cwnd=8 MSS`, the sender is congestion-limited and sends 8 MSS in flight.

### Example 3: Timeout

A segment is lost and no later ACKs arrive. The retransmission timer expires. A Reno-style sender reduces `cwnd` to a small value and returns to slow start. This is conservative and protects a heavily loaded path but creates a throughput pause.

### Example 4: Fast recovery

Three segments arrive after a gap and produce duplicate ACKs. The sender fast-retransmits the missing segment, reduces the window less than after a timeout, and avoids restarting from the minimum. If the retransmission succeeds, transmission continues at a higher rate.

### Example 5: ECN

A router marks a packet with ECN-CE instead of dropping it. The receiver returns ECN feedback. TCP reduces `cwnd` as if it had seen congestion, but it does not retransmit the marked packet. The network can preserve more packets.

### Example 6: BDP calculation

For a 10-Mbit/s path and 100-ms RTT:

`BDP = 10,000,000 x 0.1 = 1,000,000 bits = 125,000 bytes`

A window substantially below 125 KB may leave capacity unused. A larger window helps fill the path, but it can also create more data in queues if the path is shared or unstable.

## Key terms & formulas

- **Congestion control:** protect shared network resources.
- **Congestion window `cwnd`:** sender's network-load limit.
- **Receiver window `rwnd`:** receiver's advertised capacity.
- **Effective limit:** `min(rwnd, cwnd)`.
- **Slow start:** approximately exponential window growth.
- **Congestion avoidance:** cautious, approximately linear growth.
- **Fast retransmit:** retransmit after duplicate ACKs.
- **Fast recovery:** avoid a full slow start after recoverable loss.
- **RTO:** retransmission timeout.
- **Duplicate ACK:** repeated ACK indicating a gap.
- **ECN:** explicit congestion notification/marking.
- **BDP:** `R x RTT`.
- **Queueing delay:** waiting in router queues.
- **Bufferbloat:** excessive buffering causing high delay.
- **Reno:** loss-based TCP variant.
- **CUBIC/BBR:** alternative modern TCP variants.

## Common mistakes

1. **TCP congestion control is not receiver flow control.** `cwnd` and `rwnd` protect different resources.
2. **A timeout is not the only loss signal.** Duplicate ACKs and ECN can trigger earlier response.
3. **Slow start does not remain slow for the whole connection.** It is an initial growth phase.
4. **Congestion avoidance is not always exactly linear.** The basic conceptual trend is cautious growth; implementations differ.
5. **Loss is not always congestion.** Radio loss, bad links, and policy drops can trigger reduction.
6. **A large congestion window is not always good.** It requires memory and can increase queueing delay.
7. **ECN does not eliminate all loss.** A full or failing router may still drop packets.
8. **The BDP is not a throughput guarantee.** It estimates data needed in flight.
9. **UDP has no TCP congestion control.** An application must provide an appropriate scheme.
10. **Fast recovery is not the same as a timeout.** It responds to duplicate ACKs without a long timer wait.
11. **Fairness and maximum throughput can conflict.** A protocol must choose a balance.

## Exam prep

### Likely 2-mark questions

1. **What problem does TCP congestion control solve?**  
   Hint: prevent sources from overwhelming shared routers/links.
2. **Define `cwnd` and state the effective sending limit.**  
   Hint: network estimate; `min(rwnd, cwnd)`.
3. **Distinguish slow start and congestion avoidance.**  
   Hint: exponential versus cautious/approximately linear growth.
4. **What is fast retransmit?**  
   Hint: resend after duplicate ACKs before a timeout.
5. **What is ECN?**  
   Hint: router marking/feedback rather than immediate loss.
6. **State two TCP loss responses.**  
   Hint: timeout and duplicate-ACK fast retransmit/recovery.

### Likely long-answer questions

1. **Explain TCP congestion control with slow start, congestion avoidance, and loss recovery.**  
   Answer hint: cwnd growth, threshold, RTO, duplicate ACKs, fast recovery, and fairness.
2. **Differentiate TCP congestion control and flow control with a bottleneck example.**  
   Answer hint: `cwnd` versus `rwnd`, receiver buffer versus router queue, and common limit.
3. **Calculate the BDP and explain its relationship to TCP windows.**  
   Answer hint: `R x RTT`, bytes in flight, throughput, memory, and congestion trade-offs.
4. **Compare timeout recovery, fast recovery, and ECN.**  
   Answer hint: signal, speed, loss, performance, and network-support requirements.
5. **Discuss bufferbloat and fairness in TCP.**  
   Answer hint: large queues, delay, loss-based reaction, AQM/ECN, and competing flows.

### Short-answer revision checklist

Be able to state `min(rwnd, cwnd)`, sketch slow-start and congestion-avoidance growth, distinguish timeout from duplicate ACK, calculate BDP, and define ECN.
