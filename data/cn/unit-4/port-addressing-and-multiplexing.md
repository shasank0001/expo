---
subject: cn
unit: 4
topic: port-addressing-and-multiplexing
syllabus_ref: CSM3103 Unit-IV
status: draft
---
# Port Addressing and Multiplexing

## Overview

An IP address identifies a network interface, but a host often runs many applications. A **port number** identifies a transport-layer endpoint or process using that address. A TCP or UDP packet therefore contains both source and destination port numbers, allowing a receiver to deliver data to the correct application.

Transport **multiplexing** combines many application flows on a host-to-host network. **Demultiplexing** examines the destination port and delivers the segment or datagram to the right process. A typical connection is identified by the four-tuple of source address/port and destination address/port, together with the transport protocol and address family.

The syllabus includes transport services and elements, so this file expands the addressing, socket, well-known port, multiplexing, demultiplexing, and endpoint concepts needed for TCP, UDP, DNS, and HTTP.

## Explanation

### 1. Why an IP address is not enough

A server may run a web service, a mail service, a DNS resolver, and a database at the same time. All can use the same IP address. The transport port identifies which endpoint should receive a packet. A source port lets the remote endpoint return data to the correct client flow.

An IP address is normally associated with an interface and a network prefix. A port is a 16-bit number in the transport header. The port is meaningful only with:

- the address family, such as IPv4 or IPv6;
- the transport protocol, such as TCP or UDP;
- the local and remote addresses and context.

A port is not a permanent identity. A server can listen on a fixed port, while a client usually receives an ephemeral port for the duration of a connection.

### 2. Port number range

Port numbers are 16 bits:

`0` through `65,535`.

The ranges are conventionally divided into:

- **well-known/system ports:** 0–1023;
- **registered/user ports:** 1024–49,151 in the IANA registry;
- **dynamic/private/ephemeral ports:** commonly 49,152–65,535.

Exact registry boundaries and reserved values should be checked for an implementation, but the 16-bit range is fixed. A port can be reused after a connection closes, subject to safeguards such as TIME_WAIT and application rules.

### 3. Well-known and registered ports

Well-known services use conventional numbers:

| Service | Typical port | Transport |
|---|---:|---|
| FTP control | 21 | TCP |
| SSH | 22 | TCP |
| SMTP | 25 | TCP |
| DNS | 53 | TCP/UDP |
| DHCP server/client | 67/68 | UDP |
| HTTP | 80 | TCP |
| POP3 | 110 | TCP |
| IMAP | 143 | TCP |
| SNMP requests | 161 | UDP |
| SNMP notifications | 162 | UDP |
| HTTPS | 443 | TCP |

A registered port is assigned to an application so that users and firewalls can recognise it, but it is not the same as a guarantee of correctness or security. Services can run on another port.

### 4. Source and destination ports

A transport header carries a source port and destination port. For a TCP connection, the source port is normally the client's ephemeral port and the destination port is the server's listening port. Replies reverse the roles.

A server process calls a listening operation on a port. The operating system completes a connection and creates a new socket for that flow. Different clients can therefore use different remote address/port pairs even though they contact the same server port.

### 5. Socket and connection identity

A **socket** is an endpoint for communication. In a common TCP model, a socket can be identified by:

`protocol + local IP + local port + remote IP + remote port`

A **connection** is represented by a four-tuple:

`(source IP, source port, destination IP, destination port)`

for a specified transport protocol and address family. The server's listening socket is different from an accepted connection socket. This lets a server handle many clients concurrently.

A UDP socket can be unconnected and receive datagrams from many source ports. A connected UDP socket filters traffic to one peer, but it still does not gain TCP reliability.

### 6. Multiplexing

**Multiplexing** combines traffic from many processes onto a shared communication path. At the sending host, the transport layer takes data from a web process, a mail process, and a DNS process, adds their port identifiers, and passes the resulting transport units to IP. Routers do not need to know which process a packet belongs to.

Multiplexing is essential because creating a separate network interface for every application would be wasteful and difficult to manage. The port field is the local multiplexing mechanism.

### 7. Demultiplexing

At the receiving host, the transport layer reads the destination port and delivers the data to the appropriate socket:

1. remove and verify the transport header;
2. read destination port and address context;
3. find the matching listening or connected socket;
4. queue the data for the process;
5. deliver it according to the protocol's buffering and order rules.

If no process is listening on the port, the operating system may return a connection-refused response (TCP) or discard/notify the application (UDP), depending on the protocol and implementation.

### 8. Connection concurrency

A server can maintain many simultaneous connections to one listening port. The four-tuple distinguishes them:

- client A: `192.0.2.10:50001 -> 198.51.100.5:443`
- client B: `192.0.2.10:50002 -> 198.51.100.5:443`
- client C: `192.168.1.20:50001 -> 198.51.100.5:443`

Each has a different endpoint pair. The server can send data to the correct client without confusing the flows.

### 9. TCP and UDP port spaces

TCP and UDP have separate port-number spaces. TCP port 80 and UDP port 80 are different services. A firewall rule must specify the protocol as well as the port. IPv4 and IPv6 can also have different socket address families, and a dual-stack server may expose the same service on both.

### 10. Port security and firewalls

A port is an endpoint locator, not an identity credential. A firewall can allow or deny traffic based on address, port, protocol, state, and application signatures. However, an exposed port is vulnerable to scanning and attacks, and port numbers can be guessed. Authentication, authorisation, encryption, patching, and least privilege are still required.

An open port does not prove that its service is secure. A service can run on an unusual port, and a closed port does not guarantee that a host is safe. Attackers may exploit vulnerabilities through allowed ports.

### 11. NAT and port translation

Network address translation can translate an internal source address and port to a public address/port for a connection. The NAT maintains state so replies return to the correct internal host. This is called port translation or PAT. It complicates peer-to-peer applications because an external peer may not know the translated port.

### 12. Service discovery

Applications can use DNS SRV records or service metadata to discover a host and port, but DNS itself is addressed to a well-known port such as 53. A hard-coded service port is simple but inflexible. A configurable service is more adaptable but needs security and configuration management.

## Worked examples

### Example 1: Web and DNS on one host

A packet to `192.0.2.10:443` is delivered to the HTTPS process. A packet to `192.0.2.10:53` is delivered to the DNS process. The same IP address serves both because the ports differ.

### Example 2: Multiple browser connections

A browser opens three TCP connections to a web server. It may use source ports 49152, 49153, and 49154, all with destination port 443. The server uses the complete four-tuple to keep each connection separate.

### Example 3: NAT port mapping

An internal host `192.168.1.20:51000` sends a packet. A NAT maps it to `203.0.113.7:62001`. The external server replies to the public port. The NAT looks up its table and sends the reply to the internal socket. The port is meaningful only with the associated address and protocol.

### Example 4: UDP service

A DNS resolver listens on UDP port 53. A client sends a query from an ephemeral port and receives a response from port 53 to the client's port. No TCP connection state is needed, but the client still uses the four-tuple to distinguish replies.

## Key terms & formulas

- **Port:** 16-bit transport endpoint number, 0–65,535.
- **Well-known ports:** 0–1023.
- **Registered ports:** 1024–49,151 conventionally.
- **Ephemeral/dynamic ports:** commonly 49,152–65,535.
- **Source port:** client's return endpoint.
- **Destination port:** server/service endpoint.
- **Multiplexing:** combine many application flows.
- **Demultiplexing:** deliver to the correct process.
- **Socket:** endpoint object/address.
- **Four-tuple:** source IP/port plus destination IP/port.
- **Port range:** `2^16 = 65,536` possible values.
- **TCP/UDP separation:** separate port spaces.
- **PAT/NAT port translation:** map internal address/port to external address/port.
- **Listening socket:** server endpoint accepting connections.
- **Connection socket:** accepted flow-specific endpoint.
- **Port example:** DNS 53, HTTP 80, HTTPS 443, SNMP 161/162.

## Common mistakes

1. **A port is not a physical address.** It is a logical endpoint number.
2. **An IP address does not identify one application by itself.** Ports distinguish processes.
3. **Port numbers are not globally unique across all uses.** Context and protocol matter.
4. **TCP and UDP port spaces are separate.** TCP 80 is not UDP 80.
5. **A four-tuple may need the protocol too.** State the transport protocol in an answer.
6. **A server port can serve many clients.** The source address/port distinguishes connections.
7. **Multiplexing is not routing.** It combines local application flows; routers choose paths.
8. **An open port is not proof of authentication.** It is a reachability fact, not a security guarantee.
9. **NAT does not change the meaning of a port globally.** It translates a particular connection state.
10. **Ephemeral ports are not permanently owned by one application.** They are assigned and reused.

## Exam prep

### Likely 2-mark questions

1. **Why are ports needed?**  
   Hint: multiple applications share one host/IP address.
2. **State the port-number range and classify well-known/ephemeral ranges.**  
   Hint: 0–65,535; 0–1023 and commonly 49,152–65,535.
3. **Define multiplexing and demultiplexing.**  
   Hint: combine flows and deliver by destination port.
4. **What is a four-tuple?**  
   Hint: source IP/port and destination IP/port, with protocol context.
5. **Give three well-known ports.**  
   Hint: DNS 53, HTTP 80, HTTPS 443, SMTP 25, or SNMP 161.
6. **Why are TCP and UDP port spaces separate?**  
   Hint: different transport protocols and independent endpoint namespaces.

### Likely long-answer questions

1. **Explain transport addressing from IP address to socket.**  
   Answer hint: interface address, source/destination ports, protocol, four-tuple, listening/accepted sockets.
2. **Explain multiplexing and demultiplexing in a server with many clients.**  
   Answer hint: shared host, port lookup, connection state, and delivery to processes.
3. **Compare TCP and UDP port handling.**  
   Answer hint: connection state, listening port, ephemeral source port, datagram replies, and firewall implications.
4. **Explain how NAT and port translation affect a connection.**  
   Answer hint: address/port mapping table, replies, PAT, and impact on peer-to-peer services.

### Short-answer revision checklist

Be able to state the 16-bit range, list common ports, write a four-tuple, explain how a server distinguishes clients, and distinguish a port from an IP address.
