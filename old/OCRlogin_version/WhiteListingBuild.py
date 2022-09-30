from Cryptodome.Cipher import DES
import binascii
key = b'jc7oe4f8'
des = DES.new(key,DES.MODE_ECB)
data=''
file = open('WhiteListing.txt','r')
data = file.read()
text = data
text = text + (8-(len(text)%8)) * '='
print(text)
print('\n')
e_text = des.encrypt(text.encode('utf-8'))
print(e_text)
print('\n')
e_text = binascii.b2a_hex(e_text)
print(e_text)
file = open('WhiteListing','wb')
file.write(e_text)
file.close()

file = open('WhiteListing','rb')
e_text = file.read()
file.close()
e_text = des.decrypt(binascii.a2b_hex(e_text))
e_text = e_text.decode('utf-8')
e_text = e_text[:e_text.find('=')]
WhiteListing = tuple(e_text.split(','))
print(WhiteListing)