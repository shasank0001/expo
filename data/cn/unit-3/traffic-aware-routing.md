---
subject: cn
unit: 3
topic: traffic-aware-routing
syllabus_ref: CSM3103 Unit-III
status: draft
---
# Traffic-Aware Routing

## Overview

**Traffic-aware routing** chooses a path using information about current or expected network load. Instead of selecting only the route with the fewest hops or a fixed static cost, it considers metrics such as queue size, delay, available bandwidth, loss, utilisation, or a weighted combination.

The approach is useful when several links connect the same networks but have different capacities or loads. It can distribute traffic, reduce queueing delay, and improve throughput. It also introduces measurement overhead, stale information, route instability, and possible oscillations if routers react too quickly.

Traffic-aware routing is a congestion-control approach, not a guarantee that congestion disappears. A new flow can still overload a path, and a locally optimal choice can move the bottleneck elsewhere. The design must balance utilisation and stability.

## Explanation

### 1. Meaning of traffic-aware routing

A traditional shortest-path algorithm assigns each link a fixed metric and selects a route based on the sum of metrics. A traffic-aware algorithm changes or supplements the metric according to observed or estimated traffic conditions.

Examples of information used include:

- interface queue occupancy;
- measured or estimated propagation delay;
- round-trip time;
- available bandwidth;
- packet loss or error rate;
- link utilisation;
- traffic volume or flow rate;
- administrative cost or policy.

A router may compute several candidate next hops and select the one with the best current metric. A central controller or distributed protocol may collect measurements and distribute the result.

### 2. Traffic metrics

**Queue length** is a direct sign of waiting traffic but can be noisy and difficult to measure across interfaces. **Delay** captures propagation, queueing, and processing but may not identify the cause. **Available bandwidth** is useful for a large transfer but can be difficult to estimate accurately. **Loss** is a strong congestion signal but can also result from physical errors or policy.

A composite metric can be written as:

`M = w1 * delay + w2 * loss + w3 * (1 - utilisation) + w4 * cost`

The weights should reflect the application. A voice call may value delay and jitter more than raw throughput; a bulk transfer may value available bandwidth more. Metrics must be normalised and measured consistently.

### 3. Measurement and information sources

Traffic information can come from:

- periodic interface counters;
- queue and scheduler statistics;
- active probes or ping measurements;
- passive flow classification;
- router-to-router exchanges;
- traffic estimation from known flows;
- application or transport feedback.

Periodic measurements are simple but may be stale. Active probes consume traffic and may not match the real path. Passive monitoring can be accurate but requires counters and privacy/security controls. No single source is perfect.

A routing protocol can distribute a metric or a selected route, or each router can calculate locally from neighbour information. The control message should include a timestamp, metric, validity, and optional confidence/quality information.

### 4. Load balancing and heterogeneous links

Suppose two links connect the same pair of networks. Link A has high bandwidth but is currently busy; Link B has lower bandwidth but low utilisation. A traffic-aware algorithm may send a new large flow over B or split traffic according to a policy.

The choice is not always “send everything to the least-loaded link.” A small real-time flow may suffer if it is queued behind bulk traffic on the same link. Flow classes, weighted paths, and per-flow scheduling can separate requirements.

Traffic-aware routing can also avoid a predicted failure or maintenance link. A route can be selected based on delay, load, link reliability, administrative policy, and security constraints.

### 5. Path selection and next hops

For a destination, a router may maintain multiple candidate paths. It compares their metrics and chooses a next hop. The route can be:

- a single best path;
- equal-cost multipath;
- weighted multipath;
- a path selected by a controller;
- a policy-preferred path with a traffic-aware tie-breaker.

A routing table entry may include a primary and backup path. If the primary becomes congested or fails, traffic can use the backup. Rapid movement of existing flows can itself cause instability, so flow placement often needs slower control than packet forwarding.

### 6. Route oscillation and instability

Suppose two parallel links initially have equal load. Routers independently move some flows toward the link that appears slightly faster. Both routes then become overloaded and move flows back. The network oscillates, wasting control overhead and harming performance.

Controls against instability include:

- **damping:** ignore small changes or reduce update frequency;
- **hysteresis:** require a metric to cross thresholds before switching;
- **hysteresis and hold-down:** wait after a change;
- **sampling and smoothing:** use averages rather than instantaneous values;
- **rate limiting:** limit route updates;
- **hysteresis in cost:** add switching penalties;
- **stable flow assignment:** move only new flows when possible.

Traffic-aware routing is a control loop. Measurement noise and delayed feedback can make the system unstable just as in any feedback control system.

### 7. Local versus global optimality

A router may choose the path that is best for its own interface while the destination's downstream link remains congested. A locally lower queue can be created by moving traffic into a later bottleneck. Global optimisation requires knowledge of the end-to-end path and coordinated decisions, which is expensive and difficult.

A distributed algorithm can improve the situation but may converge slowly. A centrally controlled approach can use a global view but creates a control-plane dependency. Hybrid designs use local fast decisions plus slower global adjustments.

### 8. Interaction with routing algorithms

Traffic-aware routing can be built into:

- link-state metrics updated from measurements;
- distance-vector costs that change over time;
- multipath routing;
- application-aware routing;
- software-defined networking controllers;
- service-level agreements and policy engines.

The core shortest-path algorithm may remain Dijkstra or Bellman–Ford, but the edge weights are dynamic. A separate route-selection layer may then choose among equal-cost or near-equal paths according to load.

### 9. Traffic engineering

**Traffic engineering** arranges traffic to use network resources efficiently and reliably. It may use multiple routing paths, bandwidth reservation, explicit paths, constraints, and protection paths. Traffic-aware routing is one component of traffic engineering.

A primary path can carry normal traffic and a backup path can be reserved for failure. If load-aware routing moves all flows away from a primary, the backup may be less available for its protection role. Policies and metrics must account for this.

### 10. Practical considerations

A network operator must choose:

- measurement interval and averaging;
- which interfaces and flows to monitor;
- metric weighting and thresholds;
- update frequency and maximum route changes;
- treatment of stale or missing measurements;
- class-based versus per-flow decisions;
- fallback to static or minimum-cost routes;
- monitoring and audit of route changes.

Traffic-aware routing must be secure. A compromised measurement or control message could redirect traffic to a poor or hostile path. Control-plane authentication, authorisation, rate limiting, and safe defaults are important.

## Worked examples

### Example 1: Two uplinks

A router has a 1-Gbit/s uplink with 70% utilisation and a 100-Mbit/s uplink with 10% utilisation. A new bulk flow might be sent over the second path if the policy values immediate queue availability. A voice flow might use the high-capacity path with priority, despite its higher utilisation. The decision is application- and policy-dependent.

### Example 2: Congestion-aware rerouting

A path has increasing delay and packet loss. A traffic-aware controller lowers its effective metric or selects an alternative. New flows use the alternative. Existing long-lived flows may remain on the original path to avoid disruption. The controller monitors the result for a settling period.

### Example 3: Oscillation

Two routers see each other's paths as slightly cheaper in alternating measurements. Without damping, they repeatedly move traffic. A moving average and a minimum switch threshold stop small changes from causing route flips. A cost penalty can also be added after a switch.

### Example 4: Weighted multipath

A router has three paths with 4, 2, and 1 units of capacity. Weighted multipath sends approximately 4:2:1 shares of new traffic. This improves utilisation but requires per-flow hashing and state; changing a flow's path can disrupt TCP performance and complicate return traffic.

### Example 5: Fallback

A traffic-aware metric becomes unavailable. The router uses the last known route, a static minimum-cost route, or a protected backup. It should not immediately treat the destination as unreachable. A safe fallback is part of a robust design.

## Key terms & formulas

- **Traffic-aware routing:** path selection using load/traffic information.
- **Metric:** measured or estimated path cost.
- **Queue occupancy:** waiting packets in a router queue.
- **Available bandwidth:** capacity not currently used, approximately.
- **Utilisation:** used capacity divided by total capacity.
- **Composite metric:** weighted sum of normalised traffic measures.
- **Multipath:** multiple eligible paths for traffic.
- **Traffic engineering:** controlled arrangement of traffic to use resources efficiently.
- **Damping:** reduce update reaction to small changes.
- **Hysteresis:** require a threshold before switching.
- **Hold-down:** suppress changes for a period.
- **Smoothing:** average measurements over time.
- **Route oscillation:** repeated switching between paths.
- **Control overhead:** measurement and routing-update cost.
- **Local optimality:** best choice at one router, not necessarily end-to-end.

## Common mistakes

1. **Traffic-aware routing is not simply shortest path.** It uses changing or richer metrics.
2. **It does not prevent all congestion.** A selected path can still become overloaded.
3. **Lower hop count may not be better.** A longer path can have lower delay or more capacity.
4. **More frequent updates are not always better.** They can cause oscillation and control overhead.
5. **Traffic information can be stale or noisy.** A measurement is not a perfect truth.
6. **Local load does not describe the whole path.** A downstream bottleneck may remain.
7. **Rerouting all existing flows is not required.** Moving new flows can reduce disruption.
8. **Multipath needs flow consistency.** A flow's return path and state may matter.
9. **Traffic engineering is broader than one routing metric.** It includes protection, constraints, and resource planning.
10. **A controller is not automatically secure.** Measurement and route messages need authentication and safe defaults.

## Exam prep

### Likely 2-mark questions

1. **Define traffic-aware routing.**  
   Hint: select paths using current/expected load, delay, bandwidth, queue, or loss.
2. **Name three traffic metrics.**  
   Hint: queue size, delay, utilisation, bandwidth, loss, or traffic rate.
3. **State one benefit and one drawback.**  
   Hint: better utilisation versus measurement overhead, staleness, or instability.
4. **What is route oscillation?**  
   Hint: repeated switching between paths as measured costs change.
5. **Name two stabilising mechanisms.**  
   Hint: damping, hysteresis, smoothing, hold-down, or rate limiting.
6. **What is traffic engineering?**  
   Hint: arrange traffic and resources for efficiency, reliability, and policy goals.

### Likely long-answer questions

1. **Explain traffic-aware routing and its metrics.**  
   Answer hint: delay, queue, bandwidth, utilisation, loss, composite weights, and candidate paths.
2. **Describe how traffic information is collected and distributed.**  
   Answer hint: counters, probes, passive monitoring, router exchanges, control overhead, and stale data.
3. **Explain route oscillation and methods to prevent it.**  
   Answer hint: feedback loop example, damping, hysteresis, smoothing, hold-down, and thresholds.
4. **Compare a single traffic-aware path with multipath.**  
   Answer hint: load balance, state, flow consistency, return traffic, and complexity.
5. **Design a traffic-aware routing policy for voice and bulk data.**  
   Answer hint: classes, metrics, weights, priority, new-flow placement, backup routes, and monitoring.

### Short-answer revision checklist

Be able to define traffic-aware routing, list at least four metrics, explain measurement overhead, give an oscillation example, and name damping/hysteresis as controls.
