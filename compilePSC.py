import ast, re, sys, os, textwrap
# This program compiles CAIE Syntax Pseudocode to C++ Source
# To run this do "compilePSC.py {filename} {-r (run code WIP)}"

data_types = {"INTEGER":"int", "REAL":"float", "CHAR":"char*", "STRING": "string", "BOOLEAN":"bool", "DATE":"date", "integer":"int", "real":"float", "char":"char*", "string": "string", "boolean":"bool", "date":"date"}

classes = {"ENDTYPE":"}", "TYPE": "class VAR {\npublic:"}

replacements = {"'": '"', "ꞌ": "'", "←":"=", "":"=", "OTHERWISE":"default", "BYREF":"", "BYVALUE":"", "Temp": "int Temp;\nTemp", "THEN":"", "ELSE":"}else{", "RETURN ":"return "}

start_case = False

file = open(os.path.dirname(os.path.abspath(__file__))+"\\"+sys.argv[1], 'r').readlines()
parsed = ""
for line in file:
    line = ' '.join(line.split(' '))
    for k, v in data_types.items():
        if k in line:
            line = line.replace(k, v)

    for k, v in classes.items():
        if k in line:
            line = v.replace("VAR", line.replace("TYPE ", ""))

    for k, v in replacements.items():
        if k in line:
            line = line.replace(k, v)

    if "CALL" in line:
        line = line.replace("CALL ", "")
        if not ")" in line:
            line += "()"

    if "IF" in line:
        line = line.replace("IF ", "")
        line = f"if ({line}){'{'}"

    if "FUNCTION" in line:
        line = line.replace("FUNCTION", "auto")
        if "(" not in line:
            line += "= [](){"
        else:
            final = line.split("(")[0]+"= []("
            args = line.split("(")[1].split(")")[0]
            args = args.split(',')
            argv = []
            for arg in args:
                arg = arg.split(":")
                argv.append(f"{arg[1]} {arg[0]}")
            line = final + ",".join(argv) + "){"

    if "PROCEDURE" in line:
        line = line.replace("PROCEDURE ", "auto ")
        if "(" not in line:
            line += "= [](){"
        else:
            final = line.split("(")[0]+"= []("
            args = line.split("(")[1].split(")")[0]
            args = args.split(',')
            argv = []
            for arg in args:
                arg = arg.split(":")
                argv.append(f"{arg[1]} {arg[0]}")
            line = final + ",".join(argv) + "){"

    if line.startswith("ENDCASE"):
        line = "}"
        start_case=False

    if start_case and not line.startswith('default'):
        line = "case " + line + "; break"

    if line.startswith("CASE"):
        start_case = True
        line = line.replace("CASE OF ", "switch(")
        line += "){"

    if "INPUT" in line:
        var = line.replace("INPUT ", "")
        line = f"string {var};\ncin >> {var}"

    if "OUTPUT" in line or "PRINT" in line:
        line = line.replace("OUTPUT", "cout <<")
        line = line.replace("PRINT", "cout <<")
        line = line.replace('", "', '"<< "')
        line += " << endl"

    if line.startswith("END"):
        line = "}"
    
    if "FOR" in line:
        line = line.replace("FOR ", "")
        lineSplit = line.split(" = ")
        lineSplit2 = lineSplit[1].split(" TO ")
        var = lineSplit[0]
        start = lineSplit2[0]
        end = lineSplit2[1]
        line = f"for( int {var} = {start}; {var} <= {end}; ++{var} ) {'{'}"


    if "ARRAY" in line:
        line = line.replace("DECLARE ", "")
        lineSplit = line.split(" OF ")
        lineSplit2 = lineSplit[0].split(":", 1)
        Type = lineSplit[1]
        ID = lineSplit2[0]
        lenT = lineSplit2[1].replace("ARRAY", "")[1:-1]
        if "," in lineSplit2[1]:
            Length = ""
            lenSplit = lenT.split(",")
            for l in lenSplit:
                Length += f"[{l.split(':')[1]}]"
        elif ":" in lineSplit2[1]:
            Length = "[" + lineSplit2[1].split(':')[1]
        else:
            Length = f"[{lenT}]"
        line = f"{Type} {ID}{Length}"

    if re.search("\[(\w+|\d+),(\w+|\d+)\]", line):
        line = line.replace(',', '][')


    re_search = re.search("([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}", line)
    if re_search:
        line = line.replace(str(re_search.group()), f'"{re_search.group()}"')

    if line.startswith("DECLARE"):
        lineSplit = line.split(" : ")
        lineSplit[0] = lineSplit[0].replace("DECLARE ", "")
        line = f"{lineSplit[1]} {lineSplit[0]}"

    if line.startswith("CONSTANT"):
        Type = ((type(ast.literal_eval(line.split("= ")[1]))).__name__).replace('str', 'string')
        line = line.replace("CONSTANT", f"const {Type}")

    if len(line)>0:
        line = line.strip()
        if len(line)>0 and line[-1] not in ['{', '[', ':']:
            line += ';'
        parsed += line + "\n"

f = open(os.path.dirname(os.path.abspath(__file__))+"\\compiled.cpp", "w+")
f.write(f"""#include <iostream>
using namespace std;
typedef string date;
int main(){{
  //psc code
  {parsed}
  return 0;
}}
""")
f.close()