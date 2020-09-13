"""CPU functionality."""

import sys

# Operation Codes
# OP Codes
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = 256 * [0]
        self.reg = 8 * [0]
        self.pc = 0
        self.running = True
        self.branchtable = {
            LDI: self.call_LDI,
            PRN: self.call_PRN,
            HLT: self.call_HLT,
            MUL: self.call_MUL,
            PUSH: self.call_PUSH,
            POP: self.call_POP,
        }
        self.sp = 7
        self.reg[self.sp] = len(self.ram)

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""
        if len(sys.argv) != 2:
            print("Usage: example_cpu.py filename")
            sys.exit(1)

        address = 0
        file = sys.argv[1]

        try:
            with open(file) as f:
                for line in f:
                    split_line = line.split("#")

                    code_value = split_line[0].strip() 
                    if code_value == "":
                        continue

                    num = int(code_value, 2)
                    self.ram[address] = num
                    address += 1

        except FileNotFoundError: 
            print(f"{sys.argv[1]} file not found")
            sys.exit(2)

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def call_LDI(self):
        # address
        operand_a = self.ram_read(self.pc + 1)
        # value
        operand_b = self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b
        self.pc += 3

    def call_PRN(self):
        # address
        operand_a = self.ram_read(self.pc + 1)
        self.pc += 2
        print(self.reg[operand_a])
    
    def call_MUL(self):
        # first register
        operand_a = self.ram_read(self.pc + 1)
        # second register
        operand_b = self.ram_read(self.pc + 2)
        self.pc += 3
        self.alu("MUL", operand_a, operand_b)

    def call_HLT(self):
        self.running = False

    def call_PUSH(self):
        given_register = self.ram[self.pc + 1]
        value_in_register = self.reg[given_register]
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = value_in_register
        self.pc += 2

    def call_POP(self):
        given_register = self.ram[self.pc + 1]
        value_from_ram = self.ram[self.reg[self.sp]]
        self.reg[given_register] = value_from_ram
        self.reg[self.sp] += 1
        self.pc += 2


    def run(self):
        """Run the CPU."""
        while self.running:
            instruction = self.ram[self.pc]

            if instruction in self.branchtable:
                self.branchtable[instruction]()
            else:
                sys.exit(1)