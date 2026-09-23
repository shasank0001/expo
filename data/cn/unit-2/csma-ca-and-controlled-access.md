---
subject: cn
unit: 2
topic: csma-ca-and-controlled-access
syllabus_ref: CSM3103 Unit-II
status: draft
---
# CSMA/CA, Controlled Access, and Channelization

## Overview

Several data-link methods decide **who may use a shared medium**. CSMA/CA lets wireless stations try to avoid collisions before transmitting. Controlled access grants permission in advance through polling or a token. Channelization divides one medium into separate channels so users can transmit at the same time.

These methods solve related but different problems. Random access and CSMA/CA are decentralised: stations make local decisions and deal with competition. Controlled access centralises or coordinates permission, often giving predictable behaviour. Channelization provides simultaneous logical paths through frequency, time, code, or wavelength.

The syllabus groups CSMA/CA, controlled access, and channelization. Understanding their assumptions is important because a method suitable for a wired bus is not automatically suitable for a radio cell.

## Explanation

### 1. CSMA/CA: Carrier Sense Multiple Access with Collision Avoidance

**CSMA/CA** is the principal medium-access method used by wireless LANs. A station generally:

1. senses the wireless medium;
2. waits for an **inter-frame space (IFS)**;
3. selects a random backoff counter;
4. waits for the counter to reach zero while checking that the medium remains idle;
5. transmits;
6. waits for an acknowledgement when the protocol uses one.

The IFS is a short, protocol-defined idle interval that gives priority to certain types of frames, such as acknowledgements or beacon-related traffic. The random backoff prevents stations that joined at the same time from choosing the same transmit instant.

### 2. Why wireless uses avoidance

A radio receiver often cannot transmit a strong signal and listen for a weak collision at the same time. A station may also be unable to hear another station because of distance, walls, or fading. Collision detection is therefore unreliable in wireless. CSMA/CA uses sensing and randomisation to reduce the chance of an overlap rather than relying on detecting it after transmission.

Carrier sensing alone cannot solve the **hidden-node** problem. Station A and station C may both sense an idle channel because B lies between them, yet their frames collide at B. RTS/CTS, NAV, or other virtual carrier-sense mechanisms can reduce this problem when the protocol supports them.

### 3. CSMA/CA timing

After a busy medium becomes idle, a station waits for the appropriate IFS. It chooses a random backoff in a defined range. A station decrements its counter by one for each idle time slot, but if it senses the medium busy, it freezes the counter and waits again. When the counter reaches zero, it transmits. This distributed countdown spreads the stations' starting times.

Backoff and IFS are different: the IFS is a fixed waiting interval, while backoff is randomly selected and usually counted in contention slots. Congestion or frame priority can affect the selected backoff range.

### 4. Controlled access

**Controlled access** gives a station permission before it transmits. It can be implemented as:

- **polling:** a controller asks stations in turn whether they have data;
- **token passing:** a special token circulates among stations and only its holder may transmit;
- **reservation:** a station reserves a future time or channel through a control message.

Polling can be central or hierarchical. The controller may poll each device, use a multilevel arrangement, or use a monitor that listens for requests. Polling avoids data collisions but wastes time if most stations have no data. A failed controller or lost token can stop the network unless recovery mechanisms exist.

**Token Ring** is the classic controlled-access example. A station captures the token, transmits while holding it, and releases it. A **token bus** can combine controlled access on a logical ring with a physical bus.

### 5. Channelization

**Channelization** divides a medium into separate channels. Each station is assigned or selects one channel, so simultaneous transmissions can avoid mutual interference.

#### Frequency-division multiple access (FDMA)

FDMA divides the spectrum into non-overlapping frequency bands. Each user receives a different frequency channel, with guard bands or guard intervals to reduce adjacent-channel interference. Traditional cellular systems and radio links use this idea. FDMA can be simple, but channels become inefficient when traffic is bursty because an idle user still reserves a band.

#### Time-division multiple access (TDMA)

TDMA lets users share one frequency but assigns different time slots. Guard times separate slots. Each station transmits only in its assigned slots. TDMA can adapt capacity to traffic and avoids permanent frequency separation, but synchronization and slot allocation are important.

#### Code-division multiple access (CDMA)

CDMA assigns orthogonal or carefully designed spreading codes. Users transmit at the same time over a wide frequency band, and the receiver correlates the desired code to separate the signal. Proper power control and interference management are important. CDMA allows flexible sharing but is not automatically collision-free: unwanted correlation and near-far problems can reduce performance.

### 6. Comparison of methods

| Method | Permission | Main goal | Typical advantage | Main problem |
|---|---|---|---|---|
| CSMA/CA | None; local sensing/backoff | Avoid/reduce collisions | Simple distributed wireless access | Hidden nodes and exposed terminals |
| Polling | Controller grants it | Deterministic access | Central control and priority | Controller overhead/failure |
| Token | Token holder transmits | Ordered, fair access | No data collisions; predictable | Token loss and ring failure |
| FDMA | Frequency channel | Simultaneous channels | Simple logical separation | Poor use under bursty traffic |
| TDMA | Time slot | Simultaneous sharing | Flexible traffic allocation | Synchronisation/guard overhead |
| CDMA | Spreading code | Simultaneous users | Flexible spectrum sharing | Interference/power control |

The methods can be combined. A protocol may use channelization for a downlink and controlled or random access for control traffic.

### 7. Exposed and hidden terminals

A **hidden terminal** occurs when two stations cannot hear each other but can interfere at a receiver. CSMA/CA's virtual carrier-sense mechanisms and RTS/CTS can reduce the resulting collision. An **exposed terminal** is a station that hears another transmission and stays silent even though it could transmit to a different receiver without interfering. Ideally a medium-access method handles both cases.

### 8. Fairness and priority

A fair access method gives every station a reasonable opportunity. Random backoff reduces immediate collisions, but heavy traffic or a particular backoff policy can favour some stations. Controlled access can guarantee a turn or token, but a fault may stop all stations. Channelization can reserve a high-priority channel, but capacity assigned to one class is unavailable to others.

QoS, priority, and admission control add traffic classes and reservation rules. They improve service for voice or control traffic but increase management complexity.

## Worked examples

### Example 1: Wi-Fi backoff

Four stations have data after an idle interval. They all wait the fixed IFS, then choose different random backoff counters. The smallest counter transmits first. Other stations freeze or continue according to the protocol, and the remaining stations retry after the medium becomes idle again.

### Example 2: Hidden-node WLAN

A laptop and a printer are on opposite sides of a wall from an access point. They may not hear one another but both transmit to the AP. Their frames collide. RTS/CTS or a virtual carrier-sense period can reduce the collision if the stations hear the AP's control frames.

### Example 3: Polling

A server polls ten terminals. Only three have data, so seven polls receive no response. The controller eventually reaches the busy terminals. Polling is predictable, but it wastes channel time on idle stations.

### Example 4: Token ring

Only the station holding the token may transmit. It sends a frame, receives an acknowledgement, and passes the token to the next station. If a station crashes, a monitor or protocol removes the failed station and restores the token.

### Example 5: TDMA

Four voice users share one radio channel. Each gets a recurring time slot. Even if one user is temporarily silent, its slot is protected. If the application is highly bursty, dynamic allocation can reallocate unused slots to improve utilisation.

### Example 6: FDMA versus TDMA

Two users continuously transmit data. FDMA can give each a permanent band, which is simple but reserves capacity. TDMA shares one band and gives each recurring slots, which may use the spectrum more efficiently if timing is well managed.

## Key terms & formulas

- **CSMA/CA:** carrier-sense multiple access with collision avoidance.
- **Inter-frame space (IFS):** fixed waiting interval before contention.
- **Backoff counter:** randomly selected countdown, frozen when the medium is busy.
- **Hidden terminal:** mutually unheard transmitters that collide at a receiver.
- **Exposed terminal:** unnecessarily silent station because it hears an irrelevant transmission.
- **Polling:** controller asks stations in turn.
- **Token passing:** circulate a permission token.
- **Controlled access:** permission-based shared-medium method.
- **Channelization:** divide a medium into logical channels.
- **FDMA:** frequency-division multiple access.
- **TDMA:** time-division multiple access.
- **CDMA:** code-division multiple access.
- **Guard time/band:** separation to limit adjacent interference.
- **Backoff range:** normally increases after repeated failures or based on priority.
- **Fairness:** opportunity for all users to access the medium.

## Common mistakes

1. **CSMA/CA does not detect collisions as its main mechanism.** It tries to avoid them; recovery/ACK behaviour may still handle a collision.
2. **Carrier sensing does not eliminate hidden-node collisions.** Stations may not hear one another.
3. **Controlled access is not random access.** A controller or token grants permission.
4. **Token passing is not the same as polling.** The permission moves with a token rather than being requested individually by a controller.
5. **FDMA, TDMA, and CDMA are channelization methods.** They are not all collision-detection methods.
6. **CDMA is not guaranteed free of interference.** Code design and power control matter.
7. **A token is not a data frame.** It is a permission control message.
8. **Fairness is not automatic in random backoff.** A station may have a higher priority or a longer average delay.
9. **Polling is not automatically more efficient.** It can waste time on idle stations.
10. **An exposed terminal is different from a hidden terminal.** One transmits unnecessarily silently; the other collides unnoticed.

## Exam prep

### Likely 2-mark questions

1. **Explain the basic operation of CSMA/CA.**  
   Hint: sense, IFS, random backoff, transmit, and acknowledge/retry.
2. **Why is CSMA/CA preferred in wireless LANs?**  
   Hint: radio stations often cannot reliably transmit and detect collisions at the same time.
3. **Distinguish controlled access and channelization.**  
   Hint: permission-based access versus division into logical channels.
4. **Define hidden and exposed terminals.**  
   Hint: mutually unheard collision risk versus unnecessary silence.
5. **Name FDMA, TDMA, and CDMA and state their division dimension.**  
   Hint: frequency, time, and code/spreading sequence.
6. **Give one advantage and one disadvantage of token passing.**  
   Hint: orderly access versus token-loss/ring-failure overhead.

### Likely long-answer questions

1. **Explain CSMA/CA with a timing diagram and explain backoff.**  
   Answer hint: DIFS/IFS, random countdown, busy freeze, hidden-node problem, and ACK.
2. **Compare polling and token passing.**  
   Answer hint: controller versus token, fairness, overhead, failure recovery, and traffic patterns.
3. **Compare FDMA, TDMA, and CDMA.**  
   Hint: frequency, time, code; guard intervals, synchronisation, power, and efficiency.
4. **Select a medium-access method for a wireless classroom and justify it.**  
   Answer hint: mobility, hidden nodes, traffic load, QoS, and the limitations of the alternatives.

### Short-answer revision checklist

Be ready to draw a CSMA/CA backoff sequence, define hidden/exposed terminals, and compare all three channelization methods in a small table.
