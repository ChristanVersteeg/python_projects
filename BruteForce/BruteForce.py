
import itertools
import time

# --- Configuration ---
TARGET_PASSWORD = "Welkom2020"
DICTIONARY_FILE = "wordlist.txt"
MAX_COMBINATION_LENGTH = 3  # Try combinations up to this many words
STATUS_UPDATE_INTERVAL = 0.0001 # Seconds between progress prints


def load_dictionary(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return [line.strip() for line in f if line.strip()]


def simulate_brute_force_combo_attack():
    try:
        words = load_dictionary(DICTIONARY_FILE)
    except FileNotFoundError:
        print(f"Dictionary file not found: {DICTIONARY_FILE}")
        return

    print(f"Trying to guess password by combining words from dictionary (max {MAX_COMBINATION_LENGTH} words)")
    print(f"Target: '{TARGET_PASSWORD}'")
    print("-" * 60)

    start_time = time.time()
    last_print_time = start_time
    attempts = 0

    for r in range(1, MAX_COMBINATION_LENGTH + 1):
        for combo in itertools.product(words, repeat=r):
            guess = ''.join(combo)
            attempts += 1

            current_time = time.time()
            if current_time - last_print_time >= STATUS_UPDATE_INTERVAL:
                elapsed = current_time - start_time
                print(f"[{elapsed:.1f}s] Attempts: {attempts:,} | Latest guess: '{guess}'")
                last_print_time = current_time

            if guess == TARGET_PASSWORD:
                elapsed = current_time - start_time
                print(f"\nSUCCESS: Found password after {attempts:,} attempts in {elapsed:.2f} seconds.")
                print(f"Words used: {combo}")
                return

    elapsed = time.time() - start_time
    print(f"\nFAILED: Tried {attempts:,} combinations. Target not found.")
    print(f"Time taken: {elapsed:.2f} seconds.")


if __name__ == "__main__":
    simulate_brute_force_combo_attack()
