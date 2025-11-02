import sys
import re
import parser_module

# regex pattern matching
#if the pattern matches (?P) call it by <NAME>
TOKEN_REGEX = re.compile(r"""
    (?P<WHITESPACE>\s+)
  |  (?P<KEYWORD>\b(if|then|else|endif|while|do|endwhile|skip)\b)
  | (?P<IDENTIFIER>[a-zA-Z][a-zA-Z0-9]*)
  | (?P<NUMBER>[0-9]+)
  | (?P<SYMBOL>\+|\-|\*|/|\(|\)|:=|;)
  | (?P<INVALID>.)
""", re.VERBOSE)

def main():
    if len(sys.argv) < 3:
        print("console format: python scanner.py <inputfile> <outputfile>")
        return
    
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    try:
        with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
            
            for line in infile:
                for token, typ in scanner(line): #passes the line to scanner function that yields a token and token type
                    #print(f"{token} : {typ}")
                    parser_module.tokens.append((token,typ))
            parser_module.parse_program(outfile)
                
            
    except FileNotFoundError:
        print(f"The file '{input_filename}' was not found")
    except Exception as e:
        print(f"Error occurred {e}")

def scanner(line):
    for match in TOKEN_REGEX.finditer(line): # iterates through the line and checks if there's a match in the regex object
        token_type = match.lastgroup  # Name of the group matched
        token = match.group(token_type) # the token that matched the group
        if token_type == "WHITESPACE":
            continue
        elif token_type == "INVALID":
            yield token, "ERROR"
        else:
            yield token, token_type

if __name__ == "__main__":
    main()