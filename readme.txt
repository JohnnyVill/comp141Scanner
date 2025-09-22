How to run:

the terminal require you to pass in an input file and name output file to write in, if no output file exist it will create one with the name you input.
    ex:
    python scanner.py <file name>.txt <file name>.txt

The first argument is designated as the input file and the second is the output file

How the program works:

1st: The program read the input file line by line, it initial write the line it is going to parse to the outfile then call the scanner function on that line.
2nd: The scanner function takes a brute force apporach and read each character in the line and builds the token until it sees a space or a symbol then calls the parse function on the token.
3rd: The parse function has the set of rules defined in variable then iterate through the if statments to see if the token match one of the rules amd write the token and the token type to the outfile