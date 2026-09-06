import random

# BLOCK 1: Decomposition of n-1 into 2^s * r
def decompose(n_minus_1: int) -> tuple[int, int]:

    s = 0
    r = n_minus_1
    # Keep dividing r by 2 as long as it remains even
    while r % 2 == 0:
        r //= 2
        s += 1
    return s, r


# BLOCK 2: Fast modular exponentiation  (square-and-multiply)
def mod_pow(base: int, exp: int, mod: int) -> int:
    # Compute (base^exp) % mod efficiently using the square-and-multiply method.
    
    result = 1
    base = base % mod # Reduce base once at the start

    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp //= 2
        base = (base * base) % mod
    return result


# BLOCK 3: Single-witness Miller-Rabin round
def miller_rabin_witness(n: int, a: int, s: int, r: int) -> bool:
    # Execute one round of the Miller-Rabin test for a single witness base a.
    # Returns True if 'a' is a strong liar (n passes), False if n is composite.

    y = mod_pow(a, r, n)

    if y == 1 or y == n - 1:
        return True

    for _ in range(s - 1):
        y = mod_pow(y, 2, n)
        if y == n - 1:
            return True

    # Neither 1 nor -1 was encountered -> a is a strong witness to compositeness
    return False


# BLOCK 4: Main Miller-Rabin test
def miller_rabin(n: int, t: int = 20) -> bool:
    # Main probabilistic Miller-Rabin test. 
    # Runs t independent rounds. Probability of error is <= (1/4)^t.

    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    s, r = decompose(n - 1)

    for _ in range(t):
        a = random.randrange(2, n - 1)

        # Test whether a is a strong witness to compositeness
        if not miller_rabin_witness(n, a, s, r):
            return False

    # All t rounds passed -> n is a probable prime
    return True


# BLOCK 5: Deterministic version using fixed bases (for numbers < delta_t)
def miller_rabin_deterministic(n: int) -> bool:
    #Deterministic variant using fixed witness bases {2, 3, 5, 7}.
    #Valid for all n < 3,215,031,751

    if n < 2:
        return False
    if n in (2, 3, 5, 7):
        return True
    if n % 2 == 0:
        return False

    s, r = decompose(n - 1)

    for a in [2, 3, 5, 7]:
        if a >= n:
            continue           # Skip bases that are not in the valid range
        if not miller_rabin_witness(n, a, s, r):
            return False

    return True


# BLOCK 6: Automated test suite (7 test cases)
def run_tests():
    """
    Test cases chosen:
      1. Small known prime          : 7
      2. Large known prime          : 104,729
      3. Even composite             : 100
      4. Odd composite (obvious)    : 561  -> Carmichael number!
      5. Carmichael number          : 1105
      6. Carmichael number          : 1729
      7. Strong pseudoprime base 2  : 2047 (= 23 × 89, PSP to base 2)
    """

    # Reference oracle: simple trial-division 
    def is_prime_reference(num: int) -> bool:
        # Trial-division primality test used ONLY as reference comparison.
        if num < 2:
            return False
        if num == 2:
            return True
        if num % 2 == 0:
            return False
        i = 3
        while i * i <= num:
            if num % i == 0:
                return False
            i += 2
        return True

    # Test definitions
    test_cases = [
        {
            "id"         : 1,
            "value"      : 7,
            "description": "Small known prime",
        },
        {
            "id"         : 2,
            "value"      : 104729,
            "description": "Large known prime (10001st prime)",
        },
        {
            "id"         : 3,
            "value"      : 100,
            "description": "Even composite number",
        },
        {
            "id"         : 4,
            "value"      : 91,
            "description": "Odd composite – Fermat pseudoprime to base 3 (7 × 13)",
        },
        {
            "id"         : 5,
            "value"      : 561,
            "description": "Carmichael number (3 × 11 × 17) – fools Fermat test",
        },
        {
            "id"         : 6,
            "value"      : 1105,
            "description": "Carmichael number (5 × 13 × 17) – fools Fermat test",
        },
        {
            "id"         : 7,
            "value"      : 2047,
            "description": "Strong pseudoprime to base 2 (23 × 89) – from delta_1 table",
        },
    ]

    # Header
    print("=" * 80)
    print("  MILLER-RABIN PRIMALITY TEST  –  Automated Test Suite (7 cases)")
    print("  ECRYP Project 2026 | Warsaw University of Technology")
    print("=" * 80)
    print()

    all_passed = True

    for tc in test_cases:
        n = tc["value"]
        description = tc["description"]
        t = 20    # Security parameter: error probability <= (1/4)^20

        # Run our implementation (probabilistic, t=20 rounds)
        our_result = miller_rabin(n, t)

        # Run deterministic reference oracle (trial division)
        ref_result = is_prime_reference(n)

        # Determine pass/fail
        match = (our_result == ref_result)
        status = "PASS" if match else "FAIL"
        if not match:
            all_passed = False

        # Format results as strings
        our_str = "PRIME"     if our_result else "COMPOSITE"
        ref_str = "PRIME"     if ref_result else "COMPOSITE"

        print(f"Test #{tc['id']:02d}  |  n = {n}")
        print(f"Description : {description}")
        print(f"Miller-Rabin result (t={t}) : {our_str}")
        print(f"Reference result (trial div): {ref_str}")
        print(f"Status : {status}")
        print("-" * 80)

    print()
    overall = "ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED"
    print(f"  Overall result: {overall}")
    print("=" * 80)


# BLOCK 7: Interactive user interface (console mode)
def interactive_mode():
    # Simple console interface allowing the user to test arbitrary numbers. 

    print("\n" + "=" * 80)
    print("  MILLER-RABIN PRIMALITY TEST  –  Interactive Mode")
    print("=" * 80)

    while True:
        try:
            raw_n = input("\nEnter a positive integer to test (or 'q' to quit): ").strip()
            if raw_n.lower() == 'q':
                print("Goodbye.")
                break

            n = int(raw_n)
            if n < 2:
                print("  Please enter an integer >= 2.")
                continue

            raw_t = input("Enter security parameter t (number of rounds, default=20): ").strip()
            t = int(raw_t) if raw_t else 20
            if t < 1:
                print("  t must be >= 1. Using t=20.")
                t = 20

            result = miller_rabin(n, t)
            verdict = "PRIME (probable)" if result else "COMPOSITE (certain)"
            print(f"\n  n = {n}, t = {t}")
            print(f"  Result: {verdict}")

            if result:
                print(f"  Note: probability of error <= (1/4)^{t} ≈ {(0.25**t):.2e}")

        except ValueError:
            print("  Invalid input. Please enter integers only.")


# ENTRY POINT
def main():
    """
    Main entry point.

    1. Runs the automated test suite (7 cases).
    2. Launches the interactive console mode.
    """
    run_tests()
    interactive_mode()


if __name__ == "__main__":
    main()
