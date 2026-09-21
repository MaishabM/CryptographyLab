SBOX = [
    0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
    0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
    0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
    0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
    0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
    0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
    0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
    0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
    0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16
]

RCON = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]


def hex_to_bytes(text):
    data = []
    index = 0

    while index < len(text):
        value = text[index] + text[index + 1]
        data.append(int(value, 16))
        index = index + 2

    return data


def bytes_to_hex(data):
    result = ""
    index = 0

    while index < len(data):
        value = data[index]
        result = result + format(value, "02X")
        index = index + 1

    return result


def print_state(state):
    row = 0

    while row < 4:
        print(
            format(state[row][0], "02X"),
            format(state[row][1], "02X"),
            format(state[row][2], "02X"),
            format(state[row][3], "02X")
        )
        row = row + 1

    print()


def make_state(data):
    state = [[0 for i in range(4)] for j in range(4)]

    column = 0

    while column < 4:
        row = 0

        while row < 4:
            state[row][column] = data[row + (column * 4)]
            row = row + 1

        column = column + 1

    return state


def state_to_bytes(state):
    data = []

    column = 0

    while column < 4:
        row = 0

        while row < 4:
            data.append(state[row][column])
            row = row + 1

        column = column + 1

    return data


def xtime(value):
    temp = value << 1

    if value >= 128:
        temp = temp ^ 0x1B

    return temp & 0xFF


def gf_mul(a, b):
    result = 0

    while b > 0:

        if b & 1:
            result = result ^ a

        a = xtime(a)
        b = b >> 1

    return result


def sub_bytes(state):
    row = 0

    while row < 4:
        column = 0

        while column < 4:
            state[row][column] = SBOX[state[row][column]]
            column = column + 1

        row = row + 1

    return state


def shift_rows(state):
    row = 1

    while row < 4:

        temp = [0, 0, 0, 0]

        column = 0

        while column < 4:
            temp[column] = state[row][(column + row) % 4]
            column = column + 1

        state[row] = temp

        row = row + 1

    return state


def mix_columns(state):
    column = 0

    while column < 4:

        a0 = state[0][column]
        a1 = state[1][column]
        a2 = state[2][column]
        a3 = state[3][column]

        b0 = gf_mul(2, a0) ^ gf_mul(3, a1) ^ a2 ^ a3
        b1 = a0 ^ gf_mul(2, a1) ^ gf_mul(3, a2) ^ a3
        b2 = a0 ^ a1 ^ gf_mul(2, a2) ^ gf_mul(3, a3)
        b3 = gf_mul(3, a0) ^ a1 ^ a2 ^ gf_mul(2, a3)

        state[0][column] = b0
        state[1][column] = b1
        state[2][column] = b2
        state[3][column] = b3

        column = column + 1

    return state


def add_round_key(state, key_state):
    row = 0

    while row < 4:

        column = 0

        while column < 4:
            state[row][column] = state[row][column] ^ key_state[row][column]
            column = column + 1

        row = row + 1

    return state


def rot_word(word):
    result = [0, 0, 0, 0]

    result[0] = word[1]
    result[1] = word[2]
    result[2] = word[3]
    result[3] = word[0]

    return result


def sub_word(word):
    result = [0, 0, 0, 0]

    index = 0

    while index < 4:
        result[index] = SBOX[word[index]]
        index = index + 1

    return result


def key_expansion(key):
    words = []

    index = 0

    while index < 4:

        words.append([
            key[index * 4],
            key[index * 4 + 1],
            key[index * 4 + 2],
            key[index * 4 + 3]
        ])

        index = index + 1

    index = 4

    while index < 44:

        temp = list(words[index - 1])

        if index % 4 == 0:

            temp = rot_word(temp)
            temp = sub_word(temp)

            temp[0] = temp[0] ^ RCON[index // 4]

        new_word = [0, 0, 0, 0]

        j = 0

        while j < 4:
            new_word[j] = words[index - 4][j] ^ temp[j]
            j = j + 1

        words.append(new_word)

        index = index + 1

    return words


def round_keys_from_words(words):
    keys = []

    round_index = 0

    while round_index < 11:

        key_bytes = []

        word_index = 0

        while word_index < 4:

            byte_index = 0

            while byte_index < 4:
                key_bytes.append(
                    words[round_index * 4 + word_index][byte_index]
                )

                byte_index = byte_index + 1

            word_index = word_index + 1

        keys.append(make_state(key_bytes))

        round_index = round_index + 1

    return keys


plain_text = input(
    "Enter the 128 bit or 32 hexadecimal digits plaintext: "
).strip()

key_text = input(
    "Enter the 128 bit or 32 hexadecimal digits key: "
).strip()

if len(plain_text) != 32 or len(key_text) != 32:
    print("Error: plaintext and key must contain exactly 32 hexadecimal digits.")
    exit()

plain_bytes = hex_to_bytes(plain_text)
key_bytes = hex_to_bytes(key_text)

words = key_expansion(key_bytes)

round_keys = round_keys_from_words(words)

state = make_state(plain_bytes)

print("Initial State")
print_state(state)

state = add_round_key(state, round_keys[0])

print("After Initial AddRoundKey")
print_state(state)


round_number = 1

while round_number <= 9:

    print("Round", round_number)

    state = sub_bytes(state)

    print("After SubBytes")
    print_state(state)

    state = shift_rows(state)

    print("After ShiftRows")
    print_state(state)

    state = mix_columns(state)

    print("After MixColumns")
    print_state(state)

    state = add_round_key(state, round_keys[round_number])

    print("After AddRoundKey")
    print_state(state)

    round_number = round_number + 1


print("Final Round")

state = sub_bytes(state)

print("After SubBytes")
print_state(state)

state = shift_rows(state)

print("After ShiftRows")
print_state(state)

state = add_round_key(state, round_keys[10])

print("After AddRoundKey")
print_state(state)


cipher_bytes = state_to_bytes(state)

cipher_text = bytes_to_hex(cipher_bytes)

print("Ciphertext:", cipher_text)