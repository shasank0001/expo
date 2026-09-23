---
subject: cn
unit: 3
topic: congestion-control-approaches
syllabus_ref: CSM3103 Unit-III
status: draft
---
# Approaches to Congestion Control

## Overview

Network **congestion** occurs when the traffic offered to a link or router exceeds the capacity available to carry it. Packets arrive faster than routers can forward them, queues grow, delay and jitter increase, and packets may be dropped when buffers fill. Congestion can also arise from processing limits, routing concentration, or a traffic pattern that creates bursts.

Congestion control aims to use network capacity efficiently while protecting the network from collapse. It can be handled inside the network through routing, queueing, scheduling, and queue management, or at the source through feedback and rate adaptation. The syllabus names traffic-aware routing, throttling, load shedding, and traffic shaping.

Congestion control is different from error control and flow control. Error control deals with corruption or loss caused by unreliable transmission. Flow control protects one receiver from a particular sender. Congestion control protects shared network resources and may involve many senders and receivers.

## Explanation

### 1. What is congestion?

A network resource can be a link's transmission rate, a router's forwarding capacity, a queue, a processor, or an uplink. If the arrival rate `A` is greater than the service rate `C` over a period, backlog grows. Utilisation can approach or exceed one, and delay rises nonlinearly as queues fill.

Congestion is not simply a slow link. A fast link can be congested by a burst, a flow arriving at once, or a downstream bottleneck. A slow link may be lightly used. Good measurement identifies the actual bottleneck, which may be far from the source.

Congestion can be **open-loop**, controlled by configured policies and traffic profiles, or **closed-loop**, using feedback from the network. Many real systems combine both.

### 2. Congestion symptoms

- increasing queue length;
- rising end-to-end delay and jitter;
- packet loss from full buffers;
- retransmissions that add more traffic;
- lower effective throughput;
- timeouts and connection failures;
- fairness problems where one flow dominates.

Loss is not the only congestion signal. Delay can rise before a buffer is full. A network can therefore use queue occupancy, delay, explicit notification, or measurement of bottleneck bandwidth.

### 3. Congestion versus flow control

**Flow control** protects a receiver. A TCP receiver advertises how much buffer it can accept. **Congestion control** protects the network between endpoints. A receiver may have plenty of buffer, but a router in the middle may be full.

A useful example is a fast receiver connected through a slow bottleneck. The receiver can accept data quickly, so receiver flow control permits a large window, but congestion control must reduce the sending rate to protect the bottleneck.

### 4. Approach categories

Congestion-control approaches include:

- traffic-aware routing;
- source throttling and feedback;
- load shedding or packet dropping;
- traffic shaping and scheduling;
- queue management and priority;
- admission control and resource reservation;
- endpoint congestion-control algorithms.

The methods can work together. A router may shape incoming traffic, shed excess cells, mark congestion, and select a less-loaded path.

### 5. Traffic-aware routing

Traffic-aware routing selects paths using measured or estimated load, queue size, delay, available bandwidth, loss, or a combination. It can distribute flows across parallel links and avoid a locally congested route.

The information may be obtained by periodic measurements, router exchanges, link utilisation counters, or traffic estimation. Benefits include better use of heterogeneous links and resilience to a local bottleneck. Costs include measurement overhead, control traffic, stale information, and possible route oscillation.

A routing algorithm must not move all traffic at once merely because a link is temporarily slightly faster. Damping, hysteresis, and stable metrics help.

### 6. Throttling

**Throttling** reduces the rate at which sources send traffic. A router can signal congestion explicitly, mark packets, or use an implicit signal such as loss or increased delay. A sender then slows down, sends fewer packets, or increases acknowledgement delay.

A source-level throttle is useful because the sender is the entity that can reduce offered load. It is more effective than dropping many packets after they have already consumed buffer and transmission capacity. Throttling can be per flow, per source, or per class.

A token-bucket or pacing mechanism can enforce a maximum average rate while allowing controlled bursts. The rate must be chosen so the network remains stable.

### 7. Load shedding

**Load shedding** deliberately discards selected packets when a router cannot accept its full offered load. It prevents an infinite queue and keeps the forwarding plane responsive. A shed packet is not repaired; an upper layer may retransmit or the application may accept the loss.

Queue-management algorithms can:

- drop the tail when a queue is full;
- drop early before congestion becomes severe;
- use Random Early Detection (RED) or an Active Queue Management (AQM) scheme;
- use a priority policy that sheds low-priority traffic first;
- use explicit feedback to sources.

Tail drop is simple but can create a queue that is full for a long time and synchronises many senders. Early/AQM schemes attempt to signal congestion before buffers are completely full.

### 8. Traffic shaping

**Traffic shaping** regulates the timing or rate at which packets are released. It may queue, delay, mark, or discard packets so traffic becomes more predictable.

Common mechanisms include:

- **token bucket:** tokens are generated at a rate; a packet consumes a token; unused tokens permit a controlled burst;
- **leaky bucket:** packets leave at a steady rate, smoothing bursts;
- **policing:** monitor a rate and drop or mark traffic that exceeds it;
- **scheduling:** choose which queued packet is sent next using priority, fair queueing, or weighted fair queueing.

A token bucket controls an average rate with burst tolerance. A leaky bucket produces a smoother output but can add delay and may discard excess.

### 9. Queueing and scheduling

When several queues exist, a scheduler decides which packet is sent next. Priorities can protect delay-sensitive traffic, but starvation is possible. Fair queueing gives each flow or class a share and reduces one flow's domination.

Weighted fair queueing assigns different weights to flows or classes. QoS can combine classification, marking, policing, shaping, and scheduling. The goal is not simply to maximise one queue's throughput; it is to meet a mix of service requirements while avoiding congestion collapse.

### 10. Explicit congestion notification

An **explicit congestion notification** mechanism lets routers mark or notify a packet that it encountered congestion. A source can then reduce its sending rate. ECN is a common IP mechanism in which routers mark packets rather than immediately dropping them when possible.

Notification can be faster and more informative than waiting for loss, but it must be authenticated and secured. A source must not blindly trust a forged signal.

### 11. Congestion collapse and retransmissions

Congestion collapse can occur when loss causes many senders to retransmit at once. Retries consume additional network capacity, causing more loss and more retries. Good congestion control reduces sending rates, randomises recovery, and uses mechanisms that avoid synchronised bursts.

A router cannot solve every problem by dropping more packets. If it drops too aggressively, throughput collapses. The goal is a stable operating point, not zero loss at all costs.

### 12. Reactive versus proactive control

A reactive controller observes current queueing and loss and then reduces or redirects traffic. A proactive controller predicts demand from configured rates, reservations, or traffic profiles and admits or shapes traffic before queues overflow.

A hybrid design is common: reserve capacity for critical flows, monitor active queues, and provide feedback to best-effort sources. The design should account for traffic bursts, failures, and changing paths.

## Worked examples

### Example 1: Bottleneck

A 1-Gbit/s server sends to many clients through a 100-Mbit/s uplink. The server's output is not the bottleneck; the uplink is. Flow control may allow the receiver to accept data, but congestion control must reduce the aggregate send rate to avoid filling the uplink queue.

### Example 2: Load shedding

A router's queue reaches its limit during a burst. It drops low-priority video packets before high-priority control or voice packets. The video may show a short quality loss, while the more important packets are more likely to be forwarded. The source should also reduce its rate.

### Example 3: Token bucket shaping

A token bucket produces 1,000 tokens per second and each packet costs 100 tokens. It normally permits 10 packets per second. If the bucket accumulates 20 unused tokens, a short burst of 20 packets can pass, after which the rate returns to the average.

### Example 4: Traffic-aware routing

Two parallel links have the same nominal bandwidth. One queue is 80% full and the other is 10% full. A traffic-aware controller may send new flows to the less-loaded link, while existing flows remain stable. Frequent switching can make performance worse, so updates need damping.

## Key terms & formulas

- **Congestion:** offered traffic exceeds available network resources.
- **Arrival rate:** packet arrival rate `A`.
- **Service rate:** forwarding/transmission capacity `C`.
- **Utilisation:** `A / C` in a simple steady-state model.
- **Queue:** packets waiting for service.
- **Congestion collapse:** loss and retransmissions amplify overload.
- **Throttling:** reduce source sending rate.
- **Load shedding:** discard excess packets.
- **Traffic shaping:** regulate timing/rate.
- **Tail drop:** drop at a full queue.
- **AQM:** active queue management, such as RED.
- **Token bucket:** average rate plus allowed burst.
- **Leaky bucket:** smooth output rate.
- **Queueing delay:** time a packet waits in a queue.
- **ECN:** explicit congestion notification/marking.
- **Queuing stability:** incoming work does not grow without bound.
- **Schematic stability condition:** sustained offered load should remain below effective service capacity after overhead and feedback.

## Common mistakes

1. **Congestion is not the same as a transmission error.** It is excess offered load or insufficient service capacity.
2. **Congestion control is not flow control.** One protects shared network resources; the other protects a receiver.
3. **Throttling reduces offered load.** It is not merely a queueing policy.
4. **Load shedding discards packets.** It does not repair them.
5. **Traffic shaping controls timing/rate.** It may also drop or mark, but its main idea is regulation.
6. **A full queue is not always the best signal to wait for.** Early/AQM methods detect congestion earlier.
7. **Traffic-aware routing does not prevent all congestion.** A new local demand can still overwhelm a link.
8. **A token bucket allows bursts.** A leaky bucket smooths output more strongly.
9. **ECN is not a guarantee of no loss.** Marking can fail or the queue may still fill.
10. **Retransmissions can worsen congestion.** Recovery must be controlled and randomised.
11. **QoS marking is not resource reservation.** Capacity and policy must be provisioned.
12. **Congestion control aims for stable performance.** Maximising throughput at any cost can cause collapse.

## Exam prep

### Likely 2-mark questions

1. **Define network congestion and list two symptoms.**  
   Hint: demand exceeds capacity; queue growth, delay, loss, or retransmission.
2. **List four approaches to congestion control.**  
   Hint: traffic-aware routing, throttling, load shedding, shaping, AQM, or admission control.
3. **Differentiate congestion control and flow control.**  
   Hint: network-wide/shared resources versus one receiver.
4. **What is load shedding?**  
   Hint: discard selected excess packets when capacity is insufficient.
5. **What is throttling?**  
   Hint: slow or signal a source to reduce its rate.
6. **What is traffic shaping?**  
   Hint: regulate packet timing/rate with queues, tokens, policing, or scheduling.

### Likely long-answer questions

1. **Explain congestion, its symptoms, and approaches to control.**  
   Answer hint: arrival/service, queues, loss, routing, throttling, shedding, shaping, AQM, and feedback.
2. **Compare flow control and congestion control with a bottleneck example.**  
   Answer hint: receiver window, network bottleneck, loss/delay signals, and rate reduction.
3. **Explain throttling, load shedding, and traffic shaping with a router example.**  
   Answer hint: source rate, packet loss, queue/token/priority policy, and different effects.
4. **Describe token bucket and leaky bucket and compare their burst behaviour.**  
   Answer hint: token generation/consumption versus steady leak, examples, and delay.
5. **Explain congestion collapse caused by retransmission and how a system prevents it.**  
   Answer hint: positive feedback, backoff, randomisation, AQM, and fair scheduling.

### Short-answer revision checklist

Be ready to define congestion, distinguish it from errors and flow control, list all syllabus approaches, and explain the difference between token bucket and leaky bucket.
