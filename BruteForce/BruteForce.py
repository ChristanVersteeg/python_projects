import time
import os
from typing import Generator, Dict, List

# NOTE: This script is for educational purposes only to demonstrate the concept of
# a pure dictionary attack, which relies entirely on checking words present in a file.
# It does not perform actual password cracking against a real system.

# --- Configuration ---
TARGET_PASSWORD = "welkom123" 
DICTIONARY_FILE = "wordlist.txt"
# Target the simulation to run for approximately 30 seconds for demonstration purposes.
TARGET_RUNTIME_SECONDS = 30.0 

# Removed all global and internal hybrid rulesets and l33t speak functions, 
# relying solely on the content of the wordlist file.

def load_dictionary(filepath: str) -> List[str]:
    """Reads words from the simulated external wordlist file."""
    if not os.path.exists(filepath):
        print(f"Error: Dictionary file '{filepath}' not found.")
        return []
    try:
        with open(filepath, 'r') as f:
            # Strip whitespace (like newlines) from each word
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error loading dictionary: {e}")
        return []

# Hybrid mutation functions are no longer needed.


def simulate_dictionary_attack(target: str) -> Generator[str, None, None]:
    """
    Simulates a Pure Dictionary Lookup, checking only the words loaded directly 
    from the external dictionary file. Includes an artificial delay to meet the 
    TARGET_RUNTIME_SECONDS specified in the configuration.
    """
    print("--- Starting Pure Dictionary Lookup (Dictionary Attack) Simulation ---")
    print(f"Target: '{target}'")
    
    base_dictionary = load_dictionary(DICTIONARY_FILE)
    
    # The DEBUG/DEMO CHECK has been removed. The simulation will now genuinely fail
    # if the TARGET_PASSWORD is not present in the wordlist.
    
    if not base_dictionary:
        print("Dictionary is empty. Cannot run simulation.")
        return
    
    num_words = len(base_dictionary)
    # Calculate required sleep time per word to hit the target runtime.
    # We subtract a small estimated overhead (0.1s) for safety.
    overhead_estimate = 0.1
    sleep_per_word = max(0, (TARGET_RUNTIME_SECONDS - overhead_estimate) / num_words)

    print(f"Applying artificial delay of {sleep_per_word:.6f}s per word to hit {TARGET_RUNTIME_SECONDS}s target.")
    print("-" * 50)


    attempts = 0

    # 1. Check the raw dictionary words (Pure Dictionary Attack)
    print(f"\n--- Phase 1: Checking {num_words} Dictionary Words ---")
    for base_word in base_dictionary:
        attempts += 1
        
        # Apply the calculated delay
        time.sleep(sleep_per_word)
        
        yield base_word
        if base_word == target:
            return

    # All other phases (hybrid, l33t speak, etc.) have been removed.


def simulate_brute_force():
    """Main function to run the timed demonstration."""
    
    # Define the interval in seconds for printing status updates.
    PRINT_INTERVAL_SECONDS = 10 
    
    start_time = time.time()
    last_print_time = start_time 
    attempts_checked = 0
    found = False
    
    search_target = TARGET_PASSWORD 

    print(f"Simulating Pure Dictionary attack for: '{search_target}'.")
    print("-" * 50)

    try:
        candidate_generator = simulate_dictionary_attack(target=TARGET_PASSWORD)

        for candidate in candidate_generator:
            attempts_checked += 1
            
            if candidate == search_target:
                found = True
                break
                
            current_time = time.time()
            elapsed_time = current_time - start_time
            
            # Check if the print interval has elapsed (10 seconds)
            if current_time - last_print_time >= PRINT_INTERVAL_SECONDS:
                # Use current word in the status update to show progress
                print(f"Checked {attempts_checked:,} attempts in {elapsed_time:.4f} seconds. Current: {candidate}")
                last_print_time = current_time 
                
    except KeyboardInterrupt:
        print("\nSearch interrupted by user.")
        
    end_time = time.time()
    
    print("\n" + "=" * 50)
    if found:
        print(f"SUCCESS! Target '{search_target}' found in {attempts_checked} attempts.")
        print("This structure demonstrates a pure dictionary attack, relying only on the external file content.")
    else:
         print(f"Search completed after checking {attempts_checked:,} candidates.")
         print("The dictionary attack failed. The target was not in the file.")
        
    print(f"Total time taken: {end_time - start_time:.4f} seconds")
    print("=" * 50)

if __name__ == "__main__":
    simulate_brute_force()
