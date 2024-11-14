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
```
```bash
python main.py -a 03C FF4 050 070 078 0F0 FF4 03C 070 078 -b 8 -w 2 -m set_associative -x 2
```
```bash
python main.py -a 03C FF4 050 070 078 0F0 FF4 03C 070 078 -b 8 -w 2 -m fully_associative
```