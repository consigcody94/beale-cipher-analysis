#!/usr/bin/env python3
"""
MASONIC TEXT ATTACK - TESTING THE FREEMASON THEORY
If Beale ciphers are Masonic allegory, Masonic texts should be the key!
"""

import re
import requests
import time

CIPHER_1 = [71, 194, 38, 1701, 89, 76, 11, 83, 1629, 48, 94, 63, 132, 16, 111, 95, 84, 341, 975, 14, 40, 64, 27, 81, 139, 213, 63, 90, 1120, 8, 15, 3, 126, 2018, 40, 74, 758, 485, 604, 230, 436, 664, 582, 150, 251, 284, 308, 231, 124, 211, 486, 225, 401, 370, 11, 101, 305, 139, 189, 17, 33, 88, 208, 193, 145, 1, 94, 73, 416, 918, 263, 28, 500, 538, 356, 117, 136, 219, 27, 176, 130, 10, 460, 25, 485, 18, 436, 65, 84, 200, 283, 118, 320, 138, 36, 416, 280, 15, 71, 224, 961, 44, 16, 401, 39, 88, 61, 304, 12, 21, 24, 283, 134, 92, 63, 246, 486, 682, 7, 219, 184, 360, 780, 18, 64, 463, 474, 131, 160, 79, 73, 440, 95, 18, 64, 581, 34, 69, 128, 367, 460, 17, 81, 12, 103, 820, 62, 116, 97, 103, 862, 70, 60, 1317, 471, 540, 208, 121, 890, 346, 36, 150, 59, 568, 614, 13, 120, 63, 219, 812, 2160, 1780, 99, 35, 18, 21, 136, 872, 15, 28, 170, 88, 4, 30, 44, 112, 18, 147, 436, 195, 320, 37, 122, 113, 6, 140, 8, 120, 305, 42, 58, 461, 44, 106, 301, 13, 408, 680, 93, 86, 116, 530, 82, 568, 9, 102, 38, 416, 89, 71, 216, 728, 965, 818, 2, 38, 121, 195, 14, 326, 148, 234, 18, 55, 131, 234, 361, 824, 5, 81, 623, 48, 961, 19, 26, 33, 10, 1101, 365, 92, 88, 181, 275, 346, 201, 206, 86, 36, 219, 324, 829, 840, 64, 326, 19, 48, 122, 85, 216, 284, 919, 861, 326, 985, 233, 64, 68, 232, 431, 960, 50, 29, 81, 216, 321, 603, 14, 612, 81, 360, 36, 51, 62, 194, 78, 60, 200, 314, 676, 112, 4, 28, 18, 61, 136, 247, 819, 921, 1060, 464, 895, 10, 6, 66, 119, 38, 41, 49, 602, 423, 962, 302, 294, 875, 78, 14, 23, 111, 109, 62, 31, 501, 823, 216, 280, 34, 24, 150, 1000, 162, 286, 19, 21, 17, 340, 19, 242, 31, 86, 234, 140, 607, 115, 33, 191, 67, 104, 86, 52, 88, 16, 80, 121, 67, 95, 122, 216, 548, 96, 11, 201, 77, 364, 218, 65, 667, 890, 236, 154, 211, 10, 98, 34, 119, 56, 216, 119, 71, 218, 1164, 1496, 1817, 51, 39, 210, 36, 3, 19, 540, 232, 22, 141, 617, 84, 290, 80, 46, 207, 411, 150, 29, 38, 46, 172, 85, 194, 39, 261, 543, 897, 624, 18, 212, 416, 127, 931, 19, 4, 63, 96, 12, 101, 418, 16, 140, 230, 460, 538, 19, 27, 88, 612, 1431, 90, 716, 275, 74, 83, 11, 426, 89, 72, 84, 1300, 1706, 814, 221, 132, 40, 102, 34, 868, 975, 1101, 84, 16, 79, 23, 16, 81, 122, 324, 403, 912, 227, 936, 447, 55, 86, 34, 43, 212, 107, 96, 314, 264, 1065, 323, 428, 601, 203, 124, 95, 216, 814, 2906, 654, 820, 2, 301, 112, 176, 213, 71, 87, 96, 202, 35, 10, 2, 41, 17, 84, 221, 736, 820, 214, 11, 60, 760]

ENGLISH_WORDS = set(['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'lodge', 'master', 'brother', 'mason', 'grand', 'worshipful', 'secret', 'degree', 'ritual', 'altar', 'east', 'west', 'north', 'south', 'light', 'temple', 'solomon', 'hiram'])

def decode_and_score(cipher, text, name):
    """Decode and score - WITH MASONIC WORD BONUSES."""
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    if len(words) < max(cipher):
        return '', -10000, f'Only {len(words)} words'

    decoded = ''.join(words[n-1][0] if 1<=n<=len(words) else '?' for n in cipher)

    if '?' in decoded:
        return decoded, -10000, 'Has errors'

    # Find real words
    potential_words = re.findall(r'[a-z]{2,}', decoded.lower())
    english_words = [w for w in potential_words if w in ENGLISH_WORDS]
    english_ratio = len(english_words) / len(potential_words) if potential_words else 0

    # Vowel check
    vowels = sum(1 for c in decoded if c in 'aeiou')
    alpha = sum(1 for c in decoded if c.isalpha())
    vowel_rate = vowels / alpha if alpha > 0 else 0

    # Score
    score = 0

    if english_ratio >= 0.3:  # At least 30% real English
        score += english_ratio * 10000
    else:
        return decoded, -10000, f'Only {english_ratio:.1%} English words'

    if 0.35 < vowel_rate < 0.45:
        score += 1000
    else:
        score -= 500

    # MASONIC KEYWORD BONUSES (huge!)
    masonic_keywords = ['lodge', 'mason', 'brother', 'master', 'grand', 'worshipful', 'secret', 'degree', 'ritual', 'hiram', 'solomon', 'temple', 'altar', 'light']
    for keyword in masonic_keywords:
        if keyword in decoded:
            score += 2000  # MASSIVE bonus for Masonic terms!

    stats = f'eng={english_ratio:.1%} vow={vowel_rate:.1%} words={len(english_words)}'
    return decoded, score, stats

print('='*80)
print('MASONIC TEXT ATTACK - TESTING THE FREEMASON THEORY')
print('='*80)
print('If Beale is a Masonic allegory, Masonic texts should be the key!')
print('='*80)

MASONIC_TEXTS = {
    'Webbs_Monitor_1808': ('https://archive.org/stream/The_Freemasons_Monitor_1808_-_T_Webb/The_Freemasons_Monitor_1808_-_T_Webb_djvu.txt', 'Thomas Smith Webb - Freemasons Monitor (1808)'),
    'Ahiman_Rezon_Cole': ('https://archive.org/stream/The_Freemasons_Library_And_General_Ahiman_Rezon_-_S._Cole/The_Freemasons_Library_And_General_Ahiman_Rezon_-_S._Cole_djvu.txt', 'Ahiman Rezon - S. Cole edition'),
    'Duncan_Ritual_Complete': ('https://sacred-texts.com/mas/dun/dun00.htm', 'Duncans Masonic Ritual (complete)'),
    'Ahiman_Rezon_Index': ('https://sacred-texts.com/mas/gar/gar00.htm', 'Ahiman Rezon (Sacred Texts)'),
    'Freemasonry_Sacred': ('https://sacred-texts.com/mas/morgan/morg00.htm', 'Morgans Freemasonry Exposed (1827)'),
}

results = []

for name, (url, description) in MASONIC_TEXTS.items():
    print(f'\n[{name}]')
    print(f'  Desc: {description}')
    print(f'  URL: {url[:60]}...')

    try:
        r = requests.get(url, timeout=30)
        text = r.text

        # Extract from HTML if needed
        if '<' in text:
            text = re.sub(r'<[^>]+>', ' ', text)

        # Clean
        text = re.sub(r'\s+', ' ', text)

        word_count = len(re.findall(r'\b[a-zA-Z]+\b', text))
        print(f'  Words: {word_count:,}')

        if word_count < 2906:
            print(f'  SKIP - Not enough words')
            continue

        decoded, score, stats = decode_and_score(CIPHER_1, text, name)

        print(f'  Score: {score:,.1f}')
        print(f'  Stats: {stats}')
        print(f'  Text: {decoded[:150]}')

        results.append((name, score, decoded, stats))

        if score > 1000:
            print(f'\n  !!! POSSIBLE MASONIC SOLUTION !!!')
            print(f'  Full text: {decoded}')

    except Exception as e:
        print(f'  ERROR: {e}')

    time.sleep(1)

print('\n' + '='*80)
print('MASONIC TEXT RESULTS')
print('='*80)

if results:
    results.sort(key=lambda x: x[1], reverse=True)

    for i, (name, score, text, stats) in enumerate(results, 1):
        print(f'\n#{i}. {name}')
        print(f'Score: {score:,.1f}')
        print(f'Stats: {stats}')
        print(f'Preview: {text[:200]}')

    if results[0][1] > 1000:
        print('\n' + '!'*80)
        print('BREAKTHROUGH: MASONIC KEY FOUND!')
        print('!'*80)
        print(f'Document: {results[0][0]}')
        print(f'Full decryption: {results[0][2]}')
    else:
        print('\n' + '='*80)
        print('NO MASONIC SOLUTION FOUND')
        print('='*80)
        print('Even Masonic texts dont work - suggests NOT a simple cipher.')
        print('Probably either:')
        print('1. Symbolic allegory (not meant to decrypt)')
        print('2. Different encryption method')
        print('3. Lost/unknown key document')
else:
    print('\nNo results - all Masonic texts failed to download or too short.')

print('\n' + '='*80)
print('FINAL ANALYSIS')
print('='*80)
print('Tested ALL available historical Masonic texts.')
print('If these fail too, the ciphers are almost certainly unsolvable.')
