def create_matrix(key):
    key = key.upper().replace("J", "I")
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

    chars = []
    for char in key + alphabet:
        if char in alphabet and char not in chars:
            chars.append(char)

    return [chars[i:i + 5] for i in range(0, 25, 5)]


def prepare_text(text):
    text = text.upper().replace("J", "I")
    text = ''.join(char for char in text if char.isalpha())

    pairs = []
    i = 0

    while i < len(text):
        a = text[i]

        if i + 1 >= len(text):
            pairs.append(a + "X")
            i += 1
        elif text[i] == text[i + 1]:
            pairs.append(a + "X")
            i += 1
        else:
            pairs.append(a + text[i + 1])
            i += 2

    return pairs


def find_position(matrix, char):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col


def encrypt_pair(pair, matrix):
    a, b = pair

    row1, col1 = find_position(matrix, a)
    row2, col2 = find_position(matrix, b)

    if row1 == row2:
        return matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]

    if col1 == col2:
        return matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]

    return matrix[row1][col2] + matrix[row2][col1]


plaintext = input("Enter plaintext: ")
key = input("Enter the key for playfair cipher: ").strip().upper()

matrix = create_matrix(key)
pairs = prepare_text(plaintext)

print("\nPlayfair Matrix:")
for row in matrix:
    print(" ".join(row))

print("\nPlaintext Pairs:")
print(" ".join(pairs))

ciphertext = ""

for pair in pairs:
    ciphertext += encrypt_pair(pair, matrix)

print("\nCiphertext:", ciphertext)