---
subject: cn
unit: 5
topic: domain-name-system
syllabus_ref: CSM3103 Unit-V
status: draft
---
# Domain Name System (DNS)

## Overview

The **Domain Name System (DNS)** is a distributed, hierarchical naming system that maps human-friendly domain names to network information and vice versa. A name such as `www.example.org` can lead to an IPv4 address, IPv6 address, mail server, authoritative name server, or other service record.

DNS solves a practical problem: people remember names, while routers use numeric addresses. It also supports names for services and administrative records. Because no single server can hold every name or answer every query, DNS divides authority across the root, top-level domains, delegated subdomains, and authoritative servers.

The syllabus lists Domain Name Space (DNS) in Unit V. This file covers namespace organisation, labels, resource records, resolvers, authoritative and non-authoritative servers, DNS query roles, common record types, caching/TTL, DNS over UDP/TCP, and security basics. The next file covers recursive and iterative resolution in detail.

## Explanation

### 1. Why DNS exists

IP addresses identify interfaces for routing, but they are not convenient for people to remember, type, or read. DNS provides a distributed mapping from names to records. It can return:

- IPv4 address (`A`);
- IPv6 address (`AAAA`);
- mail exchanger (`MX`);
- canonical name (`CNAME`);
- authoritative name server (`NS`);
- service location (`SRV`);
- text or policy information (`TXT`);
- other specialised records.

DNS is an application-layer protocol carried over UDP or TCP, usually through port 53. It is separate from IP addressing: DNS can tell a client which address to use, but IP still forwards the resulting packets.

### 2. Domain namespace and labels

A domain name consists of labels separated by dots. The rightmost label is the top-level domain (TLD), and labels are read from right to left toward the root:

`www.example.org`

- `org` is the TLD;
- `example` is a second-level name;
- `www` is a host or service name.

A trailing dot denotes the root. DNS names can be written fully qualified with the trailing dot, for example `www.example.org.`. The root is the top of the namespace and has no name label of its own in ordinary use.

Labels have length and character rules defined by the DNS protocol. A name is hierarchical, so delegation of a subdomain can be administered by a different organisation from the parent.

### 3. Root, TLD, and authoritative servers

The DNS hierarchy has several levels:

1. **Root servers:** identify the appropriate TLD servers.
2. **TLD servers:** identify the authoritative servers for a registered domain.
3. **Authoritative servers:** hold the official records for a zone and answer from that zone's data.
4. **Recursive resolvers:** perform work for clients and cache results.
5. **Caching/local resolvers:** store recent answers to reduce traffic and delay.

A server is authoritative for a zone when it is the designated source of truth for that zone. It can answer even if its answer is not cached elsewhere. A resolver may be non-authoritative and obtain an answer from an authoritative server or cache.

### 4. Zones and resource records

A **zone** is a portion of the DNS database served by an authoritative server. It contains **resource records (RRs)**. A record has a name, type, class, TTL, and value. The class is normally Internet (`IN`), and the TTL controls cache lifetime.

Common records:

- **A:** name -> IPv4 address.
- **AAAA:** name -> IPv6 address.
- **CNAME:** alias -> canonical name.
- **NS:** domain -> authoritative name server.
- **MX:** mail domain -> mail exchanger and preference.
- **PTR:** address -> name for reverse lookup.
- **SRV:** service, protocol, and priority -> target/port.
- **TXT:** text or policy/verification information.
- **SOA:** zone authority/start-of-authority and serial information.

A record value is not always an address. DNS is a general directory for many kinds of network information.

### 5. Resolver and stub resolver

A **stub resolver** is the client-side library or process used by an application. It builds a query from a name and type and sends it to a configured recursive resolver. The application normally asks the operating system's resolver, not every authoritative server itself.

A **recursive resolver** answers a client's request by querying other servers, following referrals, and caching the result. It performs work on behalf of the client. A resolver may be operated by an organisation, an ISP, a public service, or the local network.

### 6. Root and TLD referrals

When a resolver asks for `www.example.org`, an authoritative server may return a referral rather than the final address. A referral identifies the next servers responsible for a closer part of the namespace, such as a TLD server. The resolver then asks those servers. The process continues until an authoritative server returns the requested record.

Delegation and referrals are based on the hierarchy. A root server normally does not know every host address, and a TLD server normally does not know every host in every registered domain.

### 7. Forward and reverse lookup

A **forward lookup** maps a name to an address, for example `host.example.org` to an A record. A **reverse lookup** maps an address to a name using the `in-addr.arpa` IPv4 namespace or `ip6.arpa` IPv6 namespace. A PTR record supplies the name.

Reverse DNS is useful for logs, mail policy, and administration, but it is maintained separately from forward DNS. Forward and reverse records can be inconsistent.

### 8. Aliases and canonical names

A **CNAME** record maps an alias to a canonical name. It makes one DNS name appear under another name and can simplify administration. A CNAME cannot normally be used together with other data at the same owner name, so an administrator must place the required address/MX records at the canonical target.

A CNAME is not a redirect in a browser and does not move a service. It is a DNS naming relationship.

### 9. Caching and TTL

Every resource record includes a TTL in seconds. A resolver may cache the answer until the TTL expires. Caching reduces query traffic and response time, but a cached answer may remain temporarily old after a record changes.

A lower TTL allows faster changes but produces more DNS traffic. A high TTL improves cache efficiency but can delay a change from reaching clients. Administrators choose TTLs based on update frequency and service criticality.

Negative caching remembers that a name or record type did not exist for a TTL. It prevents repeated queries for a missing name but can also delay recognition of a newly created record until the negative TTL expires.

### 10. DNS transports

DNS normally uses **UDP port 53** because queries and most responses are small and latency matters. **TCP port 53** is used for large responses, truncated UDP answers, and authoritative zone transfers. TCP provides ordered, reliable transport and framing beyond the UDP size limit.

TCP is not used to make ordinary UDP queries reliable automatically. If a response is lost, the resolver can retry; if a response is truncated, it can retry over TCP. Modern deployments also use encrypted DNS transports such as DNS over TLS and DNS over HTTPS.

### 11. DNS query message concepts

A DNS query contains an identifier used to match a response, flags indicating query/response and desired recursion, a question section, and optional answer/authority/additional sections. A response can include:

- answer records;
- authority records identifying the source of the answer;
- additional records useful for the client.

The response code tells the resolver whether the query succeeded or encountered a problem. Caching and negative responses are controlled by flags and TTLs.

### 12. DNS security

Classic DNS is mostly plaintext and unauthenticated. An attacker can spoof a response or alter a query. Security extensions and encrypted transports can provide:

- data integrity and origin authentication;
- encryption of client-to-resolver traffic;
- signed zone data through DNSSEC;
- authenticated update policies;
- protection against cache poisoning and tampering.

DNSSEC authenticates DNS data's origin and integrity but does not encrypt it. DoH/DoT protect transport between selected endpoints but do not automatically make the authoritative data trustworthy. A secure deployment combines validation, encryption where appropriate, key management, and operational controls.

## Worked examples

### Example 1: A record lookup

A client asks for `www.example.org` type A. The resolver returns an A record such as `192.0.2.10`, with a TTL. The client uses that address in an IP packet. DNS itself does not carry the subsequent web request.

### Example 2: MX record

A mail client looks up `example.org` MX and learns that `mail.example.org` should receive mail, with a priority value. It then resolves the mail hostname to an address. MX does not mean MX is an A record; it points to a mail exchanger.

### Example 3: CNAME

`shop.example.org` is a CNAME for `store.example.net`. A resolver follows the alias to obtain the canonical A/AAAA record. The alias should not be treated as an additional IP address.

### Example 4: Reverse lookup

A mail server receives a connection from `192.0.2.25` and queries the reverse zone for `25.2.0.192.in-addr.arpa`. A PTR record may return `mail.example.org`. A missing or inconsistent PTR record can affect policy and logs.

### Example 5: TTL and change

A server address changes. A resolver may return the old cached A record until its TTL expires. A lower TTL before a planned migration makes the change propagate faster but increases query volume.

## Key terms & formulas

- **DNS:** distributed hierarchical naming system.
- **Namespace:** tree of domain names.
- **Label:** one dot-separated component.
- **Root:** top of the DNS hierarchy.
- **TLD:** top-level domain, such as `org`.
- **Zone:** authoritative data for a DNS portion.
- **Resource record:** name/type/TTL/value entry.
- **A record:** name -> IPv4 address.
- **AAAA record:** name -> IPv6 address.
- **CNAME:** alias to canonical name.
- **NS:** authoritative server record.
- **MX:** mail exchanger record.
- **PTR:** reverse name record.
- **SOA:** zone authority/serial record.
- **TTL:** cache lifetime in seconds.
- **Stub resolver:** client-side resolver.
- **Recursive resolver:** performs queries and caches for clients.
- **DNS port:** usually UDP/TCP 53.
- **Forward lookup:** name to address/record.
- **Reverse lookup:** address to name using PTR.

## Common mistakes

1. **DNS is not a single database on one server.** It is distributed and hierarchical.
2. **A domain name is read from right to left for hierarchy.** The TLD is on the right.
3. **DNS does not route packets.** It provides records; IP and routers forward packets.
4. **An A record is IPv4; AAAA is IPv6.** Do not interchange them.
5. **A CNAME is an alias, not an address.** It points to a canonical name.
6. **An MX record identifies a mail exchanger.** It may require a further A/AAAA lookup.
7. **A resolver is not necessarily authoritative.** It often uses a cache and referrals.
8. **Caching can produce stale answers.** The TTL limits the normal cache lifetime.
9. **UDP is the normal DNS transport, not the only one.** TCP is used for large/truncated responses and zone transfers.
10. **DNS privacy and DNS authentication are different.** DNSSEC authenticates data; DoH/DoT encrypt selected transport.
11. **A missing PTR record does not mean an address is invalid.** Reverse data is separate and optional.

## Exam prep

### Likely 2-mark questions

1. **What is DNS and why is it needed?**  
   Hint: distributed mapping from names to network records and addresses.
2. **List the DNS hierarchy levels.**  
   Hint: root, TLD, delegated domain, authoritative server, and resolver.
3. **State the purpose of A, AAAA, CNAME, NS, and MX records.**  
   Hint: IPv4, IPv6, alias, name server, and mail exchanger.
4. **What is a resolver?**  
   Hint: software/service that obtains DNS records for an application.
5. **What is the role of TTL?**  
   Hint: maximum normal cache lifetime for a record.
6. **Why can DNS use both UDP and TCP?**  
   Hint: UDP for small low-latency queries; TCP for large/truncated responses and transfers.

### Likely long-answer questions

1. **Explain the DNS namespace, hierarchy, zones, and resource records.**  
   Answer hint: labels, root/TLD/delegation, authoritative data, and record examples.
2. **Compare forward and reverse DNS with an example.**  
   Answer hint: A/AAAA versus PTR, `in-addr.arpa`/`ip6.arpa`, and consistency.
3. **Explain DNS resolvers, caching, TTL, and negative caching.**  
   Answer hint: stub/recursive roles, speed versus freshness, and missing-name TTL.
4. **Discuss DNS security risks and protections.**  
   Answer hint: spoofing, cache poisoning, DNSSEC authentication, DoH/DoT confidentiality, and key management.
5. **Compare DNS records A, AAAA, CNAME, MX, NS, and PTR in a practical mail/web scenario.**  
   Answer hint: show how one name leads to an address or mail exchanger and where further lookups occur.

### Short-answer revision checklist

Be ready to read a domain name right-to-left, define a zone and RR, list common record types, explain TTL caching, and state the roles of stub/recursive/authoritative servers.
