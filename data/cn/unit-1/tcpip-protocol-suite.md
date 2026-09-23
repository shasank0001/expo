---
subject: cn
unit: 1
topic: tcpip-protocol-suite
syllabus_ref: CSM3103 Unit-I
status: draft
---
# TCP/IP Protocol Suite

## Overview

The **TCP/IP protocol suite** is the family of protocols that provides the common communication services of the Internet. TCP/IP is not one protocol: IP is the central network-layer protocol, TCP and UDP are transport protocols, ICMP carries network control messages, and applications such as HTTP, DNS, SMTP, and SNMP use the suite.

The suite is usually represented as four layers—application, transport, Internet, and link—or as five layers when the link is split into data-link and physical layers. Its practical success comes from open standards, layering, packet switching, logical addressing, and independent implementation by many vendors.

The syllabus includes the TCP/IP suite and addressing. This file explains the layers, encapsulation, IPv4/IPv6, transport choices, and how an Internet packet is addressed and forwarded. More detail on IP addressing appears in Unit III and on TCP/UDP in Unit IV.

## Explanation

### 1. What TCP/IP means

**IP** (Internet Protocol) provides a connectionless, best-effort packet service. It defines the network-layer packet, the logical address, and forwarding fields. It does not establish a connection, guarantee delivery, or guarantee order.

**TCP** (Transmission Control Protocol) provides a reliable, connection-oriented byte stream above IP. It uses sequence numbers, acknowledgements, retransmission, flow control, and congestion control.

**UDP** (User Datagram Protocol) provides a connectionless transport service with a small header and no built-in delivery guarantee.

The name TCP/IP is historical. It is often used to mean the Internet architecture even when a communication uses UDP rather than TCP.

### 2. Common layers

#### Application layer

The application layer provides services directly to applications and users. Examples include:

- **HTTP/HTTPS:** web resources;
- **DNS:** name-to-address and other records;
- **SMTP:** mail submission and transfer;
- **IMAP/POP3:** mail retrieval;
- **SNMP:** network management;
- **FTP/SSH:** file transfer or remote access.

An application protocol defines the syntax and semantics of requests, responses, names, or management objects.

#### Transport layer

The transport layer delivers data between processes. It uses a source and destination port to direct traffic after IP has reached a host. TCP provides a reliable ordered byte stream; UDP provides a connectionless datagram service. Transport protocols also perform segmentation and multiplexing, and TCP adds flow and congestion control.

#### Internet layer

The Internet layer is the common core of the Internet. It includes:

- **IPv4:** 32-bit logical addresses and best-effort packets;
- **IPv6:** 128-bit logical addresses and an updated packet format;
- **ICMP/ICMPv6:** errors and diagnostics;
- **IP routing and forwarding:** routers use destination prefixes to choose a next hop;
- **ARP** and neighbour discovery as link-support mechanisms, depending on the address family and layer model.

IP hides most differences between the physical links underneath it. An IP packet can cross Ethernet, Wi-Fi, fibre, and other technologies as long as each link can carry it.

#### Link or network-access layer

The link layer covers local delivery and the physical medium. In a four-layer drawing, it includes the data-link and physical functions. In a five-layer drawing:

- the **data-link layer** creates frames, uses local addresses, and controls medium access;
- the **physical layer** sends and receives signals.

The link-layer frame is normally changed at each routed hop because its MAC addresses are meaningful only on the current local link.

### 3. Addressing in the TCP/IP model

The suite uses several address types.

#### Physical and data-link addresses

A MAC address identifies a network interface on a local link. A switch learns source MAC addresses to associate interfaces with ports. A MAC address is not normally routed across the Internet.

#### IP addresses

An IPv4 address is 32 bits, commonly written as four decimal octets such as `192.168.1.10`. An IPv6 address is 128 bits, written as eight hexadecimal groups such as `2001:db8::1`.

An IP address has a **network prefix** and a **host/interface part**. The prefix length, such as `/24` or `/64`, tells routers how many leading bits identify the network. A subnet mask or prefix length is needed to distinguish local delivery from forwarding to another network.

IP addresses identify interfaces in a forwarding sense, not simply applications. A host can have several addresses on several interfaces. Routers use the destination prefix to find the next hop; the destination host ultimately delivers to the appropriate local interface.

#### Port numbers

A 16-bit transport port identifies an application endpoint. Well-known examples include DNS 53, SMTP 25, HTTP 80, and HTTPS 443. A socket or connection is normally identified by the address family, protocol, local address/port, and peer address/port.

#### Domain names

DNS gives people memorable names such as `www.example.org`, which are resolved to IP addresses and other records. DNS is an application-layer service, but its result is used by the network and transport layers.

### 4. Encapsulation and delivery

At the sender, a message is wrapped as it moves downward:

1. The application supplies data.
2. TCP or UDP adds a transport header.
3. IP adds an IP header and chooses a route.
4. The link layer adds a frame header and FCS.
5. The physical layer sends bits.

At the receiver, the layers remove and process the fields in reverse order. A router normally removes one frame, examines the IP packet, and creates a new frame for the next link. It does not normally deliver the packet to the transport layer until it reaches the destination host.

### 5. Connectionless Internet and reliable transport

IP is deliberately simple and does not maintain per-packet connection state in routers. This allows routers to forward packets quickly and lets traffic use many paths. The trade-offs are possible loss, duplication, reordering, delay, and variable routes.

TCP chooses to provide reliability at the endpoints. It establishes a connection, numbers bytes, acknowledges them, retransmits missing data, and adapts the sending rate. This is an example of the end-to-end principle: not every router needs to understand application reliability.

UDP is useful when the application can handle loss or when a late retransmission is worse than a missing datagram. Real-time voice, interactive games, and some monitoring requests commonly use UDP.

### 6. Protocol independence and interoperability

The suite is designed so that multiple applications can use the same Internet and link services. A web page may use TCP, a DNS query may use UDP, and an email submission may use TCP. All can be carried over IP. The application and transport choices are independent enough to support many services.

The Internet's open standards allow equipment and software from different organisations to interoperate. IPv4, IPv6, TCP, UDP, and ICMP have specified formats and behaviour, including rules for addressing, forwarding, reliability, and error reporting.

### 7. How IP forwarding works conceptually

A router receives a packet and performs a forwarding-table lookup based on the destination prefix. The table is populated by direct routes, static configuration, and routing protocols. The selected entry gives a next hop and outgoing interface. The packet is then encapsulated in a new link-layer frame and sent.

Routing is the process of learning paths; forwarding is the per-packet action. A route may be stale, and a packet may be dropped if no route exists. ICMP can report problems such as destination unreachable or time exceeded.

### 8. IPv4 and IPv6 comparison

IPv4 uses 32-bit addresses and has been the dominant Internet version for decades. IPv6 uses 128-bit addresses, has a simpler fixed base header, supports extension headers, and includes improved neighbour discovery and auto-configuration features. IPv6 is not automatically faster on every connection; its main advantages are address space, routing efficiency, and support for future extensions and mobility.

A dual-stack host can use both versions. Tunnelling and translation help during migration, but the complete transition methods are covered in Unit III.

### 9. Application and management protocols

DNS, HTTP, SMTP, IMAP, and SNMP use the application layer. They may use TCP, UDP, TLS, and other services below. For example, a DNS client may ask over UDP to port 53; if the response is truncated, it may retry over TCP. SMTP uses TCP for submission and relay. SNMP commonly uses UDP for requests and notifications.

This arrangement illustrates the suite's modularity: a new application protocol can be added without redesigning IP.

## Worked examples

### Example 1: A web request

A browser needs `www.example.org`. DNS resolves the name to an IP address. The browser opens a TCP connection to the server port, sends an HTTPS request, and receives data. IP forwards each packet across routers; Ethernet and Wi-Fi carry it over local links. The application sees a completed web resource, not the lower-layer details.

### Example 2: IP address and port

Two servers on the same host can use the same IP address but different ports. A packet to `192.0.2.10:443` belongs to a web service, while a packet to `192.0.2.10:53` belongs to a DNS server. The IP address identifies the interface; the port identifies the endpoint.

### Example 3: Router change of frame

A packet has IP destination `198.51.100.9`. On the first Ethernet link, the frame uses the laptop's and router's MAC addresses. The router forwards the packet through a fibre link and creates a new frame using the router's new interface and the next-hop device's addresses. The IP destination remains the end host's address.

### Example 4: Best-effort failure

If a router's queue is full, it may drop a packet. IP does not automatically resend it. TCP may notice a missing sequence range and retransmit; UDP applications may accept the loss. This is why the choice of transport protocol affects reliability and delay.

## Key terms & formulas

- **TCP/IP:** Internet protocol suite.
- **Application layer:** DNS, HTTP, SMTP, SNMP, and similar services.
- **Transport layer:** TCP and UDP.
- **Internet layer:** IPv4, IPv6, ICMP.
- **Link layer:** local frames, MAC addresses, and medium access.
- **IP address:** network-layer logical interface address.
- **Port:** 16-bit transport endpoint number, 0–65535.
- **Best effort:** delivery attempt without delivery/order/latency guarantee.
- **Encapsulation:** add headers as data moves down the stack.
- **Forwarding:** use a table to choose the outgoing interface for one packet.
- **Routing:** learn or calculate paths.
- **MTU:** maximum packet payload/frame size supported by a link.
- **Addressing relation:** `IP address = network prefix + interface/host part`.
- **Port example:** DNS 53, SMTP 25, HTTP 80, HTTPS 443.
- **Header example:** `Ethernet frame = header + IP packet + FCS` (conceptually).

## Common mistakes

1. **TCP/IP is not a single protocol.** IP, TCP, UDP, ICMP, and application protocols are distinct.
2. **IP is not reliable.** It is best effort and may lose, duplicate, or reorder packets.
3. **TCP reliability does not make IP reliable.** TCP recovers at endpoints using retransmission.
4. **A MAC address is not the same as an IP address.** MAC addresses are local; IP addresses support routed delivery.
5. **The four-layer and five-layer TCP/IP drawings are both common.** The difference is mainly whether the link layer is split.
6. **A port is not an IP address.** A port identifies a process endpoint within a host/address family.
7. **Addressing is not only the first octet.** The prefix length determines the network/host boundary.
8. **An IP address identifies an interface, not necessarily one application.** Several services can share an address with different ports.
9. **Routing and forwarding are different.** Routing builds or distributes paths; forwarding acts on a packet.
10. **DNS is not IP.** DNS is an application service that supplies names and records; IP forwards the resulting packets.
11. **IPv6 is not just IPv4 with more decimal digits.** It has a 128-bit format and a different base header and neighbour-discovery design.

## Exam prep

### Likely 2-mark questions

1. **List the four commonly used TCP/IP layers and one protocol in each relevant layer.**  
   Hint: application, transport, Internet, link; DNS/HTTP, TCP/UDP, IP/ICMP, Ethernet/Wi-Fi.
2. **Why is IP called best effort?**  
   Hint: no guarantee of delivery, order, delay, or retransmission.
3. **Distinguish an IP address from a port number.**  
   Hint: interface/network location versus process endpoint.
4. **State two functions of the Internet layer.**  
   Hint: addressing, forwarding, routing, internetworking, diagnostics.
5. **What is encapsulation in TCP/IP?**  
   Hint: adding transport/IP/link control information while moving down the sender's stack.
6. **Give two benefits of using an open protocol suite.**  
   Hint: interoperability, replaceability, multi-vendor support, and independent networks.

### Likely long-answer questions

1. **Explain the TCP/IP suite layer by layer with examples and PDUs.**  
   Answer hint: application messages, TCP/UDP segments or datagrams, IP packets, link frames, physical bits.
2. **Trace a packet from a laptop to a remote server.**  
   Answer hint: application, transport, IP, local link, routers, link changes, and reverse decapsulation.
3. **Compare IP and TCP responsibilities.**  
   Answer hint: IP moves packets between networks; TCP adds an end-to-end reliable byte stream.
4. **Explain the role of addressing in TCP/IP.**  
   Hint: MAC, IP, port, and DNS levels; prefix and scope; examples of how a destination is selected.
5. **Explain why the Internet uses a best-effort network layer and endpoint reliability.**  
   Answer hint: scalability, heterogeneous links, router simplicity, and TCP's end-to-end recovery.

### Short-answer revision checklist

Be able to draw the four/five TCP/IP layers, name at least two protocols per layer, distinguish IP/TCP/UDP, and explain which addresses are local, routed, process-specific, or human-readable.
