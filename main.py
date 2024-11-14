from create_table import DirectMapping_Table, SetAssociative_Table, FullyAssociative_Table
from mapping import direct_mapping, set_associative_mapping, fully_associative_mapping
import argparse

# Function to parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Cache mapping visualization tool.")
    parser.add_argument('-a', '--addresses', nargs='+', required=True, help="List of hexadecimal addresses to process.")
    parser.add_argument('-b', '--blocks', type=int, required=True, help="Number of blocks in the cache.")
    parser.add_argument('-w', '--words', type=int, required=True, help="Number of words per block.")
    parser.add_argument('-m', '--method', choices=['direct', 'set_associative', 'fully_associative'], required=True, help="Cache mapping method.")
    parser.add_argument('-x', '--ways', type=int, default=2, help="Number of ways for set-associative mapping (only applicable to set-associative).")
    return parser.parse_args()

# Main process
def main():
    args = parse_args()

    # Retrieve parsed arguments
    addresses = args.addresses
    num_blocks = args.blocks
    num_words = args.words
    method = args.method
    x_ways = args.ways

    # Call the appropriate mapping function based on the selected method
    if method == 'direct':
        miss_count = direct_mapping(num_words, num_blocks, addresses)
    elif method == 'set_associative':
        miss_count = set_associative_mapping(num_words, num_blocks, addresses, x_way_set_associative=x_ways)
    elif method == 'fully_associative':
        miss_count = fully_associative_mapping(num_words, num_blocks, addresses)
    
    print(f"Miss rate: {miss_count}/{len(addresses)}")

if __name__ == "__main__":
    main()





''' Old:
# instantiate addresses
addresses: tuple = ('03C', 'FF4', '050', '070', '078', '0F0', 'FF4', '03C', '070', '078')
#addresses: tuple = ('888', '100', '080', '218', '194', '2F4', '10C', '100', '094', '088')
#addresses: tuple = ('80', '48', '44', '20', '00', '40', '48', 'C0', '2C', '88')

# main process - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
print(f"Miss rate: {direct_mapping(2, 8, addresses)}/10")
print(f"Miss rate: {set_associative_mapping(2, 8, addresses, 2)}/10")
print(f"Miss rate: {fully_associative_mapping(2, 8, addresses)}/10")
'''