---
subject: cn
unit: 2
topic: error-correction
syllabus_ref: CSM3103 Unit-II
status: draft
---
# Error Correction

## Overview

**Error correction** allows a receiver to identify and repair certain transmission errors without asking the sender to send the data again. It uses deliberately designed redundancy: extra symbols are added to the original information so that the decoder can infer which value was most likely sent.

Error detection alone tells the receiver that a codeword is invalid. Error correction goes further and attempts to reconstruct the valid codeword. Forward error correction (FEC) is especially useful on satellite, wireless, deep-space, and real-time links where retransmission would take too long or where a late retransmission is less useful than an approximate or corrected message.

The syllabus includes error correction alongside detection and elementary data-link protocols. This file explains codewords, block and convolutional codes, Hamming and BCH concepts, Reed-Solomon, interleaving, ARQ versus FEC, and the trade-offs between correction power, bandwidth, complexity, and delay.

## Explanation

### 1. Redundancy and codewords

A code maps `k` information symbols to an `n`-symbol codeword, where `n > k`. The extra `n - k` symbols are redundancy. They do not carry new user information; they make the valid codewords have a measurable distance or algebraic structure.

A decoder examines a received word. If it is one of the valid codewords, it can output it. If it is not, it may select the closest valid codeword, provided the number and pattern of errors are within the correction capability. If errors exceed that capability, the decoder may declare failure or miscorrect.

A fundamental design choice is redundancy versus efficiency. More redundancy usually improves detection/correction ability but reduces the proportion of new information sent in each codeword.

### 2. Minimum distance

The **minimum distance** `d_min` of a code is the smallest Hamming distance between any two valid codewords. Hamming distance counts the positions in which two words differ.

For a code to detect up to `d - 1` errors, a useful relationship is:

`d_min >= t + 1` for detection of up to `t` errors.

For correction of up to `t` errors:

`d_min >= 2t + 1`.

The intuition is that correction must distinguish the received word from two possible original codewords, leaving enough distance for a unique nearest-neighbour decision. A code with `d_min = 3` can correct one error in every codeword.

### 3. Hamming codes

A **Hamming code** adds parity bits to detect and correct single-bit errors. Hamming codes use parity-check equations, with each check bit covering a subset of positions.

For a common form with `m` parity bits, there are `2^m - m` data bits, and the code can correct one error when `m >= 2`. A simple 3-bit parity version carries 4 data bits plus 3 parity bits, producing a 7-bit Hamming(7,4) code. A larger version carries 8 data bits plus 4 parity bits, producing Hamming(15,11).

Hamming codes are simple and efficient for memory and link systems, but one error-correction code may not detect and correct longer burst errors. Extended Hamming codes add an overall parity bit to improve detection of double-bit errors.

### 4. Block codes

A **block code** groups a fixed number of information symbols and produces a codeword for that group. Hamming and Reed-Solomon codes are block-code examples.

A block code can be:

- **systematic:** information symbols remain visibly present and parity symbols are added;
- **non-systematic:** the codeword is transformed more generally;
- **linear:** codewords can be represented using binary or finite-field linear algebra;
- **cyclic:** a codeword shift is also a codeword, useful for CRC-like operations.

Block codes are convenient when data is processed in chunks and the channel delay is reasonably bounded. A long burst may damage many symbols in one block, so interleaving or stronger codes may be needed.

### 5. Reed-Solomon codes

Reed-Solomon codes operate over a finite field and add parity symbols. They are strong against **burst errors** because a codeword can correct up to a selected number of erased or erroneous symbols, often expressed as `t` symbols.

They are used in digital storage, CDs/DVDs, QR codes, and communication systems. Reed-Solomon decoding is more computationally complex than a simple parity check, but it can recover errors without a return transmission. The exact field size and code rate determine trade-offs.

### 6. Convolutional codes

A **convolutional code** continuously processes input bits through a shift register. The current output depends on the current input and a finite history of previous inputs. A rate-1/2 code might produce two output symbols for every input symbol.

Convolutional codes are decoded with Viterbi or other algorithms. They are common in wireless communication and can perform well on random-error channels. Their performance depends on constraint length, code rate, and decoder complexity.

### 7. Interleaving

A burst error may change many consecutive symbols. **Interleaving** rearranges symbols from several codewords so that a consecutive channel error is spread across separate codewords. The receiver de-interleaves before decoding.

If a burst affects a limited number of positions, each affected codeword may see only a short error pattern that its code can correct. Interleaving adds memory and latency but is valuable for wireless, optical, and storage channels.

### 8. Forward error correction versus ARQ

An **automatic repeat request (ARQ)** protocol detects an error and requests retransmission. It can be efficient on a low-error, low-delay link because it adds little redundancy to every transmission.

FEC adds redundancy in the normal stream and decodes without retransmission. It is useful when:

- the reverse path is slow or absent;
- the channel is highly lossy;
- a deadline cannot tolerate retransmission;
- many receivers or a broadcast link make retransmission wasteful.

Hybrid ARQ combines both: it transmits coded data and uses incremental redundancy or a retransmission when feedback is available.

### 9. Energy, rate, and reliability trade-offs

A code's **rate** is information symbols divided by total transmitted symbols. A rate-1/2 code sends one information symbol for every two channel symbols. Lower rate generally means more redundancy and better correction at the cost of bandwidth and transmit power.

The design must consider:

- bit/symbol error probability;
- required probability of undetected or uncorrectable error;
- available energy and spectrum;
- decoder complexity and latency;
- channel state and whether errors are random or bursty;
- whether the receiver can request retransmission.

A satellite link may prefer strong FEC, while a local wired link may use a small CRC and immediate ARQ.

### 10. Interleaving and coding in modern links

Wireless standards combine coding, modulation, interleaving, and adaptive transmission. Strong coding is useful near a cell edge or in interference, but it requires more airtime. Fibre may use forward correction for very long high-rate links. Storage devices use checks, ECC, and bad-block recovery to preserve data over time.

## Worked examples

### Example 1: Hamming(7,4)

A 4-bit data word is mapped to a 7-bit Hamming codeword. If one bit is received incorrectly, the parity-check equations identify its position, and the decoder flips it. If two bits are wrong, the simple Hamming code may miscorrect or fail; an extended code can detect some such cases.

### Example 2: Minimum distance

A code with `d_min = 5` can correct `(5 - 1) / 2 = 2` errors per codeword. It can also detect up to 4 errors under the standard distance relationship. This is a theoretical property for the code, not a promise about every implementation.

### Example 3: Interleaving

Four codewords place symbols alternately in a channel sequence. A burst of three consecutive damaged positions affects different codewords, at most one symbol in each. A code that corrects one error per codeword may recover the entire burst, whereas without interleaving all three symbols might damage one codeword.

### Example 4: ARQ versus FEC

A deep-space probe receives a damaged image. Waiting for a retransmission may take minutes and consume scarce power. Strong FEC can reconstruct the image immediately. On a short office LAN, a 32-bit CRC and retransmission is simpler and usually efficient.

### Example 5: Rate choice

A rate-1/2 code sends twice as many channel symbols as information symbols. A rate-3/4 code is more bandwidth-efficient but has less redundancy. The choice balances link budget and reliability.

## Key terms & formulas

- **Error correction:** identify and repair errors without necessarily retransmitting.
- **Codeword:** information plus redundancy.
- **Redundancy:** extra symbols for checking/recovery.
- **FEC:** forward error correction.
- **ARQ:** automatic repeat request/retransmission.
- **Hamming distance:** count differing positions between words.
- **Minimum distance:** smallest Hamming distance between valid codewords.
- **Correction limit:** `t = floor((d_min - 1) / 2)`.
- **Detection limit:** up to `d_min - 1` errors under ideal code conditions.
- **Code rate:** `R = k / n`.
- **Block code:** maps a group of `k` symbols to `n` symbols.
- **Convolutional code:** memory-based continuous encoder.
- **Reed-Solomon:** finite-field block code strong against bursts.
- **Interleaving:** rearranges symbols to spread burst errors.
- **Burst error:** consecutive damaged symbols.
- **Hybrid ARQ:** combines FEC and retransmission.

## Common mistakes

1. **Error correction is not the same as error detection.** Correction reconstructs a valid codeword.
2. **A CRC alone does not correct errors.** It supplies a check/remainder, not a general decoder.
3. **Interleaving does not add error-correction parity.** It rearranges symbols so another code can handle a burst.
4. **More redundancy is not free.** It reduces code rate and may require more time, power, or bandwidth.
5. **FEC is not always better than ARQ.** A reliable low-delay link may retransmit a small frame more efficiently.
6. **Hamming distance is measured between codewords, not raw data words.** The code's properties matter.
7. **A code can miscorrect when errors exceed its capability.** It may produce a valid but wrong codeword.
8. **Convolutional codes process a stream, not a fixed block only.** Their encoder uses previous inputs.
9. **Reed-Solomon operates over a finite field.** Ordinary decimal addition is not the core operation.
10. **Interleaving adds delay and memory.** It is not free even when it improves burst-error recovery.
11. **FEC does not guarantee perfect recovery.** The channel and decoder must meet the code assumptions.

## Exam prep

### Likely 2-mark questions

1. **Define forward error correction and give one use.**  
   Hint: repair limited errors with redundancy, especially satellite/wireless links.
2. **Distinguish error detection, error correction, and ARQ.**  
   Hint: detect, repair, and retransmit respectively.
3. **What is interleaving?**  
   Hint: rearrange symbols to spread burst errors across codewords.
4. **State the role of minimum distance.**  
   Hint: determines the number of errors a code can correct or detect.
5. **Give one block-code and one convolutional-code example.**  
   Hint: Hamming/Reed-Solomon and a memory-based streaming code.
6. **What is code rate?**  
   Hint: information symbols divided by total transmitted symbols.

### Likely long-answer questions

1. **Compare error detection, ARQ, and FEC.**  
   Answer hint: redundancy, return path, delay, complexity, and suitable channels.
2. **Explain Hamming codes with minimum distance.**  
   Answer hint: parity checks, single-error correction, extended codes, and limitations.
3. **Explain Reed-Solomon and interleaving for burst errors.**  
   Answer hint: finite-field parity, correctable symbols, symbol spreading, and de-interleaving.
4. **Choose an error-control strategy for a satellite link and justify it.**  
   Answer hint: long delay, expensive retransmission, strong FEC, interleaving, and residual failure probability.
5. **Compare block and convolutional codes.**  
   Answer hint: grouping, memory, decoder, channel use, and complexity.

### Short-answer revision checklist

Be ready to define code rate, Hamming distance, correction/detection relationships, ARQ, FEC, block/convolutional codes, and interleaving, with one example of each.
