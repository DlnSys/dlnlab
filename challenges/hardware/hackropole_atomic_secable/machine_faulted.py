from machine import Machine, maxBitSize
from random import randrange

class FaultedMachine(Machine):

    def __init__(self, code, list_faults = []):
        super().__init__(code)
        self.list_faults = list_faults

    def finalize_move(self):
        if self.nbInstruction in self.list_faults:
            self.a = randrange(1 << maxBitSize)
        super().finalize_move()
