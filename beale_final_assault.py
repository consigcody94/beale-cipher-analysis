#!/usr/bin/env python3
"""
FINAL ASSAULT ON BEALE CIPHERS
Targeting documents that are:
1. Long enough (2906+ words for Cipher 1, 975+ for Cipher 3)
2. Available to 1820s Virginia gentleman
3. Important enough to preserve
"""

import re
import requests
import time
from typing import List, Tuple

# Full ciphers
CIPHER_1 = [71, 194, 38, 1701, 89, 76, 11, 83, 1629, 48, 94, 63, 132, 16, 111, 95, 84, 341, 975, 14, 40, 64, 27, 81, 139, 213, 63, 90, 1120, 8, 15, 3, 126, 2018, 40, 74, 758, 485, 604, 230, 436, 664, 582, 150, 251, 284, 308, 231, 124, 211, 486, 225, 401, 370, 11, 101, 305, 139, 189, 17, 33, 88, 208, 193, 145, 1, 94, 73, 416, 918, 263, 28, 500, 538, 356, 117, 136, 219, 27, 176, 130, 10, 460, 25, 485, 18, 436, 65, 84, 200, 283, 118, 320, 138, 36, 416, 280, 15, 71, 224, 961, 44, 16, 401, 39, 88, 61, 304, 12, 21, 24, 283, 134, 92, 63, 246, 486, 682, 7, 219, 184, 360, 780, 18, 64, 463, 474, 131, 160, 79, 73, 440, 95, 18, 64, 581, 34, 69, 128, 367, 460, 17, 81, 12, 103, 820, 62, 116, 97, 103, 862, 70, 60, 1317, 471, 540, 208, 121, 890, 346, 36, 150, 59, 568, 614, 13, 120, 63, 219, 812, 2160, 1780, 99, 35, 18, 21, 136, 872, 15, 28, 170, 88, 4, 30, 44, 112, 18, 147, 436, 195, 320, 37, 122, 113, 6, 140, 8, 120, 305, 42, 58, 461, 44, 106, 301, 13, 408, 680, 93, 86, 116, 530, 82, 568, 9, 102, 38, 416, 89, 71, 216, 728, 965, 818, 2, 38, 121, 195, 14, 326, 148, 234, 18, 55, 131, 234, 361, 824, 5, 81, 623, 48, 961, 19, 26, 33, 10, 1101, 365, 92, 88, 181, 275, 346, 201, 206, 86, 36, 219, 324, 829, 840, 64, 326, 19, 48, 122, 85, 216, 284, 919, 861, 326, 985, 233, 64, 68, 232, 431, 960, 50, 29, 81, 216, 321, 603, 14, 612, 81, 360, 36, 51, 62, 194, 78, 60, 200, 314, 676, 112, 4, 28, 18, 61, 136, 247, 819, 921, 1060, 464, 895, 10, 6, 66, 119, 38, 41, 49, 602, 423, 962, 302, 294, 875, 78, 14, 23, 111, 109, 62, 31, 501, 823, 216, 280, 34, 24, 150, 1000, 162, 286, 19, 21, 17, 340, 19, 242, 31, 86, 234, 140, 607, 115, 33, 191, 67, 104, 86, 52, 88, 16, 80, 121, 67, 95, 122, 216, 548, 96, 11, 201, 77, 364, 218, 65, 667, 890, 236, 154, 211, 10, 98, 34, 119, 56, 216, 119, 71, 218, 1164, 1496, 1817, 51, 39, 210, 36, 3, 19, 540, 232, 22, 141, 617, 84, 290, 80, 46, 207, 411, 150, 29, 38, 46, 172, 85, 194, 39, 261, 543, 897, 624, 18, 212, 416, 127, 931, 19, 4, 63, 96, 12, 101, 418, 16, 140, 230, 460, 538, 19, 27, 88, 612, 1431, 90, 716, 275, 74, 83, 11, 426, 89, 72, 84, 1300, 1706, 814, 221, 132, 40, 102, 34, 868, 975, 1101, 84, 16, 79, 23, 16, 81, 122, 324, 403, 912, 227, 936, 447, 55, 86, 34, 43, 212, 107, 96, 314, 264, 1065, 323, 428, 601, 203, 124, 95, 216, 814, 2906, 654, 820, 2, 301, 112, 176, 213, 71, 87, 96, 202, 35, 10, 2, 41, 17, 84, 221, 736, 820, 214, 11, 60, 760]

CIPHER_3 = [317, 8, 92, 73, 112, 89, 67, 318, 28, 96, 107, 41, 631, 78, 146, 397, 118, 98, 114, 246, 348, 116, 74, 88, 12, 65, 32, 14, 81, 19, 76, 121, 216, 85, 33, 66, 15, 108, 68, 77, 43, 24, 122, 96, 117, 36, 211, 301, 15, 44, 11, 46, 89, 18, 136, 68, 317, 28, 90, 82, 304, 71, 43, 221, 198, 176, 310, 319, 81, 99, 264, 380, 56, 37, 319, 2, 44, 53, 28, 44, 75, 98, 102, 37, 85, 107, 117, 64, 88, 136, 48, 151, 99, 175, 89, 315, 326, 78, 96, 214, 218, 311, 43, 89, 51, 90, 75, 128, 96, 33, 28, 103, 84, 65, 26, 41, 246, 84, 270, 98, 116, 32, 59, 74, 66, 69, 240, 15, 8, 121, 20, 77, 89, 31, 11, 106, 81, 191, 224, 328, 18, 75, 52, 82, 117, 201, 39, 23, 217, 27, 21, 84, 35, 54, 109, 128, 49, 77, 88, 1, 81, 217, 64, 55, 83, 116, 251, 269, 311, 96, 54, 32, 120, 18, 132, 102, 219, 211, 84, 150, 219, 275, 312, 64, 10, 106, 87, 75, 47, 21, 29, 37, 81, 44, 18, 126, 115, 132, 160, 181, 203, 76, 81, 299, 314, 337, 351, 96, 11, 28, 97, 318, 238, 106, 24, 93, 3, 19, 17, 26, 60, 73, 88, 14, 126, 138, 234, 286, 297, 321, 365, 264, 19, 22, 84, 56, 107, 98, 123, 111, 214, 136, 7, 33, 45, 40, 13, 28, 46, 42, 107, 196, 227, 344, 198, 203, 247, 116, 19, 8, 212, 230, 31, 6, 328, 65, 48, 52, 59, 41, 122, 33, 117, 11, 18, 25, 71, 36, 45, 83, 76, 89, 92, 31, 65, 70, 83, 96, 27, 33, 44, 50, 61, 24, 112, 136, 149, 176, 180, 194, 143, 171, 205, 296, 87, 12, 44, 51, 89, 98, 34, 41, 208, 173, 66, 9, 35, 16, 95, 8, 113, 175, 90, 56, 203, 19, 177, 183, 206, 157, 200, 218, 260, 291, 305, 618, 951, 320, 18, 124, 78, 65, 19, 32, 124, 48, 53, 57, 84, 96, 207, 244, 66, 82, 119, 71, 11, 86, 77, 213, 54, 82, 316, 245, 303, 86, 97, 106, 212, 18, 37, 15, 81, 89, 16, 7, 81, 39, 96, 14, 43, 216, 118, 29, 55, 109, 136, 172, 213, 64, 8, 227, 304, 611, 221, 364, 819, 375, 128, 296, 1, 18, 53, 76, 10, 15, 23, 19, 71, 84, 120, 134, 66, 73, 89, 96, 230, 48, 77, 26, 101, 127, 936, 218, 439, 178, 171, 61, 226, 313, 215, 102, 18, 167, 262, 114, 218, 66, 59, 48, 27, 19, 13, 82, 48, 162, 119, 34, 127, 139, 34, 128, 129, 74, 63, 120, 11, 54, 61, 73, 92, 180, 66, 75, 101, 124, 265, 89, 96, 126, 274, 896, 917, 434, 461, 235, 890, 312, 413, 328, 381, 96, 105, 217, 66, 118, 22, 77, 64, 42, 12, 7, 55, 24, 83, 67, 97, 109, 121, 135, 181, 203, 219, 228, 256, 21, 34, 77, 319, 374, 382, 675, 684, 717, 864, 203, 4, 18, 92, 16, 63, 82, 22, 46, 55, 69, 74, 112, 134, 186, 175, 119, 213, 416, 312, 343, 264, 119, 186, 218, 343, 417, 845, 951, 124, 209, 49, 617, 856, 924, 936, 72, 19, 28, 11, 35, 42, 40, 66, 85, 94, 112, 65, 82, 115, 119, 236, 244, 186, 172, 112, 85, 6, 56, 38, 44, 85, 72, 32, 47, 63, 96, 124, 217, 314, 319, 221, 644, 817, 821, 934, 922, 416, 975, 10, 22, 18, 46, 137, 181, 101, 39, 86, 103, 116, 138, 164, 212, 218, 296, 815, 380, 412, 460, 495, 675, 820, 952]

def download(url):
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        return r.text
    except:
        return ""

def decode_and_score(cipher: List[int], text: str, name: str) -> Tuple[str, float, dict]:
    """Decode and provide comprehensive scoring."""
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    if not words:
        return "", -10000, {}

    # Pad if needed
    max_num = max(cipher)
    if len(words) < max_num:
        return "", -10000, {'error': f'Only {len(words)} words, need {max_num}'}

    decoded = []
    errors = 0
    for num in cipher:
        if num == 0 or num > len(words):
            decoded.append('?')
            errors += 1
        else:
            decoded.append(words[num - 1][0])

    plaintext = ''.join(decoded)
    error_rate = errors / len(cipher)

    # Advanced scoring
    alpha_chars = [c for c in plaintext if c.isalpha()]
    if not alpha_chars:
        return plaintext, -10000, {}

    vowels = sum(1 for c in alpha_chars if c in 'aeiou')
    vowel_rate = vowels / len(alpha_chars)

    # English is 37-42% vowels
    score = 0
    score -= error_rate * 2000  # Heavy penalty for errors

    if 0.35 < vowel_rate < 0.45:
        score += 500  # Major bonus for correct vowel ratio
    else:
        score -= abs(vowel_rate - 0.40) * 1000

    # Check for common English patterns
    common_words = ['the', 'and', 'of', 'to', 'in', 'a', 'is', 'that', 'it', 'for']
    for word in common_words:
        score += plaintext.count(word) * 100

    # Bigrams
    bigrams = ['th', 'he', 'in', 'er', 'an', 're', 'on', 'at', 'en', 'nd']
    for bg in bigrams:
        score += plaintext.count(bg) * 20

    # Trigrams
    trigrams = ['the', 'and', 'ing', 'ion', 'ent', 'for', 'you', 'hat']
    for tg in trigrams:
        score += plaintext.count(tg) * 30

    # Check for reasonable words (3+ letters, no '?')
    potential_words = re.findall(r'[a-z]{3,}', plaintext.lower())
    score += len(potential_words) * 10

    # Max clean sequence
    max_clean = 0
    current = 0
    for c in plaintext:
        if c != '?':
            current += 1
            max_clean = max(max_clean, current)
        else:
            current = 0

    score += max_clean * 3

    stats = {
        'error_rate': error_rate,
        'vowel_rate': vowel_rate,
        'max_clean_seq': max_clean,
        'potential_words': len(potential_words),
        'word_count': len(words)
    }

    return plaintext, score, stats


# TARGET DOCUMENTS - Must be 2906+ words
DOCUMENTS_TO_TEST = {
    # FOUNDING DOCUMENTS (Long versions)
    'Federalist_Papers': ('https://www.gutenberg.org/files/1404/1404-0.txt', 'All Federalist Papers combined - ~70,000 words'),
    'US_Constitution_Complete': ('https://www.gutenberg.org/files/5/5-0.txt', 'Constitution + all amendments'),
    'Washington_Farewell': ('https://www.gutenberg.org/files/109/109-0.txt', '~6,000 words'),

    # EXPLORATION (Beale was frontiersman/explorer)
    'Lewis_Clark_Journals': ('https://www.gutenberg.org/files/8419/8419-0.txt', 'Expedition journals - massive'),

    # POPULAR LITERATURE IN 1820s
    'Paradise_Lost': ('https://www.gutenberg.org/files/26/26-0.txt', 'John Milton - very popular'),
    'Pilgrims_Progress': ('https://www.gutenberg.org/files/131/131-0.txt', 'Bunyan - hugely popular'),
    'Robinson_Crusoe': ('https://www.gutenberg.org/files/521/521-0.txt', 'Defoe - adventure story'),
    'Gullivers_Travels': ('https://www.gutenberg.org/files/829/829-0.txt', 'Swift - satirical travel'),

    # SHAKESPEARE (Very popular in that era)
    'Complete_Shakespeare_Hamlet': ('https://www.gutenberg.org/files/1524/1524-0.txt', 'Full play'),

    # PHILOSOPHY/POLITICAL (Gentleman would have read)
    'Wealth_of_Nations': ('https://www.gutenberg.org/files/3300/3300-0.txt', 'Adam Smith - economics'),
    'Common_Sense': ('https://www.gutenberg.org/files/147/147-0.txt', 'Thomas Paine'),
    'Rights_of_Man': ('https://www.gutenberg.org/files/3742/3742-0.txt', 'Paine'),

    # AMERICAN AUTOBIOGRAPHY
    'Franklin_Autobiography': ('https://www.gutenberg.org/files/20203/20203-0.txt', 'Ben Franklin'),

    # BIBLE (Most common book of era)
    'KJV_Bible_Complete': ('https://www.gutenberg.org/cache/epub/10/pg10.txt', 'Entire King James Bible'),
}

print("=" * 80)
print("FINAL ASSAULT: BRUTE FORCE WITH HISTORICALLY APPROPRIATE DOCUMENTS")
print("=" * 80)
print(f"\nCipher 1 requires: {max(CIPHER_1)} words minimum")
print(f"Cipher 3 requires: {max(CIPHER_3)} words minimum")
print(f"\nTesting {len(DOCUMENTS_TO_TEST)} documents...")

results_c1 = []
results_c3 = []

for i, (name, (url, description)) in enumerate(DOCUMENTS_TO_TEST.items(), 1):
    print(f"\n[{i}/{len(DOCUMENTS_TO_TEST)}] {name}")
    print(f"  Description: {description}")
    print(f"  Downloading...")

    text = download(url)
    if not text:
        print("  ❌ Failed to download")
        continue

    # Clean Gutenberg headers
    text = re.sub(r'\*\*\* START OF .*? \*\*\*.*?\n', '', text, flags=re.DOTALL)
    text = re.sub(r'\*\*\* END OF .*?\*\*\*', '', text, flags=re.DOTALL)

    word_count = len(re.findall(r'\b[a-zA-Z]+\b', text))
    print(f"  ✓ Downloaded: {len(text):,} chars, {word_count:,} words")

    # Test both ciphers
    pt1, score1, stats1 = decode_and_score(CIPHER_1, text, name)
    pt3, score3, stats3 = decode_and_score(CIPHER_3, text, name)

    print(f"  C1 Score: {score1:8.1f} | Errors: {stats1.get('error_rate', 1):.1%} | Vowels: {stats1.get('vowel_rate', 0):.1%}")
    print(f"  C1 Text:  {pt1[:70]}")

    print(f"  C3 Score: {score3:8.1f} | Errors: {stats3.get('error_rate', 1):.1%} | Vowels: {stats3.get('vowel_rate', 0):.1%}")
    print(f"  C3 Text:  {pt3[:70]}")

    results_c1.append((name, score1, pt1, stats1))
    results_c3.append((name, score3, pt3, stats3))

    # Check for breakthrough!
    if score1 > 1000:
        print("\n" + "!" * 80)
        print("!!! POSSIBLE CIPHER 1 SOLUTION FOUND !!!")
        print("!" * 80)
        print(f"Document: {name}")
        print(f"Full text:\n{pt1}")

    if score3 > 1000:
        print("\n" + "!" * 80)
        print("!!! POSSIBLE CIPHER 3 SOLUTION FOUND !!!")
        print("!" * 80)
        print(f"Document: {name}")
        print(f"Full text:\n{pt3}")

    time.sleep(1)  # Be nice to servers

# Final results
print("\n" + "=" * 80)
print("TOP 5 RESULTS - CIPHER 1")
print("=" * 80)

results_c1.sort(key=lambda x: x[1], reverse=True)
for i, (name, score, text, stats) in enumerate(results_c1[:5], 1):
    print(f"\n#{i}. {name}")
    print(f"Score: {score:.1f}")
    print(f"Stats: {stats}")
    print(f"Text (first 150 chars): {text[:150]}")

print("\n" + "=" * 80)
print("TOP 5 RESULTS - CIPHER 3")
print("=" * 80)

results_c3.sort(key=lambda x: x[1], reverse=True)
for i, (name, score, text, stats) in enumerate(results_c3[:5], 1):
    print(f"\n#{i}. {name}")
    print(f"Score: {score:.1f}")
    print(f"Stats: {stats}")
    print(f"Text (first 150 chars): {text[:150]}")

print("\n" + "=" * 80)
print("FINAL VERDICT")
print("=" * 80)

best_c1_score = results_c1[0][1] if results_c1 else -10000
best_c3_score = results_c3[0][1] if results_c3 else -10000

if best_c1_score > 1000 or best_c3_score > 1000:
    print("\n🎉 SUCCESS! One or more ciphers may be solved!")
else:
    print(f"\n❌ No solution found.")
    print(f"Best C1 score: {best_c1_score:.1f} from {results_c1[0][0]}")
    print(f"Best C3 score: {best_c3_score:.1f} from {results_c3[0][0]}")
    print("\nThis supports the hoax theory - ciphers may be unsolvable.")

print("\n" + "=" * 80)
