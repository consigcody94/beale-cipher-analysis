#!/usr/bin/env python3
"""
Historical Context-Based Beale Cipher Attack
Based on what Thomas Beale would have ACTUALLY had access to in 1820s Virginia
"""

import re
import requests
from typing import List, Dict, Tuple

CIPHER_1 = [71, 194, 38, 1701, 89, 76, 11, 83, 1629, 48, 94, 63, 132, 16, 111, 95, 84, 341, 975, 14, 40, 64, 27, 81, 139, 213, 63, 90, 1120, 8, 15, 3, 126, 2018, 40, 74, 758, 485, 604, 230, 436, 664, 582, 150, 251, 284, 308, 231, 124, 211, 486, 225, 401, 370, 11, 101, 305, 139, 189, 17, 33, 88, 208, 193, 145, 1, 94, 73, 416, 918, 263, 28, 500, 538, 356, 117, 136, 219, 27, 176, 130, 10, 460, 25, 485, 18, 436, 65, 84, 200, 283, 118, 320, 138, 36, 416, 280, 15, 71, 224, 961, 44, 16, 401, 39, 88, 61, 304, 12, 21, 24, 283, 134, 92, 63, 246, 486, 682, 7, 219, 184, 360, 780, 18, 64, 463, 474, 131, 160, 79, 73, 440, 95, 18, 64, 581, 34, 69, 128, 367, 460, 17, 81, 12, 103, 820, 62, 116, 97, 103, 862, 70, 60, 1317, 471, 540, 208, 121, 890, 346, 36, 150, 59, 568, 614, 13, 120, 63, 219, 812, 2160, 1780, 99, 35, 18, 21, 136, 872, 15, 28, 170, 88, 4, 30, 44, 112, 18, 147, 436, 195, 320, 37, 122, 113, 6, 140, 8, 120, 305, 42, 58, 461, 44, 106, 301, 13, 408, 680, 93, 86, 116, 530, 82, 568, 9, 102, 38, 416, 89, 71, 216, 728, 965, 818, 2, 38, 121, 195, 14, 326, 148, 234, 18, 55, 131, 234, 361, 824, 5, 81, 623, 48, 961, 19, 26, 33, 10, 1101, 365, 92, 88, 181, 275, 346, 201, 206, 86, 36, 219, 324, 829, 840, 64, 326, 19, 48, 122, 85, 216, 284, 919, 861, 326, 985, 233, 64, 68, 232, 431, 960, 50, 29, 81, 216, 321, 603, 14, 612, 81, 360, 36, 51, 62, 194, 78, 60, 200, 314, 676, 112, 4, 28, 18, 61, 136, 247, 819, 921, 1060, 464, 895, 10, 6, 66, 119, 38, 41, 49, 602, 423, 962, 302, 294, 875, 78, 14, 23, 111, 109, 62, 31, 501, 823, 216, 280, 34, 24, 150, 1000, 162, 286, 19, 21, 17, 340, 19, 242, 31, 86, 234, 140, 607, 115, 33, 191, 67, 104, 86, 52, 88, 16, 80, 121, 67, 95, 122, 216, 548, 96, 11, 201, 77, 364, 218, 65, 667, 890, 236, 154, 211, 10, 98, 34, 119, 56, 216, 119, 71, 218, 1164, 1496, 1817, 51, 39, 210, 36, 3, 19, 540, 232, 22, 141, 617, 84, 290, 80, 46, 207, 411, 150, 29, 38, 46, 172, 85, 194, 39, 261, 543, 897, 624, 18, 212, 416, 127, 931, 19, 4, 63, 96, 12, 101, 418, 16, 140, 230, 460, 538, 19, 27, 88, 612, 1431, 90, 716, 275, 74, 83, 11, 426, 89, 72, 84, 1300, 1706, 814, 221, 132, 40, 102, 34, 868, 975, 1101, 84, 16, 79, 23, 16, 81, 122, 324, 403, 912, 227, 936, 447, 55, 86, 34, 43, 212, 107, 96, 314, 264, 1065, 323, 428, 601, 203, 124, 95, 216, 814, 2906, 654, 820, 2, 301, 112, 176, 213, 71, 87, 96, 202, 35, 10, 2, 41, 17, 84, 221, 736, 820, 214, 11, 60, 760]


def decode_simple(cipher: List[int], key_text: str) -> Tuple[str, float]:
    """Quick decode and score."""
    words = re.findall(r'\b[a-zA-Z]+\b', key_text.lower())
    if not words:
        return "", -10000

    # Extend words if needed
    max_num = max(cipher)
    if len(words) < max_num:
        words = words * (max_num // len(words) + 2)

    decoded = []
    errors = 0
    for num in cipher:
        if num == 0 or num > len(words):
            decoded.append('?')
            errors += 1
        else:
            decoded.append(words[num - 1][0])

    text = ''.join(decoded)
    error_rate = errors / len(cipher)

    # Quick score
    vowels = sum(1 for c in text if c in 'aeiou')
    alpha = sum(1 for c in text if c.isalpha())
    vowel_rate = vowels / alpha if alpha > 0 else 0

    score = 0
    score -= error_rate * 1000
    if 0.35 < vowel_rate < 0.45:
        score += 200
    else:
        score -= abs(vowel_rate - 0.40) * 500

    # Common words
    score += text.count('the') * 50
    score += text.count('and') * 30
    score += text.count('of') * 30

    return text, score


# HISTORICAL CONTEXT: What would a Virginia gentleman in 1820s have?
print("=" * 80)
print("HISTORICAL CONTEXT-BASED ATTACK")
print("=" * 80)
print("""
Thomas J. Beale - 1820s Virginia Gentleman Adventurer
What documents would he have had access to?

1. GOVERNMENT DOCUMENTS (Most Likely):
   - Declaration of Independence (CONFIRMED - used for Cipher 2)
   - Articles of Confederation
   - U.S. Constitution
   - Virginia Declaration of Rights
   - Patrick Henry speeches

2. MILITARY/FRONTIER DOCUMENTS (He was supposedly a frontiersman):
   - Lewis and Clark Expedition journals
   - Military correspondence from War of 1812
   - Zebulon Pike's expedition reports (Southwest exploration)
   - Monroe Doctrine

3. POPULAR BOOKS IN 1820s VIRGINIA:
   - The Bible (KJV - most common book)
   - Common almanacs (Poor Richard's, Virginia Almanac)
   - Shakespeare
   - British novels (Scott, Richardson)
   - Washington Irving (The Sketch Book, 1819)

4. VIRGINIA-SPECIFIC:
   - Virginia Gazette (newspaper)
   - Land grant documents
   - Legal documents
   - Thomas Jefferson's writings
   - "Letters from a Farmer" by John Dickinson

5. CONSIDERING THE TREASURE STORY:
   - Documents related to Spanish territories (treasure from "north of New Mexico")
   - Mining or exploration texts
   - Maps and surveys

KEY INSIGHT: Beale used the Declaration of Independence for Cipher 2.
This suggests he preferred GOVERNMENT/PATRIOTIC documents that would:
- Be well-known and accessible
- Be preserved over time
- Be available to the treasure recipients

MOST LIKELY CANDIDATES FOR CIPHERS 1 & 3:
1. Articles of Confederation (predecessor to Constitution)
2. Virginia Declaration of Rights (George Mason)
3. Patrick Henry's "Liberty or Death" speech
4. Washington's Farewell Address
5. Monroe Doctrine
6. Virginia Statute for Religious Freedom (Jefferson)
""")

# Specific texts to test
TARGETED_TEXTS = {
    'Articles_of_Confederation': 'https://www.gutenberg.org/files/5/5-0.txt',  # Often bundled with Constitution
    'Patrick_Henry_Speeches': None,  # Need to find
    'Washington_Farewell': 'https://www.gutenberg.org/files/109/109-0.txt',
    'Virginia_Statute_Religious_Freedom': None,  # Jefferson's work
    'Lewis_and_Clark_Journals': 'https://www.gutenberg.org/files/8419/8419-0.txt',
    'Monroe_Doctrine': None,  # 1823 - right time period!
    'Jefferson_Writings': 'https://www.gutenberg.org/files/16783/16783-0.txt',
    'Virginia_Declaration_Rights': None,  # George Mason 1776
}

print("\n" + "=" * 80)
print("TESTING THEORY: Different Virginia/Government documents for each cipher")
print("=" * 80)
print("""
HYPOTHESIS: If Beale used Declaration of Independence for Cipher 2 (contents),
he might have used related but different founding documents for:
- Cipher 1 (location): Could use Articles of Confederation or Virginia document
- Cipher 3 (names): Could use another Virginia/founding document

WHY THIS MAKES SENSE:
- Using different keys prevents someone from decrypting all three at once
- All documents would be available to the intended recipients
- All would be preserved by U.S. government
- Shows a consistent pattern (American founding documents)
""")

print("\nTESTING DIFFERENT EDITIONS OF DECLARATION OF INDEPENDENCE...")
print("(Cipher 2 was solved with DOI, maybe Cipher 1/3 use different editions?)")

# Different DOI versions to test
doi_variations = [
    "When in the course of human events",  # Standard opening
    "In Congress July 4 1776",  # Official version opening
]

print("\nAlso note: The highest number in Cipher 1 is 2906")
print("This means the key document needs AT LEAST 2906 words!")
print("Declaration of Independence only has ~1,320 words")
print("So Cipher 1 CANNOT use DOI alone - must be a longer document!")

print("\n" + "=" * 80)
print("CRITICAL FINDING: Document Length Requirements")
print("=" * 80)

max_c1 = max(CIPHER_1)
print(f"Cipher 1 max number: {max_c1} - needs document with 2906+ words")
print(f"Cipher 3 max number: {max(CIPHER_3)} - needs document with 975+ words")

print("""
This eliminates many candidates:
❌ Declaration of Independence (~1,320 words) - too short for Cipher 1
❌ Monroe Doctrine (~2,300 words) - possibly too short
❌ Washington's Farewell (~6,000 words) - could work!
❌ Virginia Declaration of Rights (~600 words) - too short for Cipher 1
✅ U.S. Constitution + Amendments (~7,500 words) - long enough!
✅ Articles of Confederation (~3,000 words) - long enough!
✅ Long books (Bible, Shakespeare, etc.) - definitely long enough

MOST PROMISING:
1. U.S. Constitution with all amendments
2. Articles of Confederation + Resolutions
3. Washington's Farewell Address
4. Complete Bible
5. Lewis & Clark Journals (expedition reports would interest a frontiersman!)
""")

print("\n" + "=" * 80)
print("NEXT STEPS")
print("=" * 80)
print("""
1. Test complete U.S. founding documents collections
2. Test different orderings/editions of DOI
3. Test Lewis & Clark journals (Beale was allegedly a frontiersman/explorer)
4. Test combinations of documents
5. Try reverse-engineering: if word #18 should start with 'e',
   what documents have the right word at position 18?
""")

print("\nRun the main brute_force script to test all available documents!")
print("Looking for documents downloaded in background...")

import subprocess
import time

print("\nWaiting for background brute force to complete...")
time.sleep(5)
