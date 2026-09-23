---
subject: cn
unit: 1
topic: layered-network-model
syllabus_ref: CSM3103 Unit-I
status: draft
---
# Layered Network Model

## Overview

A **layered network model** divides communication into levels, each responsible for a smaller, well-defined job. Each layer receives a service from the layer below and provides a service to the layer above. This abstraction makes a large communication system understandable and allows different vendors to implement the same service independently.

The model is a design idea, not a single physical device or protocol. It explains how protocols cooperate, how data is encapsulated, and how a problem can be localised. A browser request uses an application protocol, transport protocol, Internet protocol, link protocol, and physical medium, but each layer only needs to understand its own interface and the service it provides.

The syllabus asks for the network model, layered tasks, interfaces, and encapsulation/decapsulation. These ideas are the foundation for comparing OSI and TCP/IP later in the unit.

## Explanation

### 1. Why use layers?

Communication involves many unrelated problems: representing characters, detecting errors, addressing devices, selecting a route, sharing a medium, and sending electrical or optical signals. A single monolithic protocol would be difficult to understand, maintain, and replace. Layering separates concerns and gives each layer a clear contract.

Benefits include:

- **Modularity:** a layer can be specified independently.
- **Replaceability:** an implementation can change without forcing every higher layer to change.
- **Interoperability:** a standard interface lets different systems communicate.
- **Troubleshooting:** a failure can be assigned to a likely layer.
- **Reuse:** generic functions such as framing or routing can support many applications.
- **Teaching and design:** engineers can reason about one job at a time.

The model does not mean that each layer is implemented by one program. A modern operating system may implement many functions in one kernel, and a hardware device may combine several functions. Layering is primarily conceptual and architectural.

### 2. Layers, peers, and interfaces

A layer on a sending host and the corresponding layer on a receiving host are called **peer layers**. They do not normally communicate directly. The sender's layer passes data to the layer below, which passes it over the physical medium; the receiving side passes it upward in the reverse order.

An **interface** or **service access point** is the boundary through which one layer uses the service of the layer below. For example, the transport layer uses the network layer's service to send a packet to a destination. The interface defines what inputs are accepted, what outputs are produced, and how errors or status are reported.

At each host, a layer normally:

1. receives a request from the layer above;
2. adds its own control information;
3. invokes the service of the layer below;
4. handles events or errors reported by that layer;
5. delivers a service response upward.

The peer on the other host interprets the control information according to the protocol used between the peers.

### 3. Encapsulation

**Encapsulation** is the process of adding protocol control information as data moves down the layers. The application payload becomes a message, the transport layer may add a header and trailer, the network layer adds an IP header, the data-link layer adds a frame header and FCS, and the physical layer encodes the result as bits.

A simplified view is:

`application data -> transport segment -> IP packet -> Ethernet frame -> physical bits`

At the receiving host:

`physical bits -> Ethernet frame -> IP packet -> transport segment -> application data`

This is often called the **encapsulation/decapsulation process**. The payload may be unchanged while the surrounding control information changes at every layer.

The headers are not redundant. A MAC address is meaningful on a local link; an IP address remains meaningful across networks; a port identifies a process; sequence and acknowledgement fields support reliability; an FCS checks one local frame. Layers therefore add different information for different scopes.

### 4. Decapsulation and delivery

The receiving physical layer detects a signal and passes a bit stream to the data-link layer. The data-link layer checks the frame boundary and error-detection field, removes the link header/trailer when appropriate, and passes the network packet upward. Each higher layer verifies its own information and removes it before giving the payload to the layer above.

If a checksum fails, the receiving layer may discard the item or ask for retransmission according to its protocol. It should not normally pass corrupted control information upward as if it were valid. An end-to-end protocol may recover the loss later.

### 5. Layered tasks in general

A common set of tasks is:

- **Physical transmission:** send and receive raw signals.
- **Framing and link access:** identify frame boundaries and share the medium.
- **Addressing and routing:** identify networks and choose a path.
- **End-to-end transport:** deliver data between processes, optionally with reliability and flow control.
- **Session management:** establish, maintain, and synchronise dialogues.
- **Presentation/data representation:** translate formats, encode, and optionally encrypt.
- **Application services:** provide network functions to user programs.

These tasks are not fixed to exactly four, five, or seven layers. The OSI reference model and the TCP/IP model organise them differently, but the same functions can be found in both.

### 6. Services and protocols

A **service** is what a layer offers. A **protocol** is the set of rules used between peer layers to provide that service. A layer may offer several services, such as reliable or best-effort delivery, and may use protocols that are independent of the upper layer's protocol.

This distinction explains why the application does not need to know whether the network uses copper or fibre, and why a DNS client can work over UDP in one implementation and another transport path in another.

### 7. Layered troubleshooting

When a service fails, identify the layer first:

- No signal or link down: physical layer.
- Corrupted frames, wrong MAC delivery, or local collision: data-link layer.
- No route, unreachable network, or TTL expired: network layer.
- Port refusal, retransmission timeout, or ordered reliable stream issue: transport layer.
- Name resolution, HTTP, DNS, or mail error with lower layers working: application layer.

A useful diagnostic moves from the lowest layer upward because an upper-layer failure often has a lower-layer cause. For example, a browser error is not investigated only in HTTP if the interface has no link or if no route exists.

### 8. Layered design and the end-to-end principle

The **end-to-end principle** says a function should be implemented at an endpoint when it is needed only for a particular communication, rather than lower layers doing work for every packet. Reliability may be provided by TCP at the endpoints, while the IP network only forwards best-effort packets. Link-layer reliability may still be useful for a local noisy link, but it is not a substitute for end-to-end delivery.

## Worked examples

### Example 1: Encapsulation of an HTTP request

Assume the request data is 1,000 bytes:

1. The application hands 1,000 bytes to TCP.
2. TCP adds a TCP header, and later a segment contains TCP control fields plus data.
3. IP adds the source/destination IP header.
4. Ethernet adds the source/destination MAC addresses and FCS.
5. The physical layer transmits the frame as electrical, optical, or radio signals.

At the server, the operations are reversed. The Ethernet layer checks the frame, the IP layer checks the destination and TTL, TCP verifies its sequence information, and HTTP receives the request.

### Example 2: A local hub and a routed Internet path

A frame travels from a laptop to a home switch, then to a home router. The Ethernet header is meaningful on each local link and may change at a router. The IP destination often stays the same through the Internet, while the link-layer addresses change. This shows why layers have different scopes.

### Example 3: Locate a fault

A web page fails to load. First check the physical link. If the link is up, check the address and default gateway at the network layer, then test port 443 and the TCP connection at the transport layer, and finally inspect DNS/HTTP at the application layer. Layering turns a broad failure into a sequence of tests.

### Example 4: Compare services

A transport layer may offer reliable ordered delivery to an application that downloads a file, or a low-overhead connectionless service to a real-time application. Both are transport services; the protocols and application requirements differ.

## Key terms & formulas

- **Layer:** a level with a defined responsibility.
- **Peer layer:** corresponding layer at the other endpoint.
- **Interface:** boundary for using a lower-layer service.
- **Service:** functionality offered to the layer above.
- **Protocol:** rules exchanged by peer entities.
- **Encapsulation:** adding headers/trailers while moving down.
- **Decapsulation:** removing headers/trailers while moving up.
- **PDU:** protocol data unit; generic name for data at a layer.
- **Frame:** data-link-layer PDU.
- **Packet/datagram:** network-layer PDU.
- **Segment:** transport-layer TCP PDU; UDP uses a datagram.
- **Bit:** physical-layer symbol in the conceptual model.
- **Layering rule:** each layer serves the layer above and uses the layer below.
- **Troubleshooting order:** physical -> link -> network -> transport -> application.

## Common mistakes

1. **A layered model is not a protocol stack.** It is a reference architecture; protocols implement its functions.
2. **Peer layers do not normally talk directly.** They exchange through adjacent layers and the communication medium.
3. **Encapsulation does not encrypt data.** It adds control fields.
4. **Decapsulation is not the same as decoding at the application layer.** It removes layer-specific control information.
5. **Every layer does not add a header.** Some may add a trailer, perform a service, or use an existing field; the general process is control encapsulation.
6. **A layer number is not a universal protocol version.** OSI and TCP/IP use different layer arrangements.
7. **Higher-layer success does not prove the physical link is healthy.** Test layers independently.
8. **Layering does not eliminate complexity.** It contains complexity and makes ownership clearer.
9. **The application layer does not directly transmit bits.** It uses the services below it.
10. **A service is not the same as its implementation.** One service can have several protocol implementations.

## Exam prep

### Likely 2-mark questions

1. **What is a layered network model?**  
   Hint: divide communication into levels, each with one responsibility.
2. **Define interface and encapsulation.**  
   Hint: boundary for a lower-layer service; adding control information on the way down.
3. **Why do we use layering?**  
   Hint: modularity, replaceability, interoperability, and easier troubleshooting.
4. **What is a peer layer?**  
   Hint: the corresponding layer at the other communicating system.
5. **Give two advantages of a layered architecture.**  
   Hint: change one layer independently; locate faults by layer.

### Likely long-answer questions

1. **Explain the layered architecture of a network with a sender-to-receiver diagram.**  
   Answer hint: show application, transport, network, link, and physical layers; describe services, peer communication, interfaces, and upward/downward movement.
2. **Explain encapsulation and decapsulation with an HTTP request.**  
   Answer hint: add application payload, TCP, IP, link, and physical information; then remove and check them in reverse order.
3. **How does layering help troubleshoot a network?**  
   Answer hint: map symptoms to layers and test from physical upward.
4. **Differentiate a service from a protocol.**  
   Answer hint: service is the offered function; protocol is the peer-to-peer rule set implementing it.

### Short-answer revision checklist

Draw a sender and receiver with peer layers, mark one interface, and show how a payload gains and loses headers. Be able to name the broad task associated with each OSI layer even before memorising its number.
