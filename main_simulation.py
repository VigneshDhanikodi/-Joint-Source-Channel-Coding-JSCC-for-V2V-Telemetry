# main_simulation.py
import numpy as np
import matplotlib.pyplot as plt

# Import custom modules
from src.huffman_codec import get_symbol_probabilities, generate_huffman_tree, print_huffman_table
from src.hamming_codec import Hamming74
from src.channel_sim import AWGNChannel

def run_source_coding_demo():
    print("="*50)
    print(" PART 1: SOURCE COMPRESSION (HUFFMAN)")
    print("="*50)
    
    # Sample Telemetry / Text
    text = "James C. Maxwell was a 19th-century pioneer in chemistry and physics who articulated the idea of electromagnetism."
    
    probabilities = get_symbol_probabilities(text)
    huffman_code = generate_huffman_tree(probabilities)
    print_huffman_table(probabilities, huffman_code)
    print("\n")

def run_channel_coding_sim():
    print("="*50)
    print(" PART 2: BER vs Eb/N0 MONTE CARLO SIMULATION")
    print("="*50)
    
    # Initialize components
    codec = Hamming74()
    channel = AWGNChannel(code_rate=4/7)
    
    # Generate 100,000 random information bits for statistical significance
    n_info_bits = 100000 
    info_bits = np.random.randint(0, 2, n_info_bits)
    
    EbN0_dB_range = np.arange(0, 11, 1)
    ber_results = np.zeros_like(EbN0_dB_range, dtype=float)

    print("Running simulation over AWGN channel...")
    for idx, ebno in enumerate(EbN0_dB_range):
        # 1. Encode
        encoded_bits = codec.encode(info_bits)
        
        # 2. Modulate
        mod_signal = channel.modulate_bpsk(encoded_bits)
        
        # 3. Add Noise
        rx_signal = channel.add_noise(mod_signal, ebno_db=ebno)
        
        # 4. Demodulate
        rx_bits = channel.demodulate_bpsk(rx_signal)
        
        # 5. Decode & Correct
        n_codewords = len(rx_bits) // 7
        rx_codewords = rx_bits.reshape((n_codewords, 7))
        decoded_bits = codec.decode(rx_codewords, verbose=False)
        
        # 6. Evaluate
        ber_results[idx] = channel.calculate_ber(info_bits, decoded_bits)
        print(f"Eb/N0 = {ebno:2d} dB  |  BER = {ber_results[idx]:.6f}")

    # Plotting the results
    plt.figure(figsize=(9, 6))
    plt.semilogy(EbN0_dB_range, ber_results, 'bo-', linewidth=2, label='Hamming (7,4) Coded BPSK')
    
    plt.xlabel('Eb/N0 (dB)', fontsize=12)
    plt.ylabel('Bit Error Rate (BER)', fontsize=12)
    plt.title('JSCC Simulation: BER Performance over AWGN', fontsize=14)
    plt.grid(True, which="both", ls="--", alpha=0.7)
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_source_coding_demo()
    run_channel_coding_sim()
