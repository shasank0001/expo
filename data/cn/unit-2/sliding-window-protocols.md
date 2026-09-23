---
subject: cn
unit: 2
topic: sliding-window-protocols
syllabus_ref: CSM3103 Unit-II
status: draft
---
# Sliding-Window Protocols

## Overview

A **sliding-window protocol** allows a sender to transmit more than one frame before it must stop and wait for acknowledgements. The window is a range of frame sequence numbers that the sender may use. As acknowledgements arrive, the window moves forward and new frames can enter it.

Sliding windows solve the idle-time problem of stop-and-wait. A fast, long-delay link can carry several frames in flight at once. The protocol therefore combines pipelining, sequence numbers, acknowledgements, flow control, and retransmission. It is a central data-link concept and also provides a useful model for TCP.

The syllabus explicitly names sliding-window protocols, so this file gives a long treatment of the sender and receiver windows, sequence-number spaces, acknowledgement rules, Go-back-N, Selective Repeat, timers, utilisation, duplicate and out-of-order cases, and worked timelines.

## Explanation

### 1. What is a window?

A window is a range of consecutive sequence numbers. If the sender uses sequence numbers 0, 1, 2, ..., and its current window starts at 5 with size 3, it may transmit frames 5, 6, and 7. It cannot transmit frame 8 until the window advances.

For the sender:

- `send_base` or `left edge`: oldest unacknowledged frame;
- `next_seq_num` or `right edge`: next new frame to send;
- `W`: number of frames allowed outstanding.

For the receiver:

- `rcv_nxt`: next sequence number expected in order;
- a receive buffer may hold later frames if the protocol permits out-of-order delivery;
- a `W`-sized window bounds the amount of data held.

When an acknowledgement for the oldest outstanding frame is received, `send_base` moves forward. The window's right edge moves by the same amount. This “sliding” is the basic idea.

### 2. Why pipeline?

Stop-and-wait leaves the sender idle during propagation and acknowledgement time. If the link has a high bandwidth-delay product, it can carry more data than the sender has in flight. Pipelining sends several frames without waiting for each individual ACK.

A useful link measure is the **bandwidth-delay product**:

`BDP = R x RTT`

It estimates how many bits must be in flight to keep a path busy. A window should be large enough to cover the BDP for ideal utilisation, but not so large that buffers overflow or the network becomes congested. The exact condition depends on frame size and protocol overhead.

### 3. Sender and receiver views

A sender's window contains frames that have been sent but not yet acknowledged, plus new frames it may send. A receiver's window contains sequence numbers it is willing to accept. In a simple cumulative-ACK protocol, the receiver often accepts frames only in order, so its window starts at the next expected frame. In Selective Repeat, later frames can arrive early and be buffered.

A frame's sequence number must be distinguishable from old retransmissions. If the sequence space is `M`, the protocol must choose a window smaller than half the sequence space for Selective Repeat to avoid confusing a new frame with an old one. Go-back-N can use a different relationship, but it still needs enough sequence-number space to distinguish delayed duplicates.

### 4. Acknowledgement choices

A **cumulative ACK** acknowledges every frame up to a sequence number. For example, `ACK 5` may mean “frame 4 and all earlier frames are received; next expected is 5.” This is simple and efficient when frames arrive in order.

A **selective ACK** identifies individual frames or ranges. It can tell the sender that frames 3 and 5 arrived but frame 4 did not. This reduces retransmission but requires more control information and receiver logic.

ACKs can be cumulative or individual, delayed or immediate. Delaying ACKs reduces overhead but increases the time before the sender learns that a frame was lost.

### 5. Go-back-N

In **Go-back-N (GBN)**, the sender can have up to `N` unacknowledged frames. The receiver normally accepts frames only in sequence. If frame `k` is lost while frames `k + 1` through `k + j` arrive, the receiver discards or ignores those later frames because it cannot deliver them before the missing frame. The sender must retransmit frame `k` and all later unacknowledged frames.

A GBN sender normally has one timer for the oldest unacknowledged frame. A cumulative ACK advances the left edge by more than one frame. GBN is simpler than Selective Repeat and uses less receiver memory, but a single loss can cause unnecessary retransmissions.

### 6. Selective Repeat

In **Selective Repeat (SR)**, the receiver can accept and buffer out-of-order frames within its window. It acknowledges each valid frame independently. If one frame is lost, only that frame is retransmitted; later correct frames can be delivered when the gap is filled.

SR is more efficient over a lossy or reordering link, but it requires:

- a receive buffer for each possible out-of-order frame;
- per-frame or range acknowledgements;
- careful duplicate detection;
- a larger sequence-number space relative to the window.

SR is commonly used in protocols where reordering and loss are common, including selected TCP variants. The basic exam distinction is “GBN retransmits from the loss onward; SR retransmits only the missing frame.”

### 7. Stop-and-wait as a special case

A window of size 1 is stop-and-wait. The sender has one unacknowledged frame. Increasing the window increases the amount of data in flight and can improve utilisation until the receiver, sender, or network becomes the bottleneck.

A window does not guarantee that every frame arrives exactly once unless the protocol also uses reliable acknowledgements, checksums, sequence numbers, timers, and duplicate handling.

### 8. Flow control and congestion awareness

The window is a **flow-control mechanism** because it limits outstanding data. A receiver may advertise a smaller window when its buffer is full. The sender should not exceed the advertised amount.

A network may also signal congestion through loss, delay, or an explicit notification. The sender can reduce its effective window. In TCP, the advertised receiver window is called `rwnd`, while the congestion window is `cwnd`; the effective sending limit is usually the smaller of the two.

The link-layer window is not automatically a congestion-control algorithm. A fixed large window can overwhelm a router. Good protocols combine window-based flow control with adaptive rate or congestion response.

### 9. Timers and retransmission

A sender may keep:

- a timer for the oldest outstanding frame;
- one timer per frame;
- a retransmission timer with exponential backoff;
- a fast-retransmit threshold based on duplicate ACKs.

When the timer expires, the sender retransmits according to GBN or SR rules. Too many retransmissions can create a congestion collapse, while too few may leave a hole unrepaired. A protocol may cap retries and report failure to the upper layer.

### 10. Buffering and out-of-order delivery

Suppose frames 1, 2, and 3 are sent and frame 2 is lost:

- **GBN:** frames 3 and later are discarded at the receiver; the sender retransmits 2, 3, and any later unacknowledged frames.
- **SR:** frame 3 is stored and acknowledged; the sender retransmits only 2. When 2 arrives, the receiver delivers 2 then 3.

Out-of-order buffering costs memory and requires a data structure or bitmap to record which sequence numbers are present. It also complicates delivery to the next layer if the next layer requires ordered data.

### 11. Error detection and frame loss

Every frame normally contains a checksum or CRC. A receiver can distinguish a damaged frame from a missing one only if it has enough context. A missing frame creates a sequence-number gap; a damaged frame is discarded and the missing number is never marked present. A timer or repeated duplicate ACK signals the sender to retry.

The link layer may also experience bit errors that change the sequence number itself. A checksum protects the header as well as the payload in a well-designed frame, reducing the chance of delivering data to the wrong sequence position.

### 12. Efficiency calculation

For a link rate `R`, frame size `L`, and one-way propagation delay `T_p`, the frame transmission time is:

`T_f = L / R`

The round-trip time is approximately:

`RTT = 2T_p + T_ack + T_f`

If the window can hold at least `RTT / T_f` frames, the sender can keep the link busy in an ideal case. A commonly quoted stop-and-wait condition is:

`W >= 1 + 2a`, where `a = T_p / T_f`.

For Selective Repeat and GBN, the precise capacity depends on acknowledgement and processing assumptions. A window larger than necessary does not increase the physical link rate; it only fills idle gaps, and it can increase queues and loss.

### 13. Protocol design choices

Important choices include:

- window size;
- sequence-number width and wrap-around;
- cumulative versus selective ACK;
- receiver buffering and delivery order;
- timeout policy and retransmission scope;
- maximum retry count;
- how congestion and zero windows are handled;
- whether the channel can reorder frames.

A protocol must balance efficiency against memory, complexity, and fairness.

## Worked examples

### Example 1: Basic window movement

The sender uses window size 3 and starts at sequence 1. It sends frames 1, 2, and 3. A cumulative ACK for frame 1 moves the left edge to 2, allowing frame 4. The current outstanding range is then 2, 3, 4. The window has advanced one position.

### Example 2: Go-back-N with a lost frame

Sender window is 4, with frames 1, 2, 3, and 4 outstanding. Frame 2 is lost; frames 3 and 4 arrive. A GBN receiver cannot accept them in order, so it sends duplicate ACKs for frame 1. The sender retransmits 2, 3, and 4. The receiver then accepts the sequence.

### Example 3: Selective Repeat with a lost frame

The same frames are sent, but the SR receiver stores 3 and 4 and acknowledges them separately. It receives no valid data for 2, so the sender retransmits only 2. Once 2 arrives, the receiver delivers 2, 3, and 4 in order. More receiver memory is used, but less bandwidth is wasted.

### Example 4: ACK loss and duplicate

The receiver accepts frame 1 and sends `ACK 1`, but the ACK is lost. The sender retransmits frame 1 after its timer. The SR receiver sees that 1 is already delivered, discards the duplicate, and sends another `ACK 1`. The application receives one copy.

### Example 5: Receiver window becomes small

A receiver's buffer is almost full and advertises a window of 1. The sender, even though it could physically send several frames, sends only one and waits. This protects the receiver. When the application reads data, the receiver advertises a larger window and the sender resumes.

### Example 6: Wrap-around

A 3-bit sequence space has values 0 through 7. A protocol using it must prevent an old frame from a previous cycle from being mistaken for a current frame. Selective Repeat therefore keeps the active window small enough relative to 8; for example, a window of 3 leaves separation between old and new values. GBN can sometimes use a larger fraction, but duplicate logic remains essential.

### Example 7: Numerical utilisation

Link rate `R = 10 Mbit/s`, frame size `L = 1,000 bits`, one-way propagation `T_p = 20 ms`, and negligible ACK time. Then:

`T_f = 1,000 / 10,000,000 = 0.0001 s = 0.1 ms`

`RTT ≈ 40 ms`, so the number of frames needed to cover the delay is about `40 / 0.1 = 400`. A window smaller than this leaves idle capacity; a window near 400 can keep the link busy if the receiver can buffer and the network does not congest. This is an idealised calculation.

## Key terms & formulas

- **Sliding window:** a range of sequence numbers allowed in flight.
- **Pipeline:** several frames sent before ACKs return.
- **Window size `W`:** number of frames/bytes allowed outstanding.
- **Send base:** oldest unacknowledged sender sequence number.
- **Next sequence number:** next new frame to transmit.
- **Receive next:** next in-order frame expected by receiver.
- **Cumulative ACK:** acknowledges all frames up to a point.
- **Go-back-N:** retransmit the missing frame and all later unacknowledged frames.
- **Selective Repeat:** retransmit only missing frames.
- **BDP:** `R x RTT`; data bits needed in flight to fill a path.
- **Frame time:** `T_f = L / R`.
- **Round-trip time:** `RTT ≈ 2T_p + T_f + T_ack`.
- **Stop-and-wait as W=1:** one outstanding frame.
- **Typical capacity condition:** `W >= RTT / T_f`, with protocol-specific adjustments.
- **Stop-and-wait formula:** `U = T_f / (T_f + 2T_p + T_ack)`.
- **GBN advantage:** simple receiver and cumulative ACKs.
- **SR advantage:** less retransmission after isolated loss.
- **Window as flow control:** limits data in flight to protect receiver/network.

## Common mistakes

1. **A window is not a physical opening or a router queue.** It is a logical range of sequence numbers/data.
2. **Sliding window is not only about ACKs.** It combines sequencing, pipelining, buffering, and retransmission.
3. **Go-back-N retransmits from the first loss onward.** It does not resend only the missing frame.
4. **Selective Repeat needs receiver buffering.** A receiver cannot simply discard later frames.
5. **A cumulative ACK does not identify every individual frame.** It acknowledges a prefix.
6. **A lost ACK is not a lost frame.** The sender must handle duplicate retransmission.
7. **A larger window is not automatically better.** It can fill the path but also overflow queues.
8. **Window size is not exactly the BDP in every protocol.** ACK, processing, and frame overhead matter.
9. **A receiver window protects the receiver; congestion control protects the network.** They can both limit the effective send rate.
10. **Out-of-order receipt does not automatically mean out-of-order delivery.** The next layer may require ordered data.
11. **The window can wrap around.** Sequence-number comparison and duplicate detection must handle it.
12. **The window does not guarantee reliability by itself.** Error detection and recovery rules are still required.

## Exam prep

### Likely 2-mark questions

1. **What is a sliding-window protocol?**  
   Hint: allow multiple frames in flight using a bounded sequence-number window.
2. **State two purposes of a window.**  
   Hint: pipelining/bandwidth utilisation and flow control.
3. **Compare Go-back-N and Selective Repeat.**  
   Hint: GBN retransmits missing plus later frames; SR retransmits only missing frames and buffers out-of-order data.
4. **Define cumulative ACK.**  
   Hint: acknowledgement covers all frames up to a sequence number.
5. **What is the bandwidth-delay product?**  
   Hint: `R x RTT`, the amount of data needed in flight to keep a path busy.
6. **Why is stop-and-wait equivalent to a window of size one?**  
   Hint: only one frame may be outstanding before an ACK.

### Likely long-answer questions

1. **Explain sliding-window operation with sender and receiver windows.**  
   Answer hint: define base, next sequence, window bounds, pipelining, ACK movement, and flow control.
2. **Draw a Go-back-N scenario with a lost frame and explain recovery.**  
   Answer hint: show later frames arriving, receiver rejection/duplicate ACKs, retransmission from the loss, and final order.
3. **Draw a Selective Repeat scenario and compare it with Go-back-N.**  
   Answer hint: buffer later frames, selective ACKs, retransmit only the missing number, and discuss memory/sequence space.
4. **Calculate the required window for a given link and RTT.**  
   Answer hint: calculate `T_f`, `RTT`, BDP, and divide by frame size; state assumptions.
5. **Compare sliding-window flow control and TCP congestion control.**  
   Answer hint: receiver window versus congestion window, effective minimum, ACK/loss signals, and buffer effects.
6. **Explain what happens when a frame, an ACK, or a sequence number is lost.**  
   Answer hint: distinguish timeout, duplicate detection, gap, and recovery policy.

### Short-answer revision checklist

Be ready to draw a window before and after ACK arrival, calculate a BDP, compare GBN/SR in one table, and explain why sequence numbers are needed even when checksums detect damage.
