
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0xfc19dc6f, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]


def Rotateright(x,n):
    return (x >> n) | (x << (32-n))

def Ch(x,y,z):
    return (x & y) ^ (~x & z)

def Maj(x,y,z):
    return (x & y) ^ (x & z) ^ (y & z)

def Sigma0(x):
    return Rotateright(x,2) ^ Rotateright(x,13) ^ Rotateright(x,22)

def Sigma1(x):
    return Rotateright(x,6) ^ Rotateright(x,11) ^ Rotateright(x,25)

def sigma0(x):
    return Rotateright(x,7) ^ Rotateright(x,18) ^ (x >> 3)

def sigma1(x):
    return Rotateright(x,17) ^ Rotateright(x,19) ^ (x >> 10)

def SHA256(message):
    
    message += b'\x80'
    
    message += b'\x00' * ((56 - (len(message) % 64)) % 64)
   
    message += (len(message) * 8).to_bytes(8, byteorder='big')

    
    for i in range(0, len(message), 64):
        w = [0] * 64
        for j in range(16):
            w[j] = int.from_bytes(message[i + j * 4:i + j * 4 + 4], byteorder='big')

        for j in range(16, 64):
            w[j] = (sigma1(w[j - 2]) + w[j - 7] + sigma0(w[j - 15]) + w[j - 16]) & 0xffffffff

        a = 0x6a09e667
        b = 0xbb67ae85
        c = 0x3c6ef372
        d = 0xa54ff53a
        e = 0x510e527f
        f = 0x9b05688c
        g = 0x1f83d9ab
        h = 0x5be0cd19

        
        for i in range(64):
            S1 = Sigma1(e)
            ch = Ch(e, f, g)
            temp1 = (h + S1 + ch + K[i] + w[i]) & 0xffffffff
            S0 = Sigma0(a)
            maj = Maj(a, b, c)
            temp2 = (S0 + maj) & 0xffffffff

            h = g
            g = f
            f = e
            e = (d + temp1) & 0xffffffff
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xffffffff

        a = (a + 0x6a09e667) & 0xffffffff
        b = (b + 0xbb67ae85) & 0xffffffff
        c = (c + 0x3c6ef372) & 0xffffffff
        d = (d + 0xa54ff53a) & 0xffffffff
        e = (e + 0x510e527f) & 0xffffffff
        f = (f + 0x9b05688c) & 0xffffffff
        g = (g + 0x1f83d9ab) & 0xffffffff
        h = (h + 0x5be0cd19) & 0xffffffff
    return '%08x%08x%08x%08x%08x%08x%08x%08x' % (a, b, c, d, e, f, g, h)





