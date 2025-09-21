import sys
import re

def main():
    # Check if argument passed in terminal was invalid
    if len(sys.argv) < 3:
        print("Usage: python scanner.py <inputfile> <outputfile>")
        return
    
    try:
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
        with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
            for line in infile: 
                print("\n" + line.strip())
                outfile.write("Line: " + line)
                scanner(line,outfile)
                outfile.write("\n")
                
          
        print(f"Content from '{input_filename}' written to '{output_filename}'")   
    except FileNotFoundError:
        print(f"The file '{input_filename}' was not found")
    except Exception as e:
        print(f"Error occured {e}")

# Scanner use to check if the token if valid or invalid, then sends token to parser
def scanner(line,outfile):
    token = ""
    
    # This loop build the token up until it sees a white space
    # prints the currently built token upon seeing a white space
    for n in line:
        if n == " ":
           if token:
               print(parse(token,outfile))
               token = ""
        else:
            if token and (token[0].isdigit() and n.isalpha()):
                print(parse(token,outfile))
                token = n
            elif token and ((n == "&" or n == ".")):
                print(parse(token,outfile))
                token = n
            else:
                token += n
    
    # prints the last token in the string since no white space will come after
    print(parse(token,outfile))

# Parse get the valid token and write/return the type of token that was passed
def parse(token,outfile):
    identifier = re.search(r"[a-zA-Z_][a-zA-Z0-9_]*$",token)
    symbol =  re.search(r"[\( | \) | \+ | \* | \- | \% | \/| \{ | \} | \=]+",token)
    number = re.search(r"[0-9]+",token)
    invalid = re.search(r"[\&|\.]", token)
  
    if identifier:
        outfile.write(f"{identifier.group()} : IDENTIFIER" + "\n")
        return(identifier.group() + " : IDENTIFIER")
    if symbol:
        outfile.write(f"{symbol.group()} : SYMBOL" + "\n")
        return(symbol.group() + " : SYMBOL")
    if number:
        outfile.write(f"{number.group()} : NUMBER" + "\n")
        return(number.group() + " : NUMBER")
    if invalid:
        outfile.write(f"ERROR READING : {invalid.group()}" +"\n")
        return(f"ERROR READING : {invalid.group()}")
        
   
  
    
    
if __name__ == "__main__":
    main()