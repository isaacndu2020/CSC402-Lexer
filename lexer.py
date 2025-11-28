"""
Lexical Analyzer for CSC 402 Compiler Construction

This lexer reads any input text file and outputs tokens in the format:
Line X: TYPE -> value

Token Categories (per assignment):
- KEYWORD: int, float, if, print
- IDENTIFIER: starts with letter/underscore, followed by letters/digits/underscores
- NUMBER: integer or decimal (e.g., 10, 25.5)
- SYMBOL: = ; + * > ( ) { }
- COMMENT: ignore everything after // on a line
- SKIP: ignore whitespace (spaces/tabs)

Author: Isaac Azuoma Daddy Ndulor
GitHub: https://github.com/isaacndu2020/CSC402-Lexer
"""
import sys
import re

KEYWORDS = {'int', 'float', 'if', 'print'}

TOKEN_SPECIFICATION = [
    ('NUMBER',     r'\d+(\.\d*)?'),          # Integer or float
    ('IDENTIFIER', r'[A-Za-z_][A-Za-z0-9_]*'),
    ('SYMBOL',     r'[=;+*\(\){}>]'),        # Only single-character symbols
    ('SKIP',       r'[ \t]+'),               # Skip whitespace
    ('COMMENT',    r'//.*'),                 # Ignore comments
    ('MISMATCH',   r'.'),
]

tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION)
get_token = re.compile(tok_regex).match

def tokenize(code, line_num):
    pos = 0
    while pos < len(code):
        match = get_token(code, pos)
        if not match:
            raise RuntimeError(f'Unexpected character at position {pos} on line {line_num}')
        token_type = match.lastgroup
        token_value = match.group(token_type)

        if token_type == 'MISMATCH':
            raise RuntimeError(f'Unexpected character "{token_value}" at position {pos} on line {line_num}')
        elif token_type == 'SKIP':
            pass  # Ignore whitespace
        elif token_type == 'COMMENT':
            pass  # Ignore comments (already removed in main, but safe to skip here too)
        elif token_type == 'NUMBER':
            yield ('NUMBER', token_value)
        elif token_type == 'IDENTIFIER':
            if token_value in KEYWORDS:
                yield ('KEYWORD', token_value)
            else:
                yield ('IDENTIFIER', token_value)
        elif token_type == 'SYMBOL':
            yield ('SYMBOL', token_value)

        pos = match.end()

def main():
    if len(sys.argv) != 2:
        print("Usage: python lexer.py <input_file>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    for i, line in enumerate(lines, start=1):
        # Remove comments (everything from // onward)
        if '//' in line:
            line = line.split('//', 1)[0]
        stripped_line = line.rstrip('\n')
        if not stripped_line.strip():
            continue  # Skip empty lines after comment removal
        try:
            for token_type, token_value in tokenize(stripped_line, i):
                print(f"Line {i}: {token_type} -> {token_value}")
        except RuntimeError as e:
            print(f"Error on line {i}: {e}")

if __name__ == "__main__":
    main()
