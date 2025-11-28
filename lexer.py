"""
Lexical Analyzer for CSC 402 Compiler Construction – Enhanced Version

This lexer reads any input text file and outputs tokens in the format:
Line X: TYPE -> value

Token Categories:
- KEYWORDS: int, float, if, print
- IDENTIFIER: [A-Za-z_][A-Za-z0-9_]*
- NUMBER: \d+(\.\d*)?
- SYMBOL: All single and multi-character operators explicitly defined below
- COMMENT: // ... (ignored entirely)
- SKIP: whitespace (spaces, tabs)
- MISMATCH: any undefined character → error

Author: Isaac Azuoma Daddy Ndulor
GitHub: https://github.com/isaacndu2020/CSC402-Lexer
"""
import sys
import re

# Define reserved keywords
KEYWORDS = {'int', 'float', 'if', 'print'}

# Token specification with explicit symbol support
# NOTE: Order matters — longer patterns MUST appear before shorter ones!
TOKEN_SPECIFICATION = [
    # Literals and identifiers
    ('NUMBER',     r'\d+(\.\d*)?'),                     # Integer or float: 10, 25.5
    ('IDENTIFIER', r'[A-Za-z_][A-Za-z0-9_]*'),        # Variable names: x, total, _val1

    # Multi-character operators (longest first!)
    ('SYMBOL',     r'\.\.\.'),                           # Ellipsis: ...
    ('SYMBOL',     r'\?\?'),                             # Nullish coalescing: ??
    ('SYMBOL',     r'->'),                               # Arrow: ->
    ('SYMBOL',     r'::'),                               # Scope resolution: ::
    ('SYMBOL',     r'=='),                               # Equality
    ('SYMBOL',     r'!='),                               # Not equal
    ('SYMBOL',     r'<='),                               # Less than or equal
    ('SYMBOL',     r'>='),                               # Greater than or equal
    ('SYMBOL',     r'\+\+'),                             # Increment
    ('SYMBOL',     r'--'),                               # Decrement
    ('SYMBOL',     r'\+='),                              # Add and assign
    ('SYMBOL',     r'-='),                               # Subtract and assign
    ('SYMBOL',     r'\*='),                              # Multiply and assign
    ('SYMBOL',     r'/='),                               # Divide and assign
    ('SYMBOL',     r'&&'),                               # Logical AND
    ('SYMBOL',     r'\|\|'),                             # Logical OR

    # Single-character symbols (include ALL requested symbols)
    # Grouped for clarity but matched as individual chars
    ('SYMBOL',     r'[=;+*\(\){}><!&|/\-#%^`~\[\],\.\'\"\\]'),

    # Whitespace and errors
    ('SKIP',       r'[ \t]+'),                           # Skip spaces and tabs
    ('MISMATCH',   r'.'),                                # Any other character → error
]

# Compile the master regex pattern
tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION)
get_token = re.compile(tok_regex).match

def tokenize(code, line_num):
    """
    Generator that yields tokens from a single line of code.
    Raises RuntimeError for unexpected characters.
    """
    pos = 0
    while pos < len(code):
        match = get_token(code, pos)
        if not match:
            raise RuntimeError(f'Unexpected character at position {pos} on line {line_num}')

        token_type = match.lastgroup
        token_value = match.group(token_type)

        # Handle each token type
        if token_type == 'MISMATCH':
            raise RuntimeError(f'Unexpected character "{token_value}" at position {pos} on line {line_num}')
        elif token_type == 'SKIP':
            pass  # Ignore whitespace
        elif token_type == 'NUMBER':
            yield ('NUMBER', token_value)
        elif token_type == 'IDENTIFIER':
            if token_value in KEYWORDS:
                yield ('KEYWORD', token_value)
            else:
                yield ('IDENTIFIER', token_value)
        elif token_type == 'SYMBOL':
            yield ('SYMBOL', token_value)
        # Advance to next position
        pos = match.end()

def main():
    """Main function: reads input file and prints tokens."""
    # Validate command-line usage
    if len(sys.argv) != 2:
        print("Usage: python lexer.py <input_file>")
        print("Example: python lexer.py source.txt")
        sys.exit(1)

    filename = sys.argv[1]
    # Attempt to open the input file
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    # Process each line
    for i, line in enumerate(lines, start=1):
        # Remove comments (everything from // onward)
        if '//' in line:
            line = line.split('//', 1)[0]
        # Remove trailing newline
        stripped_line = line.rstrip('\n')
        # Skip empty lines
        if not stripped_line.strip():
            continue

        # Tokenize and output
        try:
            for token_type, token_value in tokenize(stripped_line, i):
                print(f"Line {i}: {token_type} -> {token_value}")
        except RuntimeError as e:
            print(f"Error on line {i}: {e}")

# Entry point
if __name__ == "__main__":
    main()
