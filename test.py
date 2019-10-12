bit_sequence = '1000000000'
bytes = int(bit_sequence, 2).to_bytes((len(bit_sequence) + 7) // 8, byteorder='little')
print(bytes)