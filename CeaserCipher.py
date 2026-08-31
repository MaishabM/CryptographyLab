alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

choice = int(input('Enter 1 for plain text and 2 for cipher text: '))
if choice == 1:
    plain = input('Enter the plain text: ').strip().lower()
    con = int(input('Enter the constant for encryption: '))
    
    p = ''
    for ch in plain:
        i = alpha.index(ch)
        p += alpha[(i+con) % 26]

    print('Encrypted text: ',p)
else:
    cipher = input('Enter the cipher text: ').strip().lower()
    con = int(input('Enter the constant for decryption: '))
    c = ''
    for ch in cipher:
        i = alpha.index(ch)
        c += alpha[(i-con) % 26]
    
    print('Decrypted text: ',c)