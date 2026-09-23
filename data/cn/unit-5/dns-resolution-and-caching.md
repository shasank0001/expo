---
subject: cn
unit: 5
topic: dns-resolution-and-caching
syllabus_ref: CSM3103 Unit-V
status: draft
---
# DNS Resolution and Caching

## Overview

DNS resolution is the process of finding the record requested for a name. A client normally sends a query to a recursive resolver. The resolver answers from cache when possible or performs a sequence of queries to root, top-level-domain, and authoritative servers until it reaches the requested record.

A **recursive query** asks a server to obtain the complete answer on the resolver's behalf. An **iterative query** asks a server for the best information it has, such as a referral, and lets the requester follow that referral. The two terms describe different roles: the client requests recursion; the resolver may use iterative queries to the DNS hierarchy.

Caching makes repeated lookups fast and reduces load. It also introduces temporary staleness, so TTLs, negative caching, and secure validation must be considered.

## Explanation

### 1. Roles in a DNS query

Three roles must not be confused:

- **Stub resolver:** the client-side component used by an application. It normally asks a recursive resolver.
- **Recursive resolver:** performs the complete lookup for the stub and returns a final answer or error.
- **Authoritative server:** holds the official records for a zone and can answer authoritatively for names it serves.

A resolver can also be authoritative for its own local zone while recursively resolving other names. A root or TLD server usually returns referrals rather than recursively walking the entire hierarchy for every request.

### 2. Recursive query

A client sends a recursive query to a resolver:

> “Please find the final A/AAAA/MX/etc. record for this name and return it to me.”

The resolver may use its cache, query other servers, follow referrals, and retry. The client normally does not need to know which servers were contacted. Recursive resolution is convenient for applications and centralises cache and security logic.

If the resolver cannot reach the authority or an error occurs, it returns an error or a partial referral depending on the query and its configuration. A client should not assume every failure means the name does not exist.

### 3. Iterative query

In an iterative query, a server returns the best answer or referral it has:

> “I do not know the final address, but ask the TLD servers for `example.org`; here are their addresses.”

The resolver then queries one of those servers. The process continues through delegated domains until an authoritative server returns the requested record. Iterative queries distribute work and avoid requiring every server to query every other server recursively.

A resolver may send a recursive query to a configured recursive server or iterative queries to authoritative/referral servers, depending on its role. It normally does not send a recursive query to a root server and expect the root to perform all subsequent work.

### 4. Full resolution for `www.example.org`

Assume a client asks for the A record of `www.example.org` and the cache is empty:

1. The stub sends a recursive query to a local resolver.
2. The resolver queries a root server iteratively.
3. The root returns a referral to the `.org` TLD servers.
4. The resolver queries an `.org` server.
5. The `.org` server returns a referral to the authoritative servers for `example.org`.
6. The resolver queries an authoritative server.
7. The authoritative server returns the A record and its TTL.
8. The resolver caches the record according to policy and TTL and returns it to the stub.

The exact number of network queries can be smaller if the resolver already has a cached parent referral or record. A root server does not normally know the final A record.

### 5. Caching records and referrals

Caching can include:

- final answer records;
- CNAME targets;
- NS records and glue;
- referrals to TLD or delegated servers;
- negative answers indicating no data;
- additional records returned with a response.

A cache entry has a TTL, source, flags, and sometimes an associated security validation state. Caching reduces query traffic, root/TLD load, and response time. It can also hide a recent DNS update until the old entry expires.

Caching a referral is useful: the resolver can later begin at a closer server instead of starting at the root. The referral's own lifetime and the parent record's rules determine when it is refreshed.

### 6. TTL and freshness

A record's TTL is a maximum normal cache lifetime in seconds. Each cache can track remaining time. A resolver may serve an answer until expiry, then query again. Some resolvers apply additional safety rules or cache policies.

A lower TTL before a planned address change makes the new record visible sooner but increases query traffic. A high TTL is efficient for stable records but prolongs stale answers. The authoritative administrator and recursive resolver can use different cache policies.

Time is measured carefully: TTL values and cache expiry can be affected by clock differences, and a resolver should not treat an old record as permanently fresh.

### 7. Negative caching

If an authoritative server says the name or record type does not exist, a resolver can cache a **negative answer** for the SOA's negative TTL. This avoids repeatedly asking about a known-nonexistent name. It also means a newly created record may not be visible until the negative TTL expires.

NXDOMAIN means the name does not exist; NODATA means the name exists but the requested type has no record. A client should not treat every empty answer as proof that the entire domain is absent.

### 8. UDP, TCP, and retries

DNS normally uses UDP port 53 for small queries and responses. A DNS message has a size limit over UDP. If a response is too large, the server sets the truncated bit and the resolver retries over TCP port 53. TCP is also used for authoritative zone transfers and some signed/encrypted operations.

A lost UDP query is handled by a resolver timeout and retry, not by a general DNS acknowledgement protocol. The resolver can use a new query identifier and randomised source port to reduce spoofing and cache-poisoning risks.

TCP itself does not make the DNS data authentic. DNSSEC and encrypted transports address different threats.

### 9. Caching servers and hierarchy load

Without caching, every lookup would contact the hierarchy, placing load on root and TLD servers. Recursive resolvers and local stub caches absorb repeated requests. This is one reason DNS can scale to a very large number of clients.

A resolver cache may be:

- on the client device;
- in an operating system stub;
- in a local network resolver;
- in an ISP or organisation resolver;
- in a public anycast resolver service.

Each cache has different privacy, security, and freshness policies.

### 10. Security during resolution

An attacker can inject a forged UDP response with a matching ID/port guess, poison a resolver cache, or trick a client. Defences include:

- randomising query identifiers and source ports;
- DNSSEC validation from a trust anchor;
- encrypted DNS over TLS or HTTPS;
- restricting response acceptance to appropriate authority sections;
- rate limiting and anomaly detection;
- secure updates and signed zones;
- avoiding unauthorised open resolvers.

DNSSEC authenticates signed data's origin and integrity. DoT/DoH protect client-to-resolver traffic. A cache can be correct for the wrong resolver if the resolver itself is compromised, so endpoint and operational security remain important.

### 11. DNS resolution and connection setup

An application may need several DNS operations before connecting:

- resolve a service name to A/AAAA records;
- choose an address and test reachability;
- perform a TLS handshake whose certificate name must match;
- for email, query MX and then the exchanger's address.

DNS resolution is logically separate from TCP connection establishment, though the application may combine the steps. A successful DNS answer does not guarantee that the service is reachable.

## Worked examples

### Example 1: Recursive versus iterative

The client asks its resolver recursively. The resolver asks a root server iteratively. The root replies with a referral, not the final IP address. This is normal: the root delegates responsibility for `.org` to the TLD servers.

### Example 2: Cache hit

A first lookup returns `203.0.113.20` with a 300-second TTL. A second lookup within 300 seconds can be answered from cache, reducing query traffic. After 300 seconds, the resolver normally queries the authority again.

### Example 3: Cache miss and referral

A resolver has no final record but has a fresh referral to the example.org authority. It can query that authority directly rather than starting at the root. If the referral expires, it returns to the parent information.

### Example 4: Truncated response

A DNSSEC-signed answer or large record set exceeds the UDP response size. The server sets TC. The resolver opens a TCP connection to port 53 and repeats the query over TCP.

### Example 5: Negative caching

A client asks for `missing.example.org` and receives NXDOMAIN with a negative TTL. The resolver caches the absence for that period. If an administrator creates the record immediately, some clients may still see the cached negative answer until it expires.

### Example 6: Security

A resolver validates a DNSSEC chain from a trust anchor to the zone and rejects an invalid signature. It may use DoT/DoH to protect the client's path to the resolver. These protections solve authenticity/integrity and transport confidentiality, respectively.

## Key terms & formulas

- **Stub resolver:** client-side resolver.
- **Recursive resolver:** obtains a final answer for a client.
- **Iterative query:** requester follows returned referrals.
- **Authoritative server:** official source for a zone.
- **Referral:** NS/glue information pointing to closer servers.
- **Cache hit:** answer served without a new query.
- **TTL:** maximum normal cache lifetime, in seconds.
- **Negative caching:** cache of NXDOMAIN/NODATA.
- **NXDOMAIN:** requested name does not exist.
- **NODATA:** name exists but requested type has no data.
- **UDP DNS:** normally port 53.
- **TCP DNS:** large/truncated answers and zone transfers, port 53.
- **DNSSEC:** data-origin authentication and integrity.
- **DoH:** DNS over HTTPS.
- **DoT:** DNS over TLS.
- **Cache reduction:** fewer repeated hierarchy queries.
- **TTL timing example:** a 300-second TTL permits normal cache reuse for up to 300 seconds.

## Common mistakes

1. **Recursive and iterative are not two unrelated protocols.** They describe who performs the work in a query.
2. **A root server normally does not return the final host address.** It returns a referral to TLD servers.
3. **A stub normally does not query every DNS server.** It asks a recursive resolver.
4. **A recursive resolver may use iterative queries.** The terms apply to different steps.
5. **Caching does not mean the answer is always current.** TTL controls normal reuse.
6. **A cache hit is not authoritative.** It is a previously obtained answer.
7. **NXDOMAIN and NODATA are different.** One says the name is absent; the other says the type is absent.
8. **TCP is not always used for DNS.** UDP is normal for small queries; TCP handles large/truncated cases and transfers.
9. **DoT/DoH and DNSSEC solve different problems.** Encryption and authentication/integrity are not identical.
10. **DNS resolution success does not guarantee service availability.** The address may be down or the port blocked.

## Exam prep

### Likely 2-mark questions

1. **Distinguish recursive and iterative DNS queries.**  
   Hint: requester delegates work versus follows referrals and performs next query.
2. **What is a stub resolver?**  
   Hint: client-side component that asks a recursive resolver.
3. **Why is caching used in DNS?**  
   Hint: speed and reduced hierarchy traffic, bounded by TTL.
4. **What is an authoritative DNS server?**  
   Hint: official source for records in a zone.
5. **State the role of TTL.**  
   Hint: cache lifetime in seconds.
6. **When is TCP used for DNS?**  
   Hint: large/truncated responses and zone transfers.

### Likely long-answer questions

1. **Trace recursive DNS resolution for `www.example.org`.**  
   Answer hint: stub, recursive resolver, root, TLD, authoritative, answer, cache, and return.
2. **Compare recursive and iterative queries with a diagram.**  
   Answer hint: who does the work, referrals, final answer, and normal server roles.
3. **Explain DNS caching, TTL, referrals, and negative caching.**  
   Answer hint: speed/freshness trade-off, parent caching, NXDOMAIN/NODATA, and update delay.
4. **Explain how UDP, TCP, and encrypted DNS transports are chosen.**  
   Answer hint: size, truncation, zone transfer, latency, DoT/DoH, and limitations.
5. **Discuss DNS spoofing and defences.**  
   Answer hint: forged UDP/answers, cache poisoning, DNSSEC, encrypted transports, randomisation, and rate limiting.

### Short-answer revision checklist

Be able to draw the root–TLD–authority path, label recursive/iterative steps, explain TTL and negative caching, and state why TCP or encryption may be used.
