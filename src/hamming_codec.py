# src/hamming_codec.py
import numpy as np

class Hamming74:
    def __init__(self):
        # Generator Matrix (G)
        self.G = np.array([
            [1, 0, 0, 0, 1, 1, 0],
            [0, 1, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 1, 1],
            [0, 0, 0, 1, 1, 1, 1]
        ])
        # Parity-Check Matrix (H)
        self.H = np.array([
            [1, 1, 0, 1, 1, 0, 0],
            [1, 0, 1, 1, 0, 1, 0],
            [0, 1, 1, 1, 0, 0, 1]
        ])

    def encode(self, info_bits):
        """Encodes 4-bit blocks into 7-bit codewords."""
        n_codewords = len(info_bits) // 4
        encoded_bits = np.zeros(n_codewords * 7, dtype=int)
        
        for i in range(n_codewords):
            u = info_bits[i*4:(i+1)*4]
            c = np.dot(u, self.G) % 2
            encoded_bits[i*7:(i+1)*7] = c
            
        return encoded_bits

    def decode(self, received_codewords, verbose=False):
        """Decodes 7-bit codewords and corrects single-bit errors via Syndromes."""
        n_codewords = received_codewords.shape[0]
        decoded_bits = np.zeros(n_codewords * 4, dtype=int)
        
        for i in range(n_codewords):
            r = received_codewords[i].copy()
            s = np.dot(r, self.H.T) % 2  # Calculate Syndrome
            
            if np.any(s):
                if verbose:
                    print(f"Syndrome for CW {i}: {s}")
                    
                error_pos = np.where((self.H.T == s).all(axis=1))[0]
                if error_pos.size > 0:
                    if verbose:
                        print(f" -> Correcting error at index {error_pos[0]}")
                    r[error_pos[0]] ^= 1  # Flip the erroneous bit
                    
            # Extract original 4 information bits
            decoded_bits[i*4:(i+1)*4] = r[:4]
            
        return decoded_bits
