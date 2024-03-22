pip install libsnark

from snark import *
from snark.gadgetlib.protoboard import Protoboard
from snark.gadgetlib.gadgets.basic_gadgets import *
from snark.gadgetlib.gadgets.verifiers import *
from snark.gadgetlib.gadgets.pairing import *
from snark.gadgetlib.gadgets.verifiers import PairingVerifierGadget

# Define a simple polynomial function y = ax^2 + bx + c
class PolyFunctionGadget(Gadget):
    def __init__(self, protoboard, a, b, c):
        self.a = a
        self.b = b
        self.c = c

        self.x = protoboard.val("x")
        self.y = protoboard.val("y")

        self.constraint_system.add_r1cs_constraint(R1CSConstraint(self.a * self.x**2 + self.b * self.x + self.c == self.y))

# Define a verifier for the polynomial function
class PolyFunctionVerifier(PairingVerifierGadget):
    def __init__(self, protoboard):
        PairingVerifierGadget.__init__(self, protoboard)

        self.a = protoboard.val("a")
        self.b = protoboard.val("b")
        self.c = protoboard.val("c")

        self.x = protoboard.val("x")
        self.y = protoboard.val("y")

        self.g1 = protoboard.val("g1")
        self.g2 = protoboard.val("g2")

        self.h1 = protoboard.val("h1")
        self.h2 = protoboard.val("h2")

        self.constraint_system.add_r1cs_constraint(R1CSConstraint(self.g1 * self.a == self.h1))
        self.constraint_system.add_r1cs_constraint(R1CSConstraint(self.g2 * self.b == self.h2))
        self.constraint_system.add_r1cs_constraint(R1CSConstraint(self.h1 * self.x**2 + self.h2 * self.x + self.g2 == self.h2 * self.y))

# Create a protoboard and add the polynomial function and its verifier
pb = Protoboard(128)

a = pb.val(3)
b = pb.val(2)
c = pb.val(1)

x = pb.val(5)
y = pb.val()

poly_function = PolyFunctionGadget(pb, a, b, c)
poly_function.generate_r1cs_constraints()

poly_function_verifier = PolyFunctionVerifier(pb)
poly_function_verifier.generate_r1cs_constraints()

# Create a proving system and generate a proof
proving_system = ProvingSystem(pb)
proof = proving_system.prove()

# Create a verifier and verify the proof
verifier = Verifier(pb)
verifier.generate_r1cs_witness([a, b, c, x, y], proof)
verifier.verify()

print("Proof verified:", verifier.proof_verified)