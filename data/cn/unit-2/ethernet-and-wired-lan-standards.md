---
subject: cn
unit: 2
topic: ethernet-and-wired-lan-standards
syllabus_ref: CSM3103 Unit-II
status: draft
---
# Ethernet and Wired LAN Standards

## Overview

**Ethernet** is the dominant family of wired LAN technologies. The IEEE 802.3 standard defines Ethernet's physical and data-link operation, while the Ethernet frame format is widely recognised across many speeds and media. A wired LAN connects computers, switches, servers, access points, and routers using frames carried over copper or fibre.

The syllabus asks for IEEE standards, Standard Ethernet, and related LAN concepts. This file explains the IEEE 802.3 family, frame structure, MAC addressing, shared and switched Ethernet, CSMA/CD history, full duplex, common speeds, switch learning, collision/broadcast domains, VLANs, and practical design.

## Explanation

### 1. IEEE 802.3 and the Ethernet family

IEEE 802.3 is the standard family for Ethernet LANs. It specifies the physical layer, including signalling and media, and much of the MAC/data-link behaviour. Standards have evolved from 10 Mbit/s to very high speeds while retaining a broadly compatible frame format.

Common rate families include:

- **10BASE-T:** 10 Mbit/s over twisted pair;
- **100BASE-TX/FX:** 100 Mbit/s Fast Ethernet;
- **1000BASE-T/SX/LX:** 1 Gbit/s Gigabit Ethernet over copper or fibre;
- **10GBASE-T/SR/LR:** 10 Gbit/s Ethernet;
- **40/100/200/400 Gbit/s and beyond:** high-speed data-centre Ethernet.

A full designation describes the data rate, signalling/baseband or medium type, and cable/encoding characteristics. The physical standard can change while the higher-level frame remains broadly similar.

### 2. Why Ethernet is important

Ethernet is inexpensive, widely supported, easy to configure, and available at many rates. Its frame format and MAC service made it suitable for local networks and later for backbone links. Ethernet can carry IP, many other network-layer protocols, and various application protocols.

Ethernet is not automatically an end-to-end reliable service. A frame may be lost, duplicated, or corrupted, and a switch does not provide application-level recovery. IP and TCP provide those higher-layer behaviours.

### 3. Standard Ethernet frame

A conventional Ethernet frame contains:

1. **Preamble:** alternating bits used for clock synchronisation.
2. **Start Frame Delimiter (SFD):** marks the beginning of the frame.
3. **Destination MAC address:** link-layer destination.
4. **Source MAC address:** link-layer source.
5. **Length/Type:** a length for older frames or an EtherType for the upper-layer protocol.
6. **Payload/data:** an IP packet or other data.
7. **Frame Check Sequence (FCS):** normally a 32-bit CRC.
8. **Inter-frame gap:** idle time required between frames.

The original standard Ethernet payload is normally up to 1,500 bytes, the Ethernet MTU. Headers, trailers, and the preamble are not part of the 1,500-byte IP payload. VLAN tagging and hardware encapsulation can change the physical frame overhead, but the basic service is consistent.

The FCS detects many errors. A receiver normally discards a frame with a bad FCS. Ethernet does not normally retransmit the frame itself.

### 4. MAC addressing

A MAC address identifies a local interface on a LAN. It is normally 48 bits, shown as six hexadecimal bytes such as `00:1A:2B:3C:4D:5E`. The first three bytes can identify a manufacturer, though modern administratively assigned addresses and virtualisation make that less reliable.

The source MAC identifies the transmitting interface. The destination MAC identifies the next local interface for a unicast frame. A broadcast address `FF:FF:FF:FF:FF:FF` reaches all interfaces in the broadcast domain. Multicast identifies a group of interested stations.

MAC addresses are normally changed by a router at each hop because they are meaningful only on the local link. A switch learns source addresses and uses the destination address to forward frames.

### 5. Shared Ethernet and CSMA/CD

Early Ethernet used a shared coaxial bus or a hub. All stations shared one collision domain and a common bandwidth. A station used CSMA/CD: sense, transmit while sensing, detect a collision, jam, wait a random backoff, and retry.

The minimum frame length helped ensure that a station could detect a collision before it finished transmitting. The original collision-detection design was appropriate for a shared half-duplex medium. It has low efficiency under heavy load and is not used in normal full-duplex switched Ethernet.

### 6. Switched and full-duplex Ethernet

A **Ethernet switch** learns MAC addresses and forwards frames to a selected port. Each port normally has a separate collision domain. The switch may support full duplex, allowing a station to send and receive simultaneously. In full duplex, there are no collisions and CSMA/CD is disabled.

A switch still operates inside a broadcast domain. A broadcast or an unknown-unicast frame may be flooded to all ports in the relevant VLAN. VLANs create logical LANs, while routing between VLANs is needed to separate Layer-3 broadcast domains.

A modern switched network is scalable, quiet, and easy to manage, but a faulty switch, loop, or misconfigured VLAN can still cause serious problems.

### 7. Ethernet switch learning and forwarding

A switch maintains a MAC/CAM table mapping a learned MAC address to a port. When a frame enters port 3 with source MAC `A`, the switch records `A -> 3`.

Forwarding then works as follows:

- if the destination MAC is known, send the frame to the mapped port;
- if it is unknown, flood the frame to all other ports in the VLAN;
- if it is a broadcast or relevant multicast, flood it according to the VLAN policy;
- if the destination is on the incoming port, filter the frame instead of sending it back.

Entries may age out when traffic stops, allowing a moved device to be relearned. Switches can also use administrative access controls and port security.

### 8. Collision and broadcast domains

A **collision domain** is the region where simultaneous transmissions can interfere. A shared hub or bus is one collision domain; each connected full-duplex switch port is normally its own collision domain.

A **broadcast domain** is the range over which a Layer-2 broadcast is forwarded. A switch normally extends it within a VLAN. A router or a Layer-3 switch separates broadcast domains. This distinction explains why a switch improves performance without automatically limiting broadcasts.

### 9. Interoperability across rates

Fast Ethernet, Gigabit Ethernet, and 10 Gigabit Ethernet use different physical signalling and timing, but an Ethernet frame carries the same basic addresses, type field, payload, and FCS. A switch can connect ports at different speeds if it supports the relevant media and rates. Frames are buffered or paced so one port's speed does not violate the other port's timing.

Autonegotiation allows two devices to advertise supported speed and duplex modes and select a common mode. A mismatch can produce duplex mismatch, late collisions, reduced performance, or apparent loss, so correct configuration matters.

### 10. VLANs and virtual LANs

A VLAN logically groups switch ports or devices into separate LANs. A tag in the Ethernet frame identifies the VLAN. Benefits include segmentation, improved security and broadcast control, and flexibility to place users in logical groups independent of physical cabling. Traffic between VLANs requires a router or Layer-3 switch; a Layer-2 switch alone does not route IP packets between them.

### 11. Full-duplex, half-duplex, and auto-negotiation

Half-duplex permits one direction at a time and can experience collisions on a shared segment. Full-duplex permits simultaneous send/receive and has no collision. Autonegototiation can select the best common mode, but a manually configured mismatch must be avoided.

Full-duplex does not mean the link is guaranteed reliable. It removes the collision mechanism; the FCS still detects corruption and the upper layers still handle loss, ordering, and congestion.

### 12. Link aggregation and design

Link aggregation or EtherChannel combines several physical links into one logical link. It can increase capacity and provide some redundancy, but both ends must agree on the bundle and mode. A spanning-tree protocol prevents Layer-2 loops when redundant switched paths exist.

A good Ethernet design considers switch capacity, port speed, cabling, MTU, VLANs, redundancy, power, security, and management. Fibre may connect buildings or high-speed uplinks, while copper twisted pair is convenient for access ports.

## Worked examples

### Example 1: Learn and forward

A switch receives a frame from source MAC `A` on port 1. It learns `A -> 1`. If the destination is `B`, and `B` is known on port 4, the switch sends only to port 4. If `B` is unknown, it floods within the VLAN until a response teaches it the correct port.

### Example 2: Shared hub

Five PCs connect to a hub. A transmission is repeated to all other ports, and all PCs share one collision domain. Two simultaneous transmissions collide, so the PCs use CSMA/CD and random backoff.

### Example 3: Switched full duplex

Each PC connects to a separate switch port. The link is full duplex, so a PC can upload and download simultaneously. The switch forwards frames by MAC address. There is no collision domain shared between ports and no need for CSMA/CD.

### Example 4: VLAN separation

Ports 1–10 are in VLAN 10 and ports 11–20 in VLAN 20. A broadcast in VLAN 10 reaches ports in VLAN 10, not VLAN 20. A host in VLAN 10 that needs a server in VLAN 20 sends through the Layer-3 gateway.

### Example 5: Rate interoperability

A 1 Gbit/s server connects through a switch to 100 Mbit/s access ports. The switch can forward between speeds, but the 100 Mbit/s port limits the total traffic it can carry. The frame format remains Ethernet even though the physical timing differs.

## Key terms & formulas

- **IEEE 802.3:** Ethernet standard family.
- **Ethernet frame:** Layer-2 unit with addresses, type/length, payload, and FCS.
- **MAC address:** normally 48-bit local link address.
- **Broadcast address:** `FF:FF:FF:FF:FF:FF`.
- **MTU:** standard Ethernet payload limit of 1,500 bytes.
- **FCS:** normally a 32-bit CRC over the Ethernet frame.
- **CSMA/CD:** shared half-duplex collision detection and recovery.
- **Collision domain:** area of possible shared-collision interference.
- **Broadcast domain:** Layer-2 broadcast reach.
- **Switching:** MAC-based frame forwarding.
- **Flooding:** forward to all eligible ports when destination is unknown or broadcast.
- **Full duplex:** simultaneous bidirectional transmission; no CSMA/CD collisions.
- **Autonegototiation:** automatically select common speed/duplex.
- **VLAN:** logical Layer-2 LAN identified by a tag.
- **Link aggregation:** multiple links presented as one logical link.
- **Ethernet rate:** `10BASE-T = 10 Mbit/s`; `1000BASE-T = 1 Gbit/s`.

## Common mistakes

1. **IEEE 802.3 is not just one 10 Mbit/s Ethernet.** It is a family covering many rates and media.
2. **Ethernet FCS detects errors but does not normally repair or retransmit.** Higher layers may recover.
3. **A switch is not a router.** It makes MAC forwarding decisions inside a Layer-2 domain.
4. **A switch separates collision domains, not automatically broadcast domains.** A router or VLAN routing separates broadcasts.
5. **Full-duplex Ethernet does not use CSMA/CD.** It sends and receives simultaneously.
6. **A hub and a switch can have the same physical star shape.** Their logical collision domains differ.
7. **MAC addresses are not global IP addresses.** A router normally changes link-layer addresses per hop.
8. **The 1,500-byte MTU is the payload, not the whole frame.** Headers and FCS add overhead.
9. **An unknown destination causes flooding, not a permanent failure.** The switch learns from later replies.
10. **Different Ethernet speeds can use the same frame format.** Physical signalling and timing still differ.
11. **A VLAN is not automatically a separate IP network.** Inter-VLAN routing is needed for Layer-3 communication.
12. **Autonegotiation cannot create a mode unsupported by one device.** Both ends must share a capability.

## Exam prep

### Likely 2-mark questions

1. **State the role of IEEE 802.3.**  
   Hint: standard family for Ethernet LANs, including physical and MAC operation.
2. **List four fields of an Ethernet frame.**  
   Hint: preamble/SFD, destination/source MAC, type/length, payload, FCS.
3. **What is a 32-bit FCS used for?**  
   Hint: detect many errors in the received frame.
4. **Compare shared and switched Ethernet.**  
   Hint: shared collision domain/CSMA/CD versus per-port domains and MAC forwarding.
5. **Define collision domain and broadcast domain.**  
   Hint: collision interference area versus Layer-2 broadcast reach.
6. **State two benefits of a switch over a hub.**  
   Hint: selective forwarding, full duplex, higher efficiency, and fault isolation.

### Likely long-answer questions

1. **Explain the Ethernet frame format and the purpose of each field.**  
   Answer hint: synchronisation, boundary, addresses, type/length, payload, FCS, and inter-frame gap.
2. **Explain Ethernet switch learning and forwarding, including flooding.**  
   Answer hint: learn source addresses, look up destination, select port or flood, and age entries.
3. **Compare shared CSMA/CD Ethernet and switched full-duplex Ethernet.**  
   Answer hint: collisions, domains, backoff, duplex, performance, and modern use.
4. **Explain VLANs in a switched Ethernet LAN.**  
   Answer hint: tags, broadcast separation, routing, security, and management trade-offs.
5. **Design a wired Ethernet LAN for an office and justify media and device choices.**  
   Answer hint: switch, access ports, fibre uplinks, speed, redundancy, VLANs, and management.

### Short-answer revision checklist

Be able to draw an Ethernet frame, name the 1,500-byte MTU and 32-bit FCS, distinguish collision and broadcast domains, and explain switch learning and full duplex.
