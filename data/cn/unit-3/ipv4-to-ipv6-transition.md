---
subject: cn
unit: 3
topic: ipv4-to-ipv6-transition
syllabus_ref: CSM3103 Unit-III
status: draft
---
# Transition from IPv4 to IPv6

## Overview

IPv4 and IPv6 use different address sizes, packet formats, routing information, and neighbour-discovery mechanisms. An IPv6 packet cannot be forwarded as an ordinary IPv4 packet on an IPv4-only network. Transition mechanisms allow old IPv4-only systems and newer IPv6 systems to communicate during a gradual migration.

The syllabus includes transition from IPv4 to IPv6. The main methods are **dual stack**, **tunnelling**, and **translation**. They can be used at different points: hosts, routers, gateways, service providers, and applications. A successful transition plan must consider routing, addressing, security, DNS, monitoring, and the cost of running two address families.

## Explanation

### 1. Why transition is needed

IPv4 and IPv6 are not wire-compatible:

- IPv4 addresses are 32 bits; IPv6 addresses are 128 bits.
- IPv4 headers and IPv6 base headers have different formats and fields.
- Address prefixes and neighbour discovery differ.
- Routers and firewalls may understand one protocol but not the other.
- Applications and security policies may be tied to an address family.

Replacing every device and link at once is expensive and risky. Transition techniques allow an organisation to introduce IPv6 progressively while retaining IPv4 for older systems.

### 2. Dual stack

A **dual-stack** host or router has both IPv4 and IPv6 interfaces, stacks, addresses, and routing information. It can choose IPv6 for a destination with usable IPv6 connectivity and IPv4 for an IPv4-only destination.

A dual-stack router is often called a **6to4-style dual-stack router** only in a more specific transition context; the general term is a router with both address families. The host maintains two sets of interfaces or logical connections. A dual-stack application may use:

- an IPv6 AAAA record and connect over IPv6;
- an IPv4 A record and connect over IPv4;
- a fallback or Happy Eyeballs-style selection when one family is unavailable.

Dual stack gives the best native compatibility, but it doubles some configuration, monitoring, security, and testing work. Running both protocols does not automatically make the transition secure; each path needs firewall and access policy.

### 3. Tunnelling

A **tunnel** carries an IPv6 packet inside an IPv4 packet across an IPv4-only network. The tunnel endpoints are routers or hosts that understand the transition mechanism.

The process is:

1. An IPv6 packet enters the tunnel ingress router.
2. The router treats the IPv6 packet as payload.
3. It creates a new IPv4 header, with a tunnel endpoint as the IPv4 destination.
4. The IPv4 network forwards the outer packet.
5. The egress router removes the outer IPv4 header.
6. The original IPv6 packet is forwarded toward its destination.

The outer header provides connectivity over IPv4; the inner header preserves the original IPv6 destination. Tunnels add header overhead and can complicate MTU discovery, filtering, path validation, and monitoring.

Common transition examples include automatic tunnels and configured tunnels such as 6rd or IP-in-IP encapsulation. The exact protocol depends on the provider and network; a tunnel does not magically make the two address families equivalent.

### 4. Translation

A **translation gateway** converts between IPv4 and IPv6 address/protocol representations. It may translate headers, maintain state, rewrite checksums, and map connection state so that an IPv4 host can reach an IPv6-only service or vice versa.

Translation is useful at a controlled boundary, such as a data centre, ISP, or legacy application. It has limitations:

- address and port mapping can be complex;
- end-to-end properties may not be preserved;
- applications that inspect addresses or embed IP addresses in payloads may break;
- security and filtering state must be consistent;
- it is not a substitute for native IPv6 inside the migrated network.

### 5. Other transitional mechanisms

Other mechanisms include:

- **6rd (IPv6 over IPv4):** uses provider IPv4 infrastructure to carry customer IPv6 traffic, often with provider-assigned IPv4 addresses and routing.
- **6to4:** embeds a public IPv4 address in an IPv6 prefix; it has security and reachability limitations and is not appropriate as a general modern design.
- **Teredo:** helps provide IPv6 connectivity over difficult IPv4 paths using UDP relays and tunnelling.
- **NAT64/DNS64:** allows IPv6-only clients to reach selected IPv4-only services through a translator and DNS64 synthesis of AAAA records.
- **relay infrastructure:** forwards packets or queries across transition boundaries when direct routing is unavailable.

A student should not confuse a relay with a router or a translator with a native dual-stack endpoint. Each mechanism solves a different part of the transition problem.

### 6. DNS and application issues

During transition, a name may have both A (IPv4) and AAAA (IPv6) records. A client may choose IPv6, fail, and fall back to IPv4, or connect through a translator. Applications must handle address-family differences, timeouts, firewalls, and certificate/network policies.

An IPv6 literal address must be enclosed appropriately in configuration formats, while a domain-based service can allow the application to select an address. A server with both addresses can advertise both records, but advertising IPv6 does not guarantee that the client's path works.

### 7. Routing and deployment

An operator may first enable IPv6 on internal links, then provide dual-stack access, then tunnel a branch over IPv4, and finally remove IPv4 dependencies. IPv6 routing tables and policies must be monitored independently. A tunnel endpoint needs a stable IPv4 address and a route to the remote endpoint.

Migration stages may include:

1. inventory address families and applications;
2. test DNS, firewalls, VPN, and monitoring;
3. enable IPv6 in a lab;
4. use tunnels or translation for isolated IPv6 networks;
5. introduce dual-stack at selected sites;
6. migrate applications and users;
7. remove obsolete IPv4 paths after confirming dependencies.

A big-bang replacement is simpler in theory but carries high compatibility and rollback risk.

### 8. Security in transition

Tunnels and translators must be authenticated and protected. A tunnel endpoint should verify the route and peer, and an address translation device should prevent spoofed state from bypassing policy. Firewalls must understand both versions, and logs should record the actual address family and tunnel identity.

IPv4 and IPv6 paths can have different security controls. If one family is less restricted, attackers may use it as an alternate route. A transition firewall and regular monitoring are necessary.

## Worked examples

### Example 1: Dual-stack web access

A dual-stack laptop opens `https://example.org`. DNS returns an AAAA record and an A record. The laptop tests IPv6 and connects successfully. An older branch with no IPv6 path falls back to the A record and IPv4. No translation is needed on the native dual-stack path.

### Example 2: Tunnelling a branch

A branch's IPv6 hosts send traffic to a provider. The branch router encapsulates each IPv6 packet in an IPv4 packet addressed to the ISP's tunnel endpoint. The ISP forwards the outer packets over IPv4 and decapsulates them at an IPv6-capable router. The original IPv6 destination is inside the tunnel.

### Example 3: Translation boundary

An IPv4-only legacy application connects to an IPv6 service through a translator. The translator establishes state, rewrites the IPv4 source into an assigned IPv6 address, translates the response, and maps the connection back to the original client. This is practical for controlled migration but may not preserve every end-to-end feature.

### Example 4: NAT64/DNS64

An IPv6-only client asks for a service that has only an A record. DNS64 synthesises an AAAA record containing a special IPv4-embedded address in a known prefix. The NAT64 gateway translates the packet to IPv4 and returns the response. The service itself may not need to know about IPv6.

## Key terms & formulas

- **IPv4:** 32-bit address and packet format.
- **IPv6:** 128-bit address and new packet format.
- **Dual stack:** both protocols on a host/router.
- **Tunnelling:** encapsulate IPv6 inside IPv4 across an IPv4-only path.
- **Translation:** convert between address families and maintain state.
- **6rd:** provider IPv6-over-IPv4 transition mechanism.
- **6to4:** historical IPv6-over-IPv4 mechanism with limitations.
- **Teredo:** tunnel/relay mechanism for IPv6 connectivity.
- **NAT64:** translate IPv6 client traffic to IPv4.
- **DNS64:** synthesise AAAA records for IPv4-only destinations.
- **AAAA record:** IPv6 address record.
- **Tunnel overhead:** outer IPv4 header plus inner IPv6 packet and lower-layer overhead.
- **Migration stage:** one planned step, such as lab, tunnel, dual stack, or native IPv6.
- **Address-family compatibility:** ability of a path/application to carry both versions.

## Common mistakes

1. **IPv6 and IPv4 are not natively compatible.** A transition mechanism is required between different address families.
2. **Dual stack is not tunnelling.** Dual stack has native stacks; tunnelling encapsulates one protocol in another.
3. **A tunnel endpoint must decode the tunnel.** The outer packet alone does not reach the IPv6 destination.
4. **Translation is not exactly NAT64 in every case.** Translation is a broad category; NAT64 is a specific mechanism.
5. **DNS64 does not make an IPv4 server natively IPv6.** It creates a usable address/route through a translator.
6. **6to4 is not a universal replacement for a tunnel or managed IPv6 service.** It has reachability and security limitations.
7. **Running both protocols does not guarantee security.** Each path needs firewall, authentication, and monitoring policy.
8. **A successful IPv6 ping does not prove an application works.** Applications may use address literals, firewalls, or incompatible features.
9. **Fallback from IPv6 to IPv4 can expose a different security path.** Test both families.
10. **Transition is an operational process.** It includes DNS, routing, monitoring, training, and rollback, not just configuration.

## Exam prep

### Likely 2-mark questions

1. **Why is transition from IPv4 to IPv6 needed?**  
   Hint: incompatible address sizes, headers, routing, and devices.
2. **Define dual-stack operation.**  
   Hint: a host/router has both IPv4 and IPv6 and selects the appropriate path.
3. **Explain tunnelling in one paragraph.**  
   Hint: IPv6 packet inside an IPv4 packet, decapsulated at the tunnel endpoint.
4. **What is a translation gateway?**  
   Hint: converts between IPv4 and IPv6 representation and maintains state.
5. **Name two DNS records relevant to IPv6 transition.**  
   Hint: A and AAAA.
6. **What is NAT64/DNS64?**  
   Hint: DNS64 synthesises an AAAA address and NAT64 translates the resulting traffic.

### Likely long-answer questions

1. **Compare dual stack, tunnelling, and translation.**  
   Answer hint: native support versus encapsulation versus stateful conversion; advantages, limitations, and examples.
2. **Explain a tunnelled IPv6 packet across an IPv4-only ISP.**  
   Answer hint: inner IPv6 header, outer IPv4 header, forwarding, decapsulation, MTU and security issues.
3. **Design a gradual IPv6 migration for an organisation.**  
   Answer hint: inventory, lab, DNS, dual stack, tunnels, firewall/security, monitoring, rollback, and final IPv4 removal.
4. **Explain NAT64/DNS64 with a worked request from an IPv6-only client.**  
   Answer hint: A record lookup, AAAA synthesis, NAT64 translation, return path, and limitations.

### Short-answer revision checklist

Be able to state the three main methods, draw an IPv6-inside-IPv4 tunnel, distinguish A from AAAA, and explain why a transition plan must cover routing and security as well as addressing.
