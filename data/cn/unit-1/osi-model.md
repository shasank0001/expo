---
subject: cn
unit: 1
topic: osi-model
syllabus_ref: CSM3103 Unit-I
status: draft
---
# Open Systems Interconnection (OSI) Model

## Overview

The **Open Systems Interconnection (OSI) model** is a seven-layer reference model proposed by the International Organization for Standardization. It is a vocabulary for describing communication between open systems. It is not a protocol and does not require a network to implement exactly seven software programs.

OSI separates communication into physical transmission, local link delivery, network delivery, end-to-end transport, dialogue control, data representation, and application services. This separation makes it possible to understand a failure, compare protocols, and design interoperable systems. TCP/IP is the practical suite used by the Internet, but many TCP/IP functions map naturally onto the OSI reference model.

The seven layers from bottom to top are:

1. **Physical layer**
2. **Data-link layer**
3. **Network layer**
4. **Transport layer**
5. **Session layer**
6. **Presentation layer**
7. **Application layer**

Mnemonics differ, but a useful top-down memory is **All People Seem To Need Data Processing**. The safest exam method is to learn the layer number, name, PDU, and examples together.

## Explanation

### 1. Physical layer (Layer 1)

The physical layer transmits raw bit signals over a medium. It defines or assists with:

- electrical, optical, or radio signalling;
- voltage, light intensity, and modulation;
- bit timing and synchronisation;
- connector, cable, and channel characteristics;
- transmission rate and physical link properties.

It does not understand an IP address or an HTTP request. A repeater, hub, transceiver, and physical medium are associated mainly with this layer. A damaged cable or no carrier signal is a Layer-1 problem.

The physical layer's service is to provide a stream of bits from one interface to another. Higher layers must agree on how those bits are grouped, so framing belongs to the next layer.

### 2. Data-link layer (Layer 2)

The data-link layer moves a **frame** between two directly connected nodes. It provides service over one physical link or a local broadcast domain. Its main tasks are:

- **framing:** identify the beginning and end of a frame;
- **physical addressing:** use source and destination MAC addresses on a local link;
- **medium access:** decide when stations may use a shared channel;
- **error detection:** usually add an FCS or checksum;
- **flow control:** in some protocols, prevent a fast sender overrunning a receiver;
- **link management:** detect link failure or negotiate parameters.

Ethernet, Wi-Fi, PPP, HDLC, and many other local-link protocols use this layer. A switch or bridge is primarily a Layer-2 forwarding device. A link-layer error is local: it can tell a sender that a particular frame on a particular link is damaged, but it does not automatically provide end-to-end delivery across the Internet.

Layer-2 addressing is often flat within a LAN. A switch learns which MAC address is reachable through a port by examining source addresses. Routers normally do not forward Ethernet broadcasts between separate IP networks.

### 3. Network layer (Layer 3)

The network layer delivers a **packet** from a source network to a destination network. It provides:

- logical network addresses, usually IP addresses;
- **routing:** choose a path or next hop;
- **forwarding:** send each packet according to a forwarding table;
- internetworking across different link technologies;
- fragmentation and reassembly where a protocol requires it;
- control messages such as ICMP for diagnostics.

A router operates mainly at this layer. It examines a destination prefix, chooses an outgoing interface and next hop, and changes the link-layer header for the next link. Network-layer protocols do not normally guarantee delivery or order. IPv4 and IPv6 are best-effort packet networks; higher layers may add reliability.

A common network-layer design issue is the maximum transmission unit (MTU). A packet that is too large for a link may need fragmentation, or the source must use a smaller packet. Fragmentation can add overhead and create reassembly problems, which is one reason modern protocols prefer path-MTU discovery or smaller source packets.

### 4. Transport layer (Layer 4)

The transport layer provides **process-to-process** or end-to-end communication across an internet. A host can have many applications, so an IP address alone is not enough. The transport layer adds a source and destination port.

Its services may include:

- **multiplexing/demultiplexing:** direct data to the right process;
- **segmentation and reassembly:** divide or rebuild application data;
- **connection management:** establish, maintain, and close state;
- **error control:** detect damaged, missing, or duplicate data;
- **flow control:** protect a receiver from excessive data;
- **congestion control:** protect shared networks;
- **reliable ordered delivery:** provided by TCP, but not by UDP.

TCP provides a reliable byte stream; UDP provides a connectionless datagram service. A transport protocol does not choose a physical route through the Internet. It relies on the network layer.

### 5. Session layer (Layer 5)

The session layer manages dialogues between applications. Its abstract tasks include establishing, maintaining, synchronising, and terminating sessions. It can coordinate checkpoints and recovery in a long exchange.

In practice, many Internet applications implement session-like functions in application protocols or libraries rather than a separate OSI session-layer protocol. For example, a file transfer can use request/response sequences, and a streaming protocol can resume after interruption. The OSI name is still useful for explaining what a layer is responsible for.

### 6. Presentation layer (Layer 6)

The presentation layer handles the representation and meaning of data as it moves between applications. It can provide:

- character encoding, such as ASCII, UTF-8, or EBCDIC;
- data-format conversion;
- serialisation and deserialisation;
- compression and decompression;
- encryption and decryption in some models.

In the Internet stack, many presentation functions are performed by application libraries or protocols. For example, TLS provides encryption above TCP, and a browser interprets HTML, images, and compressed data. A compressed HTTP response may be handled by the application and its libraries rather than a separate global presentation protocol.

### 7. Application layer (Layer 7)

The application layer provides network services directly useful to programs and users. It does not usually mean the operating system's user interface. HTTP, DNS, SMTP, IMAP, FTP, and SNMP are application-layer protocols.

The application defines the meaning of requests and responses. DNS asks for a name record, SMTP submits mail, and HTTP requests a web resource. These services use lower layers for addressing, delivery, and physical transmission.

### 8. Layer interaction and encapsulation

When an application sends data, each layer adds its own control information. For example:

`HTTP request -> TCP segment -> IP packet -> Ethernet frame -> bits`

At the receiver, the process is reversed. The physical layer supplies bits, the link layer checks and removes the frame fields, the network layer reads the IP header, the transport layer reads TCP or UDP fields, and the application receives its data.

Peer layers use protocols, but normal data moves down the sender's stack, across the medium, and up the receiver's stack. This is why a switch can understand MAC addresses without understanding HTTP, and why a router can forward IP without examining the application request.

### 9. Encapsulation example and scope

A frame's MAC addresses are relevant only on one local link. When a router forwards the packet, it removes the old link frame and encapsulates the IP packet in a new frame with addresses for the next link. The IP destination can remain unchanged, while the data-link addresses change. This distinction is essential for internetworking.

### 10. OSI and TCP/IP comparison

The OSI model is a detailed seven-layer reference. The common TCP/IP model is often drawn as four or five layers:

- application;
- transport;
- Internet;
- link or network access.

Some diagrams split the link into data-link and physical layers, producing a five-layer TCP/IP view. The exact number is a convention; the functions remain similar.

| OSI layer | Common TCP/IP function | Typical examples |
|---|---|---|
| Application | Application services | HTTP, DNS, SMTP, SNMP |
| Presentation | Representation/encoding/security | TLS, character conversion |
| Session | Dialogue/synchronisation | session APIs, application sequencing |
| Transport | Process delivery | TCP, UDP |
| Network | Addressing and routing | IPv4, IPv6, ICMP |
| Data link | Framing and local delivery | Ethernet, Wi-Fi, PPP |
| Physical | Signals and media | cables, fibre, radio |

The table is a mapping, not a claim that every application protocol has separate OSI layers.

## Worked examples

### Example 1: Trace an HTTPS request

1. The browser creates an HTTP request.
2. TLS (often represented at the presentation/security level) protects the application data.
3. TCP creates a connection and adds sequence, acknowledgement, and port fields.
4. IP adds source and destination addresses and routing information.
5. Ethernet adds MAC addresses and an FCS for the local link.
6. The physical layer sends the bits.
7. The server's layers remove and check the fields in reverse order.

### Example 2: Identify a fault by layer

A user cannot open a website. The Wi-Fi icon shows no association (physical/data link). If the laptop has a local address but no default route, check the network layer. If a TCP connection to port 443 fails while routing works, check the transport layer. If the connection works but DNS does not, check the application layer.

### Example 3: A switch and a router

A switch receives a frame and looks at the destination MAC address to choose a port. It operates at Layer 2. A router receives an IP packet, looks at the destination network prefix, and chooses a next-hop interface. It operates at Layer 3. A home device may perform both functions.

### Example 4: Frame across two links

A laptop sends a frame to a router over Ethernet. The router receives the IP packet and sends it over a fibre link in a new frame. The destination IP address is preserved for end-to-end routing, but the source and destination MAC addresses are local to each link.

## Key terms & formulas

- **OSI:** seven-layer Open Systems Interconnection reference model.
- **Layer:** a defined level of communication responsibility.
- **PDU:** protocol data unit.
- **Physical bit:** Layer-1 signal unit.
- **Frame:** Layer-2 PDU.
- **Packet/datagram:** Layer-3 PDU.
- **Segment:** TCP transport PDU; UDP datagram is also transport-level.
- **MAC address:** link-layer interface identifier.
- **IP address:** network-layer logical address.
- **Port number:** transport-layer endpoint number.
- **Encapsulation:** add layer-specific control information.
- **Decapsulation:** remove and process that information.
- **MTU:** maximum transmission unit, the largest data unit a link can carry.
- **Layer address change:** link addresses may change at a router; network addresses normally persist end-to-end.

## Common mistakes

1. **OSI is not a seven-layer protocol.** It is a reference model.
2. **Layer numbering is counted bottom-up.** Physical is 1 and application is 7.
3. **A router is not a data-link device.** It is primarily Layer 3; a bridge/switch is primarily Layer 2.
4. **A switch does not normally route IP packets.** It forwards frames using MAC addresses unless it also performs routing.
5. **The network layer does not guarantee delivery.** IP is normally best effort.
6. **The transport layer identifies processes, not routes.** Ports direct data; routers choose paths.
7. **The application layer is not the same as a user interface.** HTTP and DNS are examples of network application protocols.
8. **The presentation layer is not always implemented separately.** Its functions may be inside applications or libraries.
9. **A header is not an error-correction guarantee.** It contains control information whose meaning depends on the layer.
10. **A higher layer cannot normally skip the lower layers.** Data passes through the stack and a medium, even if some functions are implemented together.

## Exam prep

### Likely 2-mark questions

1. **List the seven OSI layers in order.**  
   Hint: physical, data-link, network, transport, session, presentation, application.
2. **State the function of the network layer.**  
   Hint: logical addressing, routing, forwarding, and internetworking.
3. **What is the role of the data-link layer?**  
   Hint: frames, MAC addresses, local delivery, medium access, and error detection.
4. **What is the difference between a frame and a packet?**  
   Hint: frame is Layer 2; packet/datagram is Layer 3.
5. **Give two functions of the transport layer.**  
   Hint: process addressing, multiplexing, reliability, flow/congestion control.
6. **Why is OSI called a reference model?**  
   Hint: it provides concepts and interfaces, not one mandatory implementation.

### Likely long-answer questions

1. **Explain all seven OSI layers with PDUs, functions, and examples.**  
   Answer hint: for each layer state number, job, addressing/control, and a protocol/device example.
2. **Compare OSI and TCP/IP models.**  
   Answer hint: OSI's seven layers versus common four/five-layer TCP/IP view, plus mapping of functions and protocols.
3. **Trace a message from an application to a receiver using encapsulation.**  
   Answer hint: show HTTP/TCP/IP/Ethernet/physical steps and reverse decapsulation.
4. **Use a network fault to identify the relevant OSI layer.**  
   Answer hint: map no link, bad frame, no route, port failure, and application error to layers.

### Short-answer revision checklist

For every layer, be able to answer: what is its number, what is its PDU, what address does it use, what is its main job, and give one example.
