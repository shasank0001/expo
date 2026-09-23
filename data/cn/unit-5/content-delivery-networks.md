---
subject: cn
unit: 5
topic: content-delivery-networks
syllabus_ref: CSM3103 Unit-V
status: draft
---
# Content Delivery Networks

## Overview

A **content delivery network (CDN)** is a distributed system that stores copies of content on servers, called edge or edge-cache servers, closer to users. A request-routing system sends each user to a suitable edge location instead of always going to a distant origin server. The result is usually lower latency, less origin bandwidth, better scalability, and more resilience during traffic spikes.

A CDN is not just one fast server. It is an origin/tiered-cache architecture with many edge locations, request routing, cache-control rules, invalidation or purging, health checks, and monitoring. Static files such as images, scripts, styles, and video segments cache well. Personalised or rapidly changing content may need origin processing and a shorter cache lifetime.

The syllabus lists Content Delivery Networks and Peer-to-Peer Networks as content-delivery topics. This file explains CDN architecture, request routing, caching, replication, load balancing, cacheability, dynamic content, security, availability, and performance measurement. It also explains how a CDN differs from P2P.

## Explanation

### 1. Origin and edge servers

The **origin** is the authoritative server for content. It may serve a file directly or create a dynamic response. Edge servers cache selected responses and serve many nearby clients. A request-routing system chooses an edge based on the client, content, network, and edge state.

A simplified request path is:

1. The client resolves the service name, often through DNS or another routing mechanism.
2. The routing system chooses an edge location.
3. The client requests the content from that edge.
4. On a cache hit, the edge returns the object quickly.
5. On a cache miss, the edge requests the object from a higher-tier cache or origin.
6. The edge stores the response according to cache policy and returns it.

The origin remains important even when most requests hit an edge. It must protect itself from cache misses, updates, and attacks.

### 2. Request routing

Request routing can use:

- client geographic location;
- network/ISP location;
- current latency or measured performance;
- edge server load and capacity;
- requested file or object type;
- current health and reachability;
- content availability and cache state;
- user language, account, or authorisation context.

A common implementation uses DNS response steering or a service-discovery layer. Some CDNs route at the application layer through a domain, URL, or anycast address. Routing must be stable enough for caching and flexible enough to react to failure.

A client may be directed to a nearby edge with a high cache hit rate, or to a slightly farther edge with a much better network path. Geographic distance alone is not a perfect prediction.

### 3. Cache hit and cache miss

A **cache hit** means the edge already has a valid copy. The edge can return it without contacting the origin, reducing:

- user-to-origin path length and delay;
- origin bandwidth and CPU;
- congestion on long links;
- sensitivity to origin failure;
- cost when many users request the same object.

A **cache miss** means the edge does not have a valid copy. It must fetch from the origin or a parent cache. The response can then be cached if its freshness rules allow it. Many simultaneous misses for a popular object are called a cache stampede; request collapsing or prewarming can reduce the load.

### 4. Cache-control, TTL, and freshness

HTTP-style cache directives control whether and how long an object can be stored:

- `Cache-Control: max-age=...` gives relative freshness;
- `s-maxage` can specify shared-cache freshness;
- `Expires` gives an absolute expiry time;
- `ETag` and `Last-Modified` support validation/revalidation;
- `Vary` tells a cache which request headers affect the representation;
- `no-store` and `no-cache` have specific restrictions on reuse or validation.

A shared edge cache is different from a private browser cache. A response marked private must not be placed in a shared cache, and a personalised response should not be sent to the wrong user. Cache keys must include all dimensions that affect the response.

### 5. Replication and tiered caches

A popular object is replicated across many edges or points of presence. Replication increases capacity, availability, and geographic coverage. A **tiered cache** places large regional caches between the origin and edge servers, so an edge can obtain a miss from a closer parent rather than crossing the Internet to the origin.

Replication decisions consider:

- request rate and object popularity;
- geographic demand;
- object size and update rate;
- storage and bandwidth cost;
- origin protection;
- failover and disaster-recovery requirements.

Over-replication can waste storage and create stale copies. Under-replication can cause repeated origin misses during a traffic spike.

### 6. Static versus dynamic content

Static content is largely the same for all users: images, CSS, JavaScript, fonts, downloadable files, and pre-encoded video. It caches efficiently and benefits greatly from edge delivery.

Dynamic content depends on a database, user account, current time, inventory, location, or application logic. It may still use a CDN for TLS termination, compression, connection reuse, or selective caching, but the origin must generate a personalised response.

Typical policy is to cache:

- static files for long periods;
- popular public API responses for short periods;
- personalised pages for no time or a few seconds;
- authenticated content only with strict key and privacy controls.

A CDN does not make dynamic computation disappear; it can move suitable computation and caching closer to the user.

### 7. Invalidation and freshness

When content changes at the origin, old edge copies can remain until their TTL expires. CDNs provide invalidation or **purging** mechanisms to remove or refresh selected URLs, prefixes, tags, or versions.

Versioned URLs are another strategy: publish `app.2.js` instead of replacing `app.js`. Users and caches retain the old version safely until it is no longer needed. A short TTL is useful for frequently changing data but increases origin requests.

Invalidation must be authorised and auditable. A bad purge can remove a large amount of useful cache data and create an origin traffic spike. A cache key error can expose a personalised object to another user.

### 8. Edge protocols and delivery

Edges may use HTTP/HTTPS, QUIC, or other application protocols over TCP/UDP. TLS can be terminated at the edge to reduce repeated handshakes to the origin, provided keys and security policy are managed correctly. HTTP/2 or HTTP/3 can multiplex requests and reduce overhead for many small objects.

Video delivery often uses segmented content and range requests. The edge caches segments, allowing a viewer to begin playback quickly and resume after a failure. Large objects can be compressed or encoded into multiple bit rates, but transcoding may require origin or media-processing capacity.

### 9. Load balancing and health

The request router selects an edge based on capacity and health. Health checks detect a failed server, expired certificate, or unreachable origin. The system can remove the edge from rotation, redirect to another location, or fall back to a parent cache.

Load balancing may operate at DNS, anycast IP, HTTP routing, or application level. DNS-based routing can use health and geolocation information, but DNS caches and client resolvers may delay changes. Anycast can send a client to a nearby edge by normal network routing, but a provider must operate the global address and routing consistently.

A failed edge should not make the whole CDN unavailable. Redundancy, multiple points of presence, and origin replicas improve resilience.

### 10. Security

A CDN can improve security when used as a reverse proxy and content-delivery layer:

- terminate TLS and enforce HTTPS;
- block or rate-limit abusive requests;
- absorb volumetric traffic near the user;
- apply WAF rules;
- hide or protect the origin address;
- restrict cross-origin and content policies;
- sign URLs or tokens for authorised access.

A CDN is not automatically secure. An origin with weak authentication, an exposed admin interface, or a misconfigured cache key can still be compromised. A cache must not serve one user's private response to another user. Signed cookies/tokens, origin validation, and careful `Vary` handling are important.

### 11. Availability and disaster recovery

A CDN improves availability by keeping content away from the origin and allowing alternate edges. For critical content, the origin should be replicated across independent failure domains, with tested failover and configuration backups.

A CDN can mask an origin outage for cached content, but a cache miss or purge can still reach the failed origin. The design should state which content remains available during an origin failure and how quickly it is restored.

### 12. Performance and measurement

Useful CDN metrics include:

- cache-hit ratio;
- origin fetch rate and bandwidth;
- edge latency and time to first byte;
- request completion time;
- revalidation/error rate;
- availability and purge latency;
- bandwidth and storage cost;
- per-region and per-content performance.

A high cache-hit ratio is usually helpful but not sufficient. A tiny object may hit the edge but still have high connection or application latency. A personalised object may have a low hit ratio and still benefit from a nearby TLS edge.

### 13. CDN versus P2P

A CDN is provider-operated and centrally managed: the provider places and operates edge servers, controls routing, and returns content. A P2P system uses user computers as both clients and servers, often with peer discovery and swarm exchange.

A CDN provides predictable service, stable content, and operator support, but costs money and requires trust in the provider. P2P can reduce origin cost and distribute work, but peers are unreliable, malicious content is a concern, and availability is less controlled. Some systems combine both: a CDN provides reliable initial content while P2P assists after authorised peers obtain it.

## Worked examples

### Example 1: Video release

A film is stored in an origin and pre-cached at many regional and local edges. A viewer requests the first segment. The routing system chooses a nearby edge with the segment. Playback begins quickly, and later segments are fetched from the same or another edge.

### Example 2: Cache miss stampede

A popular software release makes thousands of users request the same uncached file at once. If every edge independently fetches it, the origin is flooded. Request collapsing, a parent cache, prewarming, or a controlled origin replica can reduce the spike.

### Example 3: Personalised content

A shopping home page contains a user's name and cart. The CDN can cache the static images and scripts, but the personalised HTML must be generated at the origin or with a strict short-lived private policy. A shared cache must not mix users' responses.

### Example 4: Invalidation

A web application releases a corrected JavaScript file. The operator purges `app.js` or publishes `app.3.js`. A purge removes old edge copies and causes a controlled origin fetch; versioning allows old and new versions to coexist safely.

### Example 5: CDN versus P2P

A streaming company uses a CDN so every user receives a reliable, authenticated copy. It separately enables P2P seeding for selected users to reduce download cost. P2P is an extra source, not a replacement for the controlled edge cache.

### Example 6: Security failure

A cache key ignores the user's region or authorisation cookie, so an edge returns a private response to another user. The CDN is misused; the correct fix is a safe key design, private/no-store policy, origin validation, and cache purge.

## Key terms & formulas

- **CDN:** content delivery network.
- **Origin:** authoritative source server.
- **Edge server/POP:** server near users that serves cached content.
- **Request routing:** select an edge for a client/content.
- **Cache hit:** valid content already at the edge.
- **Cache miss:** edge must fetch from parent/origin.
- **Cache-hit ratio:** hits divided by total cacheable requests.
- **TTL:** object freshness lifetime.
- **Tiered cache:** parent cache between edge and origin.
- **Replication:** store copies in multiple locations.
- **Invalidation/purge:** remove or refresh cached content.
- **Versioned URL:** content identifier changed to avoid stale reuse.
- **Anycast:** one address routed toward a suitable location.
- **WAF:** web application firewall.
- **Origin shield/parent cache:** protects origin from edge misses.
- **Time to first byte:** server response latency for the first byte.
- **CDN/P2P distinction:** provider-operated edges versus user peers.
- **Example cache ratio:** 900 hits out of 1,000 cacheable requests = 90%.

## Common mistakes

1. **A CDN is not one fast server.** It is a distributed origin/edge system.
2. **Geographic distance is not the only routing input.** Network path, load, health, and cache state matter.
3. **A cache hit is not guaranteed for every request.** Personalised and dynamic content may miss.
4. **Caching does not mean infinite freshness.** TTL, revalidation, versioning, and purge control age.
5. **A CDN is not automatically a security layer.** TLS, WAF, origin protection, and safe cache keys are still needed.
6. **A shared cache must not cache private personalised data for all users.** Use private/no-store and correct keys.
7. **A cache purge is not free.** It can create a sudden origin request storm.
8. **A CDN is not the same as P2P.** CDN edges are operated by the provider; peers are user computers.
9. **A high cache-hit ratio does not guarantee low end-to-end latency.** Connection and application time still count.
10. **DNS steering can be delayed by resolver and client caches.** Health changes may not be instant.
11. **Anycast is not a guarantee of geographic placement.** Routing and provider design determine the location.

## Exam prep

### Likely 2-mark questions

1. **What is a CDN and state two benefits.**  
   Hint: distributed edge copies; lower latency, scalability, origin-load reduction, resilience.
2. **What is a cache hit and cache miss?**  
   Hint: hit is available at edge; miss requires origin/parent fetch.
3. **How does CDN request routing work?**  
   Hint: use location, network, load, health, content, and cache availability.
4. **Why is dynamic content harder to cache?**  
   Hint: response depends on user/request/time and must not be shared incorrectly.
5. **State one CDN security control.**  
   Hint: HTTPS/TLS, WAF, rate limiting, signed URLs, origin hiding, or safe cache keys.
6. **Differentiate CDN and P2P.**  
   Hint: provider-operated edge servers versus user peers acting as clients and servers.

### Likely long-answer questions

1. **Explain CDN architecture from origin to client.**  
   Answer hint: origin, parent/tiered cache, edge/POP, request routing, hit/miss, and response.
2. **Describe CDN request-routing systems and their trade-offs.**  
   Answer hint: DNS, anycast, HTTP routing, location/network/load/health/cache state, and instability.
3. **Explain caching policies, invalidation, and dynamic content.**  
   Answer hint: TTL, ETag/Last-Modified, Vary, private/no-store, purge, versioning, and personalised data.
4. **Discuss CDN availability, scalability, and security.**  
   Answer hint: replication, origin protection, WAF, TLS, rate limits, safe keys, and disaster recovery.
5. **Compare a provider CDN and a P2P content-delivery system.**  
   Answer hint: control, cost, reliability, trust, peer churn, malicious content, and hybrid use.

### Short-answer revision checklist

Be able to define origin/edge/request routing/cache hit/miss, explain TTL and purge, identify static versus dynamic content, state CDN benefits, and distinguish CDN from P2P.
