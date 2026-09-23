---
subject: cn
unit: 1
topic: arpanet-and-tcpip-evolution
syllabus_ref: CSM3103 Unit-I
status: draft
---
# ARPANET and the Evolution to TCP/IP

## Overview

ARPANET was an early packet-switching network that connected computers at research institutions. It helped demonstrate that many independent computers could communicate by dividing messages into packets and forwarding them through intermediate nodes. It was an important predecessor of the Internet, but ARPANET itself is not today's Internet.

The historical path to the Internet involved packet switching, host interconnection, protocol standardisation, local and wide-area networks, and the TCP/IP suite. The important lesson for current study is architectural: networks are built from networks, and open, layered protocols let independently built networks interoperate.

The syllabus asks for ARPANET, the network model, and the evolution to TCP/IP. This file connects the historical design choices to packet switching, internetworking, addressing, and the Internet's best-effort design.

## Explanation

### 1. Why packet switching appeared

Early communication systems often reserved a dedicated circuit for each conversation. If two users needed a channel, other users could not use its capacity while it was idle. Long-distance lines were expensive, and a failure could make the whole reserved connection unavailable.

Packet switching changed the model. A message is divided into small **packets**. Each packet contains a header with source, destination, and control information, plus a payload. Packets from different conversations can share a link, taking turns or being scheduled statistically. A router stores a packet briefly, examines its destination, and forwards it over the next link.

Benefits included:

- better sharing of expensive links;
- no need to reserve a fixed circuit for a short burst;
- routes could be changed when a link failed;
- one failed conversation need not stop other conversations;
- packet headers could carry addressing and control information.

Packet switching introduces new problems. Packets may be delayed in queues, lost when queues fill, duplicated, or delivered out of order. Different packets may follow different routes. Congestion control and reliability therefore became central networking topics.

### 2. ARPANET

ARPANET began in the late 1960s as a research packet-switched network. It connected computers such as UCLA, UCSB, the University of Utah, and SRI, among others. It was designed to allow resource sharing and remote collaboration. The exact dates and milestones are less important for exams than the ideas: packet switching, store-and-forward forwarding, host interconnection, and a growing community of protocols.

In a store-and-forward network, a node receives a complete packet, checks it, and then forwards it. The receiving node may be temporarily disconnected; the packet can wait until a route or link is available. This is different from a circuit that must remain continuously open.

ARPANET experiments influenced the Internet, but it should not be described as a direct, unchanged copy of today's Internet. Later packet-switched networks, Ethernet, satellite links, and academic networks were interconnected. The term **Internet** means an interconnection of independent networks.

### 3. From one network to an Internet

When two networks use different link technologies, they still need a common way to carry packets across one another. Internetworking solves this by using a common network-layer protocol and addressing system. IP provides a packet format, logical addresses, and a forwarding method that can cross many heterogeneous links.

A **router** connects networks and chooses the next link. It does not need the two networks to use the same physical medium. Ethernet frames, radio links, and optical links can all carry IP packets if the lower layers provide a usable service.

The Internet has no single owner or central computer that controls every route. Its networks are administered by many organisations, connected by agreements and standard protocols. This distributed structure contributed to its growth, although it also made routing, security, and management difficult.

### 4. Role of TCP/IP

TCP/IP is a family of protocols that became the common language of the Internet. IP provides best-effort delivery of packets across networks. TCP can provide reliable, ordered, congestion-controlled byte streams when an application needs them. Other protocols provide names, mail, web pages, and management functions.

The suite became important because it was:

- **open and specified:** independent implementations could interoperate;
- **layered:** each protocol used a clear service from the layer below;
- **connectionless at IP:** routers did not need to maintain a connection for every packet;
- **robust:** packets could follow alternate routes;
- **flexible:** the same network layer could carry different application traffic.

TCP/IP was not the only networking technology of its time, but its adoption and the growth of the Internet made it the dominant suite. Ethernet, which originally used a different local network model, also became closely integrated with IP.

### 5. Addressing and naming

Early networks needed a way to identify a host. Logical addresses were later layered with a network prefix and host portion, so a router could locate a destination network before the destination host. Ports at the transport layer identified processes, while names such as domain names allowed people to use memorable labels.

This separation of address levels is fundamental:

- a **MAC address** identifies an interface on a local link;
- an **IP address** identifies an interface for network-layer routing;
- a **port** identifies a transport endpoint or process;
- a **domain name** identifies a service or host in a human-readable namespace.

The Internet scales because addressing is hierarchical and routing is distributed. A router need not know every host in the world; it needs a route toward a destination prefix.

### 6. Historical lessons relevant to today's networks

The ARPANET-to-Internet history teaches several exam points:

1. **Standardisation enables interoperability.** A protocol must be specified, implemented by different vendors, and widely adopted.
2. **Layering reduces coupling.** A change in one layer can be isolated from another if interfaces remain stable.
3. **Packet switching improves sharing** but creates queueing, loss, ordering, and congestion issues.
4. **Internetworking needs a common network layer** even when links are different.
5. **Distributed control increases scalability** but makes failure diagnosis more difficult.
6. **Best-effort delivery is a deliberate simplification.** Reliability is added where applications need it, often at endpoints.
7. **The Internet is an interconnection of networks,** not one enormous centrally managed LAN.

## Worked examples

### Example 1: A packet crossing different media

A laptop sends an IP packet over Ethernet to a home router. The router sends the packet over a wireless link to an ISP, and the ISP may use fibre. The IP destination can remain the same, but the Ethernet source and destination addresses and the physical encoding change on each link. This is internetworking.

### Example 2: Shared link

Suppose a fibre link is idle half the time. With circuit switching, the idle capacity is reserved and cannot be used by another conversation. With packet switching, a second host can send packets during the idle interval. Both hosts share capacity statistically.

### Example 3: Alternate route

If a router link fails, a packet may be dropped or rerouted depending on the protocol and routing information. IP itself does not guarantee rerouting; routing protocols and router tables determine available paths. The historical packet-switching idea made alternate paths possible, but recovery is not automatic in every failure.

### Example 4: Name to address

A user requests `www.example.org`. DNS obtains an IP address, and the transport layer uses a port such as 443. The packet is forwarded through routers based on the IP prefix. The browser uses TLS over TCP as appropriate. One human-readable request involves several naming, addressing, and transport concepts.

## Key terms & formulas

- **ARPANET:** early packet-switched research network.
- **Packet:** a bounded portion of a message with a header and payload.
- **Store and forward:** receive a complete unit, store/check it, then send it onward.
- **Internetworking:** connecting different networks into one larger network.
- **Internet:** the global interconnection of many networks.
- **Router:** layer-3 device that forwards packets between networks.
- **TCP/IP:** the Internet protocol suite.
- **IP:** connectionless, best-effort network-layer delivery.
- **MAC address:** local link-layer interface identifier.
- **IP address:** hierarchical logical address used for network delivery.
- **Port:** transport-layer process endpoint number.
- **Internet draft/standard:** an agreed specification used by interoperable implementations.
- **Packet forwarding time:** approximately `packet size / link rate + propagation and queueing delays`.
- **Bandwidth-delay product:** `R x RTT`; it indicates how much data can be in flight to keep a path busy.

## Common mistakes

1. **ARPANET is not the Internet.** It was an important predecessor and experimental network.
2. **Packet switching is not circuit switching.** Packets share links and are forwarded independently; a reserved circuit remains dedicated.
3. **Internetworking is not merely connecting cables.** It requires common addressing, routing, and protocol conventions.
4. **IP does not guarantee packet delivery or order.** It is best effort.
5. **The Internet is not one central network.** It is a network of networks administered by many entities.
6. **TCP/IP is not a single protocol.** It is a suite containing IP, TCP, UDP, ICMP, and many application protocols.
7. **MAC and IP addresses serve different scopes.** A MAC address is not a global replacement for an IP address.
8. **Store and forward is not a guarantee of delivery.** It allows temporary storage while a route or destination is unavailable.
9. **Open standards help interoperability but do not guarantee perfect security.** Protocols can be implemented correctly and still be attacked.
10. **Packet switching does not eliminate congestion.** It improves sharing and makes congestion management necessary.

## Exam prep

### Likely 2-mark questions

1. **What is ARPANET and why is it important?**  
   Hint: early packet-switched network that helped lead to Internet technologies.
2. **Define packet switching and give two benefits.**  
   Hint: divide messages into packets and share links; mention efficiency and alternate routes.
3. **What is internetworking?**  
   Hint: connecting different networks using a common network-layer service and addressing.
4. **State two reasons packet switching replaced dedicated circuits in many networks.**  
   Hint: statistical sharing and flexible routing/failure recovery.
5. **Why did TCP/IP become the Internet suite?**  
   Hint: open standards, layering, interoperability, and robust best-effort networking.

### Likely long-answer questions

1. **Trace the evolution from ARPANET to the Internet.**  
   Answer hint: packet switching, store-and-forward nodes, network interconnection, protocol standards, TCP/IP adoption, and distributed control.
2. **Compare packet switching and circuit switching.**  
   Answer hint: dedicated reservation versus shared packets; setup, efficiency, delay, failure behaviour, and examples.
3. **Explain how the Internet can use Ethernet, radio, and fibre links together.**  
   Answer hint: common IP network layer, routers, logical addressing, and local link-layer differences.
4. **Explain the historical significance of open standards and layering.**  
   Answer hint: independent implementations, common interfaces, reduced coupling, and growth.

### Short-answer revision checklist

Be ready to define ARPANET, packet, store-and-forward, internetworking, Internet, and TCP/IP, and give one historical lesson for each modern networking concept.
