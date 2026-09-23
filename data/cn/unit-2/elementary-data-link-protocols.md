---
subject: cn
unit: 2
topic: elementary-data-link-protocols
syllabus_ref: CSM3103 Unit-II
status: draft
---
# Elementary Data-Link Protocols

## Overview

An elementary data-link protocol defines how two directly connected stations exchange frames over a noisy medium. It turns network-layer packets into frames, adds control information, detects errors, and decides whether to send more data, wait for an acknowledgement, or retransmit a damaged frame.

The simplest protocol is **stop-and-wait**: send one frame and wait for its acknowledgement. It is easy to understand and safe when the link is slow or errors are frequent, but it wastes capacity when the round-trip delay is long. More advanced elementary protocols use sequence numbers, acknowledgements, timers, and limited windows so that several frames can be outstanding.

The syllabus places these protocols after error detection and before sliding windows. They are the foundation for understanding how a reliable link service is built and why modern protocols use pipelining.

## Explanation

### 1. Role of an elementary protocol

A data-link protocol handles one hop. It must coordinate the sender and receiver despite three uncertainties:

1. The receiver may receive a frame correctly, but its acknowledgement may be lost.
2. The acknowledgement may reach the sender, but the sender may not know whether it arrived.
3. A frame may be damaged, delayed, duplicated, or delivered out of order.

The protocol therefore needs more than an error-detection field. It needs a rule for numbering data, identifying acknowledgements, detecting a missing response, and deciding when to retry.

### 2. Stop-and-wait protocol

In **stop-and-wait ARQ**:

1. The sender puts one numbered frame on the link.
2. The receiver checks the frame.
3. If valid, it sends an acknowledgement for that sequence number.
4. The sender waits for the acknowledgement and its timer.
5. If the acknowledgement arrives before the timeout, the sender sends the next frame.
6. If the frame or acknowledgement is lost, the timer expires and the sender retransmits.
7. The receiver uses sequence numbers to recognise a duplicate.

The sender cannot transmit frame `n + 1` until frame `n` is acknowledged. This gives simple flow control and limits receiver buffering.

### 3. Acknowledgement and timer

An **acknowledgement (ACK)** tells the sender that a frame was received correctly. The acknowledgement may carry the next expected sequence number or the last correctly received sequence number, depending on the protocol.

A **timeout** is a timer started when a frame is sent. If no suitable acknowledgement arrives before it expires, the sender assumes that the frame or ACK was lost and retransmits. The timer must be long enough to cover normal round-trip delay and short enough to recover promptly.

A timeout is not proof that a frame was lost. The frame may have arrived and the ACK may have been delayed or lost. This uncertainty is why sequence numbers are necessary.

### 4. Error detection and recovery

A receiver calculates a checksum or CRC over the frame. If the check fails, it discards the frame. A reliable protocol can then:

- return a negative acknowledgement (NAK);
- remain silent and let the sender time out;
- send an explicit reject or selective-repeat request.

A positive ACK normally indicates error-free reception, not that the higher layer has processed the data. It may be generated as soon as the frame is stored.

### 5. Sequence numbers and duplicates

A sequence number identifies a frame. In a stop-and-wait protocol with one outstanding frame, alternating bit `0` and `1` may be enough. The receiver remembers the expected bit:

- if it receives the expected number, it delivers the frame and toggles the expected bit;
- if it receives the same number again, it discards the duplicate and sends the ACK again;
- if it receives the other number unexpectedly, it can reject it or ask for retransmission.

Without sequence numbers, a lost ACK could cause the sender to retransmit a frame that was already delivered, and the receiver could pass duplicate data to the next layer.

### 6. Utilisation and delay

Stop-and-wait works well when the frame transmission time is large compared with the propagation and acknowledgement delay, or when errors are common. It performs poorly on a long, fast link because the sender waits after every frame.

A simple cycle includes:

- frame transmission `T_f`;
- propagation to the receiver and back `2T_p`;
- receiver processing/ACK transmission `T_ack`;
- any retransmission delay.

Approximate ideal utilisation is:

`U = T_f / (T_f + 2T_p + T_ack)`

A 10 Mbit/s link with a tiny frame and 100 ms round-trip propagation may have a very low stop-and-wait utilisation. A pipelined window allows multiple frames to fill the path.

### 7. Simplex, half-duplex, and duplex protocols

A **simplex** protocol has a fixed one-way direction. A **half-duplex** protocol may use the same medium in either direction but only one at a time. A **full-duplex** protocol can send data and acknowledgements simultaneously, often using separate channels or full-duplex hardware.

The simplex stop-and-wait model is easy to draw but does not describe every real link. Many protocols use separate data and ACK directions or return an acknowledgement in the reverse path.

### 8. Pipelining and sliding window

A **window** is the range of sequence numbers a sender may transmit without receiving an acknowledgement. With a window size `W`, up to `W` frames may be outstanding. As ACKs arrive, the window slides forward.

Pipelining keeps the link busy and improves bandwidth-delay utilisation. It also introduces ordering and buffering requirements. A lost early frame may cause a later frame to be buffered at the receiver or retransmitted under the selected recovery rule.

### 9. Go-back-N and Selective Repeat preview

- **Go-back-N:** acknowledge frames cumulatively. If frame `k` is missing, frames `k` and later outstanding frames are retransmitted.
- **Selective Repeat:** acknowledge each frame independently. Only missing frames are retransmitted; later correctly received frames can be delivered or held according to the protocol.

Selective Repeat uses more memory and a larger sequence-number space, but avoids unnecessary retransmission. These methods are covered in depth in the sliding-window file.

### 10. Protocol design choices

A designer chooses:

- frame and sequence-number size;
- acknowledgement type and frequency;
- timer duration and retry limit;
- maximum retry count;
- duplicate handling;
- receiver buffer size;
- flow-control window;
- behaviour after an unrecoverable failure.

Too short a timer causes unnecessary retransmissions and duplicate ACKs. Too long a timer delays recovery. Too many retries can create congestion, while too few can cause a permanent failure even when a later attempt would succeed.

## Worked examples

### Example 1: Successful stop-and-wait exchange

Sender transmits frame 0. Receiver checks it and sends ACK 0. The sender receives the ACK before its timer expires and transmits frame 1. The receiver expects frame 1, accepts it, and sends ACK 1.

### Example 2: Frame lost

The sender transmits frame 0, but noise destroys it. The receiver sends no ACK. The sender's timer expires, retransmits frame 0, and the receiver accepts it. The link is protected, although the round trip consumes capacity.

### Example 3: ACK lost

The receiver accepts frame 0 and sends ACK 0, but the ACK is destroyed. The sender times out and retransmits frame 0. The receiver recognises the duplicate sequence number, discards the payload, and sends ACK 0 again. No duplicate reaches the network layer.

### Example 4: Utilisation

For a 1 Mbit/s link, a 1,000-bit frame takes `T_f = 1 ms`. If the round-trip propagation and ACK time total 20 ms, stop-and-wait utilisation is approximately `1 / (1 + 20) = 4.8%`, ignoring other overhead. A window can keep the link busy.

### Example 5: Flow control

A receiver can advertise that it has room for only two frames. Even if the sender's maximum window is ten, it sends only two outstanding frames. The sender advances only after ACKs or window updates, so a slow receiver is not overrun.

## Key terms & formulas

- **Elementary protocol:** simple sender/receiver frame exchange.
- **Stop-and-wait:** one frame outstanding at a time.
- **ACK:** positive acknowledgement.
- **NAK:** negative acknowledgement or rejection.
- **Timeout:** timer that triggers retransmission.
- **Sequence number:** identifier for a frame.
- **Duplicate:** a retransmission already received.
- **Pipelining:** multiple frames in flight.
- **Window:** range of unacknowledged sequence numbers.
- **ARQ:** automatic repeat request.
- **Frame transmission time:** `T_f = L / R`.
- **Round-trip delay:** `2T_p + T_ack` approximately.
- **Stop-and-wait utilisation:** `T_f / (T_f + 2T_p + T_ack)`.
- **Window capacity rule:** `W >= 1 + 2a` for a fully occupied stop-and-wait link, where `a = T_p / T_f`, subject to protocol constraints.

## Common mistakes

1. **An ACK is not always proof that the final application received the data.** It normally confirms link-layer receipt.
2. **A timeout does not prove the frame was lost.** The ACK may have been lost or delayed.
3. **Retransmission can create duplicates.** Sequence numbers allow the receiver to discard them.
4. **Stop-and-wait does not use the full long-fat link.** It waits for each ACK.
5. **A NAK is not always used.** A protocol may simply wait for a timeout.
6. **The sequence number is not the CRC.** It orders/identifies frames; the check field detects damage.
7. **Elementary protocols are hop-by-hop.** They do not provide a complete end-to-end service by themselves.
8. **A larger window improves utilisation only while buffers and receiver capacity allow it.** It can increase loss and reordering.
9. **ACK numbers are protocol-defined.** Some identify the next expected frame, others the last received frame.
10. **A retry limit is needed.** Infinite retries can overload a failed link.

## Exam prep

### Likely 2-mark questions

1. **Explain stop-and-wait with a sequence diagram.**  
   Hint: send frame, check, ACK, next frame, timeout/retry.
2. **State the roles of ACK, timeout, and sequence number.**  
   Hint: receipt confirmation, lost-response recovery, duplicate/order detection.
3. **Why can retransmission produce duplicates?**  
   Hint: ACK may be lost after the frame was accepted.
4. **Give a simple formula for stop-and-wait utilisation.**  
   Hint: `T_f / (T_f + 2T_p + T_ack)`.
5. **What is an elementary data-link protocol?**  
   Hint: rules for framing, error checking, acknowledgement, and retransmission over a link.

### Likely long-answer questions

1. **Explain a stop-and-wait ARQ protocol and handle all failure cases.**  
   Answer hint: successful ACK, lost frame, lost ACK, timeout, duplicate, and sequence-number check.
2. **Derive why stop-and-wait is inefficient on a long-delay link.**  
   Answer hint: include frame time, propagation, ACK, idle sender, and a numerical utilisation example.
3. **Compare stop-and-wait with a pipelined sliding-window protocol.**  
   Answer hint: outstanding frames, buffer, delay-bandwidth use, ordering, and recovery.
4. **Design a simple elementary protocol for a half-duplex noisy link.**  
   Answer hint: framing, parity/CRC, sequence number, ACK/timeout, duplicate handling, and retry limit.

### Short-answer revision checklist

Be ready to draw a stop-and-wait timeline, calculate utilisation, explain lost-frame and lost-ACK cases, and define how a sequence number prevents duplicate delivery.
