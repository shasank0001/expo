---
subject: cn
unit: 3
topic: network-layer-and-internetworking
syllabus_ref: CSM3103 Unit-III
status: draft
---
# Network Layer and Internetworking

## Overview

The **network layer** provides host-to-host packet delivery across an internetwork. It identifies networks and interfaces with logical addresses, chooses a next hop, forwards packets through routers, and hides much of the difference between the physical and link technologies underneath.

The syllabus lists network-layer design issues, internetworking, and the Internet network layer. The layer must balance simplicity, scalability, addressing, routing, error reporting, fragmentation, quality of service, and security. IP is the Internet's main example: it is connectionless and best effort, while routing protocols and higher layers provide additional behaviour where needed.

Internetworking means connecting different networks—Ethernet LANs, Wi-Fi, fibre links, cellular networks, and administrative domains—into one larger system. Routers make the connection by forwarding packets from one network to another according to a destination prefix and a forwarding table.

## Explanation

### 1. Network-layer design issues

A network-layer protocol must answer several questions:

- How is a destination network and interface identified?
- How does a host decide whether a destination is local or remote?
- How does a router learn a path or forward a packet?
- What happens when no route exists?
- How are errors and exceptions reported?
- How are packets fragmented or kept within link MTUs?
- How are priorities, security, and congestion handled?
- How do different address and packet formats interoperate?

The design must scale to millions of interfaces without requiring every router to know every host. Hierarchical prefixes and aggregation are central to this scaling.

### 2. Packet delivery and addresses

A network-layer packet contains at least source and destination network-layer addresses plus control fields such as version, length, time-to-live or hop limit, protocol type, and checksums or integrity information. The packet is encapsulated in a link-layer frame on each hop.

A host compares the destination address with its own prefix. A local destination is sent directly on the current link. A remote destination is sent to a default gateway or next-hop router. The destination IP address generally remains the same across the Internet, while link-layer addresses are local to each hop.

### 3. Routing and forwarding

**Routing** is the process of learning or selecting paths through the network. **Forwarding** is the per-packet action of examining a destination and using a forwarding table to select an outgoing interface and next hop.

A forwarding-table entry conceptually contains:

- destination prefix;
- next-hop address or outgoing interface;
- metric or preference;
- administrative distance in some protocols;
- route type and associated state.

A router normally performs a longest-prefix match for IPv4 and a similar longest-prefix process for IPv6. It then removes the incoming frame, updates packet fields such as TTL, encapsulates the packet in a new outgoing frame, and transmits it.

### 4. Internetworking

Internetworking joins networks with different:

- physical media;
- link-layer technologies;
- administrative owners;
- address or routing domains;
- maximum frame sizes;
- service policies.

A router connects two or more networks. It does not require a shared LAN or a common physical medium. The network layer supplies a common service so upper layers do not need to know whether a packet crossed Ethernet, Wi-Fi, or fibre.

Internetworking also requires agreement about addressing and routing. A router's interface addresses identify the local connections, while routes describe reachable prefixes. A route can be connected, static, or learned dynamically.

### 5. Network-layer protocols and services

IP provides a best-effort service. Other network-layer or supporting protocols provide:

- **ICMP/ICMPv6:** errors and diagnostics;
- **ARP:** IPv4 local address resolution;
- **neighbour discovery:** IPv6 local neighbour/router functions;
- **routing protocols:** path information;
- **DHCP:** address/configuration delivery at the access network;
- **tunnel and VPN protocols:** protected or transition traffic.

The network layer normally does not provide end-to-end reliability, ordering, or application security by itself. Those are choices of higher layers, although some link or network technologies may add limited protection.

### 6. Forwarding decision example

A router has:

- `192.168.1.0/24` directly connected;
- `10.0.0.0/8` through `192.168.1.1`;
- `0.0.0.0/0` through `203.0.113.1`.

A packet for `10.1.2.3` matches the `/8` and default route, so the `/8` is chosen. A packet for `203.0.113.9` matches only the default route. A packet for `192.168.1.8` is delivered directly on the local interface. The most-specific matching route wins.

### 7. Packet lifetime and loops

If a packet enters a routing loop, routers decrement TTL (IPv4) or Hop Limit (IPv6). When the field reaches zero, the packet is discarded and an ICMP message may be sent to the source. This bounds the damage of a loop but does not repair the routing configuration. A source can reduce its own TTL or use path-MTU discovery, but routers normally do not discover a loop for the source automatically.

### 8. Fragmentation and MTU

Different links support different maximum transmission units. IPv4 routers can fragment a packet when it is too large for the outgoing link, although fragmentation adds headers and can cause loss if one fragment is missing. Modern deployments generally use path-MTU discovery so the source sends appropriately sized packets.

IPv6 routers do not fragment ordinary packets. The source uses PMTU information and ICMPv6 Packet Too Big messages. A network-layer design must therefore consider path MTU, fragmentation support, and the cost of header overhead.

### 9. Error reporting

IP itself is not required to report every error. ICMP provides selected messages such as destination unreachable, time exceeded, and parameter problem. ICMPv6 adds important functions including neighbour discovery, path-MTU information, and IPv6-specific control.

Error messages are useful but can create security issues: forged ICMP packets can mislead hosts or routers, and excessive error traffic can itself be a denial-of-service vector. Rate limiting and validation are needed.

### 10. Quality of service and policy

The basic IP service treats packets similarly. Network-layer QoS can use classification, priority, queue scheduling, policing, shaping, or differentiated fields to prioritise delay-sensitive traffic. DiffServ and explicit congestion notification are examples of mechanisms that may be used in IP networks.

QoS is not a guarantee unless resources are provisioned and policy is enforced. A high-priority label alone does not create capacity.

### 11. Scalability and hierarchy

A scalable network layer uses hierarchical addresses and route aggregation. Routers need routes toward networks, not routes toward every host. A top-level provider can advertise a large aggregate, while internal networks advertise more-specific routes. When a link fails, routing protocols update reachability without changing every packet address.

Scalability also depends on forwarding speed, memory, update stability, and control-plane scalability. A simple packet header helps, but a routing protocol that reacts to every small change can still overload the control plane.

## Worked examples

### Example 1: Laptop to Internet

The laptop's destination `8.8.8.8` is outside its `/24`, so it sends the frame to the default gateway's MAC address. The home router performs longest-prefix matching, may translate the source address with NAT, and forwards the packet over the ISP link. Every router updates the link-layer frame, while the IP destination remains `8.8.8.8`.

### Example 2: Internetworking different media

An Ethernet-connected laptop sends an IP packet to a router. The router forwards it over a fibre link to a mobile network. The packet's IP address remains meaningful, but the fibre or cellular link uses its own frame and radio procedures.

### Example 3: TTL

A packet with TTL 2 reaches a router that decrements it to 1 and forwards. The next router decrements it to 0 and discards it. The loop is stopped, and an ICMP Time Exceeded message may inform the source.

### Example 4: MTU

An IPv6 packet is larger than the outgoing link's MTU. The router cannot fragment it, so it sends an ICMPv6 Packet Too Big message. The source reduces its packet size and retries. An IPv4 router may fragment, but the source-based PMTU approach is generally preferable.

## Key terms & formulas

- **Network layer:** Layer-3 packet delivery between networks.
- **Internetworking:** connecting different networks.
- **Router:** network-layer forwarding device.
- **Packet:** network-layer PDU.
- **Forwarding table:** prefix-to-next-hop mapping.
- **Routing:** learning or choosing paths.
- **Forwarding:** applying a table to one packet.
- **Longest-prefix matching:** select the most-specific matching prefix.
- **TTL/Hop Limit:** decrement per router; zero causes discard.
- **MTU:** maximum transmission unit on a link.
- **IPv4 fragmentation:** possible router/source fragmentation.
- **IPv6 fragmentation:** source-based using PMTU.
- **ICMP:** network-layer control and error messages.
- **Route aggregation:** one route for a common prefix.
- **Scalability:** ability to grow without a table/state explosion.
- **Packet forwarding time:** table lookup + queueing + transmission.

## Common mistakes

1. **The network layer is not the data-link layer.** It moves packets between networks; links carry local frames.
2. **Routing and forwarding are not synonyms.** Routing learns paths; forwarding applies a table.
3. **A router does not always calculate a new complete route for every packet.** It normally uses a forwarding table.
4. **IP does not guarantee delivery or order.** It is best effort.
5. **MAC addresses are local.** Routers normally change them at every new link.
6. **TTL does not fix routing configuration.** It only limits packet lifetime.
7. **Fragmentation is not equally supported.** IPv6 routers do not ordinarily fragment.
8. **ICMP is not a general delivery guarantee.** It reports selected errors and supports control functions.
9. **Internetworking is not just physical connection.** Logical addressing, routing, and protocol agreement are required.
10. **QoS markings are not automatically honoured.** Resource and policy configuration matters.

## Exam prep

### Likely 2-mark questions

1. **State the main functions of the network layer.**  
   Hint: logical addressing, routing, forwarding, internetworking, and error/MTU support.
2. **Differentiate routing and forwarding.**  
   Hint: path selection/learning versus per-packet table lookup and transmission.
3. **What is internetworking?**  
   Hint: connecting different networks into one larger network.
4. **What is the purpose of TTL or Hop Limit?**  
   Hint: prevent a packet from circulating indefinitely through loops.
5. **What is an MTU?**  
   Hint: maximum data unit a link can carry.
6. **Why are network-layer addresses hierarchical?**  
   Hint: aggregation and scalable routing.

### Likely long-answer questions

1. **Explain network-layer design issues with addressing, routing, MTU, errors, QoS, and scalability.**  
   Answer hint: show how a packet moves and why each design function is needed.
2. **Trace a packet across Ethernet, fibre, and a mobile link.**  
   Answer hint: common IP packet, router changes, local link frames, and different media.
3. **Compare routing and forwarding with a forwarding-table example.**  
   Answer hint: direct/default/specific routes, longest prefix, next hop, and interface.
4. **Explain IPv4 and IPv6 fragmentation and PMTUD.**  
   Answer hint: router fragmentation versus source-based IPv6 fragmentation and ICMP messages.
5. **Explain how internetworking hides physical-link differences.**  
   Answer hint: common network-layer service, routers, local link changes, and upper-layer independence.

### Short-answer revision checklist

Be ready to draw a packet crossing two routers, define routing/forwarding, state TTL/MTU, explain ICMP, and distinguish a network-layer address from a MAC address.
