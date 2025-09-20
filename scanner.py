import fileinput
import re

def main():
    input_filename = "test_input.txt"
    output_filename = "test_output.txt"
    
    try:
        with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
            for line in infile:
                read_line = line
                print(read_line)
                scanner(read_line)
                outfile.write(read_line)
                
          
        print(f"Content from '{input_filename}' written to '{output_filename}'")   
    except FileNotFoundError:
        print(f"The file '{input_filename}' was not found")
    except Exception as e:
        print(f"Error occured {e}")

def scanner(line):
    token = ""
    
    # This loop build the token up until it sees a white space
    # prints the currently built token upon seeing a white space
    for n in line:
        if n == " ":
           if token:
               print(parse(token))
               token = ""
        else:
            if token and (token[0].isdigit() and n.isalpha()):
                print(parse(token))
                token = n
            else:
                token += n
    
    # prints the last token in the string since no white space will come after
    print(parse(token))

def parse(token):
    identifier = re.search(r"[a-zA-Z_][a-zA-Z0-9_]*$",token)
    symbol =  re.search(r"[\( | \) | \+ | \* | \- | \% | \/| \{ | \} | \=]+",token)
    number = re.search(r"[0-9]+",token)
  
    if identifier:
        return (identifier.group(), "identifier")
    if symbol:
        return (symbol.group(), "symbol")
    if number:
        return(number.group(), "number")
  
    
    
if __name__ == "__main__":
    main()