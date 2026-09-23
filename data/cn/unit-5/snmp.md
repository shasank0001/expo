---
subject: cn
unit: 5
topic: snmp
syllabus_ref: CSM3103 Unit-V
status: draft
---
# Simple Network Management Protocol (SNMP)

## Overview

**Simple Network Management Protocol (SNMP)** is an application-layer protocol for monitoring and sometimes controlling network-managed devices. A **manager** collects information and issues actions, while an **agent** on each managed device exposes operational data and performs requested operations.

SNMP models device information with a **Management Information Base (MIB)**. Objects have names, types, values, and access modes. Managers use operations such as GET and GET-NEXT to read values and SET to request changes. Agents can return responses and send notifications such as TRAP or INFORM.

SNMP commonly uses UDP ports 161 for manager requests and 162 for agent notifications. Its simplicity and broad device support make it widely deployed, but its security depends strongly on the version and configuration. The syllabus includes SNMP and SNMP versions/security; this file explains architecture, MIBs, operations, notifications, polling/traps, and management design.

## Explanation

### 1. SNMP architecture

An SNMP system has two main roles:

- **manager/management station:** a network-management application and process that queries devices, schedules polling, processes responses, and issues commands;
- **agent/managed agent:** software on a router, switch, server, printer, access point, or other device that maintains local counters, answers requests, and sends notifications.

A manager can be a workstation or a network-management system (NMS) that monitors many agents. The agent is not a separate physical device; it is a process and data model inside a managed device.

SNMP operates over an application-layer transport, commonly UDP. A manager-to-agent request carries a community string or security credentials, a request identifier, and one or more operations. The agent returns a response or notification.

### 2. Managed objects and the MIB

A **managed object** is a variable representing a device property or counter, such as:

- interface index and operational status;
- input/output octets;
- error counters;
- CPU or memory use;
- routing table entries;
- system name and uptime.

A **MIB** is a structured, vendor-independent or vendor-specific catalogue of managed objects. Each object has an **object identifier (OID)**, a tree of numeric labels such as `1.3.6.1.2.1.1.1.0` or `1.3.6.1.2.1.2.2.1.10`. The OID identifies the object; a value is an instance of that object at a particular index.

MIBs are not the live database itself. The agent maintains current values based on the device, and the MIB defines how the values are named, typed, and interpreted. Vendors can define private MIB extensions, but a manager needs the relevant MIB definitions.

### 3. OID hierarchy

OIDs are arranged in a tree. Common standard branches include:

- `1.3.6.1.2.1` for standard management objects;
- system, interfaces, IP, routing, and other MIB-2 areas;
- private enterprise branches for vendor-specific objects.

An OID such as `.1.3.6.1.2.1.1.5.0` identifies the system name (`sysName`) instance. An interface counter may include an interface index, such as `.1.3.6.1.2.1.2.2.1.10.<ifIndex>`.

A dotted numeric OID is precise, while a textual name such as `IF-MIB::ifInOctets` is easier for people and tools. Textual names must be mapped using MIB definitions; they are not arbitrary aliases.

### 4. GET and GET-NEXT

**GET** requests the current value of one or more OIDs. A manager can poll a device and retrieve, for example, the system uptime and a particular interface's octet count.

**GET-NEXT (or GETBULK in modern use)** requests the next object in a MIB subtree. Repeated GET-NEXT operations can walk a table, such as all interfaces or all ARP entries. A manager uses the returned lexicographic/tree order to discover available objects.

GET requests can be lost or unanswered. The manager times out and may retry. A GET does not change the device; a SET is needed for configuration or action, subject to access control.

### 5. SET and controlled actions

**SET** requests that an agent change a writable managed object or perform an action. For example, an operator might set an interface description, enable a monitored feature, or restart a device if the MIB defines that operation.

The agent validates the type, value, permissions, and safety of the request. It may accept, reject, or return a value that reflects the actual state. SET should be protected with authentication and authorisation because an incorrect or malicious command can disrupt a network.

SNMP is often used primarily for monitoring. A separate control system or a carefully designed management ACL should govern sensitive writes.

### 6. Polling and notification

In polling, the manager sends periodic GET/GET-NEXT requests and compares values or rates. Polling gives predictable control but consumes manager and device resources and may miss short-lived events.

A **trap** is an unsolicited notification sent by an agent to a configured manager, commonly on UDP port 162. Traps can report link down, authentication failure, threshold crossing, cold start, or other events. They are low-overhead but less reliable and harder to correlate because UDP delivery is not guaranteed.

An **inform** is a notification that expects an acknowledgement. Some versions/profiles use it when more reliable delivery matters. Notifications still need authentication and should be rate-limited.

### 7. MIB browsing and discovery

An NMS can browse a device's MIB using GET-NEXT or a protocol/tool that walks the object tree. Browsing can discover supported interfaces, system information, vendor objects, and capabilities.

A manager should load the correct standard and vendor MIBs. A missing MIB can cause a tool to show an OID numerically but not a friendly name or correct type. MIB discovery must be limited to authorised devices to avoid load and information leakage.

### 8. Counter interpretation

Many SNMP values are **counters**, meaning they increase over time and may wrap around. To estimate a rate, the manager samples a counter twice and computes:

`rate = (counter2 - counter1) / elapsed_time`

If the counter wraps, the manager must handle modulo arithmetic or the value may appear negative. A sudden reboot can reset a counter to zero. The manager should detect resets and avoid interpreting them as a negative traffic rate.

Gauge values represent an instantaneous condition, such as a temperature or queue length, and do not need differencing. Correct interpretation requires the MIB type and description.

### 9. Transport and ports

SNMP commonly uses:

- **UDP 161:** manager requests and agent responses;
- **UDP 162:** agent-to-manager traps/informs.

UDP is simple and low-overhead for management traffic, but it does not guarantee delivery or order. A manager can use retries, timestamps, and acknowledgements where the protocol provides them. SNMP can run over other transports in specialised environments, but TCP/161 is less common in basic deployments.

The exact port direction and implementation may vary with SNMP version, transport mapping, and configuration. An exam should use the standard request/notification ports.

### 10. Poll intervals and scalability

A manager must choose polling intervals. More frequent polling gives faster detection but increases CPU, bandwidth, and device load. Less frequent polling reduces overhead but delays discovery of a fault.

A large network can use hierarchical polling or a manager-of-managers design. Collection can be centralised, distributed, or delegated to regional collectors. Data rates and thresholds should be chosen to avoid measuring insignificant changes and to preserve capacity during an incident.

### 11. Configuration and MIB views

Access control can restrict which manager addresses may read or write which OIDs. SNMPv3 views and communities can provide management isolation. A good deployment uses a dedicated management network, ACLs, and separate credentials from ordinary user access.

A MIB view limits the part of the management tree a principal can see. Restricting a manager to interface counters reduces exposure of sensitive system objects. Write access should be even narrower.

### 12. SNMP operations example

A manager wants to monitor interface 3:

1. It sends a GET for the interface's `ifInOctets` OID instance.
2. The agent returns a counter value and request ID.
3. The manager samples it again after 30 seconds.
4. It calculates the input bit rate from the difference and elapsed time.
5. If the counter reset or a threshold is crossed, it raises an alert; a separate TRAP/INFORM may report the event.

The request ID and source context let the manager match a response to its request. Multiple managers or agents can operate concurrently.

## Worked examples

### Example 1: Manager GET

A manager sends:

`GET sysName.0, sysUpTime.0`

The agent returns the device name and uptime with matching request identifiers. No configuration is changed.

### Example 2: GET-NEXT table walk

A manager sends GET-NEXT for the first interface OID. The agent returns the first supported interface object; the manager asks for the next and continues until it leaves the interface subtree. This discovers interfaces without knowing their indices in advance.

### Example 3: Link-down trap

An agent detects an interface failure and sends a trap to the manager on UDP 162. The manager displays an alert. If the trap is lost, a polling interval or a later threshold check is still needed because UDP is not reliable.

### Example 4: Counter rate

Interface input counter increases from 1,000,000 to 4,000,000 bytes in 10 seconds. The average rate is:

`(4,000,000 - 1,000,000) / 10 = 300,000 bytes/s = 2.4 Mbit/s`

The manager must check for a counter reset and confirm the counter's units in the MIB.

### Example 5: Controlled SET

An operator sets an interface description. The agent checks that the object is writable and the requester has access. If valid, it returns the new value; if not, it returns an error. A stronger management design may use SET only for a controlled subset of objects.

## Key terms & formulas

- **SNMP:** Simple Network Management Protocol.
- **Manager:** monitoring/control station.
- **Agent:** software on a managed device.
- **MIB:** Management Information Base.
- **Managed object:** named device variable.
- **OID:** object identifier in a MIB tree.
- **GET:** read one or more values.
- **GET-NEXT:** read the next object in a subtree.
- **GETBULK:** efficient bulk retrieval in modern SNMP.
- **SET:** request a writable value change/action.
- **TRAP:** unsolicited notification.
- **INFORM:** notification with acknowledgement expectation.
- **Polling:** manager-initiated periodic query.
- **Counter rate:** `(C2 - C1) / time`.
- **Counter wrap:** reset/wrap must be handled.
- **MIB view:** restricted object tree for a manager.
- **Ports:** UDP 161 requests, UDP 162 notifications.

## Common mistakes

1. **SNMP manager and agent are not both managers.** The manager initiates most requests; the agent answers and can notify.
2. **MIB is not the live device database.** It defines the objects; the agent maintains values.
3. **OID is an identifier, not a value.** The value is an instance at that OID.
4. **GET does not configure a device.** SET is the operation that requests a change.
5. **GET-NEXT is not the same as a random query.** It follows the MIB tree order.
6. **A trap is not guaranteed to arrive.** UDP notifications can be lost; polling provides backup.
7. **SNMP usually uses UDP 161 and 162.** Do not swap request and notification roles.
8. **A counter difference is not a rate without dividing by elapsed time.** Detect resets and wraparound too.
9. **Community strings are not strong authentication.** Security version and deployment matter.
10. **SNMP monitoring is not automatically safe.** Polling too often can load a device.
11. **MIB discovery can expose device details.** Protect and limit management access.

## Exam prep

### Likely 2-mark questions

1. **Name the two main SNMP roles.**  
   Hint: manager and agent.
2. **What is a MIB?**  
   Hint: structured catalogue of managed objects and their identifiers/types.
3. **State the purpose of GET and SET.**  
   Hint: read values versus request a change.
4. **What is a trap?**  
   Hint: unsolicited agent notification to a manager.
5. **State common SNMP ports.**  
   Hint: UDP 161 requests, UDP 162 notifications.
6. **How is a counter rate calculated?**  
   Hint: difference between two samples divided by elapsed time, handling reset/wrap.

### Likely long-answer questions

1. **Explain SNMP manager, agent, MIB, and OID architecture.**  
   Answer hint: roles, managed objects, MIB tree, OID instances, standard/vendor MIBs.
2. **Compare GET, GET-NEXT/GETBULK, and SET.**  
   Answer hint: reads, table walking/bulk, controlled writes, validation, and error handling.
3. **Explain polling versus traps/informs.**  
   Answer hint: predictable periodic reads versus event-driven notifications, UDP reliability, and hybrid design.
4. **Design an SNMP monitoring system for a campus network.**  
   Answer hint: manager/collectors, polling schedule, MIBs, thresholds, ports, ACLs, and alerts.
5. **Explain how to calculate an interface bit rate and handle counter reset.**  
   Answer hint: two samples, time difference, units, wrap/reset detection, and MIB type.

### Short-answer revision checklist

Be able to define manager/agent/MIB/OID, state GET/SET/GET-NEXT/TRAP, remember ports 161/162, and calculate a counter rate with reset handling.
