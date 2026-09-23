---
subject: cn
unit: 1
topic: hubs-switches-and-bridges
syllabus_ref: CSM3103 Unit-I
status: draft
---
# Hubs, Switches, and Bridges

## Overview

A **hub**, **switch**, and **bridge** connect computers and LAN segments, but they make different decisions and operate mainly at different layers. A hub simply repeats electrical or optical signals. A switch forwards frames using MAC addresses. A bridge connects two or more LAN segments and decides which frames need to cross between them.

These devices are important in the syllabus because they show how a network can move from a shared medium to a switched LAN. A hub creates a shared collision domain and sends traffic everywhere. A switch learns where stations are and sends a unicast frame only to the appropriate port, reducing unnecessary traffic. A bridge applies similar link-layer learning while connecting separate collision domains or LAN segments.

The distinction affects performance, fault isolation, broadcast behaviour, scalability, and troubleshooting. A modern office network may still call a physical device a “bridge,” but the core idea is link-layer filtering and forwarding.

## Explanation

### 1. Hub: physical-layer repeater

A hub has no frame awareness. It receives a signal on one port and regenerates or repeats it to all other ports. It operates at the **physical layer**.

A hub has one shared collision domain. All stations hear the signal, and if two transmit at once, their signals interfere. A hub also has one shared bandwidth environment, so total traffic and collisions affect all attached devices. Its advantages are simplicity, low cost, and easy connection of basic devices.

A hub does not learn MAC addresses, store forwarding tables, or filter frames. A frame sent to one computer is physically repeated to all other ports. This wastes bandwidth and exposes traffic to more stations, although an Ethernet NIC normally discards a frame not addressed to it.

### 2. Switch: layer-2 frame switch

A switch operates mainly at the **data-link layer**. Each physical port is normally a separate collision domain. The switch receives a frame, examines its source and destination MAC addresses, and forwards it through a selected port.

A learning switch maintains a MAC address table, also called a CAM table:

- when a frame enters port `p` with source MAC `M`, the switch learns that `M` is reachable through `p`;
- if the destination MAC is known, it sends the frame only to that port;
- if the destination is unknown, it may **flood** the frame to all ports except the incoming port;
- broadcasts and some control frames are normally flooded within the VLAN.

A switch therefore reduces unnecessary traffic and permits each port to use its own link capacity. It can support full-duplex links, where sending and receiving happen simultaneously and collisions do not occur. Full-duplex switched Ethernet does not use CSMA/CD.

Switches may also support VLANs, link aggregation, spanning tree, quality of service, and port security. These are features built on the forwarding concept rather than changes to the basic learning task.

### 3. Bridge

A **bridge** is a layer-2 device that connects two or more LAN segments and filters frames according to their addresses. It can be a standalone device or a function inside a switch. It learns which station is on which segment and forwards a frame only to the segment where the destination may reside.

A bridge can reduce unnecessary traffic and extend the logical reach of a LAN. If a destination is on the same segment, the bridge may filter the frame; if it is on another segment, the bridge forwards it. A transparent bridge learns silently, while a source-routing bridge historically used a source route supplied by the sender.

Bridges may be **spanning-tree bridges**. They calculate a loop-free forwarding topology so redundant links do not create forwarding loops. Older token-ring and spanning-tree designs are common exam examples, but the same learning idea is visible in Ethernet switches.

### 4. Hub versus switch

| Feature | Hub | Switch |
|---|---|---|
| Main layer | Physical | Data link |
| Signal/frame awareness | Repeats bits | Reads MAC addresses |
| Destination ports | All other ports | Selected port, or flood if unknown |
| Collision domain | One shared domain | Usually one per port |
| Duplex | Commonly half-duplex | Can be full-duplex |
| Efficiency | Low for busy LANs | Higher |
| Address learning | None | Yes |
| Broadcast | Repeated throughout segment | Flooded within broadcast domain/VLAN |

A switch still floods unknown-unicast and broadcast frames, so it does not eliminate all unnecessary traffic. Its major improvement is learning and selective forwarding for known destinations.

### 5. Bridge versus switch

A bridge is a conceptual or legacy Layer-2 forwarding device; a switch is a high-performance implementation with many ports and advanced features. In current terminology, most Ethernet switches are effectively multiport bridges. The distinction can matter when discussing LAN segmentation, spanning tree, or older token-ring networks.

A bridge connects segments, while a switch provides per-port switching in a single LAN. The important functional question is whether the device makes a MAC-based forwarding decision.

### 6. Collision domain versus broadcast domain

A **collision domain** is the area in which simultaneous transmissions can interfere. A **hub** creates one collision domain; a switch normally creates one collision domain per port.

A **broadcast domain** is the area in which a Layer-2 broadcast is forwarded. A switch normally extends the broadcast domain within a VLAN. To separate broadcast domains, use VLAN-aware routing or a router. This distinction is a frequent exam question.

### 7. Frame forwarding and learning example

Suppose a switch has learned:

- MAC A -> port 1
- MAC B -> port 2
- MAC C -> port 3

If A sends a frame to B, the switch forwards it only through port 2. If A sends a frame to an unknown MAC D, it floods the frame to ports 2 and 3, and then learns D's port if D replies. If A sends a broadcast, all ports in the VLAN receive it because the broadcast destination represents everyone in that domain.

### 8. Advantages and disadvantages

**Hub advantages:** cheap, simple, compatible with basic Ethernet, no learning table required.

**Hub disadvantages:** shared collision domain, shared capacity, unnecessary traffic, poor security, low scalability, and a single medium failure point.

**Switch advantages:** selective forwarding, high throughput, full duplex, per-port isolation, VLAN and management support, and easier fault localisation.

**Switch disadvantages:** cost, configuration complexity, loops if managed poorly, and broadcast flooding. A switch does not by itself provide internetworking or route packets between IP networks.

**Bridge advantages:** filters traffic, extends a LAN, and can support redundant paths with a spanning tree.

**Bridge disadvantages:** learning/configuration complexity and loop risk without loop prevention.

## Worked examples

### Example 1: Hub network

Four PCs connect to a hub. PC A sends a broadcast or a frame to PC B. All other ports receive the electrical signal, even though their NICs may discard the frame. If A and C transmit simultaneously, a collision affects the shared domain.

### Example 2: Switch network

A laptop's MAC address is learned on port 4. When it sends a frame to a printer on port 7, the switch looks up the printer's MAC and forwards the frame only to port 7. Traffic to other users is not repeated, improving available capacity.

### Example 3: Unknown destination

A newly installed device sends a frame before responding to others. The switch may not know its destination MAC, so the switch floods the frame within the VLAN. Once the device sends a reply, the switch learns its port. Flooding is a discovery mechanism, not a sign that the switch has no learning ability.

### Example 4: Bridge connecting LANs

A bridge connects a busy accounting LAN to a small printer LAN. Frames between stations on the accounting LAN can be filtered at the bridge, while printer-bound frames cross. Both LANs remain within the same Layer-2 broadcast domain unless a router or VLAN routing is used.

### Example 5: Fault isolation

A cable connected to a switch port fails. The switch can mark that port down while other ports continue operating. A backbone hub failure may affect every attached device. This illustrates the fault-tolerance advantage of a switched star.

## Key terms & formulas

- **Hub:** physical-layer repeater.
- **Switch:** layer-2 frame-forwarding device.
- **Bridge:** layer-2 device connecting/filtering LAN segments.
- **Repeater:** regenerates a physical signal.
- **Frame:** data-link-layer unit with link addresses and FCS.
- **MAC address table/CAM table:** learned source-MAC-to-port mapping.
- **Selective forwarding:** send a known-unicast frame to one port.
- **Flooding:** send a frame to all eligible ports when its destination is unknown or broadcast.
- **Collision domain:** region of shared collision risk.
- **Broadcast domain:** region reached by a Layer-2 broadcast.
- **VLAN:** logical Layer-2 broadcast/forwarding domain.
- **Full duplex:** simultaneous send and receive, no CSMA/CD collisions.
- **Spanning tree:** loop-prevention forwarding topology.
- **Forwarding delay:** time for a switch to receive, process, and transmit a frame.
- **Store-and-forward / cut-through:** buffering the whole frame or forwarding after minimal reading.

## Common mistakes

1. **A hub does not forward only to the destination.** It repeats signals to all other ports.
2. **A switch is more than a repeater.** It reads frame addresses and makes a forwarding decision.
3. **A switch separates collision domains, not automatically broadcast domains.** VLAN routing or a router separates broadcasts.
4. **A bridge and a switch are closely related.** A switch is usually a fast, multiport, feature-rich bridge implementation.
5. **Full-duplex Ethernet has no CSMA/CD collisions.** It can send and receive simultaneously.
6. **Flooding is normal for unknown destinations and broadcasts.** It does not mean every known frame is sent everywhere.
7. **A switch does not replace the router.** It does not inherently route between IP networks.
8. **A bridge does not guarantee loop freedom.** Spanning tree or an equivalent mechanism is required.
9. **One failed cable on a star does not always take down the network.** A switch can isolate the affected port.
10. **MAC learning uses source addresses.** The switch observes where a sender is, not the destination's future location.

## Exam prep

### Likely 2-mark questions

1. **Compare a hub and a switch with respect to OSI layer and forwarding.**  
   Hint: hub repeats at physical; switch learns MAC addresses at data link.
2. **Define collision domain and broadcast domain.**  
   Hint: shared collision risk versus Layer-2 broadcast reach.
3. **Why does a switch reduce unnecessary LAN traffic?**  
   Hint: selective forwarding to the known destination port.
4. **What is the purpose of a MAC address table?**  
   Hint: map learned source MAC addresses to switch ports.
5. **What is a bridge?**  
   Hint: a Layer-2 device that connects/filter LAN segments using addresses.
6. **Why can a switched full-duplex LAN avoid collisions?**  
   Hint: separate collision domain per port and simultaneous send/receive.

### Likely long-answer questions

1. **Compare hubs, bridges, and switches in detail.**  
   Answer hint: layer, forwarding, learning, domains, duplex, performance, cost, and examples.
2. **Explain how a self-learning Ethernet switch forwards a frame.**  
   Answer hint: learn source-to-port, look up destination, select or flood, and handle broadcast.
3. **Explain collision domains and broadcast domains with a hub/switch/router diagram.**  
   Answer hint: show one hub domain, per-port switch domains, and a router boundary.
4. **Why have switched Ethernet largely replaced hub Ethernet?**  
   Answer hint: full duplex, selective forwarding, higher capacity, fault isolation, and scalability.

### Short-answer revision checklist

Be ready to draw a hub, switch, bridge, router, and VLAN arrangement, and state which layer each uses and which domains it separates.
