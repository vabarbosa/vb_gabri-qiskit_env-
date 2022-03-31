import qiskit
from qiskit import QuantumCircuit
from qiskit.providers.aer import AerSimulator
qiskit.__version__

qc = QuantumCircuit(3, 3)
qc.measure([0,1,2], [0,1,2])
qc.draw(output = "mpl")

#Create simulator, run experiment and get counts
sim = AerSimulator()
job = sim.run(qc)
result = job.result()
result.get_counts()

#First use of NOT-Gate
qc = QuantumCircuit(3, 3)
qc.x([0,2])
qc.measure([0,1,2], [1,0,2])
qc.draw(output = "mpl")
job = sim.run(qc)
result = job.result()
result.get_counts()

#First use of CNOT-Gate: (0,0) = 0, (0,1) = 1, (1, 0) = 1, (1, 1) = 0
qc = QuantumCircuit(2,2)
qc.x(0)
qc.cx(0,1)
qc.measure([0,1], [0,1])
display(qc.draw(output = "mpl"))

job = sim.run(qc)
result = job.result()
result.get_counts()

#Build quantum circuit: half-adder
qc = QuantumCircuit(4,2)
qc.x([])
qc.cx(0,2)
qc.cx(1,2)
qc.ccx(0,1,3)

qc.measure(2,0)
qc.measure(3,1)
qc.draw(output = "mpl")

job = sim.run(qc)
result = job.result()
result.get_counts()

################################################################################

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit import Aer

backend = Aer.get_backend("aer_simulator")

MESSAGE = "10"
qc_alice = QuantumCircuit(2, 2)

if MESSAGE[-1] == "1":
    qc_alice.x(1)
elif MESSAGE[-2] == "1":
    qc_alice.z(1)

qc_bob = QuantumCircuit(2,2)
qc_bob.cx(1, 0)
qc_bob.h(1)
qc_bob.measure([0,1], [0,1])

qc_charlie = QuantumCircuit(2,2)
qc_charlie.h(1)
qc_charlie.cx(1,0)

complete_qc = qc_charlie.compose(qc_alice.compose(qc_bob))
complete_qc.draw(output = "mpl")
backend.run(complete_qc).result().get_counts()

meas_x = QuantumCircuit(1,1)
meas_x.h(0)
meas_x.measure(0,0)

meas_x.draw()

meas_z = QuantumCircuit(1,1)
meas_z.measure(0,0)

meas_z.draw(output = "mpl")


qc = QuantumCircuit(1,1)
qc.draw()

backend.run(qc.compose(meas_z)).result().get_counts()
backend.run(qc.compose(meas_x)).result().get_counts()

from math import pi

qc = QuantumCircuit(1,1)
qc.ry(-pi/4, 0)

for circ in [meas_x, meas_z]:
    print(backend.run(qc.compose(circ)).result().get_counts())



qc_charlie = QuantumCircuit(2, 2)
qc_charlie.ry(1.911, 1)
qc_charlie.cx(1,0)
qc_charlie.ry(0.785, 0)
qc_charlie.cx(1,0)
qc_charlie.ry(2.356, 0)

qc_charlie.draw(output = "mpl")

meas_zz = QuantumCircuit(2, 2)
meas_zz.measure([0,1], [0,1])
from qiskit.visualization import plot_histogram
counts = backend.run(qc_charlie.compose(meas_zz)).result().get_counts()

plot_histogram(counts)

meas_zx = QuantumCircuit(2,2)
meas_zx.h(0)
meas_zx.measure([0,1], [0,1])
counts = backend.run(qc_charlie.compose(meas_zx)).result().get_counts()
plot_histogram(counts)

meas_xz = QuantumCircuit(2,2)
meas_xz.h(1)
meas_xz.measure([0,1], [0,1])

counts = backend.run(qc_charlie.compose(meas_xz)).result().get_counts()
plot_histogram(counts)

import random
def setup_variables():
    r = random.random()
    A = r*(2/3)
    B = r*(1/3)
    return A, B

def hash2bit(variable, hash_type):
    if hash_type == "V":
        bit = (variable < 0.5)
    elif hash_type == "H":
        bit = (variable < 0.25)

    bit = str(int(bit))

    return bit

shots = 8192
def calculate_P():
    P = {}
    for hashes in ["VV", "VH", "HV", "HH"]:

        P[hashes] = 0
        for shot in range(shots):
            A, B = setup_variables()
            a = hash2bit(A, hashes[0])
            b = hash2bit(B, hashes[1])

            P[hashes] += (a != b)/shots

    return P

P = calculate_P()
print(P)

%matplotlib inline
import matplotlib.pyplot as plt
plt.hist(P)
plt.show()
