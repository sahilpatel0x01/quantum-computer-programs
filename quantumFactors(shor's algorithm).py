import cirq
import numpy as np
from math import gcd


def make_shors_circuit(N):
    """Creates a quantum circuit for Shor's algorithm to factorize N."""
    # Create qubits for the control and target registers
    qubits = cirq.LineQubit.range(6)  # 3 qubits for the control register, 3 for the target
    circuit = cirq.Circuit()

    # Step 1: Apply Hadamard gates to the control qubits (put them in superposition)
    circuit.append(cirq.H.on_each(*qubits[:3]))

    # Step 2: Simulate modular exponentiation (a^x mod N) using simple CNOT gates
    # For simplicity, use CNOT gates to simulate the quantum operations (this is a toy model)
    circuit.append(cirq.CNOT(qubits[0], qubits[3]))
    circuit.append(cirq.CNOT(qubits[1], qubits[4]))
    circuit.append(cirq.CNOT(qubits[2], qubits[5]))

    # Step 3: Apply Quantum Fourier Transform (QFT) to the control register
    circuit.append(cirq.H(qubits[0]))  # Apply H gate to first qubit
    circuit.append(cirq.CZ(qubits[0], qubits[1])**0.5)
    circuit.append(cirq.H(qubits[1]))  # Apply H gate to second qubit
    circuit.append(cirq.CZ(qubits[1], qubits[2])**0.25)
    circuit.append(cirq.H(qubits[2]))  # Apply H gate to third qubit

    # Step 4: Measurement of both registers
    circuit.append(cirq.measure(*qubits[:3], key="control"))
    circuit.append(cirq.measure(*qubits[3:], key="target"))

    return circuit


def find_period(measurement_result):
    """Extracts the period from the measurement result."""
    # Extract the measurement results for the control and target registers
    control_register = measurement_result.measurements['control']
    target_register = measurement_result.measurements['target']

    # Convert the arrays to binary strings and then to integers
    control_value = int(''.join(map(str, control_register[0])), 2)
    target_value = int(''.join(map(str, target_register[0])), 2)

    # Calculate the period based on the difference between the control and target registers
    period = np.abs(control_value - target_value)
    
    return period


def shors_algorithm(N, repetitions=100):
    """Simulates Shor's algorithm for factoring the integer N with multiple repetitions."""
    # Prepare the quantum circuit for Shor's algorithm
    circuit = make_shors_circuit(N)
    simulator = cirq.Simulator()

    print(f"Running Shor's Algorithm Circuit for N = {N} with {repetitions} repetitions...")
    print(circuit)

    # Run the quantum circuit for the specified number of repetitions
    result = simulator.run(circuit, repetitions=repetitions)
    print("\nSimulation Results (Measurement):")
    print(result)

    # Extract period from the results (simulated process)
    period = find_period(result)
    print(f"\nExtracted Period from the Quantum Circuit: {period}")

    # Use the period to find the factors of N
    if period % 2 == 0:
        # Find one factor using the gcd
        factor1 = gcd(N, pow(2, period // 2) - 1)
        factor2 = N // factor1  # Find the second factor by dividing N by the first factor
        print(f"\nFactors of {N}: {factor1} and {factor2}")
    else:
        print("\nFailed to find factors. Try running the algorithm multiple times.")


# Example: Run Shor's algorithm to factor N = 15 with 100 repetitions
shors_algorithm(15, repetitions=100)
