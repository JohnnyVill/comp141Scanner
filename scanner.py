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
    for n in line:
        if n != " ":
            token += n
        else:
            print(token)
            token = ""
    print(token)
           
    
if __name__ == "__main__":
    main()