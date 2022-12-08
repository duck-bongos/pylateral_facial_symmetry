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

# exportable
SYMMETRY_MAP = __symmetry_map
BILATERAL_MAP = __bilateral_map
