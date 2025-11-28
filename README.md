# CSC 402 Compiler Construction – Lexical Analyzer

A Python-based lexical analyzer that tokenizes C-like source code into structured tokens. Designed for real-time academic demonstration with arbitrary input files.

## Token Types

- **`KEYWORD`**: `int`, `float`, `if`, `print`
- **`IDENTIFIER`**: Names like `x`, `total`, `_val1` (starts with letter/underscore)
- **`NUMBER`**: Integers and decimals (e.g., `10`, `25.5`)
- **`SYMBOL`**: All of the following are supported:
  - **Single-character**: `=`, `;`, `+`, `*`, `>`, `(`, `)`, `{`, `}`, `<`, `!`, `/`, `&`, `|`, `-`, `#`, `%`, `^`, `` ` ``, `~`, `[`, `]`, `,`, `.`, `'`, `"`, `\`
  - **Multi-character**:
    `==`, `!=`, `<=`, `>=`,
    `++`, `--`, `+=`, `-=`, `*=`, `/=`,
    `&&`, `||`,
    `::`, `->`, `??`, `...`

- **Comments**: Anything after `//` is **ignored**

## Usage

```bash
python lexer.py input_file.txt
