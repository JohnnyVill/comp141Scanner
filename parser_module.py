import sys
from scanner import scanner
from scanner import TOKEN_REGEX

tokens = []
pos = 0

class ast:
    def __init__(self, value, left = None, right = None):
        self.value = value
        self.left = left
        self.right = right
        
    def print_tree(self, level = 0):
        lines = ["     " * level + f"{self.value}"]
        if self.left:
            lines.extend(self.left.print_tree(level + 1))
        if self.right:
            lines.extend(self.right.print_tree(level + 1))
        return lines


def peek():
    global pos
    return tokens[pos] if pos < len(tokens) else (None, None)

def consume():
    global pos
    pos += 1

def parse_element():
    tok, tok_type = peek()
    
    if tok_type == "NUMBER" or tok_type == "IDENTIFIER":
        consume()
        return ast(f"{tok} : {tok_type}")
    elif tok == "(":
        consume()
        node = parse_expr()
        if peek()[0] == ")":
            consume()
        return node
    else:
        raise SyntaxError(f"Unexpected token: {tok}")
        

def parse_factor():
    node = parse_element()
    
    while True:
        tok, tok_type = peek()
        if tok in ('*', '/'):
            consume()
            right = parse_element()
            node = ast(f"{tok} : {tok_type}", node, right)
        else:
            break
    return node
        

def parse_expr():
    node = parse_factor()
    
    while True:
        tok, tok_type = peek()
        if tok in ('+', '-'):
            consume()
            right = parse_factor()
            node = ast(f"{tok} : {tok_type}", node, right)
        else:
            break
    return node

def parse_program(outfile):
    global tokens, pos
    print("Tokens:")
    outfile.write("Tokens:\n")
    for tok, tok_type in tokens:
        print(f"{tok} : {tok_type}")
        outfile.write(f"{tok} : {tok_type}\n")
    print("AST:")
    outfile.write("\nAST\n")
    tree = parse_expr()
    for line in tree.print_tree():
        print(line)
        outfile.write(line + "\n")
        
    tokens.clear()
    pos = 0
        