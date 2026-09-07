alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

plain = input('Enter the plain text: ').strip().lower()
con = int(input('Enter the constant for encryption: '))
p = ''
for ch in plain:
    i = alpha.index(ch)
    p += alpha[(i+con) % 26]
print('Encrypted text: ',p, '\n|\n|\n|\ntransmit\n|\n|\n|')

# choice = input('Would you like to decrypt the encrypted text? (y/n): ').lower()
# if choice == 'n':
#     exit
cipher = p.strip().lower()
c = ''
for ch in cipher:
    i = alpha.index(ch)
    c += alpha[(i-con) % 26]
print('Decrypted text: ',c)