---
subject: cn
unit: 5
topic: peer-to-peer-networks
syllabus_ref: CSM3103 Unit-V
status: draft
---
# Peer-to-Peer Networks

## Overview

A **peer-to-peer (P2P)** network lets user computers act as both clients and servers. Instead of relying permanently on one central data server, peers exchange files, messages, computing work, or other resources directly or through an overlay network.

P2P systems can be centralised in discovery but decentralised in data transfer. A BitTorrent swarm is a familiar example: seeders and leechers exchange file pieces. A distributed hash table (DHT) can locate a peer holding a requested resource. P2P is scalable in some senses, but peers may join, leave, be malicious, or have unequal capacity.

The syllabus lists P2P networks under content delivery. This file covers centralized/decentralized/hybrid models, overlays, bootstrapping, DHTs, swarms, seeding, contribution, incentives, churn, security, NAT, and applications.

## Explanation

### 1. Client-server versus peer-to-peer

In a client-server system, a permanent server stores the main resource and clients request it. The server has a central point of control and a predictable source, but its capacity and availability are bottlenecks.

In P2P, each participating node can request and supply data. A node may download from several peers and upload to others. There is no requirement that one peer hold the complete resource at all times.

P2P does not mean every peer has equal bandwidth or that the system is always decentralised. Many deployments use a tracker, rendezvous server, or bootstrap service for discovery, while data is exchanged peer-to-peer.

### 2. Overlay network

A P2P overlay is a logical network formed by nodes and logical links on top of the Internet. The underlying TCP/IP still supplies IP forwarding, while the P2P protocol defines how peers discover one another, locate resources, and exchange data.

An overlay can use:

- direct connections between peers;
- indirect routing through a relay;
- a DHT for resource lookup;
- a tracker or rendezvous service;
- structured or unstructured membership.

The overlay is not a replacement for IP networks. It adds an application-level coordination layer.

### 3. Centralised, decentralised, and hybrid P2P

**Centralised P2P-style design:** a central index/server knows peers and coordinates them, but peers exchange data. This is often called centralised P2P because discovery is central.

**Pure decentralised P2P:** peers bootstrap from known addresses, gossip membership information, and locate resources without a central directory. This is more resilient but can be harder to join and secure.

**Hybrid P2P:** combines a central service for discovery/bootstrap with decentralised data exchange. BitTorrent commonly follows this pattern through trackers, although DHTs can remove the need for a tracker for some operations.

### 4. Bootstrapping and peer discovery

A new peer needs at least one known address, a tracker URL, a rendezvous service, or a previously cached peer list. The bootstrap process contacts a known node, receives information about other peers, and joins the overlay.

A central tracker can provide a list of peers and announce new peers. It can be spoofed or become a single point of failure. A decentralised method can use known addresses, gossip, cached routing tables, or a DHT.

Peer addresses may change, peers may be behind NAT, and churn can make a previously valid list stale. A robust system measures reachability and removes dead peers.

### 5. Distributed hash table (DHT)

A **distributed hash table** maps a resource key to one or more responsible peers. Each peer stores a small portion of the routing table rather than a complete directory.

A client hashes a resource identifier, such as a file's infohash or a key/value name. It looks for the closest responsible node in an overlay identifier space. That node either has the resource or knows another peer closer to the key. The process is similar to routing in a structured overlay.

DHT benefits include decentralised lookup and scalability. Challenges include:

- joining and maintaining the overlay;
- churn and node failure;
- NAT/firewall reachability;
- malicious peers poisoning routing information;
- inconsistent replication and data validation;
- lookup latency across many hops.

A DHT locates a resource; it does not automatically guarantee that the resource is authentic or safe. Content hashes can verify integrity if a trusted expected hash is known, but a malicious swarm can distribute a different file under the same name.

### 6. File swarms and pieces

A BitTorrent-style file is divided into pieces, and each piece is further divided into fixed-size blocks. Peers advertise which pieces they have. A downloader selects pieces from several peers, verifies them against the piece hashes, and uploads pieces to other peers.

A **seeder** has the complete file; a **leecher** is downloading it and may become a seeder after completion. Peers exchange chunks in parallel, so a slow source is not the only bottleneck. A peer may use upload bandwidth, seeding policy, and tit-for-tat behaviour to decide what to send.

A malicious peer may send incorrect pieces. Hash checking and peer selection reduce the risk, but a correctly hashed malicious file can still contain harmful content. Users need a trusted source or signature.

### 7. Unstructured versus structured P2P

An **unstructured P2P** system uses flooding, gossip, or random walks to discover peers/resources. It is flexible but lookup can be slow and traffic-heavy.

A **structured P2P** system uses a defined key space and routing rules, often implemented with a DHT. Lookup can be efficient and predictable, but joining, maintenance, and resistance to churn require design.

Some systems combine both: a DHT for structured resources and gossip or trackers for discovery and special events.

### 8. Incentives and fair contribution

A P2P network must discourage a peer that downloads without uploading. Strategies include:

- tit-for-tat reciprocal behaviour;
- weighted fairness based on upload rate;
- token or reputation systems;
- priority for trusted or seed-like peers;
- bandwidth caps and rate limits;
- penalties for repeated bad behaviour.

Incentives should account for asymmetric connections and temporary offline periods. A strict tit-for-tat rule can punish new peers that have not yet uploaded, so bootstrapping mechanisms are needed.

### 9. Churn and availability

Churn is the normal joining and leaving of peers. The system must handle:

- a peer disappearing mid-transfer;
- stale peer lists;
- routing-table repair;
- source/seeder disappearance;
- intermittent connectivity;
- a malicious peer flooding false availability;
- NAT mappings changing.

Replication of important pieces, multiple paths, and periodic validation improve availability. A single seeder is a single point of failure even if every other peer is healthy.

### 10. NAT, firewalls, and reachability

Peers may be behind NAT, firewalls, or carrier-grade restrictions. Direct connections can be impossible, so a system may use:

- direct NAT traversal;
- relay nodes;
- hole punching;
- rendezvous techniques;
- trackers or introducers;
- IPv6 where available.

A relay can improve connectivity but costs bandwidth and may expose traffic metadata. A P2P design must distinguish whether a peer is merely offline from whether it is unreachable behind NAT.

### 11. Security and privacy

P2P can distribute unauthorised or malicious content. Risks include:

- fake files and poisoned pieces;
- malicious peers and code;
- deanonymisation through peer addresses;
- tracking and correlation;
- eclipse attacks in structured overlays;
- Sybil attacks, where one participant creates many identities;
- poisoning of a DHT or tracker.

Hashes, signatures, reputable sources, peer authentication, reputation, and careful client sandboxing help. Privacy may require encryption, onion routing, or limited peer information, but strong anonymity can reduce performance and trust.

### 12. Applications beyond file sharing

P2P concepts are used for:

- content distribution;
- software updates;
- distributed storage;
- backup and archival replication;
- volunteer computing;
- instant messaging/presence;
- collaborative systems;
- IoT and sensor data exchange;
- decentralised search.

A P2P system can reduce origin-server load but needs mechanisms for discovery, integrity, fairness, and abuse prevention.

## Worked examples

### Example 1: BitTorrent swarm

A seeder has a complete film. Three leechers connect and exchange different pieces. Each downloads from several peers and uploads pieces to others. The seeder's load falls because the peers act as small caches and relays.

### Example 2: DHT lookup

A client hashes a resource name to a 160-bit key. It contacts the peer whose overlay ID is closest to the key. The peer returns another peer closer to the key or the location of the resource. Several hops locate the responsible peer without a central directory.

### Example 3: Churn

A peer disconnects while serving a piece. Other peers notice the failed connection, update the peer list, and request the missing piece from a different source. The DHT removes or refreshes stale entries.

### Example 4: Malicious file

A peer provides pieces that match the expected piece hash, so local integrity checks pass, but the complete file is not the authorised release. A trusted signature or independent hash is needed; piece hashes alone only detect accidental or inconsistent data.

### Example 5: Hybrid design

A tracker tells a new client which peers are available. The tracker is then removed from the data path; peers exchange pieces directly and use DHT gossip for discovery. If the tracker fails, existing peers may continue but new peers may need another bootstrap method.

## Key terms & formulas

- **P2P:** peer-to-peer network.
- **Peer:** node that can request and supply resources.
- **Overlay:** logical network over the Internet.
- **Centralised/decentralised/hybrid:** discovery/control structure.
- **Bootstrap:** initial method for joining.
- **DHT:** distributed hash table for structured lookup.
- **Resource key/hash:** identifier used to locate content.
- **Swarm:** group of peers sharing one torrent/resource.
- **Seeder:** peer with all pieces.
- **Leecher:** peer currently downloading.
- **Piece/block:** content division used for selective transfer.
- **Churn:** peers joining/leaving.
- **NAT traversal:** techniques to establish peer connections.
- **Sybil attack:** many identities controlled by one attacker.
- **Eclipse attack:** attackers surround a target in an overlay.
- **Tit-for-tat:** reciprocal upload/download behaviour.
- **Replication:** storing copies on multiple peers.
- **DHT lookup:** hash key, query closer IDs, reach responsible peer.

## Common mistakes

1. **P2P does not mean every peer is identical.** Bandwidth, storage, uptime, and content differ.
2. **P2P does not mean there is no server.** Trackers, bootstrap services, and relays may be central.
3. **A DHT locates a resource, not necessarily its trust.** Verify hashes/signatures and content.
4. **Piece hashes do not prove that a file is safe.** A malicious file can be internally consistent.
5. **Churn is normal, not an exceptional failure.** The protocol must handle peers leaving.
6. **NAT/firewall can prevent direct connections.** Relays or traversal may be needed.
7. **A seeder is a single point of failure.** More peers and replication improve availability.
8. **Unstructured and structured P2P use different lookup methods.** Flooding/gossip and DHT are not synonyms.
9. **P2P is not automatically anonymous.** Peer addresses and patterns can reveal information.
10. **Fairness requires incentives.** Otherwise free-riding can be common.

## Exam prep

### Likely 2-mark questions

1. **How is P2P different from client-server?**  
   Hint: peers can supply and consume resources; no permanent central source is required.
2. **What is a DHT?**  
   Hint: distributed table mapping hashed resource keys to responsible peers.
3. **What is an overlay network?**  
   Hint: logical peer network formed over an underlying IP Internet.
4. **Define seeders and leechers.**  
   Hint: seeder has all pieces; leecher is downloading.
5. **What is churn?**  
   Hint: normal peer joining and leaving.
6. **Why do P2P systems use hashes/signatures?**  
   Hint: detect incorrect pieces and provide integrity/authenticity, with trust caveats.

### Likely long-answer questions

1. **Compare client-server, centralised P2P, pure decentralised P2P, and hybrid P2P.**  
   Answer hint: control, discovery, data path, scalability, resilience, and single points of failure.
2. **Explain DHT operation and its challenges.**  
   Answer hint: hashing, closest IDs, routing table, lookup hops, churn, NAT, and malicious peers.
3. **Explain BitTorrent-style piece exchange and incentives.**  
   Answer hint: swarm, seeders/leechers, blocks, hashes, rarest pieces, tit-for-tat, and churn.
4. **Discuss security, privacy, and fair contribution in P2P.**  
   Answer hint: poisoning, Sybil/eclipsing, deanonymisation, reputation, and incentives.
5. **Design a P2P content-delivery system for a software update.**  
   Answer hint: pieces, signed manifest, bootstrap/tracker or DHT, peers, mirrors, repair, and revocation.

### Short-answer revision checklist

Be ready to define peer, overlay, DHT, seeder, leecher, churn, and bootstrap; explain why a tracker can be central while data remains P2P; and distinguish content integrity from trust.
