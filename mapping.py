from typing import List
import math
from create_table import DirectMapping_Table, SetAssociative_Table, FullyAssociative_Table

# mapping functions - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def insert_into_table(table, block: int, word: int, tag: str, num_words: int, address: str):    
    # get the number of bits in the addresss
    num_bits = len(address) * 4
    # get address in int form
    int_adress: int = binary_to_integer(hex_to_binary(address))
    # put address in correct block-word spot
    table.iloc[block, word] = address
    # loop through the upper bound of block, bits[word:8]
    i = 4
    for word_index in range(word+1, num_words-1):
        table.iloc[block, word_index] = int_to_hex(int_adress + i, num_bits)
        i+=4
    # loop through the lower bound of block, bits[0:word]
    i = word * 4 * -1
    for word_index in range(0, word):
        table.iloc[block, word_index] = int_to_hex(int_adress + i, num_bits)
        i+=4     

    # insert tag
    table.iloc[block, num_words] = tag

    

def direct_mapping(num_words: int, num_blocks: int, addresses: List[str]) -> None:
    
    # create table (using pandas data frames)
    table = DirectMapping_Table(num_words, num_blocks)
    
    # get the number of bits per address
    num_bits = len(addresses[0]) * 4

    # Create the tags array based on the number of blocks
    tags = [None] * num_blocks
    
    misses = 0
    for address in addresses:

        # Break down the address to extract the word, block & tag bits
        # then covert those bits into integer form
        bits_per_block = int(math.log2(num_blocks))
        bits_per_word = int(math.log2(num_words))

        bin_address: str = hex_to_binary(address)[::-1]                         # reverse bin_address so it can be read from bit 0
        bit_index: int = 2                                                      # start index at bit 2 by skiping first two bits
        bin_word: str = bin_address[bit_index:bit_index+bits_per_word][::-1]    # get word bits
        bit_index+=bits_per_word                                                # increment index by word bits
        bin_block: str = bin_address[bit_index:bit_index+bits_per_block][::-1]  # get block bits
        bit_index+=bits_per_block                                               # increment index by block bits
        bin_tag: str = bin_address[bit_index:num_bits][::-1]                    # get tag bits (index to end address)
        bin_address = bin_address[::-1]                                         # reverse back to forward
        # convert back to int
        word = binary_to_integer(bin_word)
        block = binary_to_integer(bin_block)
        tag = binary_to_integer(bin_tag)

        # check for a matching tag in the block accessed. if not, increment the miss counter
        # update the tag to this address's
        if tags[block] != tag:
            misses+=1
        tags[block] = tag

        # insert address into table:
        insert_into_table(table, block, word, bin_tag, num_words, address)

    # Display the table
    print(f"\n\nFinal Table: Direct Mapping on addresses{addresses}\n{table}")
    return misses

# two sets per block
def set_associative_mapping(num_words: int, num_blocks: int, addresses: List[str],  x_way_set_associative: int) -> None:
    
    # create table (using pandas data frames)
    table = SetAssociative_Table(num_words, num_blocks, x_way_set_associative)

    # get the number of bits per address
    num_bits = len(addresses[0]) * 4

    # get the dementions for the table
    num_sets: int = num_blocks // x_way_set_associative

    # Create an LRU array where each element is an independent empty tuple, [0]=tag, [1]=block index
    LRU_array = [[('', num_blocks) for _ in range(num_blocks // num_sets)] for _ in range(num_sets)]
    
    misses = 0
    for address in addresses:

        # Break down the address to extract the word, block & tag bits
        # then covert those bits into integer form
        bits_per_set = int(math.log2(num_sets))
        bits_per_word = int(math.log2(num_words))

        bin_address: str = hex_to_binary(address)[::-1]                         # reverse bin_address so it can be read from bit 0
        bit_index: int = 2                                                      # start index at bit 2 by skiping first two bits
        bin_word: str = bin_address[bit_index:bit_index+bits_per_word][::-1]    # get word bits
        bit_index+=bits_per_word                                                # increment index by word bits
        bin_set: str = bin_address[bit_index:bit_index+bits_per_set][::-1]      # get set bits
        bit_index+=bits_per_set                                                 # increment index by set bits
        bin_tag: str = bin_address[bit_index:num_bits][::-1]                    # get tag bits (index to end address)
        bin_address = bin_address[::-1]                                         # reverse back to forward
        # convert back to int
        word = binary_to_integer(bin_word)
        set_index = binary_to_integer(bin_set)
        tag = binary_to_integer(bin_tag)
        
        # Determine if the tag is in the cache set
        cache_set = LRU_array[set_index]
        hit = False
        block_index = set_index * x_way_set_associative

        def remove_empty_in_set():
            for i, cache in enumerate(cache_set):
                if cache[0] == '' and cache[1] == num_blocks: # is empty
                    cache_set.pop(i)

        for i, cache in enumerate(cache_set):
            if cache[0] == tag:
                # Cache hit
                hit = True
                # Remove the hit address
                block_index = cache_set.pop(i)[1]
                # Move this block to the most recent position for LRU
                cache_set.append((tag, block_index))
                break

        if not hit:
            # Cache miss: Increment miss count
            misses += 1
            
            stored_counter = 0
            for cache in cache_set:
                # if there is an address stored in the current set, increment counter
                if cache[1] != num_blocks:
                    stored_counter+=1
                    if cache[1] >= block_index:
                        block_index+=1

            # If the set is full, evict the LRU block (the first one in the list)
            if stored_counter >= (num_blocks//num_sets):
                # remove the least recent address
                block_index = cache_set.pop(0)[1]
            else:
                remove_empty_in_set()

            # Add the new tag to the end (most recent position)
            cache_set.append((tag, block_index))


        insert_into_table(table, block_index, word, bin_tag, num_words, address)
        
    # Display the table
    print(f"\n\nFinal Table: {x_way_set_associative}-way Set Associative Mapping on addresses{addresses}\n{table}")
    return misses




def fully_associative_mapping(num_words: int, num_blocks: int, addresses: List[str]) -> None:
    # create table (using pandas data frames)
    table = FullyAssociative_Table(num_words, num_blocks)

    # get the number of bits per address
    num_bits = len(addresses[0]) * 4

    # Create an LRU array where each element is an independent empty list
    LRU_array = [('', num_blocks) for _ in range(num_blocks)]
    
    misses = 0
    for address in addresses:
        # Break down the address to extract the word, block & tag bits
        # then covert those bits into integer form
        bits_per_word = int(math.log2(num_words))

        bin_address: str = hex_to_binary(address)[::-1]                         # reverse bin_address so it can be read from bit 0
        bit_index: int = 2                                                      # start index at bit 2 by skiping first two bits
        bin_word: str = bin_address[bit_index:bit_index+bits_per_word][::-1]    # get word bits
        bit_index+=bits_per_word                                                # increment index by word bits
        bin_tag: str = bin_address[bit_index:num_bits][::-1]                    # get tag bits (index to end address)
        bin_address = bin_address[::-1]                                         # reverse back to forward
        # convert back to int
        word = binary_to_integer(bin_word)
        tag = binary_to_integer(bin_tag)

        # Determine if the tag is in the cache set
        hit = False
        block_index = 0

        def remove_empty():
            for i, cache in enumerate(LRU_array):
                if cache[0] == '' and cache[1] == num_blocks: # is empty
                    LRU_array.pop(i)

        for i, cache in enumerate(LRU_array):
            if cache[0] == tag:
                # Cache hit
                hit = True
                # Remove the hit address
                block_index = LRU_array.pop(i)[1]
                # Move this block to the most recent position for LRU
                LRU_array.append((tag, block_index))
                break

        if not hit:
            # Cache miss: Increment miss count
            misses += 1
            
            for cache in LRU_array:
                # if there is an address stored in the current set, increment counter
                if cache[1] != num_blocks:
                    block_index+=1

            # If the set is full, evict the LRU block (the first one in the list)
            if block_index >= (num_blocks):
                # remove the least recent address
                block_index = LRU_array.pop(0)[1]
            else:
                remove_empty()

            # Add the new tag to the end (most recent position)
            LRU_array.append((tag, block_index))

        insert_into_table(table, block_index, word, bin_tag, num_words, address)

    # Display the table
    print(f"\n\nFinal Table: Fully Associative Mapping on addresses{addresses}\n{table}")
    return misses

# number base conversion - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def hex_to_binary(hex_string: str) -> str:
    return bin(int(hex_string, 16))[2:].zfill(len(hex_string) * 4)

def binary_to_integer(binary_string: str) -> int:
    return int(binary_string, 2)

def int_to_hex(value: int, num_bits: int) -> str:
    # Calculate the number of hex digits required for the specified number of bits
    num_hex_digits = (num_bits + 3) // 4  # Each hex digit represents 4 bits
    # Convert the integer to hex and pad with leading zeros
    return hex(value)[2:].upper().zfill(num_hex_digits)