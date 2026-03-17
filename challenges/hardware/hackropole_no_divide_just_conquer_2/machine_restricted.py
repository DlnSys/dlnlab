from machine import Machine
from crypto_accelerator import Fp_machine

class RestrictedMachine(Machine):
    def __init__(self, code, e = 0, N = 0):
        super().__init__(code, e, N)
        self.counter = 0

    def executeInstruction(self):
        if self.counter > 100:
            print("counter too big")
            self.error = True
        if not self.error:
            super().executeInstruction()

    def shiftL(self):
        super().shiftL()
        self.counter += 1

    def shiftR(self):
        super().shiftR()
        self.counter += 1

    def add(self):
        super().add()
        self.counter += 1

    def sub(self):
        super().sub()
        self.counter += 1

    def div(self):
        self.error = True

    def invert(self):
        self.error = True

    def gcd(self):
        self.error = True

class SuperRestrictedMachine(RestrictedMachine):

    def pow(self):
        self.error = True

    def mul(self):
        self.error = True

    def mod(self):
        self.error = True

    def init_FP_accelerator(self):
        if self.b > 1021:
            self.error = True
        else:
            super().init_FP_accelerator()

    def init_FP_accelerator_withRR(self):
        if self.b > 1021:
            self.error = True
        else:
            super().init_FP_accelerator_withRR()
