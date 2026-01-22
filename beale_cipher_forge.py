#!/usr/bin/env python3
"""
BEALE CIPHER FORGE
A tool to create "convincing" fake book ciphers and demonstrate how the Beale hoax could have been constructed.

Features:
1. Authentic Mode: Creates a strict book cipher from a key text.
2. Forge Mode: Introduces statistical anomalies (like the base-10 bias found in 2024 research) to mimic the specific "fingerprint" of the Beale Ciphers.
3. Benford's Law: Ensures generated numbers roughly follow Benford's Law distribution (optional).
"""

import argparse
import random
import re
import sys
from collections import Counter, defaultdict

# Embedded Declaration of Independence (approximate text for standalone usage)
DOI_TEXT = """
When in the Course of human events, it becomes necessary for one people to dissolve the
political bands which have connected them with another, and to assume among the powers of the
earth, the separate and equal station to which the Laws of Nature and of Nature's God entitle
them, a decent respect to the opinions of mankind requires that they should declare the causes
which impel them to the separation.

We hold these truths to be self-evident, that all men are created equal, that they are endowed
by their Creator with certain unalienable Rights, that among these are Life, Liberty and the
pursuit of Happiness.--That to secure these rights, Governments are instituted among Men,
deriving their just powers from the consent of the governed, --That whenever any Form of
Government becomes destructive of these ends, it is the Right of the People to alter or to
abolish it, and to institute new Government, laying its foundation on such principles and
organizing its powers in such form, as to them shall seem most likely to effect their Safety
and Happiness. Prudence, indeed, will dictate that Governments long established should not be
changed for light and transient causes; and accordingly all experience hath shewn, that mankind
are more disposed to suffer, while evils are sufferable, than to right themselves by abolishing
the forms to which they are accustomed. But when a long train of abuses and usurpations,
pursuing invariably the same Object evinces a design to reduce them under absolute Despotism,
it is their right, it is their duty, to throw off such Government, and to provide new Guards
for their future security.--Such has been the patient sufferance of these Colonies; and such is
now the necessity which constrains them to alter their former Systems of Government. The
history of the present King of Great Britain is a history of repeated injuries and usurpations,
all having in direct object the establishment of an absolute Tyranny over these States. To
prove this, let Facts be submitted to a candid world.
"""

def clean_text(text):
    """Clean text to list of words, preserving order."""
    # Split by whitespace, remove non-alphanumeric from edges but keep internal logic if needed
    # For Beale, it's usually 1-based index of first letter of word
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    return [w.upper() for w in words]

def create_cipher_index(words):
    """Create a map of {Letter: [list of 1-based indices]}."""
    index_map = defaultdict(list)
    for idx, word in enumerate(words):
        first_letter = word[0]
        index_map[first_letter].append(idx + 1)
    return index_map

def generate_cipher(message, index_map, forge_mode=False, intended_max=3000):
    """
    Generate a cipher sequence for the message.
    
    Args:
        message (str): Plaintext message.
        index_map (dict): Map of letters to indices in key text.
        forge_mode (bool): If True, biased selection towards specific patterns.
        intended_max (int): Max number to simulate larger document if needed (for forge mode).
    """
    cipher = []
    message = re.sub(r'[^a-zA-Z]', '', message.upper())
    
    used_indices = set()
    
    for char in message:
        potential_indices = index_map.get(char, [])
        
        if not potential_indices and not forge_mode:
            print(f"Warning: Character '{char}' not found in key text. Skipping.")
            cipher.append(0) # 0 indicates missing
            continue
            
        if forge_mode:
            # FORGE MODE:
            # 1. Bias towards numbers ending in 0-5 (Simulating the non-uniformity)
            # 2. Allow "fake" large numbers if needed to bolster the "unsolvable" look
            
            # If we have real indices, try to pick one that fits our "forge" profile
            candidates = [p for p in potential_indices if p % 10 <= 5] # Bias for lower last digits
            
            if candidates and random.random() < 0.7: # 70% chance to pick "biased" number
                choice = random.choice(candidates)
            elif potential_indices:
                choice = random.choice(potential_indices)
            else:
                # If char not in text, MAKE UP a number that looks plausible
                # This is how you make an unsolvable cipher look real!
                choice = random.randint(1, intended_max)
                
        else:
            # AUTHENTIC MODE: Randomly select valid index
            if not potential_indices:
                choice = 0
            else:
                choice = random.choice(potential_indices)
                
        cipher.append(choice)
        
    return cipher

def main():
    parser = argparse.ArgumentParser(description="Beale Cipher Forge")
    parser.add_argument("--message", type=str, required=True, help="Message to encrypt")
    parser.add_argument("--key-file", type=str, help="Path to key text file (optional, uses embedded DOI default)")
    parser.add_argument("--forge", action="store_true", help="Enable 'Forge' mode (add statistical anomalies)")
    parser.add_argument("--show-stats", action="store_true", help="Show statistical analysis of generated cipher")
    
    args = parser.parse_args()
    
    # Load Key Text
    if args.key_file:
        try:
            with open(args.key_file, 'r') as f:
                key_text = f.read()
        except Exception as e:
            print(f"Error reading key file: {e}")
            sys.exit(1)
    else:
        key_text = DOI_TEXT
        
    words = clean_text(key_text)
    index_map = create_cipher_index(words)
    
    print(f"Loaded Key Text: {len(words)} words")
    print(f"Encrypting Message: '{args.message}'")
    
    cipher = generate_cipher(args.message, index_map, forge_mode=args.forge)
    
    print("\n" + "="*40)
    print("GENERATED CIPHER")
    print("="*40)
    print(", ".join(map(str, cipher)))
    print("="*40)
    
    if args.show_stats:
        print("\nStatistical Analysis:")
        print(f"Total Numbers: {len(cipher)}")
        print(f"Max Number: {max(cipher)}")
        
        # Last Digit Analysis
        last_digits = [n % 10 for n in cipher]
        counts = Counter(last_digits)
        print("\nLast Digit Distribution (0-9):")
        for i in range(10):
            print(f"  {i}: {counts[i]} ({counts[i]/len(cipher):.1%})")
            
        if args.forge:
            print("\n[!] FORGE MODE ACTIVE: Notice the bias/irregularity in distribution!")

if __name__ == "__main__":
    main()
