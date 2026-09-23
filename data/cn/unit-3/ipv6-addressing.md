---
subject: cn
unit: 3
topic: ipv6-addressing
syllabus_ref: CSM3103 Unit-III
status: draft
---
# IPv6 Addressing

## Overview

**IPv6** uses 128-bit addresses, creating an enormously larger address space than IPv4's 32-bit space. An address is written as eight groups of four hexadecimal digits separated by colons, for example `2001:0db8:0000:0000:0000:ff00:0042:8329`.

IPv6 was designed with a much larger address space, a simpler fixed base header, efficient routing, stateless auto-configuration support, improved neighbour discovery, and better facilities for mobility and security. Deployment can still be gradual because many networks and applications remain mixed IPv4/IPv6.

An IPv6 address has a **network prefix** and an **interface identifier**. The prefix identifies the subnet; the remaining bits identify an interface. Address types include global unicast, link-local, multicast, loopback, unspecified, and anycast/special ranges.

## Explanation

### 1. The 128-bit address space

An IPv6 address contains `2^128` possible values, an address space vastly larger than the `2^32` IPv4 space. The large space makes global allocation and future growth practical, but it does not remove the need for hierarchy, routing aggregation, privacy mechanisms, and responsible configuration.

The eight hexadecimal groups represent `8 x 16 = 128` bits. Each hexadecimal digit is four bits, so a full group has 16 bits. Letters `a` through `f` represent values 10 through 15.

### 2. Writing and compressing addresses

The full address `2001:0db8:0000:0000:0000:ff00:0042:8329` can be shortened in two ways:

- remove leading zeros within each group: `2001:db8:0:0:0:ff00:42:8329`;
- replace one continuous run of all-zero groups with `::`: `2001:db8::42:8329`.

`::` represents one or more complete groups of 16 zero bits. It may be used only once in an address because otherwise the number of replaced groups would be ambiguous. An IPv6 address still contains exactly eight groups when expanded.

For `::1`, the compressed form expands to `0000:0000:0000:0000:0000:0000:0000:0001`. This is the IPv6 loopback address. The unspecified address is `::`.

### 3. Prefix, interface identifier, and subnet

An IPv6 address is interpreted with a prefix length, such as `/64`. The first 64 bits identify a subnet and the remaining 64 bits commonly identify an interface. A typical address might be `2001:db8:1:2::10/64`; the prefix is `2001:db8:1:2::/64`.

Routers use the prefix to choose a destination network. Within the subnet, neighbour discovery discovers the link-layer address and reachability of the destination interface. A subnet mask in IPv6 uses a contiguous 1 prefix followed by zeros, just as in IPv4.

A `/64` is a common LAN allocation because it provides a large address space and supports standard subnet-to-interface relationships. The exact prefix assigned to an organisation can be shorter or longer; the provider determines it.

### 4. IPv6 address types

#### Global unicast

Global unicast addresses are allocated for public networks. They commonly begin with `2000::/3`, although exact global ranges and special-purpose prefixes are defined by standards. A global address is routable across participating IPv6 networks.

#### Link-local

Link-local addresses have a scope of one link. They commonly use the prefix `fe80::/64` and are used for neighbour discovery, router solicitation, and local control traffic. A link-local address is normally not forwarded beyond the current link. A scope/interface identifier may be required when the address is ambiguous on a host with multiple interfaces.

#### Multicast

IPv6 multicast is integral to the protocol. Multicast addresses conventionally begin with `ff00::/8`, and the scope bits indicate whether the group is link-local, site-local, organisation-local, or global. IPv6 does not use a separate multicast protocol as required in some older IPv4 deployments; neighbour and router functions are integrated.

#### Loopback and unspecified

`::1` is the loopback address. `::` is the unspecified address, used when no source address is yet available. Neither is a normal routable host address.

#### Anycast and special-purpose addresses

An anycast address is assigned to more than one interface, and a router chooses a nearby/appropriate path. Special ranges support particular functions, such as IPv4-compatible or transition mechanisms, and should be used according to the relevant standard. A student should not treat every `::`-containing address as a normal public host address.

### 5. IPv6 header and address-related features

IPv6 has a fixed 40-byte base header with fields such as version, traffic class, flow label, payload length, next header, hop limit, source, and destination. Optional functions use **extension headers** rather than adding many variable fields to the base header. The address size remains 128 bits, while the base header remains a predictable size for forwarding.

IPv6 also uses a hop limit rather than IPv4's TTL. Each router decrements the hop limit; when it reaches zero, the packet is discarded and an ICMPv6 error may be sent. IPv6 fragmentation is handled by the source using Path MTU Discovery; routers do not fragment packets as part of ordinary IPv6 forwarding.

### 6. Address configuration

**Stateless address auto-configuration (SLAAC)** lets a host form a link-local address and obtain a prefix through router advertisements. EUI-64 is a historical method that derives an interface identifier from a MAC address, but privacy extensions and random interface identifiers are now common because of tracking concerns.

A router advertisement supplies a prefix and configuration information; DHCPv6 can provide stateful addresses or additional options. A host may use both mechanisms according to the network design.

### 7. Neighbour discovery

IPv6 uses ICMPv6-based **Neighbour Discovery (ND)** to replace IPv4's ARP and support router discovery, neighbour discovery, prefix information, duplicate-address detection, and other functions. It can use link-local addresses even before a global address is available.

ND messages include router solicitation, router advertisement, neighbour solicitation, neighbour advertisement, and redirect. A node learns a router's link-layer address, checks whether a neighbour is reachable, and detects duplicate addresses. ND is a control protocol, not a replacement for routing between networks.

### 8. IPv6 routing and aggregation

Routers use the IPv6 prefix to select a next hop, much as in IPv4, but the larger address space and hierarchical allocation support efficient global routing. Route aggregation is important: adjacent prefixes with a common higher-order prefix can be represented by one shorter route.

A more-specific prefix overrides an aggregate, as in longest-prefix matching. IPv6 uses a 64-bit interface identifier in common LANs, but the prefix boundary—not the fact that the address is 128 bits—determines the subnet.

### 9. Privacy, security, and identity

An IPv6 address can identify an interface and, if generated predictably, help track a user. Temporary/privacy addresses rotate the interface identifier to reduce long-term tracking. Security still requires authentication and encryption at the appropriate layers; a 128-bit address alone does not make a connection secure.

IPsec was originally closely associated with IPv6, but applications commonly use TLS and other end-to-end protections over both address families. Transition and security policies must be considered together.

### 10. IPv6 versus IPv4

| Feature | IPv4 | IPv6 |
|---|---|---|
| Address bits | 32 | 128 |
| Address text | Dotted decimal | Hexadecimal groups |
| Header | Variable/complex | Fixed 40-byte base plus extensions |
| Broadcast | Common at subnet | No general broadcast; multicast is used |
| Configuration | Often DHCP/manual | SLAAC and/or DHCPv6 |
| Fragmentation | Routers or source | Source using PMTU |
| Address exhaustion | Serious concern | Very large address space |
| Transition | Native | Dual stack, tunnelling, translation |

IPv6 is not automatically faster. Its benefits are address space, extensibility, routing, configuration, and support for modern mobility/security designs. Performance depends on the path, implementation, and congestion.

## Worked examples

### Example 1: Expand a compressed address

`2001:db8::42:8329` expands to:

`2001:0db8:0000:0000:0000:0000:0042:8329`

The `::` represents five zero groups in this case.

### Example 2: IPv6 subnet

`2001:db8:abcd:12::/64` is a subnet prefix. An interface address could be `2001:db8:abcd:12::25`. The first 64 bits identify the subnet; the final 64 bits distinguish the interface.

### Example 3: Link-local scope

A host uses `fe80::1` to reach a local router. The address cannot be routed through the Internet. If the host has several interfaces, an interface identifier or scope is included so the destination is unambiguous.

### Example 4: Hop limit

A packet arrives with Hop Limit 2. The first router decrements it to 1 and forwards; the next router decrements it to 0 and discards the packet, normally sending an ICMPv6 Time Exceeded message. This prevents a routing loop from circulating a packet forever.

### Example 5: IPv4-to-IPv6 transition

A dual-stack laptop can use IPv6 to reach an IPv6 destination and IPv4 to reach an IPv4-only destination. A tunnel can carry IPv6 across an IPv4-only ISP link, while a translation gateway handles address-family differences. A full transition plan addresses routing and security, not only the client.

## Key terms & formulas

- **IPv6 address:** 128-bit interface address.
- **Hextet/group:** one of eight 16-bit groups.
- **`::`:** compression for one or more all-zero groups.
- **Prefix length:** number of leading network bits, e.g. `/64`.
- **Global unicast:** publicly routed IPv6 address type.
- **Link-local:** single-link scope, commonly `fe80::/64`.
- **Multicast prefix:** conventionally `ff00::/8`.
- **Loopback:** `::1`.
- **Unspecified:** `::`.
- **Interface identifier:** host/interface portion of an address.
- **SLAAC:** stateless address auto-configuration.
- **EUI-64:** MAC-derived interface-identifier method.
- **Neighbour Discovery:** ICMPv6 link control and address discovery.
- **Hop Limit:** IPv6 counterpart to IPv4 TTL; decremented per router.
- **Base header:** fixed 40-byte IPv6 header.
- **Extension header:** optional IPv6 option/control header.
- **Address groups:** `8 x 16 = 128` bits.
- **Largest possible address count:** `2^128`.

## Common mistakes

1. **IPv6 is not 128 decimal digits.** It has 128 bits, written as eight hexadecimal groups.
2. **`::` can be used only once.** Otherwise the number of compressed groups is ambiguous.
3. **The `::` does not represent one group.** It represents one or more consecutive all-zero 16-bit groups.
4. **A global unicast address is not automatically the host's public identity.** It may be temporary, privacy-oriented, or assigned to an interface.
5. **IPv6 has no general broadcast like IPv4.** Multicast and anycast serve different group/selection purposes.
6. **A `/64` is common but not compulsory.** Provider allocation and design determine the prefix.
7. **IPv6 routers do not ordinarily fragment packets.** Source-side PMTU mechanisms are used.
8. **A larger address space does not make a packet secure.** Authentication, encryption, and privacy policy are separate.
9. **IPv6 does not automatically mean faster.** Overheads, routing, and congestion matter.
10. **Neighbour discovery is local, like ARP.** It does not replace inter-network routing.
11. **A link-local address is not globally routable.** It is limited to one link.

## Exam prep

### Likely 2-mark questions

1. **State two benefits of IPv6 over IPv4.**  
   Hint: 128-bit space, fixed base header, efficient routing, auto-configuration, and extension support.
2. **Explain IPv6 address compression.**  
   Hint: `::` replaces one or more consecutive zero groups and can appear only once.
3. **What is the IPv6 loopback address?**  
   Hint: `::1`.
4. **What is an IPv6 link-local address used for?**  
   Hint: local neighbour discovery and control, commonly `fe80::/64`.
5. **Define Hop Limit.**  
   Hint: per-router counter decremented on forwarding; zero causes discard.
6. **Name two IPv6 configuration mechanisms.**  
   Hint: SLAAC and DHCPv6.

### Likely long-answer questions

1. **Explain IPv6 address format, types, and prefixing with examples.**  
   Answer hint: 128 bits, eight hextets, compression, global/link-local/multicast, and `/64`.
2. **Compare IPv4 and IPv6 headers and fragmentation.**  
   Answer hint: fixed 40-byte base, extension headers, source PMTU, and no router fragmentation.
3. **Explain IPv6 Neighbour Discovery and auto-configuration.**  
   Answer hint: SLAAC, router advertisements, link-local addresses, ND messages, and duplicate detection.
4. **Describe the advantages and limitations of IPv6 deployment.**  
   Answer hint: address space, routing, configuration, transition, compatibility, privacy, and operations.

### Short-answer revision checklist

Be ready to expand `2001:db8::1`, distinguish global and link-local addresses, explain a `/64`, state `::1`, and compare IPv6 hop limit with IPv4 TTL.
