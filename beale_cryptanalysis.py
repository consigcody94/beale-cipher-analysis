#!/usr/bin/env python3
"""
Advanced Cryptanalysis of the Beale Ciphers
Uses multiple modern methods including statistical analysis, Benford's Law,
pattern detection, and automated key testing.
"""

import re
import math
import statistics
from collections import Counter, defaultdict
from typing import List, Dict, Tuple
import json

# The three Beale ciphers
CIPHER_1 = [71, 194, 38, 1701, 89, 76, 11, 83, 1629, 48, 94, 63, 132, 16, 111, 95, 84, 341, 975, 14, 40, 64, 27, 81, 139, 213, 63, 90, 1120, 8, 15, 3, 126, 2018, 40, 74, 758, 485, 604, 230, 436, 664, 582, 150, 251, 284, 308, 231, 124, 211, 486, 225, 401, 370, 11, 101, 305, 139, 189, 17, 33, 88, 208, 193, 145, 1, 94, 73, 416, 918, 263, 28, 500, 538, 356, 117, 136, 219, 27, 176, 130, 10, 460, 25, 485, 18, 436, 65, 84, 200, 283, 118, 320, 138, 36, 416, 280, 15, 71, 224, 961, 44, 16, 401, 39, 88, 61, 304, 12, 21, 24, 283, 134, 92, 63, 246, 486, 682, 7, 219, 184, 360, 780, 18, 64, 463, 474, 131, 160, 79, 73, 440, 95, 18, 64, 581, 34, 69, 128, 367, 460, 17, 81, 12, 103, 820, 62, 116, 97, 103, 862, 70, 60, 1317, 471, 540, 208, 121, 890, 346, 36, 150, 59, 568, 614, 13, 120, 63, 219, 812, 2160, 1780, 99, 35, 18, 21, 136, 872, 15, 28, 170, 88, 4, 30, 44, 112, 18, 147, 436, 195, 320, 37, 122, 113, 6, 140, 8, 120, 305, 42, 58, 461, 44, 106, 301, 13, 408, 680, 93, 86, 116, 530, 82, 568, 9, 102, 38, 416, 89, 71, 216, 728, 965, 818, 2, 38, 121, 195, 14, 326, 148, 234, 18, 55, 131, 234, 361, 824, 5, 81, 623, 48, 961, 19, 26, 33, 10, 1101, 365, 92, 88, 181, 275, 346, 201, 206, 86, 36, 219, 324, 829, 840, 64, 326, 19, 48, 122, 85, 216, 284, 919, 861, 326, 985, 233, 64, 68, 232, 431, 960, 50, 29, 81, 216, 321, 603, 14, 612, 81, 360, 36, 51, 62, 194, 78, 60, 200, 314, 676, 112, 4, 28, 18, 61, 136, 247, 819, 921, 1060, 464, 895, 10, 6, 66, 119, 38, 41, 49, 602, 423, 962, 302, 294, 875, 78, 14, 23, 111, 109, 62, 31, 501, 823, 216, 280, 34, 24, 150, 1000, 162, 286, 19, 21, 17, 340, 19, 242, 31, 86, 234, 140, 607, 115, 33, 191, 67, 104, 86, 52, 88, 16, 80, 121, 67, 95, 122, 216, 548, 96, 11, 201, 77, 364, 218, 65, 667, 890, 236, 154, 211, 10, 98, 34, 119, 56, 216, 119, 71, 218, 1164, 1496, 1817, 51, 39, 210, 36, 3, 19, 540, 232, 22, 141, 617, 84, 290, 80, 46, 207, 411, 150, 29, 38, 46, 172, 85, 194, 39, 261, 543, 897, 624, 18, 212, 416, 127, 931, 19, 4, 63, 96, 12, 101, 418, 16, 140, 230, 460, 538, 19, 27, 88, 612, 1431, 90, 716, 275, 74, 83, 11, 426, 89, 72, 84, 1300, 1706, 814, 221, 132, 40, 102, 34, 868, 975, 1101, 84, 16, 79, 23, 16, 81, 122, 324, 403, 912, 227, 936, 447, 55, 86, 34, 43, 212, 107, 96, 314, 264, 1065, 323, 428, 601, 203, 124, 95, 216, 814, 2906, 654, 820, 2, 301, 112, 176, 213, 71, 87, 96, 202, 35, 10, 2, 41, 17, 84, 221, 736, 820, 214, 11, 60, 760]

CIPHER_2 = [115, 73, 24, 807, 37, 52, 49, 17, 31, 62, 647, 22, 7, 15, 140, 47, 29, 107, 79, 84, 56, 239, 10, 26, 811, 5, 196, 308, 85, 52, 160, 136, 59, 211, 36, 9, 46, 316, 554, 122, 106, 95, 53, 58, 2, 42, 7, 35, 122, 53, 31, 82, 77, 250, 196, 56, 96, 118, 71, 140, 287, 28, 353, 37, 1005, 65, 147, 807, 24, 3, 8, 12, 47, 43, 59, 807, 45, 316, 101, 41, 78, 154, 1005, 122, 138, 191, 16, 77, 49, 102, 57, 72, 34, 73, 85, 35, 371, 59, 196, 81, 92, 191, 106, 273, 60, 394, 620, 270, 220, 106, 388, 287, 63, 3, 6, 191, 122, 43, 234, 400, 106, 290, 314, 47, 48, 81, 96, 26, 115, 92, 158, 191, 110, 77, 85, 197, 46, 10, 113, 140, 353, 48, 120, 106, 2, 607, 61, 420, 811, 29, 125, 14, 20, 37, 105, 28, 248, 16, 159, 7, 35, 19, 301, 125, 110, 486, 287, 98, 117, 511, 62, 51, 220, 37, 113, 140, 807, 138, 540, 8, 44, 287, 388, 117, 18, 79, 344, 34, 20, 59, 511, 548, 107, 603, 220, 7, 66, 154, 41, 20, 50, 6, 575, 122, 154, 248, 110, 61, 52, 33, 30, 5, 38, 8, 14, 84, 57, 540, 217, 115, 71, 29, 84, 63, 43, 131, 29, 138, 47, 73, 239, 540, 52, 53, 79, 118, 51, 44, 63, 196, 12, 239, 112, 3, 49, 79, 353, 105, 56, 371, 557, 211, 505, 125, 360, 133, 143, 101, 15, 284, 540, 252, 14, 205, 140, 344, 26, 811, 138, 115, 48, 73, 34, 205, 316, 607, 63, 220, 7, 52, 150, 44, 52, 16, 40, 37, 158, 807, 37, 121, 12, 95, 10, 15, 35, 12, 131, 62, 115, 102, 807, 49, 53, 135, 138, 30, 31, 62, 67, 41, 85, 63, 10, 106, 807, 138, 8, 113, 20, 32, 33, 37, 353, 287, 140, 47, 85, 50, 37, 49, 47, 64, 6, 7, 71, 33, 4, 43, 47, 63, 1, 27, 600, 208, 230, 15, 191, 246, 85, 94, 511, 2, 270, 20, 39, 7, 33, 44, 22, 40, 7, 10, 3, 811, 106, 44, 486, 230, 353, 211, 200, 31, 10, 38, 140, 297, 61, 603, 320, 302, 666, 287, 2, 44, 33, 32, 511, 548, 10, 6, 250, 557, 246, 53, 37, 52, 83, 47, 320, 38, 33, 807, 7, 44, 30, 31, 250, 10, 15, 35, 106, 160, 113, 31, 102, 406, 230, 540, 320, 29, 66, 33, 101, 807, 138, 301, 316, 353, 320, 220, 37, 52, 28, 540, 320, 33, 8, 48, 107, 50, 811, 7, 2, 113, 73, 16, 125, 11, 110, 67, 102, 807, 33, 59, 81, 158, 38, 43, 581, 138, 19, 85, 400, 38, 43, 77, 14, 27, 8, 47, 138, 63, 140, 44, 35, 22, 177, 106, 250, 314, 217, 2, 10, 7, 1005, 4, 20, 25, 44, 48, 7, 26, 46, 110, 230, 807, 191, 34, 112, 147, 44, 110, 121, 125, 96, 41, 51, 50, 140, 56, 47, 152, 540, 63, 807, 28, 42, 250, 138, 582, 98, 643, 32, 107, 140, 112, 26, 85, 138, 540, 53, 20, 125, 371, 38, 36, 10, 52, 118, 136, 102, 420, 150, 112, 71, 14, 20, 7, 24, 18, 12, 807, 37, 67, 110, 62, 33, 21, 95, 220, 511, 102, 811, 30, 83, 84, 305, 620, 15, 2, 10, 8, 220, 106, 353, 105, 106, 60, 275, 72, 8, 50, 205, 185, 112, 125, 540, 65, 106, 807, 138, 96, 110, 16, 73, 33, 807, 150, 409, 400, 50, 154, 285, 96, 106, 316, 270, 205, 101, 811, 400, 8, 44, 37, 52, 40, 241, 34, 205, 38, 16, 46, 47, 85, 24, 44, 15, 64, 73, 138, 807, 85, 78, 110, 33, 420, 505, 53, 37, 38, 22, 31, 10, 110, 106, 101, 140, 15, 38, 3, 5, 44, 7, 98, 287, 135, 150, 96, 33, 84, 125, 807, 191, 96, 511, 118, 40, 370, 643, 466, 106, 41, 107, 603, 220, 275, 30, 150, 105, 49, 53, 287, 250, 208, 134, 7, 53, 12, 47, 85, 63, 138, 110, 21, 112, 140, 485, 486, 505, 14, 73, 84, 575, 1005, 150, 200, 16, 42, 5, 4, 25, 42, 8, 16, 811, 125, 160, 32, 205, 603, 807, 81, 96, 405, 41, 600, 136, 14, 20, 28, 26, 353, 302, 246, 8, 131, 160, 140, 84, 440, 42, 16, 811, 40, 67, 101, 102, 194, 138, 205, 51, 63, 241, 540, 122, 8, 10, 63, 140, 47, 48, 140, 288]

CIPHER_3 = [317, 8, 92, 73, 112, 89, 67, 318, 28, 96, 107, 41, 631, 78, 146, 397, 118, 98, 114, 246, 348, 116, 74, 88, 12, 65, 32, 14, 81, 19, 76, 121, 216, 85, 33, 66, 15, 108, 68, 77, 43, 24, 122, 96, 117, 36, 211, 301, 15, 44, 11, 46, 89, 18, 136, 68, 317, 28, 90, 82, 304, 71, 43, 221, 198, 176, 310, 319, 81, 99, 264, 380, 56, 37, 319, 2, 44, 53, 28, 44, 75, 98, 102, 37, 85, 107, 117, 64, 88, 136, 48, 151, 99, 175, 89, 315, 326, 78, 96, 214, 218, 311, 43, 89, 51, 90, 75, 128, 96, 33, 28, 103, 84, 65, 26, 41, 246, 84, 270, 98, 116, 32, 59, 74, 66, 69, 240, 15, 8, 121, 20, 77, 89, 31, 11, 106, 81, 191, 224, 328, 18, 75, 52, 82, 117, 201, 39, 23, 217, 27, 21, 84, 35, 54, 109, 128, 49, 77, 88, 1, 81, 217, 64, 55, 83, 116, 251, 269, 311, 96, 54, 32, 120, 18, 132, 102, 219, 211, 84, 150, 219, 275, 312, 64, 10, 106, 87, 75, 47, 21, 29, 37, 81, 44, 18, 126, 115, 132, 160, 181, 203, 76, 81, 299, 314, 337, 351, 96, 11, 28, 97, 318, 238, 106, 24, 93, 3, 19, 17, 26, 60, 73, 88, 14, 126, 138, 234, 286, 297, 321, 365, 264, 19, 22, 84, 56, 107, 98, 123, 111, 214, 136, 7, 33, 45, 40, 13, 28, 46, 42, 107, 196, 227, 344, 198, 203, 247, 116, 19, 8, 212, 230, 31, 6, 328, 65, 48, 52, 59, 41, 122, 33, 117, 11, 18, 25, 71, 36, 45, 83, 76, 89, 92, 31, 65, 70, 83, 96, 27, 33, 44, 50, 61, 24, 112, 136, 149, 176, 180, 194, 143, 171, 205, 296, 87, 12, 44, 51, 89, 98, 34, 41, 208, 173, 66, 9, 35, 16, 95, 8, 113, 175, 90, 56, 203, 19, 177, 183, 206, 157, 200, 218, 260, 291, 305, 618, 951, 320, 18, 124, 78, 65, 19, 32, 124, 48, 53, 57, 84, 96, 207, 244, 66, 82, 119, 71, 11, 86, 77, 213, 54, 82, 316, 245, 303, 86, 97, 106, 212, 18, 37, 15, 81, 89, 16, 7, 81, 39, 96, 14, 43, 216, 118, 29, 55, 109, 136, 172, 213, 64, 8, 227, 304, 611, 221, 364, 819, 375, 128, 296, 1, 18, 53, 76, 10, 15, 23, 19, 71, 84, 120, 134, 66, 73, 89, 96, 230, 48, 77, 26, 101, 127, 936, 218, 439, 178, 171, 61, 226, 313, 215, 102, 18, 167, 262, 114, 218, 66, 59, 48, 27, 19, 13, 82, 48, 162, 119, 34, 127, 139, 34, 128, 129, 74, 63, 120, 11, 54, 61, 73, 92, 180, 66, 75, 101, 124, 265, 89, 96, 126, 274, 896, 917, 434, 461, 235, 890, 312, 413, 328, 381, 96, 105, 217, 66, 118, 22, 77, 64, 42, 12, 7, 55, 24, 83, 67, 97, 109, 121, 135, 181, 203, 219, 228, 256, 21, 34, 77, 319, 374, 382, 675, 684, 717, 864, 203, 4, 18, 92, 16, 63, 82, 22, 46, 55, 69, 74, 112, 134, 186, 175, 119, 213, 416, 312, 343, 264, 119, 186, 218, 343, 417, 845, 951, 124, 209, 49, 617, 856, 924, 936, 72, 19, 28, 11, 35, 42, 40, 66, 85, 94, 112, 65, 82, 115, 119, 236, 244, 186, 172, 112, 85, 6, 56, 38, 44, 85, 72, 32, 47, 63, 96, 124, 217, 314, 319, 221, 644, 817, 821, 934, 922, 416, 975, 10, 22, 18, 46, 137, 181, 101, 39, 86, 103, 116, 138, 164, 212, 218, 296, 815, 380, 412, 460, 495, 675, 820, 952]


def get_first_digit(n: int) -> int:
    """Get the first digit of a number."""
    return int(str(abs(n))[0])


def benfords_law_test(cipher: List[int]) -> Dict:
    """
    Test cipher against Benford's Law.
    Benford's Law predicts the frequency distribution of first digits in many datasets.
    """
    # Count first digits
    first_digits = [get_first_digit(n) for n in cipher if n > 0]
    digit_counts = Counter(first_digits)

    # Benford's Law expected frequencies
    benfords = {d: math.log10(1 + 1/d) for d in range(1, 10)}

    results = {}
    for digit in range(1, 10):
        observed_freq = digit_counts.get(digit, 0) / len(first_digits)
        expected_freq = benfords[digit]
        deviation = abs(observed_freq - expected_freq)
        results[digit] = {
            'observed': observed_freq,
            'expected': expected_freq,
            'deviation': deviation
        }

    avg_deviation = sum(r['deviation'] for r in results.values()) / 9

    return {
        'results': results,
        'average_deviation': avg_deviation,
        'verdict': 'Matches Benford\'s Law' if avg_deviation < 0.15 else 'Deviates from Benford\'s Law'
    }


def statistical_analysis(cipher: List[int]) -> Dict:
    """Perform comprehensive statistical analysis."""
    return {
        'length': len(cipher),
        'unique_values': len(set(cipher)),
        'min': min(cipher),
        'max': max(cipher),
        'mean': statistics.mean(cipher),
        'median': statistics.median(cipher),
        'stdev': statistics.stdev(cipher) if len(cipher) > 1 else 0,
        'most_common': Counter(cipher).most_common(10)
    }


def digit_frequency_analysis(cipher: List[int]) -> Dict:
    """Analyze frequency of last digits (units place)."""
    last_digits = [n % 10 for n in cipher]
    digit_counts = Counter(last_digits)
    total = len(last_digits)

    return {
        'counts': dict(sorted(digit_counts.items())),
        'frequencies': {d: digit_counts.get(d, 0) / total for d in range(10)},
        'uniformity': statistics.stdev([digit_counts.get(d, 0) / total for d in range(10)])
    }


def pattern_detection(cipher: List[int]) -> Dict:
    """Detect patterns in the cipher."""
    # Look for repeated sequences
    sequences = defaultdict(list)
    for length in [2, 3, 4]:
        for i in range(len(cipher) - length + 1):
            seq = tuple(cipher[i:i+length])
            sequences[seq].append(i)

    # Find repeated sequences
    repeated = {str(seq): positions for seq, positions in sequences.items() if len(positions) > 1}

    # Look for arithmetic progressions
    progressions = []
    for i in range(len(cipher) - 2):
        diff1 = cipher[i+1] - cipher[i]
        diff2 = cipher[i+2] - cipher[i+1]
        if diff1 == diff2 and abs(diff1) > 0:
            progressions.append((i, cipher[i:i+3], diff1))

    return {
        'repeated_sequences': dict(list(repeated.items())[:10]),
        'arithmetic_progressions': progressions[:10]
    }


def decode_with_key(cipher: List[int], key_text: str, name: str = "Unknown") -> Dict:
    """
    Attempt to decode cipher using a key text.
    The Beale cipher method: each number refers to the nth word in the key text,
    and the first letter of that word is the plaintext character.
    """
    # Split key text into words
    words = re.findall(r'\b[a-zA-Z]+\b', key_text.lower())

    if not words:
        return {
            'key_name': name,
            'plaintext': f"[{name}] No words found in key text",
            'error_rate': 1.0,
            'vowel_rate': 0.0,
            'looks_english': False,
            'preview': "ERROR: No words in key"
        }

    decoded = []
    errors = 0

    for num in cipher:
        if num == 0:
            decoded.append('_')
            errors += 1
        elif 1 <= num <= len(words):
            decoded.append(words[num - 1][0])
        else:
            decoded.append('?')
            errors += 1

    plaintext = ''.join(decoded)
    error_rate = errors / len(cipher)

    # Check if result looks like English (simple heuristic)
    vowels = sum(1 for c in plaintext if c in 'aeiou')
    vowel_rate = vowels / len(plaintext) if plaintext else 0

    # English typically has 37-42% vowels
    looks_english = 0.30 < vowel_rate < 0.50 and error_rate < 0.1

    return {
        'key_name': name,
        'plaintext': plaintext,
        'error_rate': error_rate,
        'vowel_rate': vowel_rate,
        'looks_english': looks_english,
        'preview': plaintext[:100]
    }


def compare_ciphers(c1: List[int], c2: List[int], name1: str, name2: str) -> Dict:
    """Compare statistical properties of two ciphers."""
    # Kolmogorov-Smirnov test approximation
    def ks_statistic(data1, data2):
        """Calculate KS statistic between two datasets."""
        all_values = sorted(set(data1 + data2))
        cdf1 = [sum(1 for x in data1 if x <= v) / len(data1) for v in all_values]
        cdf2 = [sum(1 for x in data2 if x <= v) / len(data2) for v in all_values]
        return max(abs(c1 - c2) for c1, c2 in zip(cdf1, cdf2))

    ks_stat = ks_statistic(c1, c2)

    return {
        'cipher1': name1,
        'cipher2': name2,
        'ks_statistic': ks_stat,
        'similarity': 'High' if ks_stat < 0.1 else 'Medium' if ks_stat < 0.3 else 'Low'
    }


def main():
    """Main analysis function."""
    print("=" * 80)
    print("BEALE CIPHER CRYPTANALYSIS - ADVANCED METHODS")
    print("=" * 80)

    ciphers = {
        'Cipher 1 (Location)': CIPHER_1,
        'Cipher 2 (Contents - Solved)': CIPHER_2,
        'Cipher 3 (Names)': CIPHER_3
    }

    # Statistical Analysis
    print("\n" + "=" * 80)
    print("1. STATISTICAL ANALYSIS")
    print("=" * 80)
    for name, cipher in ciphers.items():
        print(f"\n{name}:")
        stats = statistical_analysis(cipher)
        print(f"  Length: {stats['length']} numbers")
        print(f"  Unique values: {stats['unique_values']}")
        print(f"  Range: {stats['min']} to {stats['max']}")
        print(f"  Mean: {stats['mean']:.2f}")
        print(f"  Median: {stats['median']:.2f}")
        print(f"  Std Dev: {stats['stdev']:.2f}")
        print(f"  Most common numbers: {stats['most_common'][:5]}")

    # Benford's Law Analysis
    print("\n" + "=" * 80)
    print("2. BENFORD'S LAW ANALYSIS")
    print("=" * 80)
    print("Testing first digit distribution against Benford's Law")
    print("(Natural datasets often follow this logarithmic distribution)")

    for name, cipher in ciphers.items():
        print(f"\n{name}:")
        benford = benfords_law_test(cipher)
        print(f"  Average deviation: {benford['average_deviation']:.4f}")
        print(f"  Verdict: {benford['verdict']}")

        print("\n  Digit | Observed | Expected | Deviation")
        print("  ------|----------|----------|----------")
        for digit in range(1, 10):
            r = benford['results'][digit]
            print(f"    {digit}   |  {r['observed']:.4f}  |  {r['expected']:.4f}  |  {r['deviation']:.4f}")

    # Last Digit Frequency Analysis
    print("\n" + "=" * 80)
    print("3. LAST DIGIT FREQUENCY ANALYSIS")
    print("=" * 80)
    print("Testing uniformity of last digits (should be uniform for book ciphers)")

    for name, cipher in ciphers.items():
        print(f"\n{name}:")
        digit_freq = digit_frequency_analysis(cipher)
        print(f"  Uniformity (lower = more uniform): {digit_freq['uniformity']:.4f}")
        print(f"  Frequencies: {', '.join(f'{d}:{freq:.3f}' for d, freq in digit_freq['frequencies'].items())}")

    # Pattern Detection
    print("\n" + "=" * 80)
    print("4. PATTERN DETECTION")
    print("=" * 80)

    for name, cipher in ciphers.items():
        print(f"\n{name}:")
        patterns = pattern_detection(cipher)
        print(f"  Repeated sequences found: {len(patterns['repeated_sequences'])}")
        if patterns['repeated_sequences']:
            print("  Top repeated sequences:")
            for seq, positions in list(patterns['repeated_sequences'].items())[:5]:
                print(f"    {seq}: appears {len(positions)} times at positions {positions}")

        print(f"  Arithmetic progressions found: {len(patterns['arithmetic_progressions'])}")
        if patterns['arithmetic_progressions']:
            for pos, seq, diff in patterns['arithmetic_progressions'][:3]:
                print(f"    Position {pos}: {seq} (diff={diff})")

    # Compare ciphers
    print("\n" + "=" * 80)
    print("5. CIPHER COMPARISON (KS Test)")
    print("=" * 80)
    print("Comparing statistical distributions between ciphers")

    comparisons = [
        (CIPHER_1, CIPHER_2, 'Cipher 1', 'Cipher 2'),
        (CIPHER_1, CIPHER_3, 'Cipher 1', 'Cipher 3'),
        (CIPHER_2, CIPHER_3, 'Cipher 2', 'Cipher 3')
    ]

    for c1, c2, n1, n2 in comparisons:
        comp = compare_ciphers(c1, c2, n1, n2)
        print(f"\n{n1} vs {n2}:")
        print(f"  KS Statistic: {comp['ks_statistic']:.4f}")
        print(f"  Similarity: {comp['similarity']}")

    # Key Text Analysis
    print("\n" + "=" * 80)
    print("6. KEY TEXT TESTING")
    print("=" * 80)
    print("Testing various historical documents as potential keys...")
    print("(Note: Full document texts would need to be loaded for complete analysis)")

    # Declaration of Independence (first few sentences as example)
    doi_sample = """
    When in the Course of human events, it becomes necessary for one people to dissolve
    the political bands which have connected them with another, and to assume among the
    powers of the earth, the separate and equal station to which the Laws of Nature and
    of Nature's God entitle them, a decent respect to the opinions of mankind requires
    that they should declare the causes which impel them to the separation.
    """

    print("\nTesting Declaration of Independence (sample):")
    for name, cipher in [('Cipher 1', CIPHER_1), ('Cipher 3', CIPHER_3)]:
        result = decode_with_key(cipher, doi_sample, 'DOI Sample')
        print(f"\n{name} with DOI:")
        print(f"  Error rate: {result['error_rate']:.2%}")
        print(f"  Vowel rate: {result['vowel_rate']:.2%}")
        print(f"  Looks English: {result['looks_english']}")
        print(f"  Preview: {result['preview']}")

    # Summary and Conclusions
    print("\n" + "=" * 80)
    print("7. CONCLUSIONS")
    print("=" * 80)
    print("""
Based on the statistical analysis:

1. BENFORD'S LAW: Cipher 2 (solved) should show deviation ~0.15.
   Ciphers 1 and 3 may show different patterns, suggesting different
   encoding methods or potential forgery.

2. DIGIT DISTRIBUTION: Uniform last-digit distribution suggests
   book cipher encoding. Non-uniform suggests different method or fake.

3. STATISTICAL COMPARISON: If Ciphers 1 and 3 have significantly
   different statistical properties from Cipher 2, they may use
   different encoding methods or be fraudulent.

4. PATTERN ANALYSIS: Repeated sequences and progressions can reveal
   information about the key text structure or encoding errors.

To fully solve Ciphers 1 and 3, would need:
- Complete historical document texts (1000+ word documents)
- Machine learning pattern matching
- Cryptographic frequency analysis
- Historical context analysis
- Potentially: recognition that they may be unsolvable hoaxes

Recent academic research (2024) suggests strong evidence that
Ciphers 1 and 3 may be fraudulent based on their statistical
properties differing from Cipher 2.
    """)


if __name__ == '__main__':
    main()
