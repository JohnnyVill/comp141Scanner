import sys
from scanner import scanner
from scanner import TOKEN_REGEX

tokens = []
pos = 0

class ast:
    def __init__(self, value, children = None):
        self.value = value
        self.children = children if children is not None else []
    
    def create_stack(self):
        if not self.children:
            return [self.value]
        res = []
        for child in self.children:
            res.extend(child.create_stack())
        res.append(self.value)
        return res
    
    def stack_eval(self, mem):
        res = self.create_stack()
        stack = []
        
        for item in res:
            word, _ , c = item.partition(' : ')
            if word == "NUMBER":
                stack.append(int(c))
            elif word == "IDENTIFIER":
                if c not in mem:
                    raise RuntimeError("Uninitialized identifier " + c)
                stack.append(mem[c])
            elif word == "SYMBOL" and c in "+-*/":
                right = stack.pop()
                left = stack.pop()
                if c == '+':
                    stack.append(left + right)
                elif c == '-':
                    stack.append(left - right)
                elif c == '*':
                    stack.append(left * right)
                elif c == '/':
                    if right != 0:
                        stack.append(left // right)
                    else:
                        raise ValueError("Cannot divide by 0")
        return stack[0]
    

    def print_tree(self, level = 0):
        lines = ["     " * level + f"{self.value}"]
        
        for child in self.children:
            lines.extend(child.print_tree(level + 1))
        return lines

def eval_stmt(node, memory):
    if node is None:
        return None, memory

    label = node.value
    parts = label.split(" ", 1)
    kind = parts[0]
    payload = parts[1] if len(parts) > 1 else ""

    if label == "SKIP":
        return None, memory

    if kind == "SYMBOL" and payload == ":=":
        id_node, expr_node = node.children
        _, name = id_node.value.split(" ", 1)  
        value = expr_node.stack_eval(memory)
        memory[name] = value
        return None, memory

    if kind == "SYMBOL" and payload == ";":
        left, right = node.children
        new_left, memory = eval_stmt(left, memory)

        if new_left is None:
            return right, memory
        else:
            node.children[0] = new_left
            return node, memory

    if label == "IF-STATEMENT":
        cond_node, then_node, else_node = node.children
        cond_val = cond_node.stack_eval(memory)
        if cond_val > 0:
            return then_node, memory
        else:
            return else_node, memory

    if label == "WHILE-LOOP":
        cond_node, body_node = node.children
        cond_val = cond_node.stack_eval(memory)
        if cond_val > 0:
            new_while = ast("WHILE-LOOP", [cond_node, body_node])
            new_seq = ast("SYMBOL ;", [body_node, new_while])
            return new_seq, memory
        else:
            return None, memory

    raise RuntimeError(f"Unknown statement node: {label}")
        
        

################################################
def peek():
    global pos
    return tokens[pos] if pos < len(tokens) else (None, None)

def consume():
    global pos
    pos += 1

def expect(expected_token):
    tok, tok_type = peek()
    if tok != expected_token:
        raise SyntaxError(f"Unexpected token {tok} found, but expected '{expected_token}'")
    consume()

def expect_type(expected_type):
    tok, tok_type = peek()
    if tok_type != expected_type:
        raise SyntaxError(f"Unexpected token type {tok_type}, but expected '{expected_type}'")
    consume()
    return (tok,tok_type)


##################################################
def parse_element():
    tok, tok_type = peek()
    
    if tok_type == "NUMBER" or tok_type == "IDENTIFIER":
        consume()
        return ast(f"{tok_type} : {tok}")
    elif tok == "(":
        consume()
        node = parse_expr()
        if peek()[0] == ")":
            consume()
        return node
    else:
        raise SyntaxError(f"Unexpected token: {tok}")
def parse_piece():
    node = parse_element()
    
    while True:
        tok, tok_type = peek()
        if tok == '*':
            consume()
            right = parse_element()
            node = ast(f"{tok_type} : {tok}", [node, right])
        else:
            break
    return node        

def parse_factor():
    node = parse_piece()
    
    while True:
        tok, tok_type = peek()
        if tok =='/':
            consume()
            right = parse_piece()
            node = ast(f"{tok_type} : {tok}", [node, right])
        else:
            break
    return node

def parse_term():
    node = parse_factor()
    
    while True:
        tok, tok_type = peek()
        if tok =='-':
            consume()
            right = parse_factor()
            node = ast(f"{tok_type} : {tok}", [node, right])
        else:
            break
    return node        

def parse_expr():
    node = parse_term()
    
    while True:
        tok, tok_type = peek()
        if tok =='+':
            consume()
            right = parse_term()
            node = ast(f"{tok_type} : {tok}", [node, right])
        else:
            break
    return node

##################################################

def parse_statement():
    stmt_node = parse_basestatement()
    tok, tok_type = peek()
    while tok == ';':
        consume()
        next_tok, _ = peek()
        if next_tok is None or next_tok in ("endwhile", "endif", "else"):
            # allow final semicolon with no following statement
            break
        node = parse_basestatement()
        stmt_node = ast(f"SYMBOL ;", [stmt_node, node])
        tok, tok_type = peek()
    return stmt_node
def parse_basestatement():
    tok,tok_type = peek()
    if tok_type == "IDENTIFIER":
        return parse_assignment()
    elif tok == "if":
        return parse_ifstatement()
    elif tok == "while":
        return parse_whilestatement()
    elif tok == "skip":
        consume()
        return ast(f"SKIP")
    else:
        raise SyntaxError(f"Unexpected token {tok}")

def parse_assignment():
    tok,tok_type = expect_type("IDENTIFIER")
    expect(":=")
    node = parse_expr()
    id_node = ast(f"{tok_type} {tok}")
    return ast(f"SYMBOL :=", [id_node, node])
        
def parse_ifstatement():
    expect("if")
    if_cond = parse_expr()
    expect("then")
    then_cond = parse_statement()
    expect("else")
    else_cond = parse_statement()
    expect("endif")
    return ast("IF-STATEMENT",[if_cond,then_cond,else_cond])
    
def parse_whilestatement():
    expect("while")
    while_cond = parse_expr()
    expect("do")
    do_cond = parse_statement()
    expect("endwhile")
    return ast("WHILE-LOOP", [while_cond, do_cond])
                    

def parse_program(outfile):
    global tokens, pos
   
    for tok, tok_type in tokens:
        print(f"{tok} : {tok_type}")
        outfile.write(f"{tok} : {tok_type}\n")
    print("AST:")
    outfile.write("\nAST\n")
    tree = parse_statement()
    for line in tree.print_tree():
        print(line)
        outfile.write(line + "\n")
    
    memory = {}
    t = tree
    while t is not None:
        t, memory = eval_stmt(t, memory)

    # 4. Print final memory state
    print("Output:")
    outfile.write("\nOutput:\n")
    # Print in deterministic order
    for name in sorted(memory.keys()):
        line = f"{name} = {memory[name]}"
        print(line)
        outfile.write(line + "\n")
        
    tokens.clear()
    pos = 0
        