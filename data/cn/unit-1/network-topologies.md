---
subject: cn
unit: 1
topic: network-topologies
syllabus_ref: CSM3103 Unit-I
status: draft
---
# Network Topologies

## Overview

A **network topology** is the arrangement of nodes and links in a network. The arrangement may describe the cables and devices that physically exist (**physical topology**) or the paths over which frames logically flow (**logical topology**). A topology matters because it affects cost, cable length, fault isolation, performance, scalability, and ease of management.

There is no universally best topology. A bus is inexpensive for a small area, a star is easy to manage in an office, a ring can provide orderly access, and a mesh offers high availability. A tree is useful for large campuses, while a hybrid combines layouts to suit different parts of an organisation.

The syllabus also connects topology to data flow and network criteria. If every station shares a long backbone, a cable failure can affect the whole network. If each station has a dedicated link to a central switch, one cable failure is local. If a critical network needs continued operation after a link failure, redundant mesh links may justify their cost.

## Explanation

### 1. Basic terms

A **node** is a device attached to the network, such as a computer, printer, switch, router, or access point. A **link** is a communication path between nodes. The topology can be represented as vertices and edges in a graph or drawn with symbols.

The **physical topology** shows the actual arrangement of cables, rooms, and equipment. The **logical topology** shows how data travels and which device controls access. These do not have to match. A physically star-shaped Ethernet network with a central switch is logically point-to-point because each switch port has its own link. An old hub-based physical star has a shared logical Ethernet segment.

### 2. Bus topology

In a **bus topology**, all nodes attach to one shared backbone, and the signal travels along the backbone in both directions. Terminators absorb the signal at the ends. This arrangement uses relatively little cable and was common in early Ethernet.

Advantages include low cable cost, simple connection for a small installation, and easy communication between any two stations. Disadvantages include a single point of failure: a break in the backbone can divide or disable the network. Every station can hear traffic on the shared medium, so faults and electrical loading are harder to isolate. Performance decreases as traffic and length grow, and a failed terminator can create reflections.

A bus is therefore attractive for a small, controlled installation, but less attractive where availability and easy fault isolation are priorities. Modern Ethernet installations usually use a star with a switch because a switch breaks the shared collision domain and gives each station a dedicated path.

### 3. Star topology

In a **star topology**, each node has a separate link to a central device, traditionally a hub and now usually a switch. The central device repeats or forwards signals.

With a hub, all stations share the same collision domain and the hub repeats incoming bits to all other ports. With a switch, each port normally has its own collision domain, and the switch forwards frames using MAC addresses. The physical shape remains a star even though the logical traffic path depends on the switch.

Advantages include easy installation and removal of one station, local fault isolation, and straightforward central management. A failed station cable usually affects only that station. A switch also reduces unnecessary traffic. Disadvantages include the need for more cable, a dependency on the central device if it fails, and a port/cable cost for every node. A smart switch can mitigate the central-device risk through redundancy and stacking.

### 4. Ring topology

In a **ring topology**, each node connects to two neighbours and the links form a closed loop. Data moves from one node to the next. A **dual ring** can provide an alternate direction if one link fails, but it is more complex.

A ring can make access orderly: Token Ring historically passed a permission token around the ring, so only the token holder transmitted. This reduces collisions compared with uncontrolled random access. Its disadvantages include sensitivity to a single link or node failure, more difficult troubleshooting, and possible delay as the token travels around the ring. Protection mechanisms can bypass a failed node or use two paths.

### 5. Mesh topology

A **mesh topology** connects nodes through multiple paths. A **full mesh** has a direct link between every pair. A **partial mesh** has some redundant paths but not all possible links.

The major strength is fault tolerance. If one link fails in a redundant mesh, traffic can use another route. Mesh also offers predictable performance and can distribute traffic. Its disadvantages are very high cable cost, many interfaces, complex administration, and possible congestion on alternative links after a failure. Full mesh is normally justified only for small numbers of critical nodes or backbone links.

### 6. Tree and hybrid topologies

A **tree topology**, also called a hierarchical topology, has a root and branches. It scales well because a network can be divided into smaller domains connected through a central backbone. A failure can be localized to a branch, but a failure near the root can affect many users. Tree designs are common in large campus and enterprise networks.

A **hybrid topology** combines layouts. An enterprise may use a star in each office floor, a ring or redundant backbone between buildings, and a tree-like hierarchy of routers. The physical and logical views can differ at different levels. A good hybrid design uses each topology where its strengths are useful.

### 7. Physical versus logical topology

A physical question asks **where are the cables and devices?** A logical question asks **how are frames delivered and who controls the medium?**

Example: Five computers may be wired to a central hub in a physical star, but the logical topology is a shared bus because every transmission reaches every port. If the hub is replaced with a switch and the same cables remain, the physical topology is unchanged while the logical topology becomes a switched star or set of point-to-point links.

Another example: a wireless mesh uses radio links and a multi-hop path. It may look like a star at the access point but use a logical path through several repeaters. Topology must therefore be described at the level being studied.

### 8. Selection criteria

When selecting a topology, ask:

- **Cost:** cable, ports, installation, maintenance, and replacement cost.
- **Scalability:** how many more nodes and how much traffic can be added?
- **Performance:** contention, delay, bandwidth, and error rates.
- **Fault tolerance:** what happens after a cable, node, or central-device failure?
- **Security:** how easily can traffic be intercepted or segmented?
- **Management:** how easy is monitoring, reconfiguration, and troubleshooting?
- **Physical constraints:** distance, building layout, and interference.

A star is often best for a modern office because switches provide predictable performance and easy per-port management. A mesh may be best for a high-availability backbone. A bus may be acceptable in a small isolated network but should not be chosen merely because it uses less cable.

## Worked examples

### Example 1: Office layout

Twenty office PCs connect to a central managed switch with one cable per PC. The physical topology is a star, and with a switch each port is a separate collision domain. A failed PC cable affects one port; a switch failure affects the whole office unless the switch is redundant.

### Example 2: Campus design

Each department has a star network. Department networks connect to a backbone through a hierarchical tree of switches and routers. A failure in one department may be contained, while the backbone provides shared connectivity. This is a hybrid topology.

### Example 3: High-availability core

Two core switches are connected by several links. If one link fails, traffic can use another, and the switches can fail over. This is a partial mesh rather than a full mesh. The design improves fault tolerance but uses more ports and may need loop-prevention mechanisms.

### Example 4: Physical and logical mismatch

A cable layout with one computer connected to a central hub is physically a star. Since a hub repeats every frame to all ports, it is logically a shared bus/collision domain. Replacing the hub with a switch changes the logical behaviour without moving a cable.

### Example 5: Ring failure

A ring with a single link break may stop traditional unidirectional ring operation. A dual ring or bypass mechanism can keep the network running in the opposite direction. This illustrates why fault tolerance can justify extra cost.

## Key terms & formulas

- **Topology:** physical or logical arrangement of nodes and links.
- **Node/host:** device that sends or receives network data.
- **Link:** connection between nodes.
- **Bus:** shared backbone arrangement.
- **Star:** one central connection point with separate node links.
- **Ring:** closed loop of nodes.
- **Mesh:** multiple paths between nodes; full or partial.
- **Tree/hierarchical:** branches from a root or hierarchy of levels.
- **Hybrid:** combination of topologies.
- **Physical topology:** actual cable/device arrangement.
- **Logical topology:** path and access behaviour seen by frames.
- **Fault tolerance:** ability to continue after a failure.
- **Scalability:** ability to grow without unacceptable performance loss.
- **For a full mesh of `n` nodes:** `n(n - 1) / 2` point-to-point links.
- **For a star of `n` nodes:** `n` links to the centre.
- **For a bus or ring of `n` nodes:** roughly `n` physical links in a simple implementation.

## Common mistakes

1. **Topology is not just the drawing.** Include physical and logical meaning and the traffic/access behaviour.
2. **A hub-based star is not automatically a modern switched LAN.** Its logical collision domain is shared.
3. **A switch does not create one broadcast domain in every design.** It normally separates collision domains; VLANs or routers are needed to separate broadcast domains.
4. **Ring is not automatically fault tolerant.** A single unprotected break can disrupt a basic ring.
5. **Mesh is not always the best network.** Redundancy improves availability but increases cost and management complexity.
6. **Do not confuse a tree with a bus.** A tree has hierarchical branches; a bus is a shared backbone.
7. **A full mesh and a partial mesh are different.** Full mesh has every possible node-to-node link; partial mesh has some redundancy.
8. **Physical and logical topologies can differ.** Describe both when asked.
9. **Scalability is not the same as speed.** A topology may grow well but become congested without adequate bandwidth.
10. **A central device is a single point of failure unless redundancy is provided.** A star is easy to manage, but resilience depends on the centre and power.

## Exam prep

### Likely 2-mark questions

1. **Define topology and distinguish physical from logical topology.**  
   Hint: actual cables/devices versus the path and access method.
2. **Draw or describe bus and star topologies.**  
   Hint: one shared backbone versus one separate link per node to a central device.
3. **Give one advantage and one disadvantage of mesh.**  
   Hint: fault tolerance versus cost/complexity.
4. **What is a hybrid topology?**  
   Hint: a design that combines two or more topology types.
5. **Why is a star common in Ethernet LANs?**  
   Hint: easy per-station fault isolation and switch-based performance.

### Likely long-answer questions

1. **Compare bus, star, ring, mesh, tree, and hybrid topologies with diagrams and selection criteria.**  
   Answer hint: define each, discuss cost, performance, fault tolerance, scalability, and management, then recommend a topology for a stated scenario.
2. **Explain physical and logical topology with an Ethernet example.**  
   Answer hint: compare hub and switch while keeping the cable arrangement unchanged.
3. **Design a network for a college campus and justify the topology.**  
   Answer hint: propose star access in departments, a hierarchical backbone, redundant links for critical areas, and explain fault isolation and scalability.
4. **Explain why a full mesh is not normally used for hundreds of hosts.**  
   Answer hint: calculate `n(n - 1)/2` links and discuss cost, ports, and management.

### Short-answer revision checklist

Be ready to draw all six layouts, give a realistic device for each, and explain the difference between a physical star and a logical shared segment.
