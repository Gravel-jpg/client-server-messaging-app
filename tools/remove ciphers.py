# two simple functions can be used to convert text into an integer and visce versa. this saves the cipher and will likely cut down on time and improve simplicity.

import math
text = 'hello! my world.'
byte = text.encode()
integer = int.from_bytes(byte)
print(f'int: {integer}')
length = math.ceil(integer.bit_length() / 8)
text2 = integer.to_bytes(length).decode()
print(f'text:{text2}')
# https://stackoverflow.com/questions/69801359/python-how-to-convert-a-string-to-an-integer-for-rsa-encryption
