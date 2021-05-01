def xor(data, key): 
    return bytearray(a^b for a, b in zip(*map(bytearray, [data, key]))) 