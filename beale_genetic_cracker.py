#!/usr/bin/env python3
"""
BEALE GENETIC CRACKER
A sophisticated Genetic Algorithm (GA) to attack the Beale Ciphers as Homophonic Substitution Ciphers.
This method does NOT require the original book key. It attempts to evolve the key mapping based on English statistics.

Algorithm:
1. Treat each number in the cipher as a distinct symbol.
2. Evolve a mapping {Number -> Letter} that maximizes the "English-likeness" of the decrypted text.
3. Use Quadgram Statistics (4-letter sequences) as the Fitness Function.
"""

import random
import sys
import time
import math
from collections import Counter
import requests
import os

# Import scoring helper
try:
    from ngram_score import NgramScore
except ImportError:
    print("Error: ngram_score.py not found.")
    sys.exit(1)

# Cipher Data
CIPHER_1 = [71, 194, 38, 1701, 89, 76, 11, 83, 1629, 48, 94, 63, 132, 16, 111, 95, 84, 341, 975, 14, 40, 64, 27, 81, 139, 213, 63, 90, 1120, 8, 15, 3, 126, 2018, 40, 74, 758, 485, 604, 230, 436, 664, 582, 150, 251, 284, 308, 231, 124, 211, 486, 225, 401, 370, 11, 101, 305, 139, 189, 17, 33, 88, 208, 193, 145, 1, 94, 73, 416, 918, 263, 28, 500, 538, 356, 117, 136, 219, 27, 176, 130, 10, 460, 25, 485, 18, 436, 65, 84, 200, 283, 118, 320, 138, 36, 416, 280, 15, 71, 224, 961, 44, 16, 401, 39, 88, 61, 304, 12, 21, 24, 283, 134, 92, 63, 246, 486, 682, 7, 219, 184, 360, 780, 18, 64, 463, 474, 131, 160, 79, 73, 440, 95, 18, 64, 581, 34, 69, 128, 367, 460, 17, 81, 12, 103, 820, 62, 116, 97, 103, 862, 70, 60, 1317, 471, 540, 208, 121, 890, 346, 36, 150, 59, 568, 614, 13, 120, 63, 219, 812, 2160, 1780, 99, 35, 18, 21, 136, 872, 15, 28, 170, 88, 4, 30, 44, 112, 18, 147, 436, 195, 320, 37, 122, 113, 6, 140, 8, 120, 305, 42, 58, 461, 44, 106, 301, 13, 408, 680, 93, 86, 116, 530, 82, 568, 9, 102, 38, 416, 89, 71, 216, 728, 965, 818, 2, 38, 121, 195, 14, 326, 148, 234, 18, 55, 131, 234, 361, 824, 5, 81, 623, 48, 961, 19, 26, 33, 10, 1101, 365, 92, 88, 181, 275, 346, 201, 206, 86, 36, 219, 324, 829, 840, 64, 326, 19, 48, 122, 85, 216, 284, 919, 861, 326, 985, 233, 64, 68, 232, 431, 960, 50, 29, 81, 216, 321, 603, 14, 612, 81, 360, 36, 51, 62, 194, 78, 60, 200, 314, 676, 112, 4, 28, 18, 61, 136, 247, 819, 921, 1060, 464, 895, 10, 6, 66, 119, 38, 41, 49, 602, 423, 962, 302, 294, 875, 78, 14, 23, 111, 109, 62, 31, 501, 823, 216, 280, 34, 24, 150, 1000, 162, 286, 19, 21, 17, 340, 19, 242, 31, 86, 234, 140, 607, 115, 33, 191, 67, 104, 86, 52, 88, 16, 80, 121, 67, 95, 122, 216, 548, 96, 11, 201, 77, 364, 218, 65, 667, 890, 236, 154, 211, 10, 98, 34, 119, 56, 216, 119, 71, 218, 1164, 1496, 1817, 51, 39, 210, 36, 3, 19, 540, 232, 22, 141, 617, 84, 290, 80, 46, 207, 411, 150, 29, 38, 46, 172, 85, 194, 39, 261, 543, 897, 624, 18, 212, 416, 127, 931, 19, 4, 63, 96, 12, 101, 418, 16, 140, 230, 460, 538, 19, 27, 88, 612, 1431, 90, 716, 275, 74, 83, 11, 426, 89, 72, 84, 1300, 1706, 814, 221, 132, 40, 102, 34, 868, 975, 1101, 84, 16, 79, 23, 16, 81, 122, 324, 403, 912, 227, 936, 447, 55, 86, 34, 43, 212, 107, 96, 314, 264, 1065, 323, 428, 601, 203, 124, 95, 216, 814, 2906, 654, 820, 2, 301, 112, 176, 213, 71, 87, 96, 202, 35, 10, 2, 41, 17, 84, 221, 736, 820, 214, 11, 60, 760]

# Sample of Cipher 2 (Verified)
CIPHER_2_SHORT = [115, 73, 24, 807, 37, 52, 49, 17, 31, 62, 647, 22, 7, 15, 140, 47, 29, 107, 79, 84, 56, 239, 10, 26, 811, 5, 196]
# Starts: "I HAVE DEPOSITED IN THE COUNTY OF BEDFORD..."

# Constants
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
MAX_GENERATIONS = 100
POPULATION_SIZE = 500
ELITISM_COUNT = 50

class GeneticCracker:
    def __init__(self, cipher, ngram_file='english_quadgrams.txt'):
        self.cipher = cipher
        self.unique_numbers = list(set(cipher))
        self.num_unique = len(self.unique_numbers)
        self.scorer = NgramScore(ngram_file)
        
        # Download quadgrams if missing
        if not os.path.exists(ngram_file):
            print(f"Downloading {ngram_file}...")
            url = "https://gist.githubusercontent.com/calvinmetcalf/9384179/raw/4dd17e90c679234b333830c25d808d29a0082987/english_quadgrams.txt"
            try:
                r = requests.get(url)
                with open(ngram_file, 'w') as f:
                    f.write(r.text)
                self.scorer = NgramScore(ngram_file)
            except:
                print("Failed to download quadgrams. Using basic fallback (poor performance expected).")

    def decrypt(self, key_map):
        """Convert cipher to text using key_map {number: letter}."""
        return ''.join([key_map.get(n, '-') for n in self.cipher])

    def create_random_key(self):
        """Create a random mapping for all unique numbers."""
        key_map = {}
        for num in self.unique_numbers:
            # Bias initial population towards common First Letters (S, T, A, B, C, W, H, I, M, P) for book ciphers
            # But keep it random enough for diversity
            key_map[num] = random.choice(ALPHABET)
        return key_map

    def mutate(self, key_map, rate=0.05):
        """Randomly change some mappings."""
        new_map = key_map.copy()
        for num in self.unique_numbers:
            if random.random() < rate:
                new_map[num] = random.choice(ALPHABET)
        return new_map

    def crossover(self, parent1, parent2):
        """Combine two keys."""
        child = {}
        crossover_point = random.randint(0, len(self.unique_numbers))
        
        for i, num in enumerate(self.unique_numbers):
            if i < crossover_point:
                child[num] = parent1[num]
            else:
                child[num] = parent2[num]
        return child

    def solve(self):
        print(f"Genetic Attack on {len(self.cipher)} numbers ({len(self.unique_numbers)} unique)")
        print(f"Population: {POPULATION_SIZE}, Generations: {MAX_GENERATIONS}")
        
        # Initialize Population
        population = [self.create_random_key() for _ in range(POPULATION_SIZE)]
        
        best_score = -float('inf')
        best_key = None
        best_text = ""
        
        for gen in range(MAX_GENERATIONS):
            # Evaluate
            scores = []
            for key in population:
                text = self.decrypt(key)
                score = self.scorer.score(text)
                scores.append((score, key, text))
            
            # Sort by score descending
            scores.sort(key=lambda x: x[0], reverse=True)
            
            current_best_score, current_best_key, current_best_text = scores[0]
            
            if current_best_score > best_score:
                best_score = current_best_score
                best_key = current_best_key
                best_text = current_best_text
                print(f"Gen {gen:3d} | Score: {best_score:8.2f} | Text: {best_text[:60]}...")
            
            # Selection (Elitism + Parents)
            survivors = [s[1] for s in scores[:ELITISM_COUNT]]
            
            # Breeding
            new_population = list(survivors)
            while len(new_population) < POPULATION_SIZE:
                p1 = random.choice(survivors)
                p2 = random.choice(survivors)
                child = self.crossover(p1, p2)
                child = self.mutate(child)
                new_population.append(child)
                
            population = new_population
            
        return best_text, best_score

def main():
    print("="*60)
    print("BEALE GENETIC CRACKER")
    print("="*60)
    print("Attempting to evolve a solution for CIPHER 1...")
    
    cracker = GeneticCracker(CIPHER_1)
    text, score = cracker.solve()
    
    print("\n" + "="*60)
    print("FINAL RESULT (CIPHER 1)")
    print("="*60)
    print(f"Best Score: {score}")
    print(f"Decrypted Text:\n{text}")
    print("="*60)
    
    if score > -3000: # Heuristic threshold for "gibberish" vs "something kinda English"
        print("RESULT: Plausible English structure found!")
    else:
        print("RESULT: Still looks like gibberish. Cipher 1 likely unbreakable via simple substitution.")

if __name__ == "__main__":
    main()
