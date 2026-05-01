<div align="center">

# 📡 Joint Source-Channel Coding (JSCC) for V2V Telemetry
### Using Huffman Compression & Hamming (7,4) FEC in AWGN Channels

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![NumPy](https://img.shields.io/badge/NumPy-1.24%2B-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Research%20Simulation-blueviolet?style=for-the-badge)]()

---

> **Research Project:** *Performance Evaluation of Compression and Hard-Decision Block Codes in High-Interference Environments*
>
> An end-to-end Information Theory framework that compresses text telemetry using **dynamic Huffman encoding** and protects it using a **(7,4) Hamming code** with BPSK modulation—simulated across varying Signal-to-Noise Ratios (Eb/N0) over an Additive White Gaussian Noise (AWGN) channel.

</div>

---

## 📋 Table of Contents

| # | Section |
|---|---------|
| 1 | [🌐 Overview](#-overview) |
| 2 | [🏗️ Repository Structure](#️-repository-structure) |
| 3 | [📦 Information Source](#-information-source) |
| 4 | [⚡ Channel Simulation Engine](#-channel-simulation-engine) |
| 5 | [🔤 Transmission Pipeline](#-transmission-pipeline) |
| 6 | [🧠 Coding Schemes](#-coding-schemes) |
| 7 | [🔧 Signal & Noise Metrics](#-signal--noise-metrics) |
| 8 | [🏋️ Simulation Configuration](#️-simulation-configuration) |
| 9 | [📊 Results](#-results) |
| 10 | [🔬 Syndrome Analysis](#-syndrome-analysis) |
| 11 | [🚀 Quickstart](#-quickstart) |
| 12 | [📁 Notebook Outline](#-notebook-outline) |
| 13 | [📜 Citation](#-citation) |

---

## 🌐 Overview

In modern communication networks like Vehicular Ad-Hoc Networks (VANETs), data must be transmitted efficiently (low bandwidth) and reliably (low error rate). This project implements a **Joint Source-Channel Coding (JSCC)** approach to analyze the trade-off between approaching the Shannon entropy limit via source compression and adding redundant parity bits for deterministic channel robustness.

### Key Contributions

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ✅  Custom Huffman Engine  —  dynamic probability-driven tree building │
│  ✅  (7,4) Hamming Encoder  —  generator matrix G implementation        │
│  ✅  BPSK Modulation        —  antipodal signaling (2-PAM) mapping      │
│  ✅  AWGN Channel Simulator —  dynamic noise variance based on Eb/N0    │
│  ✅  Syndrome Decoder       —  hard-decision matrix H parity checks     │
│  ✅  Monte Carlo Sim        —  100,000 bit runs for smooth BER curves   │
│  ✅  Verbose Debugging      —  real-time syndrome equation printing     │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Repository Structure

```
jscc-v2v-telemetry/
│
├── 📓 notebooks/
│   └── coding_theory_evaluation.ipynb    ← Full end-to-end experiment
│
├── 🐍 src/
│   ├── huffman_codec.py                  ← Source compression algorithms
│   ├── hamming_codec.py                  ← (7,4) FEC block coding & syndromes
│   └── channel_sim.py                    ← AWGN injection & BPSK modulation
│
├── 📊 data/                              ← Input text sources (e.g., Maxwell bio)
├── 📈 results/                           ← Exported BER data arrays
├── 🖼️ figures/                           ← Generated BER vs Eb/N0 plots
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 📦 Information Source

The simulation operates on two distinct data generation paradigms to independently verify source and channel coding efficiency.

### Source Data

| Source Type | Description | Purpose |
|:------|:---------|:-----------|
| `Natural Language Text` | 3,000+ character string (James C. Maxwell Biography) | To calculate natural symbol probabilities and demonstrate Huffman tree generation. |
| `Monte Carlo Bitstream` | 100,000 uniformly distributed random integers (0 or 1) | To provide a statistically significant payload for accurate Bit Error Rate (BER) calculations. |

---

## ⚡ Channel Simulation Engine

The physical transmission medium is modeled as an Additive White Gaussian Noise (AWGN) channel. Noise power is dynamically scaled based on the desired Energy per bit to Noise power spectral density ratio ($E_b/N_0$).

| Parameter | Formula / Implementation | Description |
|:---------|:------------|:--------|
| **Modulation** | $s(t) = 1 - 2c$ | BPSK maps bits {0, 1} to symbols {+1, -1} |
| **Code Rate ($R$)** | $4/7$ | Ratio of information bits to total transmitted bits |
| **Linear SNR** | $10^{(E_b/N_0 / 10)} \times R$ | Scales bit energy ratio to symbol SNR |
| **Noise Variance** | $\sigma^2 = \frac{1}{2 \times \text{SNR}}$ | Variance for the Gaussian noise distribution |
| **Received Signal** | $r(t) = s(t) + \mathcal{N}(0, \sigma^2)$ | The noisy symbols received by the demodulator |

---

## 🔤 Transmission Pipeline

Data moves through a rigorous mathematical pipeline representing a complete digital communication system:

```
  Information Source
        │
        ▼
  ① Source Encoder      Symbol Probabilities ──► Huffman Tree ──► Variable-length Bits
  ② Channel Encoder     4-bit blocks ──────────► G Matrix ──────► 7-bit Codewords
  ③ Modulator           {0, 1} ────────────────► BPSK ──────────► {+1, -1} Baseband
  ④ AWGN Channel        Signal + Noise ────────► Eb/N0 Scaling ─► Noisy Analog Signal
  ⑤ Demodulator         Hard Decision (r < 0) ─► Bits {0, 1}
  ⑥ Syndrome Decoder    7-bit blocks ──────────► H Matrix ──────► Error Correction
        │
        ▼
  Recovered Information Bits
```

---

## 🧠 Coding Schemes

### 1. Source Coding: Huffman Compression
A lossless data compression algorithm. The characters in the input text are sorted by frequency, and a binary tree is constructed where the least frequent characters are placed deeper in the tree, resulting in shorter bit codes for highly probable symbols (e.g., space, 'e', 't').

### 2. Channel Coding: (7,4) Hamming Code
A linear error-correcting block code capable of detecting up to two simultaneous bit errors and correcting single-bit errors.

**Generator Matrix ($G$)**
Transforms 4 bits of data into a 7-bit codeword (systematic form):
```
[1, 0, 0, 0, 1, 1, 0]
[0, 1, 0, 0, 1, 0, 1]
[0, 0, 1, 0, 0, 1, 1]
[0, 0, 0, 1, 1, 1, 1]
```

**Parity-Check Matrix ($H$)**
Used at the receiver to calculate the 3-bit syndrome:
```
[1, 1, 0, 1, 1, 0, 0]
[1, 0, 1, 1, 0, 1, 0]
[0, 1, 1, 1, 0, 0, 1]
```

---

## 🔧 Signal & Noise Metrics

The simulation explicitly tracks these parameters at each stage:

| # | Metric | Output Example |
|:-:|:--------|:----|
| 0 | `Original Information Bits` | `[1 0 1 1 0 1 0 0 ...]` |
| 1 | `Encoded Codewords` | `[1 0 1 1 0 1 0 ...]` |
| 2 | `Modulated Signal` | `[-1  1 -1 -1  1 ...]` |
| 3 | `Noise Variance` | Calculated dynamically per Eb/N0 step |
| 4 | `Received Noisy Signal` | `[-1.23  0.89 -0.12 ...]` |
| 5 | `Demodulated Bits` | Hard decision thresholds applied |
| 6 | `Calculated Syndrome` | `[1 0 1]` (indicates specific bit error) |

---

## 🏋️ Simulation Configuration

| Hyperparameter | Value | Description |
|:---------------|:-----------:|:-----------|
| Monte Carlo Runs | 10,000 to 100,000 | Number of bits simulated per Eb/N0 step |
| Eb/N0 Range | 0 dB to 10 dB | Steps of 1 dB to map the BER curve |
| Hard Decision Threshold | 0.0 | BPSK boundary |
| Generator Method | Matrix Multiplication | $C = U \cdot G \pmod 2$ |
| Syndrome Method | Transposed Check | $S = R \cdot H^T \pmod 2$ |

---

## 📊 Results

### Bit Error Rate (BER) Performance

As the Signal-to-Noise Ratio ($E_b/N_0$) increases, the Bit Error Rate drops significantly, demonstrating the effectiveness of the Hamming Code in mitigating channel noise.

| Eb/N0 (dB) | Expected BER Range | System Behavior |
|:----------:|:---------:|:------|
| **0 - 2 dB** | High (~$10^{-1}$) | Noise heavily corrupts signal; Hamming code frequently overwhelmed by 2+ bit errors per block. |
| **3 - 6 dB** | Waterfall Region | Single-bit errors dominate; Hamming code successfully corrects the vast majority of block errors. |
| **7 - 10 dB** | Low (< $10^{-4}$) | Clean channel; near-perfect recovery of original information payload. |

---

## 🔬 Syndrome Analysis

The script features a verbose decoding engine that outputs the exact mathematical logic used to correct bit flips in real-time.

```
  Example Console Output for a Corrupted Block:
  ─────────────────────────────────────────────────
  Syndrome Equations for Codeword 0:
  s1 = r1 ⊕ r2 ⊕ r4 ⊕ r5 = 1
  s2 = r1 ⊕ r3 ⊕ r4 ⊕ r6 = 0
  s3 = r2 ⊕ r3 ⊕ r4 ⊕ r7 = 1
  
  Result: Syndrome [1 0 1]
  Action: Error detected at position: 2
  Correction: Bit 2 flipped successfully.
  ─────────────────────────────────────────────────
```

> *Note on Limitation:* If the AWGN noise flips *two* bits in a single 7-bit block, the calculated syndrome will falsely point to a third, incorrect position, causing the decoder to introduce an additional error (aliasing). This explains the curve flattening at very low SNR environments.

---

## 🚀 Quickstart

### Installation

```bash
git clone https://github.com/YourOrg/jscc-v2v-telemetry.git
cd jscc-v2v-telemetry
pip install numpy matplotlib
```

### Run the Simulation

```bash
# Execute the combined pipeline (Huffman + Hamming + BER Plot)
python src/main_simulation.py
```

### Environment

| Requirement | Version |
|:------------|:-------:|
| Python | ≥ 3.8 |
| NumPy | ≥ 1.24 |
| Matplotlib | ≥ 3.8 |

---

## 📁 Notebook Outline

| Step | Focus | Description |
|:----:|:------|:------------|
| **0** | Setup | Import collections, heapq, numpy, matplotlib |
| **1** | Source Data | Initialize James C. Maxwell text & count symbol frequencies |
| **2** | Huffman Coding | Build priority queue, construct binary tree, output code dictionary |
| **3** | Channel Prep | Generate 100,000 random bits and establish G and H matrices |
| **4** | Encoding | Multiply bits by G matrix modulo 2 |
| **5** | Channel | Modulate to BPSK, scale noise variance, add AWGN array |
| **6** | Demodulation | Apply $r < 0$ hard-decision boundary |
| **7** | Error Correction | Calculate $R \cdot H^T$, identify syndrome match, flip erroneous bits |
| **8** | BER Calculation | Compare decoded output to original array |
| **9** | Visualization | Plot semilogy graph of BER against Eb/N0 values |

---

## 📜 Citation

```bibtex
@misc{InformationTheoryToolkit2026,
  title        = {Joint Source-Channel Coding: Huffman and Hamming (7,4) Evaluation over AWGN},
  author       = {Vignesh D.},
  year         = {2026},
  howpublished = {GitHub Repository},
  note         = {Information Theory & Coding Implementations}
}
```

</div>
