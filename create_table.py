import pandas as pd

# Data structure for the direct-mapping cache table: (columbs = words), Row labels (rows = blocks)
cache_table_dm = {
    'word0': ['', '', '', '', '', '', '', ''],
    'word1': ['', '', '', '', '', '', '', ''],
    'word2': ['', '', '', '', '', '', '', ''],
    'word3': ['', '', '', '', '', '', '', ''],
    'word4': ['', '', '', '', '', '', '', ''],
    'word5': ['', '', '', '', '', '', '', ''],
    'word6': ['', '', '', '', '', '', '', ''],
    'word7': ['', '', '', '', '', '', '', '']
}
block_labels = ['block0', 'block1', 'block2', 'block3', 'block4', 'block5', 'block6', 'block7']
# Create a DataFrame
table = pd.DataFrame(cache_table_dm, index=block_labels)
# create tag array
tags = [None] * len(cache_table_dm['word0'])



def DirectMapping_Table(num_words: int, num_blocks: int) -> pd.DataFrame:
    # Create a dictionary for the cache table with empty strings for each word
    cache_table = {f'word{i}': [''] * num_blocks for i in range(num_words)}
    
    # Create block labels for the index
    block_labels = [f'block{i}' for i in range(num_blocks)]
    
    # Create the DataFrame with block labels as row indices
    table = pd.DataFrame(cache_table, index=block_labels)

    # Add an additional column titled 'tag' with default empty values
    table['tag'] = [''] * num_blocks
    
    return table

def SetAssociative_Table(num_words: int, num_blocks: int, x_way_set_associative: int) -> pd.DataFrame:
    # Create a dictionary for the cache table with empty strings for each word
    cache_table = {f'word{i}': [''] * num_blocks for i in range(num_words)}

    # Calculate the number of sets based on num_blocks and x_way_set_associative
    num_sets: int = num_blocks // x_way_set_associative

    # Create set labels with repetitions based on the ratio
    set_labels = [f'set{i // (num_blocks // num_sets)}' for i in range(num_blocks)]
    
    # Create the DataFrame with block labels as row indices
    table = pd.DataFrame(cache_table, index=set_labels)

    # Add an additional column titled 'tag' with default empty values
    table['tag'] = [''] * num_blocks
    
    return table


def FullyAssociative_Table(num_words: int, num_blocks: int) -> pd.DataFrame:
    # Create a dictionary for the cache table with empty strings for each word
    cache_table = {f'word{i}': [''] * num_blocks for i in range(num_words)}

    # Create set labels with repetitions based on the ratio
    set_labels = [f'block{i}' for i in range(num_blocks)]
    
    # Create the DataFrame with block labels as row indices
    table = pd.DataFrame(cache_table, index=set_labels)

    # Add an additional column titled 'tag' with default empty values
    table['tag'] = [''] * num_blocks

    return table