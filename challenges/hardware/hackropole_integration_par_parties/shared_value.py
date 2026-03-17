from Crypto.Random.random import randrange

#Class to share (secret) values, and
#securely perform computations without leaking information if at most 'order'
#values are observed.
class SharedValue:
    #Initialize a new object for a given bit size and desired security order.
    #Optionally give input shares
    def __init__(self, bit_size, order, shares = None):
        self.order = order
        self.value = []
        self.bit_size = bit_size
        if shares != None:
            if len(shares) == order+1:
                self.value = shares.copy()
            #else:
                #raise error
        else:
            self.value = [0]*(order+1)

    #set SharedValue to 0
    def reset(self):
        self.value = [0]*(self.order+1)

    #set SharedValue to input value
    def set(self, value):
        self.value = [0]*self.order
        self.value.append(value)

    #set SharedValue to random value
    def randomize(self):
        for i in range(self.order + 1):
            self.value[i] = randrange(1 << self.bit_size)

    #randomize the representation of SharedValue
    def refresh(self):
        for i in range(self.order):
            for j in range(i+1, self.order + 1):
                t = randrange(1 << self.bit_size)
                self.value[i] ^= t
                self.value[j] ^= t

    #Overload xor operator to compute the xor of two SharedValue objects
    def __xor__(self, other):
        shares = []
        for i in range(self.order + 1):
            shares.append(self.value[i] ^ other.value[i])
        return SharedValue(self.bit_size, self.order, shares)

    #Overload and operator to compute the and of two SharedValue objects
    def __and__(self, other):
        shares = []
        for i in range(self.order + 1):
            shares.append(self.value[i] & other.value[i])
        for i in range(self.order):
            for j in range(i + 1, self.order + 1):
                t = randrange(1 << self.bit_size)
                shares[i] ^= t ^ (self.value[i] & other.value[j])
                shares[j] ^= t ^ (self.value[j] & other.value[i])
        return SharedValue(self.bit_size, self.order, shares)

    #Export a SharedValue objects
    def export(self):
        return self.value.copy()

#Basic tests of the class and its methods
if __name__ ==  "__main__":
    order = 32
    bit_size = 128
    key = SharedValue(bit_size, order)
    key.reset()
    key.randomize()
    key.refresh()

    message = 0xFFEEDDCCBBAA99887766554433221100
    msg = SharedValue(bit_size, order)
    msg.set(message)

    x = msg ^ key
    a = msg & key
    print(x.export())
