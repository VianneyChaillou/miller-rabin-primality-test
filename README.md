# Miller-Rabin Primality Test 🔒

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Cryptography](https://img.shields.io/badge/Cryptography-Security-red?style=for-the-badge)

This repository contains a from-scratch Python implementation of the **Miller-Rabin Primality Test**, developed as part of the ECRYP (Cryptography) project during my Erasmus exchange at the Warsaw University of Technology.

## 📌 Project Overview

The objective was to build an efficient probabilistic primality testing algorithm **without using any external cryptographic libraries**. 
Naive trial division is exponentially slow for large numbers, while the Fermat primality test fails against Carmichael numbers. The Miller-Rabin test solves this by detecting strong witnesses to compositeness.

### Key Features
- **No external crypto libraries:** The core algorithm and modular arithmetic are entirely custom-built.
- **Fast Modular Exponentiation:** Implemented the *square-and-multiply* method to avoid exponential growth when computing very large exponents.
- **Automated Test Suite:** Includes 7 specific pathological test cases (including Carmichael numbers like 561 and 1105, and strong pseudoprimes like 2047) to prove the robustness of the algorithm.
- **Interactive Mode:** A console CLI allowing users to test any integer with a custom security parameter `t`.

---

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone [https://github.com/VianneyChaillou/miller-rabin-primality-test.git](https://github.com/VianneyChaillou/miller-rabin-primality-test.git)
   
2. Navigate to the directory:
   ```bash
   cd miller-rabin-primality-test

3. Run the script:
   ```bash
   python miller_rabin.py

Upon execution, the script will first run the automated test suite against the reference oracle (trial-division), and then launch the interactive console mode.

## 🧠 Code Architecture

The code is strictly divided into functional blocks:
- `decompose(n_minus_1)`: Factors $n-1$ into $2^s \cdot r$.
- `mod_pow(base, exp, mod)`: Efficient binary exponentiation algorithm.
- `miller_rabin_witness(...)`: Executes a single round of the Miller-Rabin test for a witness base a.
- `miller_rabin(n, t)`: Main probabilistic loop checking t independent rounds. (Error probability $\le (1/4)^t$).
- `run_tests()`: The automated oracle test suite.

For more mathematical details and proof of correctness, please refer to the attached Miller-Rabin-Report.pdf.

Project developed by Vianney Chaillou (2026).
