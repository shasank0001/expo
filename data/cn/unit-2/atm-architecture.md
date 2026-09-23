---
subject: cn
unit: 2
topic: atm-architecture
syllabus_ref: CSM3103 Unit-II
status: draft
---
# Asynchronous Transfer Mode (ATM) Architecture

## Overview

**Asynchronous Transfer Mode (ATM)** is a connection-oriented, cell-switching technology designed to carry voice, video, and data in one integrated network. Its defining idea is to divide information into small, fixed-size **cells** and label them with a virtual-circuit identifier. Switches can then forward cells quickly with predictable hardware processing.

ATM was important in telecommunications and high-speed enterprise backbones. It is not the same as IP packet switching: IP generally forwards independent packets and offers best effort, while ATM establishes a virtual circuit and can negotiate quality-of-service guarantees. The technology is now less common than MPLS and Ethernet/IP, but its architecture remains important for understanding virtual circuits, QoS, and cell relay.

The syllabus includes ATM architecture and layers. This file explains the cell, virtual path/channel, ATM layer, physical layer, adaptation layer, service categories, traffic management, advantages, limitations, and a worked cell-forwarding example.

## Explanation

### 1. ATM design goals

ATM was designed to support several traffic types:

- constant-rate voice;
- variable-rate video;
- data and file transfer;
- traffic with strict delay or jitter requirements;
- bursty data traffic.

The design goals were predictable delay, controlled bandwidth, statistical multiplexing, and integrated service. Small fixed cells make switch queues and timing behaviour predictable. A virtual circuit reserves or associates a path so that cells for one flow follow a known route through switches.

### 2. ATM cell format

An ATM cell is **53 bytes** long:

- **5-byte header (header/header-error control):** contains VPI/VCI, payload type, CLP, and header-error information;
- **48-byte payload:** user data, signalling, or management information.

The fixed size makes parsing and switching hardware simple. A large IP packet may be segmented into multiple ATM cells. A small application message may be padded, which is an inefficiency. The small cell also adds header overhead for short packets, but that is accepted in exchange for predictable cell processing.

The **Virtual Path Identifier (VPI)** and **Virtual Channel Identifier (VCI)** together identify a virtual circuit at a particular link. A VPI groups many virtual channels, while a VCI identifies one channel within that group. Labels are changed at each switch according to the connection's forwarding table; they are not a globally unique end-to-end IP address.

### 3. ATM physical layer

The ATM physical layer provides transmission of cells over a chosen medium and defines characteristics such as electrical/optical signalling, line rate, timing, and cell alignment. It is broadly analogous to an OSI physical layer but is specified together with ATM's transmission convergence functions.

ATM has been defined over fibre, copper, and other media. The physical layer must transmit 53-byte cells and allow the receiver to identify cell boundaries. It may also provide operations, maintenance, and error-related functions.

### 4. ATM layer

The **ATM layer** is the common switching and multiplexing layer. It handles:

- cell multiplexing;
- virtual-path and virtual-channel switching;
- cell header generation and removal;
- header error control;
- cell transfer and QoS-related functions.

At a switch, the input port and VPI/VCI select an output port and a new label. The switch forwards the 48-byte payload with a new cell header. ATM does not normally examine the full user message; it switches fixed cells quickly.

The header-error-control field detects some header errors before the cell is used for forwarding. A defective cell can be discarded according to the service and protocol policy.

### 5. ATM adaptation layer (AAL)

The **ATM Adaptation Layer (AAL)** presents suitable services to upper-layer protocols while hiding differences between ATM cells and application messages. It handles segmentation and reassembly, because application data may not be a multiple of 48 bytes.

Common AAL concepts include:

- **AAL1:** constant-rate, real-time services such as fixed-bandwidth voice;
- **AAL2:** variable-rate real-time or packetised services with tighter timing;
- **AAL3/4:** data services, with error recovery and segmentation/reassembly;
- **AAL5:** simpler data service with segmentation/reassembly and trailer-oriented framing.

AAL functionality is a good example of a layer's purpose: ATM switches cells, while the AAL makes the cell transport useful to a particular application. Different AALs provide different error, ordering, timing, and bandwidth assumptions.

### 6. Virtual circuits

ATM is **connection-oriented**. Before user data is sent, a signalling procedure establishes a virtual circuit. A call can reserve resources and select a service category. Each cell then carries the VPI/VCI label, and switches forward it without examining the complete destination IP address.

A **virtual channel** is a logical connection between endpoints. A **virtual path** bundles multiple virtual channels that share a path. This reduces the number of separate switching-table entries in some network designs.

A virtual circuit is not a physical dedicated wire. Several cells from different circuits can share the same physical link, and the label identifies the logical flow. However, a QoS reservation can reserve capacity even when the link is physically shared.

### 7. Connection types

ATM supports **point-to-point** virtual circuits, where endpoints communicate over a path, and **point-to-multipoint** circuits, where one source sends to several receivers. Multicast traffic is useful for video distribution and conference systems.

The connection is established for a session, and cells belonging to it carry the same local label at each switch. If a switch or link fails, the connection may need to be re-established or repaired; ATM is not automatically resilient to every failure.

### 8. Service categories and QoS

ATM defines service categories to describe traffic behaviour and resource guarantees. Common categories in the ATM Forum model include:

- **Constant-bit-rate (CBR):** predictable rate, often for voice; strict timing and delay.
- **Variable-bit-rate (VBR):** average and peak rate with burst allowance.
- **Available-bit-rate (ABR):** applications indicate a minimum and maximum requirement; the network tries to provide at least the minimum.
- **Unspecified-bit-rate (UBR):** best effort, no guarantee.

The service category affects admission control, queueing, scheduling, and how congestion is handled. A network may reject a CBR connection if it cannot reserve the required resources, while an ABR or UBR flow can adapt more.

### 9. Traffic and congestion management

ATM uses a combination of:

- connection admission control;
- traffic shaping at the edge;
- traffic policing;
- per-virtual-channel queues;
- service-specific scheduling;
- cell loss priority (CLP) marking;
- feedback or resource management for ABR.

The cell header includes a **Cell Loss Priority (CLP)** bit. A cell marked low priority may be discarded before a high-priority cell when the network is congested. This helps protect delay-sensitive traffic, though it does not make the network lossless.

ATM can use **peak cell rate (PCR)**, **sustainable cell rate (SCR)**, and **burst cell rate** in traffic descriptors. These values help the network decide whether the offered traffic fits the connection and the available capacity.

### 10. Cell switching example

Suppose a video call has a virtual-circuit label VPI 3, VCI 20 on the first link. An input switch looks up `(input port, VPI 3, VCI 20)` and finds an outgoing port and a new label, perhaps VPI 1, VCI 8. It copies the 48-byte payload into a new cell with the new label. The next switch repeats the procedure. The application does not need to know the label changes.

If a queue is full, the switch may drop a low-CLP cell first. A higher-priority control or CBR cell is more likely to be scheduled on time, while the sender or network may react to the resulting quality change.

### 11. Advantages of ATM

- Integrated service for voice, video, and data.
- Small fixed cells for predictable switching.
- Virtual circuits and explicit QoS.
- Statistical multiplexing of bursty traffic.
- Traffic shaping and priority mechanisms.
- Efficient hardware switching and service categories.

### 12. Limitations of ATM

- Small cell overhead is high for short IP packets.
- Connection setup adds delay and state.
- IP and Ethernet became dominant, with simpler and more flexible deployment.
- ATM network management and service definitions can be complex.
- A connection-oriented virtual circuit is less flexible than IP's connectionless forwarding.
- A single service category or reservation may waste resources when traffic is bursty.
- Historical deployment requires compatible equipment and trained operators.

## Worked examples

### Example 1: Cell segmentation

A 1,200-byte application message is carried by ATM. After adaptation-layer overhead, the data is split into 48-byte cell payloads. If the useful data is exactly 1,200 bytes, it requires 25 cells (`1,200 / 48 = 25`). Each cell has a 5-byte header, so the total cell transmission overhead is `25 x 5 = 125` bytes, excluding other fields and physical framing.

### Example 2: CBR video

A camera sends a constant number of cells per second on a reserved CBR virtual circuit. Switches schedule the cells predictably. If the network cannot provide the reserved rate, it may refuse the connection or provide a different service category; it does not silently guarantee the rate as IP best effort would.

### Example 3: VCI translation

A cell arrives with VPI 5, VCI 100. The switch's table maps that label to an output fibre and VPI 2, VCI 40. The switch changes the label and forwards the payload. The endpoints may see the connection as one logical channel even though labels differ at each hop.

### Example 4: Congestion and CLP

A file-transfer circuit and a voice circuit compete for a buffer. The network marks some file cells CLP 1. When the queue is full, low-priority cells are discarded first. Voice cells may be delayed less, although loss or delay can still affect the voice call.

## Key terms & formulas

- **ATM:** Asynchronous Transfer Mode.
- **Cell:** fixed 53-byte ATM unit.
- **Header:** 5 bytes.
- **Payload:** 48 bytes.
- **VPI:** virtual path identifier.
- **VCI:** virtual channel identifier.
- **ATM layer:** cell switching/multiplexing layer.
- **AAL:** ATM adaptation layer.
- **CBR:** constant-bit-rate service.
- **VBR:** variable-bit-rate service.
- **ABR:** available-bit-rate service.
- **UBR:** unspecified-bit-rate service.
- **CLP:** cell-loss-priority bit.
- **PCR:** peak cell rate.
- **SCR:** sustainable cell rate.
- **Cell overhead:** `5 / 53` of each cell, approximately 9.43%.
- **Cells for `L` bytes:** approximately `ceil(L / 48)` before adaptation overhead.
- **Point-to-multipoint:** one source, multiple virtual-circuit destinations.

## Common mistakes

1. **ATM cells are not 48 bytes total.** The cell is 53 bytes: 5-byte header plus 48-byte payload.
2. **ATM is not ordinary IP packet switching.** It establishes a virtual circuit and switches labelled cells.
3. **A virtual circuit is not a dedicated physical cable.** Multiple circuits can share the same link.
4. **The ATM layer does not normally understand the whole application message.** It switches cells.
5. **AAL is not the switching layer.** It adapts upper-layer data to ATM cells.
6. **CBR, VBR, ABR, and UBR are not all best effort.** They describe different traffic/service assumptions.
7. **A VPI/VCI is not a global IP address.** It identifies a connection on a link and is translated by switches.
8. **Small cells do not mean low total overhead.** Short messages pay a large 5-byte header proportion.
9. **CLP does not make ATM lossless.** It gives the switch a priority hint during congestion.
10. **ATM is not the same as a virtual LAN.** It is a connection-oriented cell-switching architecture.

## Exam prep

### Likely 2-mark questions

1. **State the ATM cell size and its two parts.**  
   Hint: 53 bytes = 5-byte header + 48-byte payload.
2. **Why does ATM use fixed-size cells?**  
   Hint: predictable, fast switching and simple hardware queues.
3. **What is a virtual circuit?**  
   Hint: a logical, connection-oriented path identified by VPI/VCI labels.
4. **Name the broad ATM layers.**  
   Hint: physical, ATM, and ATM adaptation layers.
5. **Give two ATM service categories.**  
   Hint: CBR, VBR, ABR, or UBR.
6. **What is the function of the AAL?**  
   Hint: adapt application data to ATM cells, including segmentation/reassembly.

### Likely long-answer questions

1. **Explain ATM architecture from application message to switched cell.**  
   Answer hint: AAL segmentation, 5/48-byte cell, header fields, VPI/VCI switching, and reassembly.
2. **Compare ATM with IP packet switching.**  
   Answer hint: connection setup, cells versus packets, QoS, flexibility, overhead, and deployment.
3. **Explain ATM service categories and traffic management.**  
   Answer hint: CBR/VBR/ABR/UBR, admission, shaping, policing, queues, CLP, and scheduling.
4. **Trace an ATM cell through a switch and explain label translation.**  
   Answer hint: input lookup, output port, new VPI/VCI, payload preservation, and CLP handling.

### Short-answer revision checklist

Be able to draw a 53-byte cell, state 5 plus 48, define VPI/VCI and AAL, and explain why ATM can provide predictable QoS better than ordinary best-effort IP.
