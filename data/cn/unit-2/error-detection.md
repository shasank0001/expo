---
subject: cn
unit: 2
topic: error-detection
syllabus_ref: CSM3103 Unit-II
status: draft
---
# Error Detection in the Data-Link Layer

## Overview

Transmission errors occur when noise, interference, attenuation, or faulty equipment changes a bit between sender and receiver. **Error detection** adds a carefully calculated check value so the receiver can discover many damaged frames. Detection does not necessarily repair the data. A protocol may discard a bad frame, ask for retransmission, or pass the result upward for a higher layer to handle.

The syllabus places error detection in the data-link layer. This file covers the need for it, parity, checksums, cyclic redundancy checks, polynomial division, error patterns, detection guarantees, and worked calculations. Ethernet, Wi-Fi, PPP, HDLC, and many storage systems use error-detection ideas, although their exact fields and polynomial widths differ.

## Explanation

### 1. Why detect errors?

A physical link cannot promise that every bit arrives correctly. Errors can arise from thermal noise, electrical interference, crosstalk, signal reflection, radio fading, connector faults, and sudden changes in the medium. A receiver needs to distinguish a valid frame from a damaged one before using its address or payload.

Without detection, a corrupted address could deliver data to the wrong station, a corrupted length field could make the receiver wait for the wrong number of bytes, and a corrupted payload could silently reach an application. Detection improves reliability, but it adds header bits, computation, and a response when an error occurs.

### 2. Error, codeword, and redundancy

A code takes `k` information bits and produces an `n`-bit **codeword**, with `n - k` redundant check bits. A receiver computes a check condition. A valid codeword satisfies the code's mathematical rule; a damaged word may violate it.

The number and position of check bits affect the kinds of error patterns detected. A simple code may catch a single error but miss some multiple-bit errors. A stronger code can detect more patterns or correct limited errors, at the cost of extra bits.

A useful distinction is:

- **undetected error:** a damaged codeword still passes the check;
- **detected error:** the check fails;
- **corrected error:** redundancy identifies and repairs the original value;
- **retransmission:** the receiver asks the sender to send the data again.

### 3. Parity

**Parity** adds one or more bits so that the number of 1s has a required parity.

- **Even parity:** the total number of 1s, including the parity bit, is even.
- **Odd parity:** the total number of 1s is odd.

For 4 data bits `1011`, there are three 1s. An even-parity bit must be `1` to make the total four; an odd-parity bit must be `0` to keep the total three.

Parity can detect an odd number of bit errors in the data-plus-parity word, but it can miss an even number of errors. Two parity bits (two-dimensional parity) improve detection but still do not provide general correction.

### 4. Internet checksum

A checksum adds a fixed-size check word computed by one's-complement addition of 16-bit words. The sender forms a one's-complement sum, puts the complement in the checksum field, and transmits the data. The receiver forms the sum including the checksum; a result of all 1s (after complement rules) indicates no detected error.

The Internet checksum is simple in software and is used by IPv4, TCP, UDP, and ICMP in various forms. It is not a cryptographic integrity mechanism: an attacker can deliberately construct a modified payload with the same checksum. It also does not guarantee that every error is detected.

### 5. Cyclic redundancy check (CRC)

A **cyclic redundancy check** treats a frame as a polynomial over GF(2), divides it modulo 2 by a generator polynomial, and appends the remainder. The receiver divides the received codeword by the same generator. A valid codeword has a zero remainder; a detected error generally produces a nonzero remainder.

In GF(2):

- addition and subtraction are both XOR;
- there is no carry;
- division is performed by bitwise XOR shifts.

A common representation is `message(x) * x^r + remainder(x)`, where `r` is the degree of the generator polynomial. The remainder is the FCS, commonly 16, 32, or another number of bits.

Ethernet uses a 32-bit CRC commonly associated with the generator polynomial `x^32 + x^26 + x^23 + x^22 + x^16 + x^12 + x^11 + x^10 + x^8 + x^7 + x^5 + x^4 + x^2 + 1` (the exact notation and bit ordering are protocol-specific). A detailed exam calculation should use the generator supplied in the question.

### 6. Worked CRC procedure

Given data `1011001` and generator `1011` (`r = 3`):

1. Append three zeros: `1011001000`.
2. Divide this value by `1011` using XOR.
3. The remainder is `001` in one common convention.
4. The transmitted codeword is `1011001` + `001` = `1011001001`.

At the receiver, divide `1011001001` by `1011`. The remainder is zero for an undamaged codeword. If a bit changes, the remainder will normally be nonzero.

The exact division and bit order should be shown in an exam rather than relying only on a final number.

### 7. CRC properties and burst errors

A CRC is especially effective at detecting **burst errors**, in which several consecutive bits change. With a generator of degree `r`, a well-designed CRC can detect all single-bit errors, all double-bit errors under common distance properties, and all burst errors of length at most `r` (subject to the polynomial's conditions). Larger bursts are detected with very high probability, but detection is not absolute for every possible pattern.

A good generator has suitable mathematical properties, including a nonzero constant term and appropriate distance properties. A weak or poorly chosen polynomial can miss common errors.

### 8. Error detection versus error correction

A checksum or CRC is efficient when the receiver can ask for retransmission. If the return path is slow, expensive, or unavailable, forward error correction may be better. Error-correction codes add more redundancy and include a decoder capable of locating or correcting errors.

An ARQ protocol uses detection plus retransmission. A forward-error-correction protocol uses a codeword designed to recover limited errors without waiting for another transmission.

### 9. Protocol examples

- **Ethernet:** an FCS containing a 32-bit CRC; a bad frame is normally discarded.
- **Wi-Fi:** a frame check sequence protects the MAC frame; the receiver checks it and may signal failure depending on the protocol.
- **PPP:** a FCS commonly uses a 16-bit CRC.
- **HDLC:** a 16-bit FCS and sequence/acknowledgement mechanisms.
- **Storage:** SATA, NVMe, and disks use checks or CRCs to detect corruption, often with repair or bad-block handling.
- **IP/TCP/UDP:** checksums detect accidental corruption at their own scopes, but do not provide cryptographic authentication.

### 10. What happens after detection?

The receiver must choose a policy:

1. **Discard:** simple, but the sender may retry.
2. **Return an error/negative acknowledgement:** asks for retransmission.
3. **Forward an error indicator:** lets a higher layer decide.
4. **Correct in place:** possible only with an error-correction code.
5. **Repair from redundant storage or parity:** used in storage systems.

The design choice depends on latency, link speed, error rate, and the cost of retransmission. On a satellite link, a long round trip may make correction attractive; on a fast wired LAN, detection and quick retransmission may be simpler.

## Worked examples

### Example 1: Parity

Data `1001` has two 1s, so an even-parity bit is `0` and an odd-parity bit is `1`. If one bit flips, even parity may detect the error, but if two bits flip, even parity may still appear valid.

### Example 2: Internet checksum concept

Split data into 16-bit words, add them with end-around carry, complement the sum, and place the result in the checksum field. The receiver repeats the calculation. This demonstrates the method; a complete numerical example should show each intermediate hexadecimal word.

### Example 3: CRC with a small generator

For a one-bit error in a codeword protected by a suitable CRC, the received word differs from the valid word in one position and produces a nonzero remainder. This is why Ethernet's FCS can detect ordinary isolated bit corruption.

### Example 4: Retransmission

A receiver detects a bad frame and sends a NAK or waits for a timeout. The sender retransmits the same sequence number. The receiver must distinguish a retransmission from a duplicate so that it does not deliver the data twice. This links error detection to elementary protocols and sliding windows.

### Example 5: Checksums are not security

An attacker can alter a message and recompute its checksum. A checksum is useful against accidental noise, not a malicious person who controls the sender. Authentication requires cryptographic message authentication or a digital signature.

## Key terms & formulas

- **Error detection:** discover transmission errors with redundancy.
- **Error:** received bit differs from the sent bit.
- **Redundancy:** extra information for checking, correcting, or recovering.
- **Codeword:** information plus redundancy.
- **Parity:** even/odd count of 1 bits.
- **Internet checksum:** one's-complement 16-bit sum.
- **CRC:** polynomial remainder over GF(2).
- **Generator:** divisor polynomial in CRC calculation.
- **Remainder:** CRC result, usually sent as the FCS.
- **FCS:** frame check sequence field containing a checksum/CRC.
- **Burst error:** several consecutive changed bits.
- **Detection probability:** likelihood that a specified error pattern is detected.
- **CRC computation:** `code = data || remainder`; `remainder = (data * x^r) mod generator`.
- **Ethernet FCS:** 32-bit CRC in the common Ethernet frame format.
- **Undetected-error rate:** `1 - detection probability` for a specified error model.

## Common mistakes

1. **Error detection is not error correction.** Detection says “something is wrong”; correction restores the original data.
2. **A checksum is not encryption.** It does not provide confidentiality or sender authentication.
3. **Parity does not detect every error.** An even number of changed bits can remain valid.
4. **CRC is not simple division in ordinary integer arithmetic.** It uses XOR and polynomial arithmetic over GF(2).
5. **The generator degree is the number of appended zeros for the initial division.** It is not automatically the FCS length in every description.
6. **A nonzero CRC remainder indicates a detected failure, not which bit failed.** Correction is a separate mechanism.
7. **Ethernet does not retransmit a bad frame by itself.** The normal FCS action is to discard it; higher protocols may recover.
8. **A checksum cannot prove that a frame is authentic.** An attacker can calculate a matching value.
9. **More redundant bits do not automatically make every error detectable.** Code choice and error patterns matter.
10. **A CRC is local unless another protocol uses it end-to-end.** Its FCS is normally regenerated or checked per link.

## Exam prep

### Likely 2-mark questions

1. **Why is error detection needed at the data-link layer?**  
   Hint: noise/interference changes bits; detection prevents corrupted frames being accepted.
2. **Define even and odd parity.**  
   Hint: total number of 1s including the parity bit.
3. **What is a CRC?**  
   Hint: a polynomial remainder using GF(2) division, usually stored as an FCS.
4. **State two differences between checksum and CRC.**  
   Hint: arithmetic/operation, typical use, and strength; avoid saying one never detects errors.
5. **What does a zero CRC remainder mean on reception?**  
   Hint: the received codeword satisfies the code and no error was detected, not absolute proof of correctness.
6. **What is a burst error?**  
   Hint: several consecutive bits changed.

### Likely long-answer questions

1. **Explain parity, Internet checksum, and CRC with examples.**  
   Answer hint: define each, show the check field, describe operation, and state limitations.
2. **Perform a CRC division and explain the result.**  
   Answer hint: append `r` zeros, XOR-divide, record remainder, append it, and verify at the receiver.
3. **Compare error detection, error correction, and retransmission.**  
   Answer hint: mechanism, redundancy, delay, and suitable environments.
4. **Explain how a CRC protects an Ethernet frame and what happens after failure.**  
   Answer hint: FCS calculation, receiver check, discard, and higher-layer recovery.

### Short-answer revision checklist

Be ready to calculate a small parity and CRC example, define FCS, explain GF(2), and distinguish accidental error detection from cryptographic integrity.
