---
subject: cn
unit: 3
topic: routing-algorithms
syllabus_ref: CSM3103 Unit-III
status: draft
---
# Routing Algorithms

## Overview

A **routing algorithm** chooses paths through a graph of routers and links. The input is a topology, link metrics, and policy; the output is a route—or a forwarding-table entry—for a destination prefix. A good algorithm balances delay, throughput, hop count, reliability, cost, administrative policy, and stability.

Routing can be **static** or **dynamic**. Static routing is configured in advance and is simple and predictable, but may not react to traffic or failures. Dynamic routing exchanges information and adapts to changes, but consumes bandwidth and control-plane resources and can converge slowly or temporarily produce loops.

The syllabus names routing algorithms in the network layer. This file covers algorithm goals, static and dynamic routing, centralised/distributed approaches, distance-vector and link-state methods, Bellman–Ford and Dijkstra-style calculations, flooding, path instability, hierarchical routing, metrics, and worked examples.

## Explanation

### 1. Routing as a graph problem

Represent a network as a graph:

- vertices are routers or networks;
- edges are links;
- each edge has a metric such as hop count, delay, bandwidth, cost, or reliability.

A routing algorithm attempts to find a path with a low total metric while meeting policy and avoiding loops or unstable changes. The objective may be a single shortest path, multiple equal-cost paths, or a path that balances load and delay. The choice of metric matters more than the word “shortest.”

A simple unweighted graph may use hop count. A delay-aware graph may use measured or estimated propagation and queueing delay. A policy-aware Internet routing system may prefer one provider or avoid a particular path even if another is technically shorter.

### 2. Static routing

In **static routing**, an administrator enters routes and interfaces, or a fixed algorithm selects a path at design time. Static routing is useful for small, stable networks, stub networks, and emergency backup routes.

Advantages:

- simple to configure and understand;
- no routing-update traffic;
- no convergence delay;
- predictable and easy to audit;
- avoids a failed dynamic protocol affecting control traffic.

Disadvantages:

- manual work for a large network;
- poor adaptation to link or traffic changes;
- possible unused or unbalanced paths;
- human errors;
- slow recovery unless redundant static routes are planned.

A default static route is common on a small LAN: send all remote destinations to one next-hop router.

### 3. Dynamic routing

**Dynamic routing** exchanges information among routers and updates routes as links, destinations, or metrics change. It can react to a link failure, discover a new network, and select a new path.

Dynamic routing requires convergence: after a change, routers must reach a consistent view. During convergence, different routers may have different tables, causing loops, black holes, or temporary loss. Protocols use timers, sequence information, acknowledgements, path-vector attributes, hold-downs, and other mechanisms to reduce inconsistent views.

Dynamic routing can be **centralized** or **distributed**.

### 4. Centralised routing

In a centralized algorithm, a controller or designated router collects the network state, calculates routes, and distributes forwarding information. It has a global view and can optimise load, but the controller is a single point of failure and may create a bottleneck. A failure or wrong calculation can affect many routers.

A logically centralized controller may still be implemented with redundant control servers. The design must specify how routers behave if the controller or its network fails.

### 5. Distributed routing

In a distributed algorithm, every router makes or participates in routing decisions using local or exchanged information. There is no single required decision-maker. Distributed algorithms scale across administrative domains but require consistent message exchange and protection against stale or malicious information.

Common distributed families are:

- distance-vector;
- link-state;
- path-vector;
- flooding and hierarchical algorithms.

### 6. Distance-vector routing

A **distance-vector** router maintains a vector of estimated costs to destinations. It exchanges this vector with directly connected neighbours. On receiving an update, a router adds the cost of the link to the neighbour and selects a better route.

The core update can be written as:

`D_x(y) = min_v { c(x,v) + D_v(y) }`

where `D_x(y)` is the estimated distance from router `x` to destination `y`, `v` is a neighbour, and `c(x,v)` is the link cost. This is the Bellman–Ford recurrence. It can find shortest paths when metrics are non-negative and the network eventually converges.

Distance-vector is simple and uses little router memory. However, it can converge slowly after a failure and may experience the **count-to-infinity** problem: routers can gradually increase a believed distance when the best path disappears. Split horizon, poison reverse, hold-down timers, and more advanced path-vector techniques mitigate or avoid parts of the problem.

RIP is a classic distance-vector protocol using hop count as its main metric. It is simple but has a limited useful hop range.

### 7. Link-state routing

A **link-state** router builds a topology database describing its own links and the links reported by neighbours. It floods or relays link-state advertisements (LSAs), computes a shortest path, and installs forwarding entries.

A link-state algorithm generally uses a local view of the whole topology, so it can converge quickly and choose paths using richer metrics. The memory, CPU, flooding traffic, and protocol complexity are higher than for a basic distance-vector protocol.

A link-state protocol often uses **Dijkstra's algorithm**:

1. Set the source router's distance to 0 and all other distances to infinity.
2. Mark the source visited.
3. Select the unvisited node with the smallest tentative distance.
4. Relax its links: for each neighbour, update its distance if the path through the current node is better.
5. Mark the node visited and repeat until all reachable nodes are selected.

OSPF and IS-IS are common link-state interior protocols. Their databases, areas, and design are more detailed than the basic textbook algorithm.

### 8. Worked distance-vector calculation

Suppose routers A, B, and C have these link costs:

- A–B = 1
- B–C = 2
- A–C = 10

Initially, A believes C can be reached directly at cost 10. B advertises that C is reachable through B at cost 2, so A calculates `1 + 2 = 3` and changes its route to C through B. The shortest path is A–B–C with total cost 3, not 10.

A distance-vector update must be periodic or triggered by a change. If the A–B link fails, stale information can cause a temporary wrong route. Split horizon can prevent B from advertising its route back to A as a simple next hop; poison reverse can advertise the route as unreachable.

### 9. Worked Dijkstra calculation

Use the graph:

- A–B = 1
- A–C = 4
- B–C = 2
- B–D = 5
- C–D = 1

Starting at A:

- initial distances: A=0, B=∞, C=∞, D=∞.
- select A; update B to 1 and C to 4.
- select B; update C to `1 + 2 = 3` and D to `1 + 5 = 6`.
- select C; update D to `3 + 1 = 4`.
- select D; the shortest distance to D is 4 through A–B–C–D.

The algorithm uses a priority queue or an equivalent efficient implementation. It requires non-negative link costs; negative costs can make shortest paths ill-defined or cause repeated relaxation.

### 10. Link-state versus distance-vector

| Property | Distance-vector | Link-state |
|---|---|---|
| Information shared | Cost/vector to neighbours | Topology/link-state database |
| Router view | Neighbour estimates | More complete network topology |
| Memory/computation | Low | Higher |
| Convergence | Can be slower | Usually faster in a stable area |
| Typical issue | Count-to-infinity | Flooding and database synchronisation |
| Example | RIP | OSPF, IS-IS |

The table is a generalisation. Specific implementations add mechanisms and use different metrics.

### 11. Path-vector routing

A **path-vector** protocol, represented by BGP, exchanges reachability and an AS path rather than only a numeric distance. It applies policy: a router may prefer a path through one provider, reject a route with a particular AS, or avoid a particular prefix.

BGP does not simply choose the mathematically shortest path in the distance-vector sense. It exchanges enough information to enforce administrative policy, loop prevention, and stable inter-domain routing. BGP convergence and table size require careful operation.

### 12. Flooding and hierarchical routing

**Flooding** sends information to every reachable node. It can be simple and robust for small or special networks, but duplicates and loops are possible. Controlled flooding uses sequence numbers, acknowledgements, and TTL to reduce duplicates and stop stale information.

**Hierarchical routing** divides a large network into areas, autonomous systems, or domains. Routers exchange detailed information inside a domain and summary routes between domains. This reduces memory and update traffic, but less-specific summaries can hide the best local path.

### 13. Metrics and route selection

Common route metrics include:

- hop count;
- propagation or fixed link delay;
- measured queueing delay;
- available bandwidth;
- reliability or error rate;
- monetary cost;
- administrative preference;
- security or policy attributes.

A metric should be consistent enough for routing to converge. Mixing unstable measurements can cause oscillation: routers move flows to a path, overload it, then move them back. Traffic-aware routing can improve utilisation but needs dampening and careful update frequency.

### 14. Routing-table output and forwarding

A routing algorithm computes a route; the router installs a forwarding entry. A forwarding entry may contain:

- destination prefix;
- next hop;
- outgoing interface;
- metric;
- administrative distance/preference;
- route source and age.

A data-plane lookup should be fast and independent of the algorithm's control-plane computation. The routing algorithm may run periodically or in response to events, while forwarding occurs for every packet.

### 15. Failure and convergence

When a link fails, adjacent routers detect it through physical, keepalive, or hello information. They update their control state and advertise the change. The network converges after a finite but possibly variable delay. During convergence, packets may loop, be dropped, or take an old path.

Metrics such as convergence speed, stability, overhead, and route quality are used to compare algorithms. A protocol can be fast but unstable, or stable but slow. No single algorithm is ideal for every network.

## Worked examples

### Example 1: Static versus dynamic

A small office with one router can use a default route. A multi-campus network with changing links uses dynamic protocols so routes can update automatically. Both can be valid; the better choice depends on scale, stability, and administrative capability.

### Example 2: Distance vector

A has a direct cost-10 route to C. B advertises cost 2 to C and A–B costs 1. A changes to cost 3 via B. When A–B fails, A temporarily needs a new update; protocol safeguards help prevent a false route through B.

### Example 3: Link state

Each router reports all of its directly connected links and their metrics. Every router in the area receives a consistent topology database and independently runs Dijkstra. OSPF uses areas and interface types in its real design, so the textbook graph is a simplification.

### Example 4: Policy routing

BGP may prefer a path with a higher technical delay if it crosses a preferred provider. The route is not mathematically shortest but is administratively desirable. This is why Internet routing cannot be described only by hop count.

### Example 5: Oscillation

Two routers send traffic to each other's links because each sees the other path as less loaded. The first change overloads the new path, which then becomes the more attractive path again. Damping, hysteresis, and stable metrics reduce route flapping.

## Key terms & formulas

- **Routing algorithm:** method for selecting paths.
- **Graph model:** routers as nodes and links as edges.
- **Metric:** value used to compare paths.
- **Static routing:** manually configured routes.
- **Dynamic routing:** routes learned and maintained automatically.
- **Convergence:** routers reach a consistent routing state.
- **Centralized routing:** one controller calculates routes.
- **Distributed routing:** routers share information and participate in decisions.
- **Distance vector:** vector of estimated costs to destinations.
- **Bellman–Ford:** `D_x(y) = min_v(c(x,v) + D_v(y))`.
- **Link state:** advertised topology database used for path calculation.
- **Dijkstra:** nonnegative-cost shortest-path algorithm.
- **Count-to-infinity:** stale distance-vector update problem.
- **Split horizon:** do not advertise a route back to the neighbour from which it was learned.
- **Poison reverse:** advertise a learned route as unreachable in the reverse direction.
- **Path vector/BGP:** policy-aware inter-domain reachability.
- **Flooding:** distribute information throughout a reachable area.
- **Hierarchical routing:** divide the network and exchange summaries.
- **Administrative preference:** local policy priority for a route.
- **Route flap:** repeated change between paths.

## Common mistakes

1. **Shortest path does not always mean fewest hops.** It means lowest chosen metric.
2. **Distance vector does not share a complete topology database.** It exchanges cost vectors with neighbours.
3. **Link state does not mean every router uses a globally current Internet view.** It usually has a scoped area/database.
4. **Convergence is not instant.** During it, routers can have inconsistent routes.
5. **Dijkstra assumes non-negative link costs.** Negative weights break the ordinary shortest-path guarantee.
6. **Static routing is not always wrong.** It can be appropriate for small or stable networks.
7. **BGP is not simply distance vector.** It is policy- and path-aware.
8. **Flooding can create duplicates and loops.** Sequence numbers and bounds are needed.
9. **A routing algorithm is not the forwarding lookup.** Algorithms build tables; forwarding uses them.
10. **Traffic-aware metrics can cause oscillation.** Stability mechanisms are necessary.
11. **Convergence does not guarantee zero packet loss.** Packets in flight or queued during the change may be dropped.
12. **A route with a high administrative preference is not necessarily technically best.** Policy is a separate decision criterion.

## Exam prep

### Likely 2-mark questions

1. **Define a routing algorithm and name two metrics.**  
   Hint: choose paths; hop count, delay, bandwidth, cost, reliability.
2. **Compare static and dynamic routing.**  
   Hint: manual/fixed versus exchanged/adaptive.
3. **Define convergence.**  
   Hint: time/point after a change when routers agree on routing state.
4. **State one advantage and one disadvantage of link-state over distance-vector.**  
   Hint: faster/global view versus more memory and flooding.
5. **What is the count-to-infinity problem?**  
   Hint: stale distance-vector routes gradually increase in cost after a failure.
6. **What is the difference between routing and forwarding?**  
   Hint: select/learn paths versus apply a forwarding table per packet.

### Likely long-answer questions

1. **Explain static, dynamic, centralised, and distributed routing.**  
   Answer hint: definitions, control location, update traffic, failure behaviour, and examples.
2. **Describe distance-vector routing with a numerical example.**  
   Answer hint: exchange vectors, add neighbour cost, show a route change, and discuss count-to-infinity safeguards.
3. **Describe link-state routing and Dijkstra's algorithm step by step.**  
   Answer hint: LSA construction, database, relaxation, termination, and OSPF/IS-IS context.
4. **Compare distance-vector and link-state routing in a table and discuss convergence.**  
   Answer hint: information, memory, speed, complexity, failure, and scale.
5. **Explain path-vector/BGP routing and why policy matters in the Internet.**  
   Answer hint: AS path, reachability, provider policy, loop avoidance, and trade-offs.
6. **Discuss route metrics, traffic-aware selection, and route oscillation.**  
   Answer hint: delay/bandwidth/load, measurement, update frequency, damping, and stability.

### Short-answer revision checklist

Be ready to draw a small weighted graph, run Bellman–Ford or Dijkstra, distinguish routing from forwarding, and explain count-to-infinity, convergence, static/dynamic, and link-state/distance-vector.
