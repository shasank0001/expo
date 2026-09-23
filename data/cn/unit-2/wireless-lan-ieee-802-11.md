---
subject: cn
unit: 2
topic: wireless-lan-ieee-802-11
syllabus_ref: CSM3103 Unit-II
status: draft
---
# Wireless LAN and IEEE 802.11

## Overview

A **wireless LAN (WLAN)** provides network access over radio instead of a cable. IEEE 802.11 is the family of standards defining wireless LAN MAC and physical operation; the common name **Wi-Fi** usually refers to a family of compatible implementations based on these standards, though Wi-Fi is technically a certification/trademark term rather than the full IEEE standard.

A WLAN may operate in **infrastructure mode**, where stations communicate through an access point, or **ad hoc mode**, where stations communicate directly. Most home, campus, and enterprise networks use infrastructure mode. The access point bridges radio traffic to a wired LAN and normally provides authentication, association, and network services.

The syllabus includes Wireless LAN: IEEE 802.11. This file covers modes, frames, CSMA/CA, hidden nodes, association, radio/channel design, roaming, security, interference, and practical WLAN design.

## Explanation

### 1. IEEE 802.11

IEEE 802.11 defines the MAC and physical layers for wireless LANs. Later amendments and standards add higher rates, wider channel widths, improved modulation, security, and management. Examples of common bands include the 2.4 GHz and 5 GHz bands; newer systems may also use 6 GHz.

The standard supports different physical techniques, including spread-spectrum approaches such as **frequency-hopping spread spectrum (FHSS)** and **direct-sequence spread spectrum (DSSS)**, plus modern OFDM-based variants. A WLAN's actual rate depends on the radio, band, channel width, signal, interference, and the negotiated standard.

### 2. Infrastructure and ad hoc modes

#### Infrastructure mode

In infrastructure mode, stations communicate with an **access point (AP)**. The AP is a bridge between a wireless LAN and a distribution system, usually a wired Ethernet LAN. A router and DHCP server may provide Internet access and addresses. One AP can serve many associated stations, and overlapping APs can support roaming.

A frame from a laptop may travel from the laptop to an AP and then to the destination on the wired LAN. The AP is not necessarily the Internet router; it may be a bridge, controller-managed device, or a combined router/AP product.

#### Ad hoc mode

In ad hoc mode, stations form an independent wireless network without a central AP. They use a service-set identifier to identify the logical WLAN and may elect a peer to coordinate. An ad hoc network is useful for temporary device-to-device communication, but security, address management, and power management require care.

The mode names can vary by standard generation, so an exam answer should state the basic relationship: infrastructure uses an AP; ad hoc allows peer-to-peer communication without one.

### 3. WLAN frame and MAC addressing

A typical 802.11 MAC frame contains:

- frame control;
- duration/ID;
- sequence control;
- addresses (one to four depending on frame type);
- a QoS control field in some frames;
- frame body/payload;
- FCS.

The addresses can represent the transmitter, receiver, basic service-set identifier, and, in some management/data contexts, the intended end station. They should not be confused with IP addresses: 802.11 addresses support local wireless MAC operation, while IP addresses support end-to-end network routing.

The FCS detects many frame errors. A missing acknowledgement can cause a retry, but wireless ACK behaviour is affected by power, interference, and power saving.

### 4. CSMA/CA in WLANs

WLAN stations normally use CSMA/CA rather than CSMA/CD. A station may not be able to transmit and listen for a collision at the same time, and hidden stations may not hear each other. The basic access process includes:

1. physical carrier sense;
2. an inter-frame space such as DIFS;
3. a random backoff counter;
4. frozen backoff when the medium becomes busy;
5. transmission when the counter reaches zero;
6. ACK for frames that require acknowledgement.

The random backoff spreads stations' attempts. The IEEE standard defines contention parameters for different priorities, so voice or control frames may receive a shorter or differently structured wait than bulk data.

### 5. Hidden nodes and RTS/CTS

A hidden node is a station that another station cannot hear but whose frame can still collide at an AP or receiver. RTS/CTS uses short Request-to-Send and Clear-to-Send control frames. A station asks the AP for permission, and the AP sends a CTS that other stations hear, causing them to defer for a Network Allocation Vector (NAV).

RTS/CTS adds overhead and is not always used for every data frame. It is more useful when hidden nodes, long frames, or an environment make collision cost high. Exposed-terminal behaviour and the exact frame exchange depend on the standard and implementation.

### 6. Association and scanning

A station seeking service scans for APs using a probe request, receives probe responses or beacon frames, and selects an AP. It then performs an authentication and association procedure. The AP records the station's MAC address and security state in its tables.

A station may reassociate when it moves to a stronger AP. Roaming can cause a brief interruption and may involve authentication, key negotiation, and address/context updates. Controller-based systems centralise these decisions.

### 7. Channel access and radio planning

A WLAN channel is a portion of spectrum. 2.4 GHz channels overlap more because of their narrow available band; 5 GHz and 6 GHz usually offer more non-overlapping channels and often less interference, but propagation and obstacle effects vary. Wider channels can offer higher peak rates but use more spectrum and may increase interference.

A site survey should identify:

- AP placement and channel reuse;
- expected client density and application traffic;
- interference from other radios and non-Wi-Fi devices;
- walls, floors, furniture, and other attenuation;
- capacity and roaming requirements;
- available power and cabling for wired uplinks.

Using the same channel on nearby APs without proper planning can increase contention. Non-overlapping channel reuse can improve capacity, but too little overlap can leave coverage holes.

### 8. WLAN security

An open WLAN provides little privacy and allows clients to attempt association without meaningful authentication. Practical WLANs use:

- **authentication:** proving identity of the station or user;
- **encryption:** protecting frame contents;
- **access control:** limiting which users or devices may join;
- **key management:** rotating and distributing session keys;
- **guest/isolation controls:** limiting untrusted clients.

WPA/WPA2/WPA3 families use authentication and encryption mechanisms defined for wireless security. A strong password is necessary but not sufficient if the WLAN uses an obsolete or misconfigured protocol. Management frames, rogue APs, evil twins, and denial-of-service remain concerns.

### 9. WLAN performance factors

Throughput and delay depend on:

- radio standard and negotiated rate;
- signal-to-noise ratio and received signal strength;
- distance, fading, walls, and antenna placement;
- channel width and interference;
- number of simultaneous stations;
- airtime used by acknowledgements, management, and control frames;
- channel contention and hidden nodes;
- wired backhaul and Internet capacity;
- power-saving and client behaviour.

A high advertised PHY rate does not guarantee high application throughput. Protocol overhead, contention, retransmissions, and the uplink can reduce it substantially.

### 10. WLAN topology and AP functions

An AP can provide:

- wireless bridge;
- security and authentication;
- MAC filtering or dynamic ACLs;
- QoS prioritisation;
- power management and beacon scheduling;
- client accounting and location services;
- local forwarding or gateway/NAT functions in a consumer product.

Enterprise APs often send traffic through a controller, while small APs may be self-contained. An AP's bridge does not necessarily route between IP networks; a separate router is needed unless the product performs routing.

### 11. WLAN and wired LAN comparison

A wired LAN generally has stable bandwidth, low interference, and easier physical security. A WLAN provides mobility, easier deployment, and flexible access, but it shares radio spectrum and is affected by distance and obstacles. WLAN traffic eventually uses a wired distribution system, so a slow AP uplink can limit wireless performance.

## Worked examples

### Example 1: Campus WLAN

A laptop scans several campus APs, authenticates with campus credentials, associates with the strongest suitable AP, and sends an IP packet to a server. The AP forwards the frame over a fibre backbone. A roaming event may cause a short interruption while the laptop changes AP.

### Example 2: Hidden node

Two laptops on opposite sides of a thick wall both transmit to an AP. They cannot hear one another, so carrier sense alone does not prevent a collision. RTS/CTS or a virtual carrier-sense period may cause one to defer after hearing the CTS.

### Example 3: CSMA/CA backoff

A station has data while the channel is busy. It waits for DIFS, chooses a random backoff, and freezes when another station transmits. After the medium is idle, it continues the countdown and transmits when the counter reaches zero.

### Example 4: Security

An open guest WLAN uses an isolated VLAN and a portal, while staff traffic uses WPA3-like authentication and encryption. The guest network can be separated from internal systems by VLANs and firewall rules. A strong password alone is not the whole security design.

### Example 5: Capacity

Ten APs are placed close together in the 2.4 GHz band. If all use the same channel, clients compete for airtime and throughput falls. A survey can reduce overlap and reuse channels while preserving coverage.

## Key terms & formulas

- **WLAN:** wireless LAN.
- **IEEE 802.11:** wireless LAN MAC and physical standard family.
- **Wi-Fi:** commonly used name for wireless LAN technology/certification.
- **Infrastructure mode:** stations communicate through an AP.
- **Ad hoc mode:** stations communicate directly without a central AP.
- **AP:** access point bridging WLAN and distribution system.
- **CSMA/CA:** collision-avoidance access with DIFS/backoff/ACK.
- **DIFS:** distributed inter-frame space used in contention.
- **NAV:** network allocation vector, a virtual busy indication.
- **RTS/CTS:** request-to-send and clear-to-send handshake.
- **FHSS:** frequency-hopping spread spectrum.
- **DSSS:** direct-sequence spread spectrum.
- **OFDM:** orthogonal frequency-division multiplexing family used by many WLANs.
- **Channel utilization:** useful airtime divided by available airtime.
- **Signal-to-noise ratio (SNR):** signal power relative to noise power.
- **Security elements:** authentication, encryption, key management, access control.

## Common mistakes

1. **Wi-Fi and IEEE 802.11 are not identical terms.** Wi-Fi is a common certification/market term based on IEEE standards.
2. **Infrastructure mode is not the same as a router.** An AP may only bridge WLAN traffic.
3. **WLANs normally use CSMA/CA, not CSMA/CD.** Wireless collision detection is difficult.
4. **Carrier sensing does not solve hidden nodes.** They may not hear one another.
5. **A strong password is not the entire WLAN security design.** Authentication, encryption, VLANs, and management matter.
6. **A high wireless PHY rate is not guaranteed application throughput.** Overhead and interference reduce it.
7. **Roaming is not always seamless.** Authentication, association, and context changes can cause delay.
8. **2.4 GHz channels may overlap.** Channel planning is necessary.
9. **MAC addresses in an 802.11 frame are not automatically IP addresses.** Different layers and scopes apply.
10. **An AP may still need a wired uplink.** A fast radio cannot compensate for a slow distribution link.

## Exam prep

### Likely 2-mark questions

1. **Compare infrastructure and ad hoc WLAN modes.**  
   Hint: AP-mediated versus direct station communication.
2. **Why do wireless LANs use CSMA/CA?**  
   Hint: difficult collision detection and hidden stations.
3. **List four components of a WLAN frame.**  
   Hint: frame control, addresses, sequence control, payload, and FCS.
4. **State two WLAN security features.**  
   Hint: authentication, encryption, key management, or access control.
5. **What is an access point?**  
   Hint: a bridge between wireless stations and a distribution system.
6. **Give two factors affecting WLAN performance.**  
   Hint: interference, distance, channel width, number of clients, or backhaul.

### Likely long-answer questions

1. **Explain the IEEE 802.11 WLAN architecture and access process.**  
   Answer hint: infrastructure/ad hoc, scanning, authentication, association, CSMA/CA, ACK, and AP distribution.
2. **Explain hidden-node problems and RTS/CTS in a WLAN.**  
   Answer hint: carrier-sense limits, virtual carrier sense, NAV, handshake, and overhead.
3. **Describe 2.4 GHz versus 5/6 GHz WLAN planning.**  
   Answer hint: propagation, channels, interference, range, capacity, and site survey.
4. **Design a secure campus WLAN.**  
   Answer hint: coverage, channel reuse, authentication/encryption, VLANs, guest isolation, wired uplinks, and management.

### Short-answer revision checklist

Be able to draw a laptop–AP–server path, list a WLAN frame, explain DIFS/backoff/ACK, define hidden nodes, and compare infrastructure and ad hoc modes.
