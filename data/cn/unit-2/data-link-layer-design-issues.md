---
subject: cn
unit: 2
topic: data-link-layer-design-issues
syllabus_ref: CSM3103 Unit-II
status: draft
---
# Data-Link Layer Design Issues

## Overview

The **data-link layer** moves data across one physical link or local broadcast domain. It sits above the physical layer and below the network layer. The physical layer can place bits on a medium, but the data-link layer decides where a unit of data begins and ends, how a local receiver recognises it, which station may transmit, and what to do when noise damages the signal.

The syllabus asks for the design issues of this layer. The most important are framing, error control, flow control, medium access control, transparency, addressing, connection management, and half-duplex/full-duplex operation. These issues are closely related. Poor framing makes error checking impossible; error detection without a recovery policy causes repeated failures; a sender that ignores flow control can overwhelm a receiver; and an unfair access method can waste a shared medium.

The data link is normally a **hop-by-hop** service. A link can detect damage on a particular cable without guaranteeing delivery across a multi-hop path. End-to-end protocols such as TCP add broader reliability.

## Explanation

### 1. Position and scope

The data-link layer receives a network-layer packet and places it in a **frame**. On the receiving side, it checks the frame, recovers or discards it according to the protocol, removes the link header, and gives the packet to the network layer.

“Local” does not mean a fixed distance. A link can be a short cable, a wireless cell, a point-to-point WAN link, or a bridge segment. The key is that the layer usually has direct control over one medium and does not need to route through unrelated networks.

The data-link layer is also where a frame normally carries:

- a frame delimiter or start marker;
- a source link-layer address;
- a destination link-layer address;
- control information such as sequence or acknowledgement fields;
- the network-layer packet;
- an error-detection or error-correction field;
- sometimes a trailer or end delimiter.

### 2. Framing

A physical medium carries a continuous stream of signals, but the receiver must know where a frame starts and ends. **Framing** defines boundaries so a receiver can extract complete units. Common methods include:

- **sentinel bytes/flags:** special beginning and ending markers;
- **length field:** the frame header declares its length;
- **bit stuffing:** a reserved bit pattern is escaped inside data;
- **character stuffing:** a reserved character is escaped;
- **clock and preamble:** a receiver synchronises to a preamble and then reads a fixed or declared frame;
- **delimiters:** fixed separation between frames or cells.

A preamble helps the receiver's clock recover synchronisation. A start-frame delimiter marks the beginning, and an end delimiter or length field marks the end. If a delimiter pattern occurs in ordinary data without escaping, the receiver may falsely detect a boundary.

Ethernet uses a preamble, a start-frame delimiter, and a length-type field. PPP uses a flag and byte/character stuffing in asynchronous links. ATM uses fixed-size cells, so a receiver knows the boundary after reading the fixed 53-byte unit.

### 3. Transparency

A protocol must be **transparent**: ordinary user data should not be mistaken for control fields. If a flag or escape character can occur in the payload, the sender changes it according to a reversible rule and the receiver restores it.

- In **bit stuffing**, a zero bit is inserted after every sequence of five consecutive 1s if the next data bit is 1. The receiver removes inserted zeros.
- In **character stuffing**, a reserved character is preceded by an escape character. The receiver reverses the rule.
- A length field avoids delimiter ambiguity but must itself be protected from corruption.
- Fixed-size cells give an unambiguous boundary but can waste space when the payload is small.

Transparency is essential when an application sends binary data that happens to contain the control pattern.

### 4. Error control

Noise, interference, attenuation, and equipment faults can change bits. The link layer can:

- **detect** an error using parity, checksum, or CRC;
- **correct** it using a code with enough redundancy;
- **discard and request retransmission** using an acknowledgement/ARQ protocol;
- **mark** a damaged frame as unreliable for the upper layer;
- use a combination of detection, correction, and retransmission.

A checksum or CRC is usually an error-detection mechanism, not proof of correctness. Some undetected error patterns are possible, though a good code makes them rare. An acknowledgement is also not universal: some unacknowledged links may rely on correction and upper-layer checks.

Error control at the link layer concerns one or a small number of links. TCP error control is end-to-end and can recover data lost anywhere along the path. A CRC in an Ethernet frame does not repair a damaged IP packet automatically.

### 5. Flow control

**Flow control** prevents a sender from transmitting faster than a receiver can process or buffer data. It may use:

- a stop-and-wait scheme;
- a receiver window or sequence numbers;
- credits or permits;
- acknowledgements that release buffer space;
- link-level rate control.

If a receiver's buffer is full, it can advertise zero available space, stop acknowledging, or send a pause/control message. A large sender that ignores this condition can cause memory overflow, packet loss, or excessive retransmissions.

Flow control is receiver protection. It is different from congestion control, which protects shared network resources such as routers and links. A receiver may be healthy while a bottleneck occurs in the middle of a path.

### 6. Medium access control

When many stations share a medium, the link layer needs a **medium-access-control (MAC)** method. It decides which station can transmit and handles collisions or controlled access. The syllabus's random-access, controlled-access, and channelization topics are all solutions to this problem.

- Random access lets any station try, then handles collisions.
- Controlled access grants permission through polling or a token.
- Channelization divides the medium into channels by frequency, time, code, or another dimension.

The choice depends on topology, traffic pattern, propagation delay, collision detection ability, and required fairness. Wired Ethernet historically used CSMA/CD; wireless LANs generally use CSMA/CA because a station may not hear a collision while transmitting.

### 7. Addressing and multiplexing

A link-layer address identifies a local interface or station. In Ethernet, the destination MAC address tells the link layer where a frame should go on the current LAN. Link addresses are normally changed at a router because they are meaningful only on the local link.

Some link protocols also support protocol multiplexing by identifying which higher-layer protocol or service a frame carries. A PPP protocol field, for example, tells the receiver how to interpret the payload.

### 8. Connection management and service modes

A link can be connectionless or connection-oriented. A connectionless link sends independent frames and uses addressing and error detection for each one. A connection-oriented link may establish state, number frames, acknowledge them, and release the connection after the exchange.

Full-duplex links allow simultaneous sending and receiving. Half-duplex links need to coordinate direction. Link management also includes detecting loss of carrier, negotiating speed or duplex, and bringing an interface up or down.

### 9. Interaction with upper and lower layers

The network layer supplies a packet and destination address. The data-link layer chooses a local representation, including a link address and frame boundary. The physical layer transmits the resulting bits. If the physical link has excessive errors, a lower-layer problem may appear as frequent FCS failures or retransmissions above it.

A link-layer implementation may also carry QoS priority information, VLAN tags, flow-control credits, and security-related metadata. The field structure depends on the protocol.

### 10. Design trade-offs

Every design choice has a cost:

- larger headers improve reliability and options but add overhead;
- more redundancy improves detection/correction but uses bandwidth;
- smaller frames reduce MTU problems but increase header and timing overhead;
- larger windows improve bandwidth-delay utilisation but require buffers and can increase congestion;
- acknowledgements improve recovery but add delay and traffic;
- full duplex reduces collisions but may require more capacity or hardware.

The right design depends on error rate, propagation delay, traffic load, available bandwidth, and the importance of delay.

## Worked examples

### Example 1: Frame boundary and stuffed data

A frame uses `01111110` as a flag. If payload data contains the same pattern, the sender stuffs a zero after every five consecutive ones or escapes the flag. The receiver removes the stuffing and searches for the real flag. Without transparency, the receiver could end the frame early.

### Example 2: Flow-control failure

A high-speed camera sends frames to a receiver that can process only 10 frames per second. If the camera sends 100, the receiver's buffer fills. A credit scheme reduces the camera's allowance, or the receiver advertises a small window. Without flow control, frames are dropped and the upper layer sees missing data.

### Example 3: Collision handling

Two stations on a shared Ethernet segment sense an idle medium and transmit at the same time. Their signals overlap. A CSMA/CD protocol detects the collision, sends a jam signal, chooses a random backoff, and retries. Modern switched full-duplex Ethernet avoids shared collisions.

### Example 4: Local versus end-to-end error

An Ethernet frame has a bad CRC on the cable from a laptop to a switch. The switch may discard the frame. Even if the link recovers, many Internet paths may still lose or duplicate IP packets; TCP must provide end-to-end reliability for an application that needs it.

### Example 5: Fixed boundary

An ATM cell is always 53 bytes. A receiver knows that 53 bytes form one cell, so it does not need a variable delimiter. The fixed size simplifies switching but may waste capacity for a small message.

## Key terms & formulas

- **Data-link layer:** Layer 2; frame delivery over a local link.
- **Frame:** Layer-2 protocol data unit.
- **Framing:** identifying frame start and end.
- **Transparency:** preventing user data from being mistaken for control information.
- **Sentinel/flag:** a special boundary marker.
- **Bit stuffing:** inserting a 0 after five consecutive 1s when required.
- **Error detection:** discovering many transmission errors.
- **Error correction:** repairing errors without retransmission.
- **ARQ:** automatic repeat request; retransmit detected bad frames.
- **Flow control:** protect receiver capacity.
- **Congestion control:** protect shared network capacity.
- **MAC:** medium access control.
- **Poll cycle:** a successful transmission plus required waiting interval.
- **Utilisation for stop-and-wait:** approximately `Tframe / (Tframe + 2Tprop + Tack)` under a simple model.
- **Window size:** number of unacknowledged frames permitted.

## Common mistakes

1. **The data-link layer is not the network layer.** It moves frames over a local link; the network layer routes between networks.
2. **A CRC does not usually correct a frame.** It detects damage, after which a protocol may discard or retransmit.
3. **Framing is not just a header.** It includes delimiters, length, escaping, and synchronisation methods.
4. **Flow control and congestion control are different.** One protects a receiver; the other protects the network.
5. **CSMA/CD is not suitable for every medium.** Wireless stations often cannot detect collisions while transmitting.
6. **Link reliability is not automatically end-to-end reliability.** A local ACK does not prove delivery to the final application.
7. **A fixed-size cell is a framing choice, not necessarily better for every payload.** It can waste space.
8. **Bit stuffing changes the transmitted representation, not the original application data.** The receiver reverses it.
9. **MAC addresses are local.** A router normally changes them on each new link.
10. **A larger window is not always better.** It can consume buffers and contribute to congestion.

## Exam prep

### Likely 2-mark questions

1. **List four design issues of the data-link layer.**  
   Hint: framing, error control, flow control, medium access, transparency, and connection management.
2. **Define framing and transparency.**  
   Hint: boundaries; making data unable to confuse control delimiters.
3. **Distinguish flow control and congestion control.**  
   Hint: receiver protection versus shared-network protection.
4. **What is the role of a frame check sequence?**  
   Hint: detect many bit errors in a local frame.
5. **Why is a preamble sent?**  
   Hint: allow receiver synchronisation before frame data.
6. **What does MAC mean in a data-link context?**  
   Hint: method for deciding which station may use the shared medium.

### Likely long-answer questions

1. **Explain the main design issues of the data-link layer.**  
   Answer hint: framing, transparency, error control, flow control, access, addressing, connection management, and trade-offs.
2. **Compare bit stuffing, character stuffing, and length-based framing.**  
   Answer hint: control pattern escaping versus declared length, advantages, overhead, and failure handling.
3. **Describe how a receiver handles a damaged frame in an ARQ protocol.**  
   Answer hint: detect, discard or mark, signal/retransmit, and account for duplicate frames.
4. **Explain why link-layer control does not replace transport-layer reliability.**  
   Answer hint: local versus end-to-end scope, multiple links, loss/delay, and TCP's role.

### Short-answer revision checklist

You should be able to draw a frame, explain each field's purpose, give a framing and flow-control example, and distinguish all three of error detection, error correction, and congestion control.
