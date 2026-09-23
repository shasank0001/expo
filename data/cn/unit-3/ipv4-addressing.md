---
subject: cn
unit: 3
topic: ipv4-addressing
syllabus_ref: CSM3103 Unit-III
status: draft
---
# IPv4 Addressing

## Overview

An **IPv4 address** identifies a network interface for the Internet Protocol. It is a 32-bit value normally written as four decimal octets separated by dots, such as `192.168.1.10`. Each octet is eight bits, so the four octets together represent 32 bits.

An address is interpreted with a **network prefix** and a **host or interface part**. The prefix length, written with a slash, tells a router how many leading bits identify the network and how many remain for the host/interface. Modern IPv4 uses classless prefix allocation; the old A, B, and C classes are mainly historical teaching aids.

IPv4 addressing matters because routers use it to forward packets, hosts use it to decide whether a destination is local, and administrators use subnet structure to organise addresses. Private addresses and NAT support internal networks, while unicast, multicast, and broadcast describe different delivery targets. The finite 32-bit address space is a major motivation for IPv6.

## Explanation

### 1. The 32-bit IPv4 address

An IPv4 address has `2^32` possible bit patterns, or `4,294,967,296` values. In dotted-decimal notation, each of the four fields ranges from 0 to 255. For example:

`192 . 168 . 1 . 10`

The octets are read as a binary address, not as four independent host numbers. A host must apply a mask or prefix before it can identify a network.

There are several representations:

- dotted decimal: `192.168.1.10`;
- binary: `11000000.10101000.00000001.00001010`;
- hexadecimal: `C0A8010A`.

The binary form is useful for finding bit boundaries. The hexadecimal form is convenient in routing tables and packet headers.

### 2. Network prefix and host part

A prefix is shared by addresses on the same network, while the remaining bits distinguish interfaces or subnets. A mask such as `255.255.255.0` means that the first 24 bits are network bits and the last eight are host bits. Prefix notation writes the same boundary as `/24`.

Given an address and prefix, a host can determine:

- the network address: address AND mask;
- its own host/interface number: address AND inverse mask;
- whether a destination is on the local subnet;
- the gateway to use for a remote destination.

Example:

`192.168.1.130/25`

- `/25` means 25 network bits and 7 host bits.
- Mask: `255.255.255.128`.
- Network address: `192.168.1.128`.
- Broadcast address: `192.168.1.255`.
- Usable host range in this traditional IPv4 subnet: `192.168.1.129` to `192.168.1.254`.

The router uses the prefix, not the first octet alone, to select a route.

### 3. Dotted-decimal conversion

To convert an octet to binary, divide it into powers of two or use its 8-bit representation. For example:

`192 = 128 + 64 = 11000000`  
`168 = 128 + 32 + 8 = 10101000`  
`1 = 00000001`  
`10 = 8 + 2 = 00001010`

The full address is `11000000.10101000.00000001.00001010`.

The first bit of a conventional IPv4 address is the IANA/global-unicast bit, but students should not assume every public or private range from the first octet alone. Prefixes and administrative allocation determine the actual scope.

### 4. Classful history and CIDR

Early IPv4 allocated addresses in classes:

- Class A: first bit 0, historically `/8`;
- Class B: first two bits 10, historically `/16`;
- Class C: first three bits 110, historically `/24`.

The class system wasted address space because an organisation needing a few more than 254 hosts might receive a whole `/16`. **Classless Inter-Domain Routing (CIDR)** allows prefixes of many sizes. A route such as `203.0.113.0/24` identifies 256 total addresses, and the organisation can allocate smaller subnets inside it.

CIDR also supports route aggregation. If several adjacent prefixes share a common prefix, one aggregate route can represent them, reducing routing-table size. A longer, more-specific route overrides a less-specific aggregate when both match.

### 5. Subnet mask and prefix length

A subnet mask is a 32-bit value with a contiguous series of ones for the network portion and zeros for the host portion. Prefix length is simply the number of ones. Examples:

| Prefix | Mask | Host bits | Total addresses | Usable traditional addresses |
|---|---|---:|---:|---:|
| `/24` | `255.255.255.0` | 8 | 256 | 254 |
| `/25` | `255.255.255.128` | 7 | 128 | 126 |
| `/26` | `255.255.255.192` | 6 | 64 | 62 |
| `/27` | `255.255.255.224` | 5 | 32 | 30 |
| `/28` | `255.255.255.240` | 4 | 16 | 14 |
| `/30` | `255.255.255.252` | 2 | 4 | 2 |

The “traditional usable address” count subtracts the network address and directed broadcast address. Some special-purpose links and newer conventions have different host rules, so state the assumption in an exam.

A prefix can be written in dotted decimal, hexadecimal, or CIDR form. The information is the same:

`255.255.255.192 = /26`.

### 6. Address types and scope

**Unicast** identifies one interface. A host sending to a unicast address generally expects a particular recipient.

**Broadcast** identifies all IPv4 interfaces on a particular local subnet in traditional IPv4. A directed broadcast can be `192.168.1.255/24`; a limited broadcast `255.255.255.255` is intended for the local link. Routers normally do not forward ordinary broadcasts between subnets.

**Multicast** identifies a group of receivers. IPv4 multicast addresses conventionally begin in the `224.0.0.0/4` range, with a scope in the address. Multicast routing and group membership are more complex than unicast forwarding.

**Anycast** is more commonly associated with IPv6 but can be implemented in other systems: several interfaces advertise the same address and routing chooses one.

### 7. Public and private IPv4 ranges

RFC 1918 reserves private IPv4 ranges for internal networks:

- `10.0.0.0/8`;
- `172.16.0.0/12` (`172.16.0.0` through `172.31.255.255`);
- `192.168.0.0/16`.

Private addresses are not globally routed on the public Internet. An organisation can use them freely behind a NAT boundary. Public addresses must be allocated and routed globally; simply choosing a number outside the private ranges does not make it a valid public assignment.

There are also special-use ranges such as loopback `127.0.0.0/8`, link-local `169.254.0.0/16`, documentation ranges, and multicast. A complete answer should distinguish “private organizational range” from every reserved range.

### 8. Loopback and link-local addresses

`127.0.0.1` is a loopback address: traffic sent to it stays in the host and tests the local TCP/IP stack. The whole `127.0.0.0/8` is reserved for loopback, not a normal network prefix.

`169.254.0.0/16` is the IPv4 link-local range. A host may self-assign a link-local address when no normal address is available. It is normally valid only on the local link and is not routed through the Internet.

### 9. Static and dynamic address assignment

A **static address** is configured manually and normally remains unchanged. It is easy to document but consumes an address and can be misconfigured.

**DHCP** dynamically leases addresses. A DHCP server gives a client an address, prefix, gateway, DNS servers, lease time, and other options. The lease is renewed before expiry. Dynamic assignment reduces administrative work but depends on the server and correct scope.

A sample DHCP exchange is DHCPDISCOVER, DHCPOFFER, DHCPREQUEST, and DHCPACK. The address is not permanently owned, so a host must renew it.

### 10. Address resolution

To send an IPv4 packet to a destination on the local link, a host needs the destination's link-layer address. **ARP (Address Resolution Protocol)** maps a local IPv4 address to a MAC address. The host broadcasts a request, and the owner replies with its MAC address. The result is cached temporarily.

For a remote destination, the host sends the frame to its default gateway's MAC address while keeping the remote IP destination in the IP packet. This distinction is a common exam point.

### 11. Basic delivery decision

Given local address `192.168.1.10/24` and destination `192.168.1.20`:

1. Apply the `/24` mask to both addresses.
2. Both have network `192.168.1.0/24`.
3. The destination is local, so ARP for `192.168.1.20` and send directly.

For destination `8.8.8.8`, the local network is different. The host sends the IP packet to its default gateway's MAC address. The router forwards the packet through its forwarding table.

### 12. Address exhaustion and IPv6

IPv4 has a finite address space, and public address allocation has been a serious constraint. NAT, DHCP, and careful subnetting reduce internal consumption but do not create a new global IPv4 bit. IPv6 uses 128-bit addresses and a much larger address space, along with a simplified base header and improved support for auto-configuration and extension mechanisms.

IPv6 is not a simple replacement for every application at once. Migration requires compatible endpoints, routers, DNS, security policies, and transition mechanisms.

## Worked examples

### Example 1: Dotted decimal to binary

Convert `172.16.5.130`:

- `172 = 10101100`
- `16 = 00010000`
- `5 = 00000101`
- `130 = 10000010`

Binary: `10101100.00010000.00000101.10000010`.

### Example 2: Find a network address

Address: `10.20.30.40/22`  
Mask: `255.255.252.0`

`10.20.30.40 AND 255.255.252.0 = 10.20.28.0/22`.

The address is not necessarily `10.20.0.0`; the mask determines the boundary.

### Example 3: Host range

Network `192.168.5.0/27` has mask `255.255.255.224`, 5 host bits, and `2^5 = 32` total addresses. Traditional usable hosts are `192.168.5.1` to `192.168.5.30`; `.0` is the network address and `.31` is the broadcast address.

### Example 4: Longest prefix

A router has routes for `0.0.0.0/0`, `10.0.0.0/8`, and `10.1.0.0/16`. Destination `10.1.2.3` matches all three. It chooses `10.1.0.0/16` because it is the most specific.

### Example 5: Local versus remote

A host at `192.168.10.50/25` sends to `192.168.10.70/25`. Both are in `192.168.10.64/25`, so the packet is sent directly. It sends to `192.168.10.200`, which is in a different `/25`; the packet goes to the gateway.

## Key terms & formulas

- **IPv4 address:** 32-bit interface address.
- **Dotted-decimal:** four decimal octets, each 0–255.
- **Octet:** eight bits.
- **Prefix length:** number of leading network bits, written `/n`.
- **Subnet mask:** 1s for network bits and 0s for host bits.
- **Network address:** address AND mask.
- **Host address:** address AND inverse mask.
- **CIDR:** classless prefix allocation and routing.
- **Unicast:** one destination.
- **Broadcast:** all receivers in a local broadcast domain.
- **Multicast:** a group of receivers.
- **Private ranges:** `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`.
- **Loopback:** `127.0.0.0/8`, especially `127.0.0.1`.
- **Link-local:** `169.254.0.0/16`.
- **Total addresses in a subnet:** `2^(32 - prefix length)`.
- **Traditional usable hosts:** `2^h - 2`, where `h` is host bits.
- **Address resolution:** IPv4-to-MAC mapping using ARP on a local link.
- **DHCP:** dynamic address and configuration lease.
- **Maximum IPv4 bit patterns:** `2^32 = 4,294,967,296`.

## Common mistakes

1. **The first octet does not by itself define the network.** The prefix length defines the boundary.
2. **An address is not automatically a subnet or public address.** Scope and allocation matter.
3. **There are 32 bits, not 4 independent addresses.** The octets are parts of one address.
4. **A private address is not routable on the public Internet.** It needs NAT or another translation boundary.
5. **The network and broadcast addresses are not ordinary traditional host addresses.** Exclude them when the question asks for usable hosts.
6. **`127.0.0.1` does not go to a remote host.** It tests the local stack.
7. **ARP is local.** A host does not ARP for a remote IP destination; it uses the gateway's MAC.
8. **A longer prefix is more specific and wins.** Do not choose the first matching route.
9. **Broadcast and multicast are different.** One targets everyone on a local domain; the other targets a group.
10. **NAT does not increase the global IPv4 bit space.** It reuses private addresses at a boundary.
11. **DHCP is not a static address plan.** A lease can change and must be renewed.
12. **Public-looking decimal numbers are not automatically assigned public addresses.** Administrative allocation is required.

## Exam prep

### Likely 2-mark questions

1. **What is an IPv4 address and how many bits does it contain?**  
   Hint: 32-bit interface identifier, normally four dotted-decimal octets.
2. **Explain network and host portions using `192.168.1.10/24`.**  
   Hint: first 24 bits network, last 8 host/interface; mask `255.255.255.0`.
3. **State the three private IPv4 ranges.**  
   Hint: `10/8`, `172.16/12`, and `192.168/16`.
4. **What is CIDR?**  
   Hint: classless prefix-based allocation and routing using `/n`.
5. **Differentiate unicast, broadcast, and multicast.**  
   Hint: one recipient, local all recipients, and a group.
6. **Why is ARP used for a local IPv4 destination?**  
   Hint: obtain the destination MAC address for the local frame.

### Likely long-answer questions

1. **Explain IPv4 address structure, masks, CIDR, and classful history.**  
   Answer hint: 32 bits, dotted decimal, network/host boundary, masks, class limitations, and prefix aggregation.
2. **Calculate the network, broadcast, and usable host range of a given address and prefix.**  
   Answer hint: convert mask, AND the address, count host bits, and state the traditional `-2` assumption.
3. **Explain public, private, loopback, and link-local IPv4 addresses with uses.**  
   Answer hint: ranges, routing scope, ARP/NAT, and examples.
4. **Describe how a host decides between direct delivery and its default gateway.**  
   Answer hint: apply prefix, compare network addresses, ARP locally, and forward remotely.
5. **Explain IPv4 address exhaustion and why IPv6 is needed.**  
   Answer hint: finite 2^32 space, allocation pressure, NAT limitations, and transition needs.

### Short-answer revision checklist

Be ready to convert dotted decimal to binary, calculate a masked network address, identify the most-specific route, state private ranges, and distinguish an IP address from a MAC address and a port.
