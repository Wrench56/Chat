import rsa

pu, pr = rsa.newkeys(512)

text = 'Hello Worldfghfgh'

print(text.encode())
enc = rsa.encrypt(text.encode(), pu)


print(type(pu))
print(type(pr))
print(enc)

print('Decrypt: %s' % rsa.decrypt(enc, pr))