import os

class Hash:
    def __init__(self):
        l = []
        for i in range(256):
            while True:
                x = os.urandom(1)[0]
                if x not in l:
                    l.append(x)
                    break
        self.lookup = l

    def hash_single(self, buf):
        h = 0
        for byte in buf:
            h = self.lookup[h ^ int(byte)]
        return h


hash = Hash()
x = bin(hash.hash_single(b"0110 1111 0100 1100"))[2:]
print(x)
