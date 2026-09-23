---
subject: cn
unit: 3
topic: throttling-load-shedding-and-shaping
syllabus_ref: CSM3103 Unit-III
status: draft
---
# Throttling, Load Shedding, and Traffic Shaping

## Overview

When a router's offered traffic exceeds its forwarding capacity, the router needs active congestion-control techniques. **Throttling** asks or causes sources to send less. **Load shedding** discards selected packets when capacity is unavailable. **Traffic shaping** regulates the timing or rate of traffic, often by queuing, pacing, marking, or dropping.

The three techniques differ in where they act and what the user observes. Throttling reduces the offered load before or near the bottleneck. Load shedding accepts that some packets will be lost and protects the forwarding system. Shaping converts bursts into a controlled output and can prioritise traffic or smooth an aggregate flow.

They are related but not interchangeable. A token bucket may shape an individual flow; a queue manager may shed packets; an edge router may signal a TCP sender to throttle. A complete congestion-control design can use all three.

## Explanation

### 1. Throttling

Throttling reduces the rate at which a flow or source sends data. It can be implemented by:

- explicit router feedback or a congestion notification;
- packet loss or delay as an implicit signal;
- source-side pacing or rate-based congestion control;
- an edge policer that marks or drops packets above a rate.

For TCP, loss of a segment and duplicate acknowledgements or increased delay cause the sender to reduce its congestion window. A UDP application needs its own rate control because UDP has no built-in congestion-control algorithm. Real-time applications may adapt media rate, resolution, or frame quality.

Throttling is valuable because a source that sends less avoids consuming the congested queue in the first place. It can be applied to a source, a flow, a traffic class, or an entire domain. A policer can enforce a committed rate but may drop or mark excess traffic.

### 2. Load shedding

Load shedding is deliberate packet loss at a router or queue when the network cannot accept all offered traffic. It can be:

- **tail drop:** discard the newly arriving packet when the queue is full;
- **front drop:** discard a packet already in the queue to make room for a new one;
- **priority shedding:** drop lower-priority traffic first;
- **class-based shedding:** protect high-value traffic;
- **early/AQM shedding:** signal before a queue is completely full.

The purpose is to keep queues short and the forwarding path responsive. If an input queue has no storage, the router must either drop traffic, block, or use unbounded memory. Unbounded memory increases delay and can cause timeout-based retransmissions, so dropping controlled traffic is often preferable.

Load shedding is not error correction and does not recover data. TCP may retransmit dropped packets, but the retransmission itself adds load. An application using UDP may simply lose a datagram.

### 3. Queue management

A queue stores packets waiting for a link or router. Its length affects delay, burst tolerance, and loss. **Tail drop** is simple, but a long full queue creates high delay and can synchronise many senders. **Active Queue Management (AQM)** tries to keep queues short by dropping or marking packets before they are completely full.

Random Early Detection (RED) uses queue occupancy to decide when to drop some packets or set an explicit congestion mark. Other AQM algorithms use delay, packet pairs, or virtual queues. A good AQM policy balances low delay against unnecessary loss.

A queue manager does not decide the overall route or the receiver's acceptable rate. It manages the local bottleneck or a related queue and may provide feedback to sources.

### 4. Traffic shaping

Traffic shaping controls when packets are released or whether they are admitted. It can:

- delay packets until the permitted time;
- smooth a burst into a steady stream;
- enforce an average rate;
- prioritise one class over another;
- mark packets for downstream treatment;
- drop packets that exceed a strict policy.

Shaping is often performed by a token bucket, leaky bucket, policer, or scheduler. It changes the temporal distribution of traffic, not only the total volume.

### 5. Token bucket

A **token bucket** has a bucket capacity `B` and generates tokens at rate `r` tokens per second. A packet of size `P` consumes tokens. If enough tokens are available, it is sent; otherwise it is queued or dropped according to the policy.

If the bucket accumulates unused tokens, a short burst of size up to `B` can be sent. After the burst, the long-term rate is limited to `r`. This is useful for file transfer or application traffic that can tolerate occasional bursts.

A numeric example: `r = 1,000 packets/s`, each packet costs 100 tokens, and bucket capacity is 20 packets. The long-term rate is 10 packets/s, and up to 20 unused packets can create a burst.

### 6. Leaky bucket

A **leaky bucket** releases packets at a fixed rate, often by draining a queue at a steady rate. A burst enters the queue and leaves more smoothly. If the queue is full, input can be dropped or marked.

A token bucket is permissive about bursts, while a leaky bucket is designed to smooth them. Both can be combined: a token bucket controls average rate and burst size, and a scheduler or queue controls output timing.

### 7. Policing versus shaping

A **policer** monitors a flow and drops or marks traffic that exceeds a configured rate. A **shaper** queues and delays traffic to enforce a desired rate and burst profile. Policing reacts to excess; shaping tries to smooth it before transmission.

A traffic contract may specify committed information rate, peak rate, and burst size. The enforcement mechanism can be a policer, shaper, or both. Excess may be discarded, remarked, or sent in a lower-priority class.

### 8. Scheduling and priority

Once packets are queued, a scheduler chooses which queue receives the link. Priority scheduling protects delay-sensitive traffic but can starve low-priority classes. Fair queueing and weighted fair queueing allocate service more evenly or according to weights.

Priority can be based on a packet field such as DSCP, a flow class, or an application profile. A router should combine priority with capacity planning; marking too much traffic high priority provides no benefit.

### 9. Throttling versus load shedding versus shaping

| Method | Main action | Where it acts | Typical effect |
|---|---|---|---|
| Throttling | Reduce source/flow rate | Endpoint or edge control | Lower offered load |
| Load shedding | Drop selected packets | Congested queue/router | Immediate capacity relief, loss |
| Shaping | Delay/paced release or classify | Edge/router queue | Smoother, controlled output |

A throttled sender reduces traffic; a shaper changes when packets leave; a shedding policy decides which packets cannot be accepted. They can be used sequentially.

### 10. Congestion and fairness

One aggressive flow can fill a shared queue and cause many small flows to time out. Weighted fair queueing, per-flow queues, and traffic classification can improve fairness. Throttling a particularly high-volume source and protecting low-rate interactive traffic are common policies.

Fairness is not always equal rates. A real-time voice flow may receive a small reserved share and priority, while a bulk transfer receives the remaining capacity. Admission control prevents a new flow from destroying existing guarantees.

## Worked examples

### Example 1: Throttle a TCP flow

A router's queue grows because many TCP connections send at high rates. Loss and delay signal the senders. Each reduces its congestion window, so the aggregate rate approaches the bottleneck capacity. The router does not need to store all newly arriving packets while waiting for the sources to slow down.

### Example 2: Load shedding by priority

A router is full. It drops a low-priority video packet before a control or voice packet. The video may show a short quality loss, but the important packet has a better chance of being delivered. The source should later adapt; dropping alone does not permanently reduce load.

### Example 3: Token bucket

A source is allowed an average of 500 packets per second and can burst by 100 packets. A token bucket with rate 500 and capacity 100 accumulates unused capacity during idle time. A short 100-packet burst can pass, after which the source is limited to the average.

### Example 4: Leaky bucket smoothing

A backup process sends a large burst in one second. A leaky bucket releases packets at a constant 10 Mbit/s. The receiver sees a smoother flow and can use a smaller buffer. If the input queue is full, the source is told to wait or some data is dropped.

### Example 5: Policer

An ISP contract provides 10 Mbit/s but permits bursts to 20 Mbit/s for short periods. A policer marks packets above the committed rate, and a downstream policy sends marked packets with lower priority. If the policy is strict, the policer drops them instead.

## Key terms & formulas

- **Throttle:** reduce sending rate.
- **Load shed:** discard excess packets.
- **Traffic shaping:** regulate timing/rate.
- **Queue:** waiting buffer.
- **Tail drop:** drop on full queue.
- **AQM:** active queue management.
- **RED:** random early detection.
- **Token bucket:** rate `r`, bucket size `B`, packet cost `P`.
- **Leaky bucket:** fixed output rate.
- **Policer:** enforce rate by drop/mark.
- **Shaper:** delay/queue traffic to enforce a profile.
- **Average rate:** tokens generated per second.
- **Burst allowance:** unused capacity accumulated in a bucket.
- **Weighted fair queueing:** service shares based on weights.
- **Priority scheduling:** serve high-priority queues first, with starvation risk.
- **Stable system:** offered traffic remains within service capacity after retransmissions.

## Common mistakes

1. **Throttling is not load shedding.** One reduces offered traffic; the other discards packets.
2. **Traffic shaping is not simply queuing.** It regulates timing, rate, classification, or admission.
3. **Token bucket permits bursts; leaky bucket smooths them.** Do not swap their defining properties.
4. **Load shedding does not repair lost data.** A higher layer may retransmit, but that adds traffic.
5. **Tail drop is simple but can create high delay.** AQM tries to act earlier.
6. **A policer and shaper differ.** A policer drops/marks excess; a shaper delays/paces it.
7. **Priority is not fairness.** A low-priority flow can starve.
8. **A token bucket does not guarantee instantaneous rate.** Its long-term rate is limited; burst capacity is allowed.
9. **Shaping at one router may not control the whole path.** The bottleneck can be elsewhere.
10. **Dropping is not always the best response.** Aggressive loss can trigger a congestion collapse.

## Exam prep

### Likely 2-mark questions

1. **Define throttling.**  
   Hint: reduce the rate at which a source or flow sends.
2. **Define load shedding.**  
   Hint: discard selected excess packets when capacity is insufficient.
3. **Define traffic shaping.**  
   Hint: regulate packet timing/rate through queueing, tokens, policing, or scheduling.
4. **Compare token bucket and leaky bucket.**  
   Hint: token bucket allows a controlled burst; leaky bucket produces a smoother output.
5. **What is AQM?**  
   Hint: active queue management that signals/drops before a queue is full.
6. **Differentiate a policer and a shaper.**  
   Hint: drop/mark excess versus delay/queue to enforce a rate.

### Likely long-answer questions

1. **Compare throttling, load shedding, and traffic shaping.**  
   Answer hint: action, location, effect, examples, and interaction.
2. **Explain token-bucket and leaky-bucket algorithms with numerical examples.**  
   Answer hint: rate, bucket size, burst, output rate, queueing, and drop conditions.
3. **Explain tail drop, RED, priority, and fair queueing.**  
   Answer hint: queue length, early signalling, service order, delay, loss, and fairness.
4. **Design a congestion-control policy for an edge router carrying voice and file traffic.**  
   Answer hint: classification, admission, shaping, priority, throttling feedback, and AQM.
5. **Explain why retransmission can worsen congestion and how to stabilise it.**  
   Answer hint: loss feedback, backoff, randomisation, ECN/AQM, and rate limits.

### Short-answer revision checklist

Be ready to define all three syllabus methods, calculate a token-bucket average/burst, explain tail drop versus AQM, and compare a policer with a shaper.
