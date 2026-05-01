# src/huffman_codec.py
import collections
import heapq

def get_symbol_probabilities(text):
    """Calculates the probability of each symbol in the text."""
    symbol_counts = collections.Counter(text)
    total_symbols = sum(symbol_counts.values())
    return {symbol: count / total_symbols for symbol, count in symbol_counts.items()}

def generate_huffman_tree(probabilities):
    """Builds the Huffman tree and returns sorted codes."""
    # Create a heap with (weight, [symbol, ""]) for each symbol
    heap = [[weight, [symbol, ""]] for symbol, weight in probabilities.items()]
    heapq.heapify(heap)  
    
    # Build the Huffman tree
    while len(heap) > 1:
        low = heapq.heappop(heap)
        high = heapq.heappop(heap)
        for pair in low[1:]:
            pair[1] = '0' + pair[1]  # Lower branch
        for pair in high[1:]:
            pair[1] = '1' + pair[1]  # Higher branch
        heapq.heappush(heap, [low[0] + high[0]] + low[1:] + high[1:])
    
    # Return symbols with their codes sorted by code length and symbol
    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

def print_huffman_table(probabilities, huffman_code):
    """Helper to display the compression table."""
    print("Symbol | Probability | Huffman Code")
    print("-------|-------------|--------------")
    for symbol in sorted(probabilities.keys()):
        prob = probabilities[symbol]
        code = next((c[1] for c in huffman_code if c[0] == symbol), "")
        print(f"  {repr(symbol):<4} | {prob:.6f}    | {code}")
