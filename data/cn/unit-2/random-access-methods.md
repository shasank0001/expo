---
subject: cn
unit: 2
topic: random-access-methods
syllabus_ref: CSM3103 Unit-II
status: draft
---
# Random-Access Methods

## Overview

A **random-access** method allows any station to transmit on a shared medium without first receiving permission. It is attractive because the method is simple and stations can transmit whenever they have data. The cost is that two stations may transmit at the same time, creating a **collision** whose signals are corrupted and whose frames must be discarded or retransmitted.

The syllabus names ALOHA, CSMA/CD, and the general random-access idea, with channel-sense methods compared to controlled access and channelization. Random access works best when traffic is light, stations are independent, and the cost of waiting for a reservation is greater than the occasional collision. As traffic increases, collisions become more likely, throughput falls, and retransmissions waste capacity.

## Explanation

### 1. Random access and collisions

In a random-access system, stations share a common channel. If no other station is transmitting, a station may start. If another station starts at nearly the same time, their signals overlap. The receiver cannot distinguish the two messages correctly, so the frames are lost.

A collision affects stations whose transmissions overlap in time. The protocol can detect or infer the collision, discard affected data, and retry. The retry time should be random so the same stations do not collide again in the same pattern.

The key design parameters are propagation delay, frame duration, offered traffic, number of stations, and the ability to sense or detect a collision. A station may “hear idle” but another station's signal may still be propagating toward it.

### 2. Pure ALOHA

In **pure ALOHA**, a station may begin transmitting at any time, without sensing the channel or synchronising to slots. A transmission occupies the medium for a fixed frame time. Vulnerable periods overlap for any frames whose transmissions overlap.

The classic simplified analysis models Poisson-arrival transmissions and finds a maximum normalised throughput of about `1/(2e) ≈ 0.184`, or 18.4%. This is a low efficiency because a frame can be damaged not only by a simultaneous transmission at its start but also by a transmission beginning during its vulnerable period. Pure ALOHA is therefore mainly a historical and conceptual baseline.

Advantages include no carrier sensing, no permission, and easy operation for bursty low-rate users. Disadvantages include poor channel utilisation and weak performance at high load.

### 3. Slotted ALOHA

**Slotted ALOHA** divides time into equal slots equal to the time needed to transmit one frame. A station may transmit only at the beginning of a slot. If another station transmits in the same slot, a collision occurs. If a station begins in a later slot, it does not overlap the previous frame.

Under the ideal slotted model, the maximum normalised throughput is `1/e ≈ 0.368`, or 36.8%, higher than pure ALOHA because each frame has only one vulnerable slot. Real systems still lose throughput because stations may choose empty slots and retransmit after collisions.

Slotted ALOHA requires shared timing. A receiver can use a synchronisation marker or a clock reference so stations know slot boundaries.

### 4. CSMA

**Carrier Sense Multiple Access (CSMA)** improves on ALOHA by listening to the channel before transmitting. A station that senses busy waits until the medium becomes idle. It may then transmit, often after a small inter-frame gap.

Carrier sensing reduces the chance of a collision when propagation delay is small and stations can reliably hear one another. It does not eliminate collisions: two stations can both sense the channel idle at distant locations, then their signals can arrive at a receiver together. This is the **hidden-terminal** situation.

A station should also continue monitoring after transmitting if it needs to detect a collision. Pure CSMA without collision detection is therefore not a complete protocol on a noisy shared link.

### 5. CSMA/CD

**Carrier Sense Multiple Access with Collision Detection (CSMA/CD)** is used by shared, wired half-duplex Ethernet. A station:

1. senses the medium;
2. transmits while sensing;
3. continues listening while transmitting;
4. detects a collision when the channel voltage differs from the expected signal;
5. stops, sends a jam signal, and waits for a random backoff;
6. retries using an exponential-backoff algorithm.

The minimum frame duration is chosen so a transmitting station remains capable of detecting a collision until the signal from the far end could have arrived. On the classic shared Ethernet, the slot time is 512 bit times. Modern switched full-duplex Ethernet has a separate collision domain per link and does not use CSMA/CD.

CSMA/CD needs a receiver that can transmit and listen simultaneously. Many wireless radios cannot do this reliably, so wireless LANs use CSMA/CA instead.

### 6. CSMA/CA preview

**CSMA/CA** avoids collisions rather than detecting them after transmission. A wireless station senses the channel, waits an inter-frame gap, chooses a random backoff, and transmits after other required waits. Physical carrier sensing helps avoid transmissions heard by the station, but hidden stations may not hear one another. RTS/CTS and other virtual-carrier mechanisms reduce the hidden-terminal effect.

CSMA/CA is covered in a separate file because it is central to IEEE 802.11.

### 7. Random backoff and retransmission

After a collision, stations wait for a random amount of time. If every station waited a fixed time, they could collide again. Ethernet's binary exponential backoff randomly chooses a slot from a range that grows after repeated failures:

- after the first collision: choose from 0 or 1 slot;
- after the second: choose from 0 to 3 slots;
- then 0 to 7, and so on, up to a limit.

A frame is discarded after a maximum number of attempts, and the higher layer is informed. The method improves fairness, although a small number of stations can dominate access.

### 8. Performance and offered load

**Offered load** is the traffic demand expressed as a fraction of the channel's service capacity. At low load, random access is efficient because a station often finds the channel idle. As offered load approaches or exceeds one, many stations transmit, collisions increase, and throughput may collapse. The network can become unstable if retransmissions add more traffic than the channel can carry.

This is why congestion control and admission control matter. A protocol should avoid retransmitting faster than the medium can successfully carry frames.

### 9. Random access versus controlled access

Random access is decentralised and suitable for bursty traffic. Controlled access uses a controller or token to grant permission and can provide predictable delay and fairness, but it may be slower when traffic is light or when a controller/token fails. A token ring and a centrally polled bus are controlled-access examples.

### 10. Random access versus channelization

Channelization divides the medium into separate channels, so users may transmit concurrently on their assigned channel. Random access lets users share the whole medium and deals with conflicts. Frequency-division, time-division, and code-division methods are channelization; ALOHA and CSMA are random-access methods.

## Worked examples

### Example 1: Pure ALOHA collision

Station A begins transmitting at time 0 and needs 10 ms. Station B begins at 7 ms. Their transmissions overlap, so a receiver may see a collision even though the stations did not begin at exactly the same instant.

### Example 2: Slotted ALOHA

The slot time is 5 ms. A and B transmit in different slots, so their frames do not overlap. If both choose the same slot, they collide and wait for random slots before retrying.

### Example 3: CSMA hidden station

A and C cannot hear each other because B is between them or blocks the radio. Both sense an idle channel and transmit. B hears overlapping signals and experiences a collision. A pure CSMA decision did not prevent the collision.

### Example 4: Ethernet retry

Two shared-Ethernet stations collide. Both stop, send a jam, and choose a random backoff. If they choose different slots, one retransmits first. If repeated collisions occur, the backoff range grows; after the retry limit, the frame is reported as failed.

### Example 5: Light versus heavy traffic

With two stations sending a short packet occasionally, random access has little delay. With many stations sending continuously, collisions and retransmissions dominate. A controlled or channelized method may be more efficient in that situation.

## Key terms & formulas

- **Random access:** transmit without prior permission.
- **Collision:** overlapping transmissions that corrupt one another.
- **Pure ALOHA:** unrestricted start time; ideal maximum `1/(2e) ≈ 0.184`.
- **Slotted ALOHA:** transmit only at slot boundaries; ideal maximum `1/e ≈ 0.368`.
- **CSMA:** carrier sense before transmission.
- **CSMA/CD:** sense during transmission and react to detected collisions.
- **CSMA/CA:** avoid collisions using sensing, waits, and random backoff.
- **Hidden terminal:** stations that cannot hear each other but collide at a receiver.
- **Inter-frame gap:** required idle time between frames.
- **Slot time:** time unit for random backoff and collision detection.
- **Binary exponential backoff:** choose from a range that doubles after repeated collisions.
- **Offered load:** demand relative to service capacity.
- **Throughput:** successfully delivered frames per unit time.
- **Contention:** stations competing for the same shared medium.

## Common mistakes

1. **Random access does not mean collisions are ignored.** They are part of the method and must be handled.
2. **Carrier sensing does not guarantee no collision.** Propagation delay and hidden stations matter.
3. **Pure ALOHA and slotted ALOHA have different vulnerable periods.** Slot synchronisation is the major difference.
4. **CSMA/CD is not normal in modern switched full-duplex Ethernet.** It belongs to shared half-duplex Ethernet.
5. **CSMA/CA is not CSMA/CD.** Collision avoidance is different from collision detection.
6. **A fixed backoff can cause repeated collisions.** Randomisation is needed.
7. **Throughput is not the same as offered load.** Lost and retransmitted frames consume capacity.
8. **Random access is not controlled access.** No token or controller grants permission in the basic method.
9. **Channelization is not random access.** It separates users into channels.
10. **The quoted ALOHA efficiencies are ideal theoretical maxima.** Real hardware and traffic produce lower results.

## Exam prep

### Likely 2-mark questions

1. **Define random access and collision.**  
   Hint: stations transmit without permission; overlapping frames are corrupted.
2. **Compare pure and slotted ALOHA.**  
   Hint: arbitrary versus slot-boundary starts; vulnerable period and efficiency.
3. **What is CSMA?**  
   Hint: listen before transmitting.
4. **How does CSMA/CD work?**  
   Hint: sense, transmit while listening, detect, jam, random backoff, retry.
5. **State the two ideal ALOHA throughput values.**  
   Hint: `1/(2e)` and `1/e`.
6. **Why can hidden stations still collide under CSMA?**  
   Hint: they cannot hear one another but their signals overlap at a receiver.

### Likely long-answer questions

1. **Compare ALOHA, slotted ALOHA, CSMA, CSMA/CD, and CSMA/CA.**  
   Answer hint: sensing, timing, collision handling, suitable media, and efficiency.
2. **Explain Ethernet binary exponential backoff.**  
   Answer hint: collision detection, jam, random slot range, repeated-collision growth, and retry limit.
3. **Analyse why random-access throughput falls at high offered load.**  
   Answer hint: more simultaneous attempts, collisions, retransmissions, positive feedback, and channel saturation.
4. **Compare random access, controlled access, and channelization.**  
   Answer hint: permission, collisions, predictability, examples, and traffic conditions.

### Short-answer revision checklist

Be ready to draw a CSMA/CD frame exchange, quote both ALOHA efficiency formulas, explain hidden terminals, and state why full-duplex switched Ethernet does not collide.
