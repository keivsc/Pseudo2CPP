# Pseudo2CPP
A very scuffed python script that converts CAIE Syntax Pseudocode to C++

Current Features
IF
SWITCH-CASE
FOR
PROCEDURES
FUNCTIONS
OUTPUT

Learn about the syntax [here](https://learnlearn.uk/alevelcs/wp-content/uploads/sites/20/2020/09/9608_PSEUDOCODE_GUIDE.pdf)

Example Code
```
PROCEDURE countdown(end : INTEGER)
    FOR Ind = 1 TO 30
    OUTPUT Ind
    ENDFOR Index
ENDPROCEDURE
```

Convert by running 
```console
foo@bar:~$ compilePSC.py {file.txt}
```

