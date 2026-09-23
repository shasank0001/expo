---
subject: cn
unit: 1
topic: routers-and-gateways
syllabus_ref: CSM3103 Unit-I
status: draft
---
# Routers and Gateways

## Overview

A **router** is a network-layer device that forwards packets between different IP networks. It examines the destination IP address, consults a forwarding table, and sends the packet through the appropriate next hop and outgoing interface. A **gateway** is a broader term for a connection or translation point between unlike systems; it may use a protocol or data format different from the local system.

The syllabus groups routers and gateways with connecting devices. The key distinction is scope and function. A router normally connects networks using the same internetworking protocol and preserves the end-to-end IP address while changing link-layer information at each hop. A gateway is not limited to Layer 3; it can connect a database to an application, translate address formats, or act as a default router in older terminology.

A home “router” often combines several functions: routing, Ethernet switching, wireless access point, firewalling, and NAT. This makes the name practical rather than a precise description of one layer.

## Explanation

### 1. Router: network-layer forwarding

A router operates mainly at the **network layer (OSI Layer 3)**. It receives a frame, removes the local link-layer header, examines the IP destination, and looks up a route. The route gives a next hop, outgoing interface, and sometimes metrics and preferences. The router encapsulates the IP packet in a new frame for the outgoing link.

A router can:

- connect different Layer-2 broadcast domains;
- forward packets using logical IP addresses;
- isolate broadcasts from one network to another;
- select paths using static routes or routing protocols;
- perform packet filtering, NAT, firewalling, or quality-of-service functions in some devices;
- fragment IPv4 packets or handle path-MTU features, depending on the design.

A basic forwarding table looks conceptually like:

| Destination prefix | Next hop | Interface | Metric |
|---|---|---|---|
| 192.168.1.0/24 | directly connected | Ethernet0 | 0 |
| 0.0.0.0/0 (default) | 203.0.113.1 | WAN0 | 1 |

The router uses longest-prefix matching for IPv4. If several entries match, the most specific prefix is selected. A default route matches when no more specific route exists.

### 2. Routing versus forwarding

**Routing** means learning or choosing paths through a network. It may be static, manually configured, or learned dynamically through a routing protocol. **Forwarding** means applying the forwarding table to one arriving packet. Routing builds information; forwarding uses it.

A router may forward a packet in microseconds while a routing protocol takes seconds or minutes to converge. Do not say that the router “calculates a complete route from scratch” for every packet; modern routers normally perform a table lookup.

### 3. Router functions and interfaces

Routers use interfaces connected to different networks. A packet arriving on an interface is processed, and the outgoing interface can be different. The router also maintains state such as counters, ARP/neighbour entries, queues, access-control rules, and protocol adjacencies.

Some common router features are:

- packet forwarding and longest-prefix matching;
- route advertisement and path selection;
- connection tracking and NAT;
- packet filtering and firewall rules;
- traffic classification and queue scheduling;
- encapsulation of tunnels or virtual private networks;
- management through a CLI, web interface, or SNMP.

A router must also handle limitations such as packet size, queue capacity, TTL, and administrative control. If a route is missing, it may send an ICMP destination-unreachable message when appropriate.

### 4. Gateway: broad meaning

A **gateway** is a point where two systems or protocols meet and the data must be translated or coordinated. Unlike a router, the term does not imply one fixed OSI layer. A gateway can:

- translate between different network protocols;
- translate data formats or character encodings;
- connect an application to a database or external service;
- provide protocol conversion between a client and a server;
- bridge dissimilar systems;
- serve as a default route in a host's configuration.

A gateway may operate at several layers or at an application layer. A protocol converter that maps an IPv4 packet to IPv6 is an example of a network-transition gateway. A mail gateway that accepts SMTP and forwards messages to another mail system is an application gateway. A database gateway exposes a database to remote applications.

The word **default gateway** normally means the router to which a host sends packets when the destination is outside its local subnet. In this use, the default gateway is still normally a router; “gateway” is a role in the host's next-hop decision.

### 5. Router versus switch versus gateway

| Device | Main layer | Typical decision | Scope |
|---|---|---|---|
| Hub | Physical | Repeat signal | Shared collision domain |
| Switch | Data link | Forward frame by MAC | Local LAN ports/segments |
| Router | Network | Forward packet by IP prefix | Separate IP networks |
| Gateway | Any layer | Translate/coordinate unlike systems | Protocol, format, or application boundary |

A gateway can include router functions, and a router can provide a default-gateway service. The names are sometimes used loosely in consumer products, so the function and layer should be stated.

### 6. Address and header changes at a router

Suppose a laptop has `192.168.1.10/24` and sends a packet to `203.0.113.20`. The laptop determines that `203.0.113.20` is outside its local prefix and sends the Ethernet frame to its default gateway's MAC address. The router removes that frame, keeps the IP destination, and creates a new frame for the ISP link using its own outgoing MAC address and the next-hop MAC address.

The IP packet may be unchanged, while the link-layer addresses change at every hop. NAT can change the IP address/port at a boundary, and routing can change the Time to Live (TTL) or Hop Limit by one at each router. A router does not normally read the HTTP request.

### 7. Routing tables and packet filters

A forwarding table can be built from:

- directly connected networks;
- static routes;
- default routes;
- dynamic routing protocols such as OSPF, IS-IS, RIP, EIGRP, or BGP.

Packet filters match fields such as source/destination address, protocol, port, interface, or application information. A firewall policy may allow, drop, reject, or rewrite traffic. Routing decides where a packet goes; filtering decides whether it is permitted or how it is treated.

### 8. NAT and service integration

Network address translation (NAT) maps private internal addresses to public addresses at a boundary. It is commonly implemented in a home router, but it is not the same as routing. Routing forwards packets; NAT changes address information and maintains state so replies can return.

A home router may provide:

- Ethernet switching;
- Wi-Fi access-point service;
- IP routing;
- NAT;
- firewalling;
- DHCP address assignment;
- port forwarding or virtual-server functions.

A packet-filtering port-forwarding rule can direct a public request to an internal host, but this is a separate control from selecting the default route.

### 9. Gateway design and security

A gateway is often a security boundary. It can authenticate protocols, translate addresses, inspect content, filter packets, and log events. It must be designed so that translation does not break end-to-end security protocols or return traffic. Overly permissive rules can expose internal services.

### 10. Faults and limits

A router can fail because of hardware, power, software, configuration, a full routing table, or an overloaded queue. Common symptoms include unreachable networks, excessive latency, high CPU, dropped packets, and routing loops. Routing protocols use sequence numbers, hold-down or path-state mechanisms, and TTL/Hop Limit to limit some failures; these are not guarantees against every misconfiguration.

## Worked examples

### Example 1: Home LAN to Internet

A laptop `192.168.1.10` sends a packet to `8.8.8.8`. The destination is outside `192.168.1.0/24`, so the laptop sends the frame to `192.168.1.1`, its default gateway. The home router removes the LAN frame, selects its WAN interface, may perform NAT, creates a new frame, and forwards the packet to the ISP. Return traffic uses NAT state to reach the laptop.

### Example 2: Prefix selection

A forwarding table contains `10.0.0.0/8` and `10.1.0.0/16`. A packet to `10.1.2.3` matches both. The router selects the `/16` route because it is more specific. This is longest-prefix matching.

### Example 3: Protocol translation gateway

A legacy device sends a proprietary message to a gateway. The gateway translates the message into HTTP, sends it to a web service, translates the response back, and returns it. This gateway's main function is protocol conversion, not IP forwarding.

### Example 4: Switch versus router

A switch receives a frame for `192.168.1.20` on a LAN port and uses the MAC table to select a port. A router receives a packet for `8.8.8.8` and uses an IP route to select a WAN interface. The first decision is local link delivery; the second is internetwork forwarding.

### Example 5: MTU problem

A router receives an IP packet larger than the outgoing link's MTU. It may fragment IPv4, send an ICMP “packet too big” indication, or use a mechanism such as path-MTU discovery. The outcome depends on the protocol and configuration. Fragmentation can increase overhead and delay.

## Key terms & formulas

- **Router:** Layer-3 device that forwards IP packets between networks.
- **Gateway:** broad translator/connection point between unlike systems or protocols.
- **Routing table/forwarding table:** prefixes mapped to next hops and interfaces.
- **Next hop:** address of the next router or directly connected destination.
- **Default route:** route used when no more specific route matches.
- **Longest-prefix matching:** choose the most specific matching destination prefix.
- **Directly connected route:** route for a network on a router interface.
- **Static routing:** manually configured routes.
- **Dynamic routing:** routes learned and maintained by routing protocols.
- **NAT:** translation of private source/destination addresses and usually ports.
- **TTL/Hop Limit:** field decremented at each router; zero causes discard.
- **MTU:** largest packet/frame payload a link can carry.
- **Broadcast domain:** Layer-2 area; routers normally separate broadcast domains.
- **Next-hop match example:** destination `10.1.2.3` matches both `10.0.0.0/8` and `10.1.0.0/16`; choose `/16`.
- **Packet-forwarding time:** approximately `lookup time + queueing delay + transmission time`.

## Common mistakes

1. **A router is not just a gateway.** A router is a specific network-layer function; gateway is broader.
2. **A default gateway is normally a router.** The word gateway describes the host's next-hop role.
3. **A switch and a router use different addresses and decisions.** Switches mainly use MAC addresses; routers use IP prefixes.
4. **Routing is not forwarding.** Routing learns paths; forwarding applies a table to each packet.
5. **A router does not guarantee that a packet reaches its destination.** It may drop packets or have no route.
6. **A router changes link-layer headers at each hop.** It normally does not change the end-to-end IP destination during ordinary forwarding.
7. **NAT is not the same as routing.** NAT translates address/port state; routing selects a path.
8. **Gateway does not mean only a network device.** Application and protocol gateways also exist.
9. **A home router may not perform every function in the physical box.** Wireless and firewall services may be integrated with routing.
10. **Longest-prefix matching is not simple default-route selection.** The most specific matching route wins.
11. **A gateway is not automatically secure.** It can be a security boundary, but it also needs correct rules and maintenance.

## Exam prep

### Likely 2-mark questions

1. **State the OSI layer and function of a router.**  
   Hint: network layer; forwards IP packets between networks using a forwarding table.
2. **Define gateway and give one example.**  
   Hint: translation/connection point between unlike systems; protocol converter or default gateway.
3. **Differentiate a router from a switch.**  
   Hint: Layer 3 IP and networks versus Layer 2 MAC and LAN ports.
4. **What is a default route?**  
   Hint: route used when no more specific route matches.
5. **State two functions commonly integrated into a home router.**  
   Hint: switching, Wi-Fi, NAT, firewall, DHCP, and routing.
6. **What is longest-prefix matching?**  
   Hint: select the most specific route whose prefix matches the destination.

### Likely long-answer questions

1. **Explain the functions of a router with a forwarding-table example.**  
   Answer hint: receive frame, remove link header, look up IP destination, choose next hop/interface, re-encapsulate, and forward.
2. **Differentiate routers, switches, hubs, bridges, and gateways.**  
   Answer hint: state layer, address, domain, function, and a realistic example for each.
3. **Explain routing and forwarding with a home Internet example.**  
   Answer hint: local prefix, default gateway, route lookup, NAT, WAN interface, and return path.
4. **Explain how NAT is used in a gateway and why it is not identical to routing.**  
   Answer hint: private/public address translation, state table, filtering, and forwarding decisions.
5. **Describe two gateway types and the security/design issues in translating protocols.**  
   Answer hint: address/protocol translation, authentication, compatibility, and return-path management.

### Short-answer revision checklist

Be ready to draw a LAN connected through a router to two different networks, show how a default gateway is chosen, and explain why link addresses change while the IP destination usually does not.
