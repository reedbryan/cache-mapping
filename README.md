# Cache Mapping Visualization Tool

This Python program visualizes cache mapping using different methods: Direct Mapping, Set-Associative Mapping, and Fully Associative Mapping. Users can specify hexadecimal addresses, the number of blocks and words, and the cache mapping method.

I wrote this program to give myself practice problems in my Microprocessor-Based Systems class so if your taking something similar and were also not given any practice material here you go.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Arguments](#arguments)
- [Examples](#examples)

---

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/username/cache-mapping.git
    cd repo_name
    ```

2. Install required packages. This program uses `pandas`, so ensure it is installed:
    ```bash
    pip install pandas
    ```

3. Ensure that `main.py`, `mapping.py`, `create_table.py` files, are in the same directory.

## Usage

Run the program with the following command structure:

```bash
python main.py -a <addresses> -b <num_blocks> -w <num_words> -m <method> [-x <ways>]
```
### Arguments
- -a or --addresses: A list of hexadecimal addresses to process (required). Example: 03C FF4 050 070
- -b or --blocks: Number of blocks in the cache (required).
- -w or --words: Number of words per block (required).
- -m or --method: Cache mapping method (required). Options are:
    - direct: Direct mapping
    - set_associative: Set-associative mapping
    - fully_associative: Fully associative mapping
- -x or --ways: Number of ways for set-associative mapping (optional, default is 2). Only used when the method is set_associative.

### Examples
```bash
python main.py -a 03C FF4 050 070 078 0F0 FF4 03C 070 078 -b 8 -w 2 -m direct

Ouput:

Direct Mapping on addresses:
['03C', 'FF4', '050', '070', '078', '0F0', 'FF4', '03C', '070', '078']
       word0 word1     tag
block0                    
block1                    
block2   050   054  000001
block3                    
block4                    
block5                    
block6   070   074  000001
block7   078   07C  000001

Miss rate: 10/10
```
```bash
python main.py -a 03C FF4 050 070 078 0F0 FF4 03C 070 078 -b 8 -w 4 -m set_associative -x 2

Ouput:

2-way Set Associative Mapping on addresses:
['03C', 'FF4', '050', '070', '078', '0F0', 'FF4', '03C', '070', '078']
     word0 word1 word2 word3     tag
set0                                
set0                                
set1   050   054   058   05C  000001
set1                                
set2                                
set2                                
set3   070   074   078   07C  000001
set3   030   034   038   03C  000000

Miss rate: 8/10
```
```bash
python main.py -a 03C FF4 050 070 078 0F0 FF4 03C 070 078 -b 8 -w 8 -m fully_associative

Output:

Fully Associative Mapping on addresses:
['03C', 'FF4', '050', '070', '078', '0F0', 'FF4', '03C', '070', '078']
       word0 word1 word2 word3 word4 word5 word6 word7      tag
block0   020   024   028   02C   030   034   038   03C  0000001
block1   FE0   FE4   FE8   FEC   FF0   FF4   FF8   FFC  1111111
block2   040   044   048   04C   050   054   058   05C  0000010
block3   060   064   068   06C   070   074   078   07C  0000011
block4   0E0   0E4   0E8   0EC   0F0   0F4   0F8   0FC  0000111
block5                                                         
block6                                                         
block7                                                         

Miss rate: 5/10                                                    
```