---
subject: cn
unit: 3
topic: internet-network-layer
syllabus_ref: CSM3103 Unit-III
status: draft
---
# Network Layer in the Internet

## Overview

The Internet's principal network-layer protocol is the **Internet Protocol (IP)**. IP provides a best-effort packet service: it attempts to deliver each packet across interconnected networks but does not promise that the packet will arrive, arrive once, arrive in order, or arrive within a time limit.

This design made the Internet scalable and easy to interconnect. Routers forward packets using logical addresses and local tables instead of maintaining a connection for every flow. Applications that need reliability, ordering, or congestion protection use higher-layer protocols such as TCP. IPv4 and IPv6 are the two principal IP versions.

The syllabus also names ICMP, routing, and network-layer Internet services. This file explains the IP service, addresses, packet forwarding, TTL, fragmentation, best-effort properties, ICMP, routing, and the relationship to higher layers.

## Explanation

### 1. Internet network-layer service

The network layer offers a **connectionless, best-effort** service. A sender passes a packet with a destination address to IP. IP and routers try to move the packet toward the destination, but they do not reserve resources, confirm receipt, or guarantee order.

The service model deliberately keeps routers relatively simple:

- no per-packet state for a conversation;
- no guarantee of a fixed path;
- no guarantee of bandwidth;
- no automatic retransmission;
- no guarantee that a packet survives a failure.

A packet may be lost in a queue, delayed, duplicated, or delivered after a later packet. A later packet may take a different route after a topology change. These are acceptable at the IP layer because end-to-end protocols can decide which errors matter for an application.

### 2. IPv4 and IPv6

IPv4 uses 32-bit addresses and a header with fields for source, destination, protocol, TTL, and other control information. IPv6 uses 128-bit addresses, a fixed 40-byte base header, a Hop Limit, flow-label support, and extension headers for optional functions.

Both versions are connectionless and best effort at the network layer. They differ in address space, header design, fragmentation, neighbour discovery, and configuration. A network may operate one or both versions.

### 3. IP packet and encapsulation

An IP packet is encapsulated in a link-layer frame at the sender. It contains a network-layer header and payload. The header includes:

- version;
- header length or fixed-header indication;
- total length or payload length;
- identification and fragmentation fields in IPv4;
- time-to-live or hop limit;
- protocol or next-header value;
- header checksum in IPv4;
- source and destination IP addresses.

The payload may be a TCP segment, UDP datagram, ICMP message, or another network-layer protocol. A link-layer frame surrounds the IP packet with local addresses and an FCS. The frame is not the IP packet.

### 4. Forwarding through routers

A router receives a frame, verifies it, removes the link header, and examines the IP destination prefix. It looks up the most-specific route in its forwarding table, selects an outgoing interface and next hop, decrements the TTL/Hop Limit, and encapsulates the packet in a new frame.

The IP destination normally remains unchanged across ordinary routed hops. Link-layer source and destination addresses change because each link has its own local addressing. If a route points directly to a connected network, the router uses an ARP or neighbour-discovery exchange as appropriate.

Routers do not normally examine the application payload. They can apply policies based on prefix, address, flow classification, or QoS metadata without being an application gateway.

### 5. TTL and Hop Limit

TTL in IPv4 and Hop Limit in IPv6 protect the network from packets circulating through routing loops. Each router decrements the field before forwarding. At zero, the packet must be discarded. An ICMP or ICMPv6 Time Exceeded message may be sent, subject to rate limiting and security policy.

TTL also affects multicast scope and can be used for administrative tools such as traceroute. It is a lifetime bound, not a route-repair mechanism. A router that decrements it does not know why the packet is looping or automatically remove the faulty route.

### 6. Fragmentation and path MTU

Different links have different MTUs. An IPv4 router can fragment a packet that is too large for the next link, adding fragment headers and requiring the destination to reassemble fragments. If one fragment is lost, the whole packet may be unusable. Fragmentation is therefore avoided when possible.

IPv6 routers do not fragment ordinary packets. If a packet is too large, the router sends an ICMPv6 Packet Too Big message. The source reduces its packet size and uses Path MTU Discovery. This reduces router processing and makes fragmentation a source responsibility.

### 7. ICMP and ICMPv6

The **Internet Control Message Protocol (ICMP)** carries network-layer control and error information. Common IPv4 messages include:

- destination unreachable;
- time exceeded;
- parameter problem;
- echo request/reply used by ping.

ICMPv6 adds neighbour discovery, router discovery, path-MTU information, and other functions required by IPv6. ICMP does not provide general reliable delivery; it reports selected conditions.

Error messages should be rate-limited and validated. A forged ICMP message can cause a host to make a wrong route or state decision, and a flood of errors can consume resources.

### 8. Routing in the Internet

Routing protocols learn reachability and construct paths. Interior gateway protocols such as OSPF and IS-IS operate within an administrative domain. Border Gateway Protocol (BGP) exchanges reachability between Internet domains, using policy and AS paths as well as technical reachability.

IP forwarding itself is not a routing protocol. A router can forward based on static or dynamic routes. A link-state protocol may flood topology information and run a shortest-path calculation; a distance-vector protocol may exchange costs with neighbours. Both ultimately populate forwarding tables.

Routing can fail, loop, oscillate, or select an unsuitable path. Metrics may measure hop count, delay, bandwidth, reliability, or policy. The best route is best for a chosen metric and policy, not automatically the route with the fewest hops.

### 9. Addressing and the routing hierarchy

IP prefixes group addresses so routers can aggregate routes. A provider may advertise a large aggregate, while a customer advertises more-specific prefixes. A destination is forwarded using longest-prefix matching. This hierarchy is one reason the Internet can scale.

A single host normally has:

- a global or local IP address;
- a subnet prefix;
- a default gateway;
- a local link-layer address for neighbours.

A packet to a remote destination goes first to the default gateway. The source does not need to know every router or host in the Internet.

### 10. Quality of service and policy

The basic IP service does not guarantee a particular delay or bandwidth. Network operators can use traffic classification, priority marking, queueing, scheduling, policing, and shaping to prioritise some traffic. DiffServ and explicit congestion notification are examples of IP-related mechanisms.

Best-effort IP is flexible, but applications with strict real-time requirements may need admission control, reservation, or an upper-layer adaptation mechanism. Marking a packet alone does not reserve capacity.

### 11. NAT and the Internet network layer

NAT is commonly used at the edge of an IPv4 network to translate private addresses. It can make a private host appear to use a public address to the outside world. NAT is not part of the basic IP forwarding service and can complicate applications that embed addresses or depend on end-to-end reachability.

IPv6 is designed to use globally scoped addresses more directly, although privacy mechanisms and firewalls remain important. A transition gateway can translate during migration.

### 12. Layered responsibilities

IP provides network-layer delivery. TCP may provide reliable ordered bytes, flow control, and congestion control. UDP may provide low-overhead datagrams. Application protocols define messages such as HTTP requests or DNS questions. Each layer has a different purpose.

A common mistake is to blame IP for every end-to-end failure. A packet can have a valid IP route yet be dropped by a firewall, an application can reject a message, or a destination can be offline. Troubleshooting should identify the layer and symptom.

## Worked examples

### Example 1: Best-effort loss

A router's queue is full when several large packets arrive. The router drops one packet. IP does not retransmit it. A TCP receiver notices a missing byte range and requests retransmission; a UDP application may simply continue or report a quality loss.

### Example 2: TTL loop

A misconfigured pair of routers sends a packet back and forth. Each router decrements the TTL. When it reaches zero, the packet is discarded, limiting the loop. The administrator must correct the route; IP's TTL does not do that.

### Example 3: Path MTU

An IPv6 packet is 1,500 bytes and the next link supports 1,400. The router sends an ICMPv6 Packet Too Big message. The source lowers its packet size and retries. In IPv4, a router might fragment, but source PMTU discovery is generally preferred.

### Example 4: DNS and forwarding

A client asks DNS for `www.example.org`. The DNS query travels through IP routers; the resolver receives an address; the client then opens a connection to that address. DNS does not forward application packets itself, and IP does not resolve names.

## Key terms & formulas

- **IP:** Internet Protocol; best-effort packet service.
- **Best effort:** no guarantee of delivery, order, delay, or bandwidth.
- **IPv4:** 32-bit address version.
- **IPv6:** 128-bit address version.
- **Packet:** network-layer PDU.
- **Forwarding:** per-packet lookup and transmission.
- **Routing:** path learning/selection.
- **TTL/Hop Limit:** per-router decrement; zero discards.
- **ICMP:** IPv4 control/error protocol.
- **ICMPv6:** IPv6 control, discovery, and PMTUD protocol.
- **MTU:** maximum transmission unit.
- **Fragmentation:** divide a packet for a smaller link.
- **Longest prefix:** most-specific matching route.
- **BGP:** inter-domain policy routing protocol.
- **OSPF/IS-IS:** common interior link-state routing protocols.
- **IP checksum:** IPv4 header integrity check; IPv6 does not use this field.
- **Packet lifetime:** roughly TTL/Hop Limit router decrements before discard.

## Common mistakes

1. **IP does not guarantee delivery.** It is best effort.
2. **IP does not guarantee order or uniqueness.** Duplicate and out-of-order packets are possible.
3. **Routing protocols are not IP forwarding.** They populate or influence the forwarding table.
4. **TTL is not a repair mechanism.** It only limits packet lifetime.
5. **IPv6 routers do not fragment ordinary packets.** The source handles fragmentation through PMTU.
6. **ICMP is not a guarantee of end-to-end delivery.** It reports selected errors and supports control.
7. **A MAC address is not the IP destination across an Internet path.** Link addresses change by hop.
8. **A route with the fewest hops is not automatically best.** The metric and policy matter.
9. **Best-effort does not mean badly designed.** It is a scalable service with end-to-end mechanisms above it.
10. **IP address exhaustion is not solved by one private range.** NAT reuses private addresses but does not create global IPv4 bits.

## Exam prep

### Likely 2-mark questions

1. **Why is IP called a best-effort protocol?**  
   Hint: no guarantee of delivery, order, delay, or retransmission.
2. **State two functions of the Internet network layer.**  
   Hint: logical addressing, routing, forwarding, internetworking, or error reporting.
3. **What is the purpose of TTL/Hop Limit?**  
   Hint: stop packets from circulating indefinitely.
4. **State two purposes of ICMP.**  
   Hint: report errors and provide network diagnostics/control.
5. **What is the difference between routing and forwarding?**  
   Hint: route learning versus per-packet table action.
6. **How does IPv6 handle a packet too large for the next link?**  
   Hint: router sends Packet Too Big; source fragments or reduces packet size.

### Likely long-answer questions

1. **Explain the Internet network-layer service and why it is best effort.**  
   Answer hint: connectionless packets, router simplicity, loss/reordering/delay trade-offs, and upper-layer recovery.
2. **Trace an IP packet across multiple routers and links.**  
   Answer hint: encapsulation, prefix lookup, TTL, local link changes, and decapsulation.
3. **Compare IPv4 and IPv6 network-layer behaviour.**  
   Answer hint: addresses, headers, fragmentation, ICMP, configuration, and transition.
4. **Explain how IP routing and forwarding tables support scalability.**  
   Answer hint: aggregation, longest prefix, routing protocols, and separation of control/data planes.
5. **Discuss how the Internet handles errors, congestion, and quality of service.**  
   Answer hint: ICMP, loss, queueing, traffic policy, and higher-layer adaptation.

### Short-answer revision checklist

Be ready to state the best-effort guarantees IP does and does not provide, draw a forwarding table lookup, explain TTL and PMTUD, and name ICMP's role.
