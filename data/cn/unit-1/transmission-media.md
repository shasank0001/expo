---
subject: cn
unit: 1
topic: transmission-media
syllabus_ref: CSM3103 Unit-I
status: draft
---
# Transmission Media

## Overview

A **transmission medium** is the physical path and signalling mechanism that carries information between network devices. Media are broadly divided into **guided media**, where the signal is confined to a physical cable, and **unguided media**, where electromagnetic or optical waves travel through space.

The choice of medium affects bandwidth, distance, attenuation, interference, security, installation cost, and reliability. Copper twisted pair is inexpensive and common inside buildings. Fibre offers very high bandwidth and long distance but needs optical transceivers. Radio supports mobility but shares an interference-prone environment. A good network design matches the medium to distance, traffic, environment, and budget.

## Explanation

### 1. Guided transmission media

In guided media, a physical conductor or fibre constrains the signal to a defined path. The transmitter sends a signal at one end and the receiver detects it at the other. Guided media include twisted pair, coaxial cable, and optical fibre.

#### Twisted-pair cable

Twisted-pair cable contains pairs of insulated copper wires. The two conductors carry a signal in opposite polarities, and the twisting reduces electromagnetic radiation and crosstalk by making external interference affect both wires similarly. A differential receiver subtracts the two voltages, cancelling common-mode noise.

Twisted pair is used by Ethernet, telephone systems, and many building networks. Categories such as Cat 5e, Cat 6, and Cat 6a specify performance and frequency support. It is inexpensive, easy to install, and easy to terminate, but its attenuation and crosstalk increase with length and frequency. A typical wired Ethernet link is limited to about 100 metres for copper twisted pair without additional equipment.

#### Coaxial cable

Coaxial cable has a central conductor, insulation, a metallic shield, and an outer jacket. The shield reduces external interference and the central conductor provides a controlled impedance. Coaxial cable can carry a signal farther than ordinary twisted pair and has better shielding, but it is bulkier and usually more expensive per port.

Coaxial cable has been used for cable television, early Ethernet, and radio connections. A bus installation must be properly terminated to prevent reflections. Modern office LANs generally use twisted pair because it is easier and cheaper to wire individually.

#### Fibre-optic cable

Fibre carries information as pulses of light through a glass or plastic core surrounded by cladding. It is a guided medium even though the signal is light. Light is affected by different physical rules from an electrical copper signal, so optical transceivers convert electrical data to light and back.

Fibre has very high bandwidth, low attenuation, immunity to electrical interference, no electromagnetic radiation from the signal, and good security. It is suitable for long distances and high-speed backbones. Its limitations include higher equipment cost, more difficult termination, sensitive connectors, and the need for optical interfaces. Single-mode fibre can travel much farther than multimode fibre, but single-mode transceivers and cabling may cost more.

#### Other guided media

- **Shielded twisted pair (STP):** adds a metallic shield for better noise immunity.
- **Leaded cable:** older telephone wiring; not equivalent to modern high-speed Ethernet.
- **Optical guides and waveguides:** carry light in controlled paths.
- **Power-line or metallic broadband:** use electrical conductors for data in special systems.

### 2. Unguided transmission media

Unguided media carry signals through space without a confined cable. Electromagnetic energy is radiated, so the signal can be affected by obstacles, distance, other transmissions, and atmospheric conditions.

#### Radio waves

Radio uses frequency bands such as VHF, UHF, and higher bands for television, cellular communication, Wi-Fi, Bluetooth, and other wireless systems. Radio can penetrate some walls and supports mobility, but it can interfere with other users and is easier to intercept than a well-contained fibre link. Range depends on frequency, power, antennas, obstacles, and regulatory limits.

#### Microwave

Microwave communication uses very high-frequency electromagnetic waves and directional antennas. It can carry large amounts of data between buildings or towers without laying fibre across the ground. It requires a clear line of sight; buildings, terrain, and rain can affect the link. Fixed microwave links are common in telecommunications backbones.

#### Infrared

Infrared uses light in the infrared band. It can be inexpensive and difficult to intercept from outside a room, but it generally has a short range and cannot pass easily through opaque walls. It is used in short-range remote controls and some point-to-point links.

#### Other wireless media

Microwave and radio are examples of unguided media. Satellite communication uses microwave signals over a long path. Optical wireless links can use light in air. Wireless LANs, cellular networks, and satellite links share spectrum and require careful channel allocation.

### 3. Signal characteristics

A transmission system must deal with several physical properties:

- **Attenuation:** signal energy decreases with distance and frequency.
- **Distortion:** the shape of the signal changes so the receiver may misinterpret it.
- **Noise:** unwanted electrical or electromagnetic energy adds uncertainty.
- **Crosstalk:** coupling from one pair or channel into another.
- **Impedance mismatch:** a mismatch at a connection can reflect energy.
- **Jitter/phase variation:** timing changes can make symbols difficult to decode.
- **Bit rate:** number of bits sent per second.
- **Bandwidth:** range or capacity of frequencies/signals a medium can carry.

A channel with more nominal bandwidth can still have poor performance if noise, interference, or distance is severe. A medium's useful bandwidth is the portion that can carry data with an acceptable error rate.

### 4. Guided versus unguided media

| Property | Guided | Unguided |
|---|---|---|
| Path | Physical cable/fibre | Open space |
| Signal | Electrical, light, or guided radio | Radio, microwave, infrared |
| Typical range | Determined by cable and repeaters | Varies by frequency, power, and obstacles |
| Interference | Usually lower with proper shielding | More exposed to shared spectrum |
| Mobility | Usually limited while connected | Naturally supports mobility |
| Installation | Requires cable and connectors | Requires antennas and coverage planning |
| Security | Easier to contain physically | Can be intercepted if not encrypted |

The comparison is a generalisation. Fibre is highly resistant to electrical interference, and well-designed copper can perform well over short distances. Wireless systems can use encryption and directional antennas, while wired media can be tapped physically.

### 5. Transmission modes and duplex

The medium can support different communication modes:

- **simplex:** one direction only;
- **half-duplex:** either direction, one at a time;
- **full-duplex:** both directions at the same time.

Full-duplex can be achieved with separate pairs/fibres, separate frequencies, or advanced time/coding methods. Duplex mode and media type are related but not identical.

### 6. Media selection and network design

Select a medium by asking:

1. What distance must the signal cover?
2. What data rate and bandwidth are required?
3. How much electrical or radio interference is present?
4. Is mobility or flexibility important?
5. What installation and maintenance budget is available?
6. What security and regulatory requirements apply?
7. Can intermediate repeaters, switches, or optical gear be powered and maintained?

A hospital may use fibre between buildings and twisted pair inside rooms. A campus may combine fibre backbones, copper access ports, and Wi-Fi in meeting areas. A rural radio link may be the only practical way to connect distant sites.

### 7. Physical-layer standards

Physical-layer specifications define signalling rates, voltage or optical levels, connectors, cable categories, and encoding. Ethernet over twisted pair and fibre uses different physical specifications even though the higher-level frame format can be similar. A network interface must support the medium and speed actually connected.

## Worked examples

### Example 1: Building network

A university connects two buildings with fibre because the distance is long, the link carries high traffic, and electrical noise is present. Inside each building, it uses Cat 6 twisted pair to access points and wall ports. The design combines high-capacity long-distance media with inexpensive short-distance access.

### Example 2: Wireless comparison

A warehouse uses Wi-Fi because devices must move around and cable installation is expensive. A fixed fibre backbone connects the access points. The wireless access portion is unguided; the fibre portion is guided.

### Example 3: Noise problem

An Ethernet cable runs next to a motor and causes packet errors. Replacing unshielded cable with shielded cable, changing the route, or shortening the run may reduce interference. The issue is physical-layer or link quality, not necessarily an IP configuration problem.

### Example 4: Choosing coax versus fibre

A cable-TV distribution segment can use coax because it is designed for a shared broadcast environment and a controlled distance. A long high-rate backbone between campuses benefits more from fibre's low attenuation and bandwidth. Both are guided media, but the design constraint is different.

## Key terms & formulas

- **Guided media:** signal confined to a physical path.
- **Unguided media:** signal radiates through space.
- **Twisted pair:** two insulated copper conductors twisted to reduce noise.
- **Coaxial cable:** centre conductor, insulation, shield, and outer jacket.
- **Fibre optic:** light pulses through a glass/plastic core and cladding.
- **Attenuation:** loss of signal strength with distance.
- **Crosstalk:** unwanted coupling between pairs/channels.
- **Noise:** unwanted energy that interferes with the signal.
- **Bandwidth:** information-carrying capacity of a medium/channel.
- **Bit rate:** `bits per second`.
- **Nyquist relation (ideal noiseless channel):** `C = 2 B log2(M)` bits/s.
- **Shannon relation (with noise):** `C = B log2(1 + S/N)` bits/s.
- **Ethernet copper reach:** commonly 100 m for a twisted-pair link segment.
- **Full-duplex:** simultaneous two-way communication.
- **Attenuation compensation:** amplifier, repeater, or regenerative receiver.

## Common mistakes

1. **Fibre carries light, not electrical data pulses through copper.** Electrical interfaces are still used at the ends.
2. **Twisted pair is not only one wire.** The two conductors carry a differential signal.
3. **Coax shielding is not complete immunity.** Poor terminations and bends can still cause faults.
4. **Wireless is not automatically faster or slower than wired.** It depends on spectrum, modulation, interference, and link design.
5. **Bandwidth is not the same as bit rate.** Modulation, noise, overhead, and protocol limits affect the achieved rate.
6. **A longer distance is not always better.** It increases attenuation, delay, and cost.
7. **Attenuation and distortion are different.** Attenuation reduces strength; distortion changes the waveform.
8. **Crosstalk is not ordinary external noise.** It is coupling from another nearby conductor or channel.
9. **Unguided does not mean no antennas or infrastructure.** Wireless networks need carefully placed access points and spectrum planning.
10. **Physical media alone do not guarantee security.** Encryption and access control are still needed.

## Exam prep

### Likely 2-mark questions

1. **Define guided and unguided media and give two examples of each.**  
   Hint: twisted pair/coax/fibre versus radio/microwave/infrared.
2. **List four characteristics used to compare media.**  
   Hint: bandwidth, attenuation, interference, distance, cost, security, and mobility.
3. **Why is twisted pair twisted?**  
   Hint: reduce radiation and crosstalk by cancelling common-mode noise.
4. **Give two advantages of fibre-optic communication.**  
   Hint: high bandwidth, long distance, low attenuation, and electrical-noise immunity.
5. **Why is fibre a guided medium?**  
   Hint: light is confined to the fibre core by the cladding.
6. **Define attenuation and crosstalk.**  
   Hint: signal-strength loss and unwanted coupling between conductors.

### Likely long-answer questions

1. **Compare guided and unguided media with examples, characteristics, and selection criteria.**  
   Answer hint: construction, signal, interference, range, mobility, cost, and a design scenario.
2. **Explain the construction and advantages of twisted-pair, coaxial, and fibre-optic media.**  
   Answer hint: physical layers, noise behaviour, bandwidth, reach, installation, and applications.
3. **Explain the effects of attenuation, distortion, noise, and crosstalk on a transmission system.**  
   Answer hint: define each, give a cause/effect pair, and suggest a mitigation.
4. **Design media for a campus network.**  
   Answer hint: fibre backbone, copper access, wireless mobility, and reasons for each choice.

### Short-answer revision checklist

Be ready to draw the basic construction of twisted pair, coax, and fibre; identify guided/unguided examples; and state what signal is carried by each.
