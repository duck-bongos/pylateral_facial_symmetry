__symmetry_map = {}

# lower face outline
__symmetry_map[1] = 17
__symmetry_map[2] = 16
__symmetry_map[3] = 15
__symmetry_map[4] = 14
__symmetry_map[5] = 13
__symmetry_map[6] = 12
__symmetry_map[7] = 11
__symmetry_map[8] = 10
__symmetry_map[9] = 9

# eyebrows
diff = 0
for i in range(18, 23):
    __symmetry_map[i] = i + 9 + diff
    diff -= 2

# eyes
__symmetry_map[37] = 46
__symmetry_map[38] = 45
__symmetry_map[39] = 44
__symmetry_map[40] = 43
__symmetry_map[41] = 48
__symmetry_map[42] = 47

# nose
__symmetry_map[32] = 36
__symmetry_map[33] = 35
__symmetry_map[28] = 28
__symmetry_map[29] = 29
__symmetry_map[30] = 30
__symmetry_map[31] = 31
__symmetry_map[34] = 34

# mouth
__symmetry_map[49] = 55
__symmetry_map[50] = 54
__symmetry_map[51] = 53
__symmetry_map[52] = 52
__symmetry_map[61] = 65
__symmetry_map[62] = 64
__symmetry_map[63] = 63
__symmetry_map[68] = 66
__symmetry_map[60] = 56
__symmetry_map[59] = 57
__symmetry_map[67] = 67
__symmetry_map[58] = 58

__bilateral_map = {
    28: 29,
    29: 30,
    30: 31,
    31: 34,
    34: 52,
    52: 63,
    63: 67,
    67: 58,
    58: 9,
}

__half_face_left = {
    18: 28,
    19: 28,
    20: 28,
    21: 28,
    22: 28,
    37: 28,
    38: 28,
    39: 28,
    40: 28,
    41: 28,
    42: 28,
    1: 29,
    2: 30,
    3: 34,
    4: 52,
    5: 58,
    6: 58,
    7: 9,
    8: 9,
    51: 52,
    50: 63,
    49: 63,
    62: 63,
    61: 67,
    60: 67,
    68: 67,
    59: 58,
}

__outline_half_face_left = {
    18: 19,
    19: 20,
    20: 21,
    21: 22,
    22: 28,
    28: 29,
    29: 30,
    30: 31,
    31: 34,
    34: 52,
    52: 63,
    63: 67,
    67: 58,
    58: 9,
    9: 8,
    8: 7,
    7: 6,
    6: 5,
    5: 4,
    4: 3,
    3: 2,
    2: 1,
    1: 18,
}

__outline_half_face_right = {
    23: 24,
    24: 25,
    25: 26,
    26: 27,
    27: 17,
    17: 16,
    16: 15,
    15: 14,
    14: 13,
    13: 12,
    12: 11,
    11: 10,
    10: 9,
    9: 58,
    58: 67,
    67: 63,
    63: 52,
    52: 34,
    34: 31,
    31: 30,
    30: 29,
    29: 28,
    28: 23,
}

LEFT_HALF_OUTLINE_LANDMARKS = [
    28,
    29,
    30,
    31,
    34,
    52,
    63,
    67,
    58,
    9,
    8,
    7,
    6,
    5,
    4,
    3,
    2,
    1,
    18,
    19,
    20,
    21,
    22,
]

# exportable
SYMMETRY_MAP = __symmetry_map
BILATERAL_MAP = __bilateral_map
HALF_FACE_LEFT = __half_face_left
OUTLINE_HALF_FACE_LEFT = __outline_half_face_left
OUTLINE_HALF_FACE_RIGHT = __outline_half_face_right
