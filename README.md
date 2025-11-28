# CSC 402 Compiler Construction – Lexical Analyzer

A Python-based lexical analyzer that tokenizes C-like source code into:
- `KEYWORD` (`int`, `float`, `if`, `print`)
- `IDENTIFIER` (e.g., `x`, `_val1`)
- `NUMBER` (e.g., `10`, `25.5`)
- `SYMBOL` (`=`, `;`, `+`, `*`, `>`, `(`, `)`, `{`, `}`)

Comments (`// ...`) are ignored.

## Usage
```bash
python lexer.py input_file.txt
