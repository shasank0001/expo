---
subject: cn
unit: 3
topic: ip-subnetting
syllabus_ref: CSM3103 Unit-III
status: draft
---
# IP Subnetting

## Overview

**Subnetting** divides one IP network prefix into smaller subnets. An organisation may receive a `/16` or `/20` allocation and create subnets for departments, buildings, labs, or point-to-point links. Subnetting improves address organisation, reduces the size of broadcast domains when routers are used, supports different communication needs, and makes routing summaries possible.

The key idea is a prefix boundary. A subnet mask has a contiguous block of 1 bits for the network/subnet portion and zeros for the host portion. If `h` host bits remain, the subnet has `2^h` total addresses. In ordinary traditional IPv4, the all-zero host value is the network address and the all-one host value is the directed broadcast address, leaving `2^h - 2` usable host addresses.

Subnets must be aligned to powers of two. A careless division can create overlapping or unreachable subnets. This file develops the binary method, equal and variable-length subnetting, route summarisation, and worked numerical examples.

## Explanation

### 1. Why subnet?

Without subnetting, a large allocated network could be treated as one huge broadcast domain. Routers would need to know about every host, broadcasts could reach many devices, security groups would be difficult to isolate, and address space might be used inefficiently.

With subnetting, an administrator extends the prefix length. For example, a `10.0.0.0/8` allocation can be divided into `10.0.0.0/16`, `10.1.0.0/16`, and so on. Each `/16` is a separate subnet if a router connects them. Subnets can use different prefix lengths to match their size—variable-length subnetting (VLSM).

Subnetting does not by itself provide encryption, complete security, or guaranteed bandwidth. It provides logical and routing separation; firewalls, access lists, VLANs, and security policy add protection.

### 2. Mask and host bits

A subnet mask has network bits set to 1 and host bits set to 0. For prefix length `/n`, there are `n` network bits and `32 - n` host bits.

Examples:

- `/24`: mask `255.255.255.0`, 8 host bits.
- `/26`: mask `255.255.255.192`, 6 host bits.
- `/28`: mask `255.255.255.240`, 4 host bits.

The network address is the address with all host bits zero. The traditional directed broadcast address is the address with all host bits one. The usable range lies between them:

- first usable: network + 1;
- last usable: broadcast - 1;
- total addresses: `2^h`;
- usable hosts: `2^h - 2`.

The `-2` rule is not applied to every special-purpose network in every modern protocol. In an exam, state that the calculation assumes an ordinary IPv4 subnet that reserves network and broadcast addresses. A `/31` point-to-point link and `/32` host route are special cases with different conventions.

### 3. Equal-sized subnetting

An equal split changes the prefix by `k` bits, creating `2^k` equal subnets:

- borrow 1 bit -> 2 subnets;
- borrow 2 bits -> 4 subnets;
- borrow 3 bits -> 8 subnets;
- borrow 4 bits -> 16 subnets.

To split a `/24` into four `/26` subnets, borrow two host bits. The subnets are:

- `192.168.1.0/26`: `.0`–`.63`, usable `.1`–`.62`
- `192.168.1.64/26`: `.64`–`.127`, usable `.65`–`.126`
- `192.168.1.128/26`: `.128`–`.191`, usable `.129`–`.190`
- `192.168.1.192/26`: `.192`–`.255`, usable `.193`–`.254`

The total usable capacity is `4 x 62 = 248` hosts, less than the original `/24`'s 254 because the new subnet boundaries consume four network and four broadcast addresses.

### 4. Binary subnetting method

To subnet an address:

1. Write the original address in binary.
2. Write the original prefix and count the host bits.
3. Borrow the desired number of bits from the host portion.
4. Make the new subnet bits vary through all combinations.
5. Convert each resulting prefix and range back to dotted decimal.
6. Check alignment: the new prefix boundary must fall on a valid power-of-two block.

For example, `192.168.1.0/24` is:

`11000000.10101000.00000001.00000000`

Borrowing two bits creates `/26` boundaries `00`, `01`, `10`, `11` in the former host portion:

- `00` -> `.0/26`
- `01` -> `.64/26`
- `10` -> `.128/26`
- `11` -> `.192/26`

The binary method prevents the common mistake of choosing subnet starts that are not aligned.

### 5. Variable-length subnetting (VLSM)

**VLSM** assigns different prefix lengths according to host requirements. Allocate the largest requirement first, then smaller networks, and finally point-to-point links.

Suppose a company needs:

- one subnet for 500 hosts;
- two subnets for 100 hosts each;
- two subnets for 50 hosts each;
- four point-to-point links.

A traditional calculation is:

- 500 hosts: `2^9 - 2 = 510`, so `/23`;
- 100 hosts: `2^7 - 2 = 126`, so `/25` each;
- 50 hosts: `2^6 - 2 = 62`, so `/26` each;
- point-to-point links may use `/30` or `/31` depending on the design.

VLSM uses fewer addresses than equal subdivision. The allocated blocks must not overlap, and the router's connected routes must cover every subnet.

### 6. Subnet selection from a requirement

To choose a prefix for `H` hosts, find the smallest `h` such that:

`2^h - 2 >= H`

Then prefix length is:

`p = 32 - h`

Examples:

- 50 hosts: `h = 6` because `2^6 - 2 = 62`; use `/26`.
- 100 hosts: `h = 7` because `126 >= 100`; use `/25`.
- 500 hosts: `h = 9` because `510 >= 500`; use `/23`.

For 254 hosts, `h = 8` gives 254, so `/24` is the smallest ordinary subnet. If the question requires a network and broadcast reservation, do not choose `/25` merely because it has 128 total addresses.

### 7. Subnet zero and all-ones subnets

Older classful routing conventions sometimes treated subnet zero and the all-ones subnet as unusable. Modern CIDR and common routing systems permit all correctly aligned subnets, including `.0` and the last block, as long as the organisation follows current conventions. In an exam, mention the assumption rather than blindly excluding them.

The network and broadcast addresses within a subnet remain special under the traditional model. A router interface uses its subnet's network address for the connected route, not as an ordinary host destination.

### 8. Broadcast domains and routers

A subnet is normally a separate Layer-3 broadcast domain when routers separate the subnets. A switch can connect hosts within one subnet, but a router or Layer-3 switch is needed to move packets between subnets. A VLAN is a Layer-2 broadcast domain; different VLANs require routing even if they use the same IP subnet? In a correctly designed network, VLANs and IP subnets are usually coordinated.

Subnetting reduces the number of hosts that receive a directed broadcast, but it can increase the number of connected routes and routing-table entries. Route summarisation can reduce those entries.

### 9. Route summarisation

A router can represent several adjacent subnets with one aggregate route if they share a common prefix. For example:

- `192.168.0.0/24`
- `192.168.1.0/24`
- `192.168.2.0/24`
- `192.168.3.0/24`

can be summarised as `192.168.0.0/22` because their first 22 bits are identical. The summary covers `192.168.0.0` through `192.168.3.255`. A more specific route can still override the aggregate.

Summarisation reduces table size and update traffic but may advertise or route to an unused block if the summary is too broad. A more-specific route can still override the aggregate.

### 10. Address calculation checklist

For every numerical subnet question:

1. Convert the address to binary.
2. Determine the prefix and host bits.
3. Calculate total and usable addresses.
4. Find aligned subnet boundaries.
5. Write network, usable range, and broadcast.
6. Check that two subnets do not overlap.
7. State special conventions explicitly.

## Worked examples

### Example 1: Basic `/27`

Given `172.16.40.0/27`:

- prefix = 27, host bits = 5;
- total = `2^5 = 32`;
- mask = `255.255.255.224`;
- network = `172.16.40.0`;
- usable = `172.16.40.1`–`172.16.40.30`;
- broadcast = `172.16.40.31`.

### Example 2: Split a `/24` into `/28`

Borrow four bits: `2^4 = 16` subnets.

- `192.168.10.0/28`
- `192.168.10.16/28`
- `192.168.10.32/28`
- `192.168.10.48/28`
- `192.168.10.64/28`
- `192.168.10.80/28`
- `192.168.10.96/28`
- `192.168.10.112/28`
- `192.168.10.128/28`
- `192.168.10.144/28`
- `192.168.10.160/28`
- `192.168.10.176/28`
- `192.168.10.192/28`
- `192.168.10.208/28`
- `192.168.10.224/28`
- `192.168.10.240/28`

Each has 16 total and 14 traditional usable addresses.

### Example 3: VLSM allocation

From `192.168.0.0/22`, allocate:

1. `/23` -> `192.168.0.0/23`, covering `.0.0`–`.1.255`.
2. `/25` -> `192.168.2.0/25`, covering `.2.0`–`.2.127`.
3. `/25` -> `192.168.2.128/25`, covering `.2.128`–`.2.255`.
4. `/26` -> `192.168.3.0/26`, covering `.3.0`–`.3.63`.
5. `/26` -> `192.168.3.64/26`, covering `.3.64`–`.3.127`.
6. `/30` links can be placed in the next aligned blocks, such as `192.168.3.128/30`, `192.168.3.132/30`, and so on.

This demonstrates why VLSM needs alignment and a complete address map.

### Example 4: Wrong boundary

A student tries to create `192.168.1.100/26` and `192.168.1.164/26`. The first block is actually `192.168.1.64/26`; the second is `192.168.1.128/26`. Arbitrary starts overlap or leave holes. Always use the aligned network address.

### Example 5: Route decision

A router receives a packet for `10.2.3.4` and has `10.0.0.0/8` and `10.2.0.0/16`. The `/16` route is more specific and is selected. Subnet boundaries therefore affect forwarding as well as address planning.

## Key terms & formulas

- **Subnet:** a smaller network created by extending a prefix.
- **Subnet mask:** contiguous 1s for network bits and 0s for host bits.
- **Prefix length:** `/n`; `n` network bits.
- **Host bits:** `h = 32 - n`.
- **Total addresses:** `2^h`.
- **Traditional usable hosts:** `2^h - 2`.
- **Network address:** all host bits 0.
- **Broadcast address:** all host bits 1.
- **Borrowing `k` bits:** creates `2^k` equal subnets.
- **Smallest prefix for H hosts:** choose `h` with `2^h - 2 >= H`, then `p = 32 - h`.
- **VLSM:** different prefix lengths for different needs.
- **CIDR:** classless allocation and route prefixes.
- **Route summary:** one aggregate prefix for adjacent subnets.
- **Subnet start:** first address of an aligned block.
- **Example `/26`:** 6 host bits, 64 total, 62 traditional usable.

## Common mistakes

1. **Forgetting to exclude network and broadcast addresses.** A `/26` has 62 traditional usable hosts, not 64.
2. **Using the wrong mask.** `/26` is `255.255.255.192`, not `.224`.
3. **Choosing unaligned subnet boundaries.** A subnet starts at a multiple of its block size.
4. **Using the first octet instead of the prefix.** The prefix defines the network boundary.
5. **Counting a router interface as a host without considering special links.** State the ordinary-subnet assumption or use `/30`, `/31`, `/32` as appropriate.
6. **Allocating subnets from largest to smallest without checking alignment.** VLSM still needs a precise map.
7. **Assuming all equal subnets are efficient.** Different host requirements justify VLSM.
8. **Summarising non-adjacent networks.** A single aggregate covers only a common contiguous prefix.
9. **Thinking a subnet is automatically a physical network.** It is logical addressing; routers and links implement connectivity.
10. **Confusing a subnet network address with a usable host address.** The router uses `.0` as the network identifier in the traditional model.

## Exam prep

### Likely 2-mark questions

1. **Define subnetting and give two benefits.**  
   Hint: divide a network; address organisation, broadcast control, routing, and security segmentation.
2. **Calculate usable hosts for a `/27`.**  
   Hint: 5 host bits, `2^5 - 2 = 30`.
3. **What is the subnet mask for `/25`?**  
   Hint: `255.255.255.128`.
4. **State the network and broadcast addresses of `192.168.1.0/28`.**  
   Hint: network `.0` and broadcast `.15`.
5. **What is VLSM?**  
   Hint: allocate different prefix lengths according to host requirements.
6. **Why must subnet boundaries be aligned?**  
   Hint: each prefix denotes a fixed-size block; arbitrary boundaries overlap or leave holes.

### Likely long-answer questions

1. **Explain subnetting and calculate a complete subnet table.**  
   Answer hint: binary prefix, borrowed bits, every range, broadcast, usable range, and host count.
2. **Perform VLSM for a given address and host requirements.**  
   Answer hint: sort largest first, choose prefixes, align blocks, check non-overlap.
3. **Explain route summarisation with an example and its trade-off.**  
   Answer hint: common prefix, table reduction, and risk of an overly broad aggregate.
4. **Design subnets for a college and explain routing and broadcast effects.**  
   Answer hint: departments, labs, point-to-point links, routers, connected routes, and security.

### Short-answer revision checklist

Be ready to convert a `/24` into `/26` or `/28` subnets, calculate host counts, identify masks, apply longest-prefix matching, and explain why `-2` appears in ordinary IPv4 subnet questions.
