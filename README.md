# TyC Compiler Project

A comprehensive compiler implementation for **TyC**, a simple C-like programming language with complete type inference, using the ANTLR4 parser generator.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![ANTLR](https://img.shields.io/badge/ANTLR-4.13.2-orange.svg)](https://www.antlr.org/)
[![License](https://img.shields.io/badge/License-Academic-green.svg)](LICENSE)

## Overview

This is a mini project for **Principles of Programming Languages** course that implements a compiler for **TyC**, a custom C-like programming language designed for educational purposes.

📋 **For detailed language specification, see [TyC Specification](tyc_specification.md)**

The project demonstrates fundamental concepts of compiler construction including:

- **Lexical Analysis**: Tokenization and error handling for invalid characters, unclosed strings, and illegal escape sequences
- **Syntax Analysis**: Grammar-based parsing using ANTLR4 (ANother Tool for Language Recognition)
- **AST Generation**: Building abstract syntax trees from parse trees
- **Semantic Analysis**: Complete type inference system with static type checking
- **Code Generation**: Generating target code from validated AST
- **Error Handling**: Comprehensive error reporting for all compilation phases
- **Testing Framework**: Automated testing with HTML report generation

---

## Assignment 1 - Lexical Analysis and Syntax Analysis

### Required Tasks to Complete

1. **Read the language specification carefully**

   - Study the detailed [TyC Specification](tyc_specification.md) document
   - Understand the syntax and semantics of the TyC language
   - Master the lexical and syntax rules

2. **Implement the TyC.g4 file**

   - Complete the ANTLR4 grammar file in `src/grammar/TyC.g4`
   - Define lexical rules (tokens)
   - Define parser rules (grammar rules)
   - Handle precedence and associativity

3. **Write 100 lexer tests and 100 parser tests**
   - **100 test cases for lexer** in `tests/test_lexer.py`
     - Test valid and invalid tokens
     - Test error handling (unclosed strings, illegal escape sequences, etc.)
     - Test edge cases and boundary conditions
   - **100 test cases for parser** in `tests/test_parser.py`
     - Test valid grammar structures
     - Test syntax errors and error recovery
     - Test nested structures and complex expressions

### Lexical Error Handling Requirements

For lexical errors, the lexer must return the following tokens with specific lexemes:

- **ERROR_TOKEN** with `<unrecognized char>` lexeme: when the lexer detects an unrecognized character.

- **UNCLOSE_STRING** with `<unclosed string>` lexeme: when the lexer detects an unterminated string. The `<unclosed string>` lexeme does not include the opening quote.

- **ILLEGAL_ESCAPE** with `<wrong string>` lexeme: when the lexer detects an illegal escape in string. The wrong string is from the beginning of the string (without the opening quote) to the illegal escape.

### Evaluation Criteria

- **Grammar Implementation**: Accuracy and completeness of the `TyC.g4` file
- **Test Coverage**: Quantity and quality of test cases (200 tests total)
- **Error Handling**: Capability to handle lexical and syntax errors

---

## Assignment 2 - AST Generation

### Required Tasks to Complete

1. **Study the AST Node Structure**

   - Read carefully all node classes in `src/utils/nodes.py`
   - Understand the AST node hierarchy and their properties
   - Master how different language constructs map to AST nodes

2. **Implement the ASTGeneration Class**

   - Create a class `ASTGeneration` in `src/astgen/ast_generation.py`
   - Inherit from `TyCVisitor` (generated from ANTLR4)
   - Override visitor methods to construct appropriate AST nodes
   - Handle all language constructs defined in the TyC specification

3. **Write AST Generation Test Cases**
   - Implement test cases in `tests/test_ast_gen.py`
   - Test AST generation for all language features
   - Verify correct node types and structure
   - Test edge cases and complex nested structures

### AST Generation Requirements

The `ASTGeneration` class must:

- **Inherit from TyCVisitor**: Use the visitor pattern to traverse parse trees
- **Return AST nodes**: Each visit method should return appropriate node objects from `nodes.py`
- **Handle all constructs**: Support all language features defined in the grammar
- **Maintain structure**: Preserve the logical structure and relationships between language elements

### Evaluation Criteria

- **AST Implementation**: Correctness and completeness of the `ASTGeneration` class
- **Node Usage**: Proper utilization of node classes from `nodes.py`
- **Test Coverage**: Quality and comprehensiveness of AST generation test cases
- **Structure Accuracy**: AST must correctly represent the source program structure

---

## Project Structure

```
.
├── Makefile              # Cross-platform build automation
├── run.py                # Main project entrypoint
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
├── tyc_specification.md  # Language specification
├── external/             # External dependencies
│   └── antlr-4.13.2-complete.jar
├── src/                  # Source code
│   ├── astgen/           # AST generation module
│   │   ├── __init__.py   # Package initialization
│   │   └── ast_generation.py # ASTGeneration class implementation
│   ├── grammar/          # Grammar definitions
│   │   ├── TyC.g4        # ANTLR4 grammar specification
│   │   └── lexererr.py   # Custom lexer error classes
│   └── utils/            # Utility modules
│       ├── error_listener.py
│       ├── nodes.py      # AST node class definitions
│       └── visitor.py    # Base visitor classes
└── tests/                # Test suite
    ├── test_lexer.py     # Lexer tests
    ├── test_parser.py    # Parser tests
    ├── test_ast_gen.py   # AST generation tests
    └── utils.py          # Testing utilities
```

## Quick Start

### Prerequisites

- **Python 3.12+** (recommended) or Python 3.8+
- **Java Runtime Environment (JRE) 8+** (required for ANTLR4)

### Setup

1. **Clone the repository:**
   ```bash
   cd TyC-compiler
   ```

2. **Check system requirements:**
   ```bash
   python3 run.py check
   ```

3. **Set up the environment:**
   ```bash
   python3 run.py setup
   ```

4. **Activate virtual environment:**
   ```bash
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

5. **Build the compiler:**
   ```bash
   python3 run.py build
   ```

6. **Run tests:**
   ```bash
   python3 run.py test-lexer
   python3 run.py test-parser
   python3 run.py test-ast
   ```

## Available Commands

- `python3 run.py setup` - Install dependencies and set up environment
- `python3 run.py build` - Compile ANTLR grammar files
- `python3 run.py check` - Verify required tools are installed
- `python3 run.py test-lexer` - Run lexer tests
- `python3 run.py test-parser` - Run parser tests
- `python3 run.py test-ast` - Run AST generation tests
- `python3 run.py clean` - Clean build files

## License

This project is developed for educational purposes as part of the **Principles of Programming Languages** course.

**Author**: MEng. Trần Ngọc Bảo Duy  
**Institution**: Faculty of Computer Science and Engineering, Ho Chi Minh City University of Technology, VNU-HCM
