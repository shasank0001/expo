---
subject: cn
unit: 1
topic: data-communication-fundamentals
syllabus_ref: CSM3103 Unit-I
status: draft
---
# Data Communication Fundamentals

## Overview

Data communication is the exchange of information between a source and a destination using a communication system. A network is useful only when people or applications can send data, have it delivered with acceptable speed and accuracy, and do so at a reasonable cost. The subject starts with the vocabulary needed to compare communication systems: messages, signals, senders, receivers, channels, bandwidth, delay, throughput, and reliability.

A good mental model is a road system. A message is a parcel, the sender and receiver are the endpoints, a medium is a road, bandwidth is how many vehicles can pass in a period, and delay is the time a vehicle spends travelling or waiting. A wide road can carry many vehicles, but it may still be far away. Networking therefore considers capacity, latency, loss, security, and cost together rather than just “speed.”

The syllabus identifies five ideas in this topic: characteristics, components, data-flow directions, network criteria, and the basic communication model. These ideas are used throughout Units I–V. A router, a TCP connection, a DNS lookup, and an email message all have an end-to-end goal, but each uses components and protocols to turn that goal into a reliable exchange.

## Explanation

### 1. Characteristics of data communication

A communication system has several useful characteristics:

- **Sender/source:** the device or person that produces the information.
- **Receiver/destination:** the device or person that consumes it.
- **Message:** the information being communicated, such as text, an image, audio, video, or control data.
- **Signal:** a physical representation of the message suitable for the medium, such as voltage, current, light, or radio waves.
- **Medium/channel:** the path and physical means by which the signal travels.
- **Protocol:** the agreed set of rules for representing, sending, receiving, and interpreting the data.
- **Bandwidth:** the maximum data-carrying capacity of a channel, normally in bits per second (bit/s).
- **Delay/latency:** the time between sending a bit and receiving it.
- **Throughput:** the useful data rate actually achieved, which is normally lower than the nominal bandwidth.
- **Reliability:** the probability that data arrives intact, in time, and in the required order.
- **Security:** protection against unauthorized access, alteration, disclosure, or disruption.

The common characteristics are direction, mode, timing, and synchronism. **Direction** describes whether data flows one way or both ways. **Mode** describes whether both directions can happen at once. **Synchronism** means the sender and receiver agree on when a symbol or block begins and ends.

Data can be represented digitally as bits. A bit is the smallest unit used in the discussion of data communication. In a real signal, one bit may be represented by a voltage range or a light pulse. A byte normally contains eight bits. Protocols must agree on how many bits make a character, where a frame begins, what a zero or one means, and what a checksum means.

Three delay components are especially important:

- **Transmission delay:** time to put all bits on the medium, approximately `L / R`, where `L` is the number of bits and `R` is the link rate.
- **Propagation delay:** time for a signal to travel; it grows with distance.
- **Processing and queueing delay:** time spent in routers or waiting for access to a link.

Thus a fast link can still produce a large response time if packets wait in a queue or travel a long physical distance. This distinction will be useful when studying TCP congestion control and routing.

### 2. Components of a communication system

A complete data communication system normally has these components:

1. **Input or source device:** creates the message, for example a keyboard, microphone, sensor, or application.
2. **Input transducer or interface:** converts the message into a signal where necessary.
3. **Transmitter:** amplifies, encodes, and shapes the signal for the medium.
4. **Transmission medium:** carries the signal; it may be copper, fiber, radio, or another path.
5. **Receiver:** detects and recovers the signal from the medium.
6. **Destination device:** presents the message to a person or application.
7. **Output transducer/interface:** converts the result back into a usable form.
8. **Protocol software/hardware:** coordinates both ends and handles addressing, framing, errors, and timing.

In a computer network, a sender application creates data, the transport and network protocols add control information, the data-link layer places the packet in a frame, and the physical layer sends individual bits. The receiver performs the reverse operations. This is why a small file can require work at several layers even though the user sees only one file transfer.

A protocol is not the same as a service. A service describes what a layer offers to the layer above; a protocol defines the rules and messages used to implement that service. A router service may be “forward a packet,” while the IP protocol defines the address and header that allow a packet to be forwarded.

### 3. Data flow

Data flow describes the direction and timing of communication.

**Simplex** communication is one-way only. A traditional broadcast, such as a radio station transmitting to listeners, is simplex. A keyboard sending keystrokes to a computer is another example if no return path is used.

**Half-duplex** communication can travel in both directions, but only one direction at a time. A walkie-talkie is a useful analogy: one person speaks, then the other replies. Half-duplex uses a shared resource efficiently but introduces waiting time.

**Full-duplex** communication allows both directions at the same time. A telephone call and a switched full-duplex Ethernet link are examples. Full-duplex reduces turn-taking and can improve utilization, but it may require separate channels or more sophisticated hardware.

Data-flow direction and communication mode answer different questions. Direction asks **which way can data go?**. Mode asks **can both sides send at the same time?** Therefore, “two-way” does not automatically mean full-duplex: a two-way half-duplex link alternates directions.

### 4. Network criteria and performance measures

Network quality is judged using several criteria.

- **Performance:** how much useful data is delivered quickly. It is measured with throughput, bandwidth, latency, and jitter.
- **Reliability:** the probability of error-free delivery and recovery from failure.
- **Security:** confidentiality, integrity, authentication, and availability.
- **Scalability:** ability to grow in users, distance, or traffic while preserving performance.
- **Accessibility:** whether authorized users can reach the service.
- **Economics:** purchase, installation, maintenance, power, and upgrade cost.
- **Manageability:** ease of configuration, monitoring, fault detection, and recovery.

**Bandwidth** is capacity, not the delay of a particular packet. **Throughput** is the goodput or actual useful rate, after overhead and retransmissions. **Latency** is delay. **Jitter** is variation in delay; it matters greatly for real-time voice and video.

A network can have high bandwidth but poor latency, for example a fast link with a long satellite path. It can have low loss but poor performance if a central server is overloaded. Good network design therefore states the traffic and application requirements first.

A basic capacity calculation is:

`throughput <= bandwidth x protocol efficiency`

If a nominal 100 Mbit/s link spends part of its time sending headers, acknowledgements, retransmissions, or collisions, useful throughput is less than 100 Mbit/s. For a file of `S` bits on a link of rate `R` with no queueing delay, the ideal transmission time is `S / R`.

### 5. Basic communication model and network criteria in practice

A sender encodes information into a message, a protocol packages it, the transmission system changes it into a signal, and the medium carries it. The receiver detects the signal, checks integrity, removes protocol information, and delivers the data. Control information in the opposite direction may acknowledge receipt or report a problem.

In a reliable system, “delivered” should be defined carefully. A link receiver may detect a corrupted frame, but an end-to-end TCP receiver may need to request retransmission of a missing byte range. Reliability can therefore be built at different layers for different purposes. A checksum detects damage; a sequence number detects missing or duplicate data; an acknowledgement confirms receipt; a timeout or retransmission mechanism tries to recover.

Network criteria are not independent. Increasing reliability may add acknowledgements and retransmissions, which consume bandwidth. Encryption improves security but can add processing delay. A redundant mesh improves fault tolerance but costs more. A design is good when it balances criteria for the application rather than maximizing one number.

## Worked examples

### Example 1: Identify flow mode

A police radio used by two officers carries a message from officer A to officer B, and then the officers take turns talking. It is two-way but half-duplex: both directions are possible, but not simultaneously.

### Example 2: Explain a home download

A laptop requests a file from a server:

1. The application creates a request.
2. DNS later provides an IP address.
3. TCP assigns source and destination ports and adds sequence/acknowledgement information.
4. IP adds the destination network address.
5. Ethernet frames carry the IP packet over each local link.
6. The physical medium carries bits.
7. The server returns data; TCP detects losses and retransmits them.
8. The application displays the file.

The user sees one service, but several components and layers cooperate.

### Example 3: Compare two links

Link A has 1 Gbit/s bandwidth and 80 ms propagation delay. Link B has 100 Mbit/s bandwidth and 5 ms delay. For a large bulk file, A may finish sooner; for a short interactive request, B may feel more responsive. This demonstrates why bandwidth must not be confused with latency.

### Example 4: Estimate transmission delay

A 4,000,000-bit file travels on a 100 Mbit/s link. The ideal transmission time is:

`4,000,000 / 100,000,000 = 0.04 seconds = 40 ms`

This ignores protocol overhead, propagation, processing, and queueing. It is a useful first estimate, not a promise about the complete response time.

### Example 5: Choose a topology

A school lab needs easy replacement of one computer and inexpensive cabling. A physical star is normally preferable: each computer has its own cable to a central switch, and a failed cable affects one station. A mesh would provide more fault tolerance but cost more and be harder to administer.

## Key terms & formulas

- **Data communication:** exchange of information between devices using a medium and agreed rules.
- **Message:** the information being sent.
- **Signal:** physical representation of a message.
- **Bandwidth:** channel capacity, commonly measured in bit/s.
- **Throughput:** useful data rate actually delivered.
- **Latency:** end-to-end delay.
- **Jitter:** variation in latency.
- **Simplex:** one direction only.
- **Half-duplex:** either direction, one at a time.
- **Full-duplex:** both directions simultaneously.
- **Protocol:** rules governing communication.
- **Reliability:** error-free, timely delivery as required.
- **Security:** confidentiality, integrity, authentication, and availability.
- **Transmission delay:** `L / R`.
- **Utilization:** useful traffic divided by available capacity over a period.
- **Bit rate:** `data bits / time`.
- **Baud:** signal changes per second; with one bit per change, bit rate and baud are equal.

## Common mistakes

1. **Bandwidth is not delay.** Bandwidth is capacity; latency is travel and waiting time.
2. **Throughput is not nominal bandwidth.** Overhead, contention, loss, and retransmissions reduce goodput.
3. **Simplex, half-duplex, and full-duplex are not the same as unicast, broadcast, and multicast.** The first group describes direction and simultaneous use; the second describes destinations.
4. **A protocol is not a physical device.** It is a set of communication rules; software and hardware may implement it.
5. **A checksum does not prove that data is correct.** It usually detects some errors; a receiver still needs a recovery policy.
6. **A two-way link is not automatically full-duplex.** Both parties may still have to take turns.
7. **High throughput does not guarantee low delay or good security.** These are separate criteria.
8. **Transmission delay is not propagation delay.** Sending the bits and waiting for them to travel are different stages.
9. **A network is more than its cables.** Protocols, addressing, management, security, and users are also part of it.
10. **Do not confuse full-duplex with two separate physical cables in every case.** Some technologies achieve simultaneous operation through frequency, time, or coding methods.

## Exam prep

### Likely 2-mark questions

1. **Define data communication and list any four components.**  
   Hint: use source, message, transmitter, medium, receiver, destination, and protocol; then name the communication system.
2. **Distinguish simplex, half-duplex, and full-duplex with one example each.**  
   Hint: direction plus ability to send simultaneously.
3. **Distinguish bandwidth and throughput.**  
   Hint: maximum channel capacity versus useful data actually delivered.
4. **Name four network quality criteria.**  
   Hint: performance, reliability, security, cost, scalability, or manageability.
5. **What is the function of a protocol?**  
   Hint: agreed rules for representation, timing, error handling, and interpretation.
6. **Give the formula for transmission delay.**  
   Hint: number of bits divided by link rate.

### Likely long-answer questions

1. **Explain the characteristics, components, and data-flow modes of a communication system, with examples.**  
   Answer hint: explain each characteristic, draw a labelled sender–medium–receiver path, distinguish direction from simultaneity, and use radio, walkie-talkie, and telephone examples.
2. **Explain how network criteria are used to evaluate a communication system.**  
   Answer hint: define performance, reliability, security, cost, and scalability; explain how they can conflict; calculate a simple bandwidth/delay example.
3. **Compare a high-bandwidth satellite link with a lower-bandwidth short-distance link.**  
   Answer hint: discuss transmission delay, propagation delay, queueing, interactive traffic, and application requirements rather than declaring one universally faster.
4. **Describe the process of sending a file in a computer network.**  
   Answer hint: source, encoding, protocol headers, medium, receiver, error detection, acknowledgement, and destination; refer briefly to encapsulation.

### Short-answer revision checklist

You should be able to name the seven common components, draw all three flow directions, define the four common delay components, and explain why bandwidth, throughput, latency, and jitter are different.
