# This program reads a source file of commands.
# Each line of the file is tokenized into a array (list).
# A new list is created by examining each token and identify its token code.
# For example, A EQ 5; is translated into ["Variable", "Equator", "Number", ";"]
# This new list is evaluated for its syntax.
# Many commands involve a subexpression. For example, A EQ OPENPAREN 17 MUL 7 ADD 5 CLOSEPAREN.
# In this case, the OPENPENPAREN 17 MUL 7 ADD 5 CLOSEPAREN is the subexpression.
# Subexpressions can be arbitrarily long, and conditionals and loops can have more than one subexpression.
# As each statement is evaluated, subexpressions are identified and evaluated with the evaluate_subexpression function.
# Subexpressions have rules too. For example, a OPENPAREN must be followed by a Number or a Variable.
# Every input line is printed out. If there are no errors, the line is simply reprinted.
# If there are errors, an error message is printed along with the line itself.

import re

def evaluate_token(token):
    if token in ['tiny','small','medium','large']:
        return "Declaration"
    elif token in ['LST','GRT','LSTE','GRTE','EQ','NEQU']:
        return "Equator"
    elif token == 'OPENPAREN':
        return "OPENPAREN"
    elif token == 'CLOSEPAREN':
        return "CLOSEPAREN"
    elif token in ['ADD','SUB','MUL','DIV','MODULUS']:
        return "Operator"
    elif token == "COND":
        return "Conditional"
    elif token == "REPEAT":
        return "Loop"
    elif token == "=":
        return "Assignment"
    elif re.match("[0-9]+",token):
        return "Number"
    elif len(token) < 10 and re.match("^[a-zA-Z]+.*",token) and re.match("^[a-zA-Z0-9_-]*$", token):
        return "Variable"
    else:
        return "Error Unknown Token"

def evaluate_subexpression(sub_expression_list):
    count_openparens = sub_expression_list.count("OPENPAREN")
    count_closeparens = sub_expression_list.count("CLOSEPAREN")
    if count_openparens != count_closeparens:
       return "Error: Paren Count Mismatch in line "
    elif sub_expression_list[-1] in ["Operator","OPENPAREN"]:
       return "Error: Subexpression Syntax Error in line "
    else:
       x = 0
       while x < len(sub_expression_list) - 2:
          if sub_expression_list[x] == "OPENPAREN" and sub_expression_list[x+1] not in ["Number","Variable"]:
             return "Error: Subexpression Syntax Error in line "
          elif sub_expression_list[x] == "CLOSEPAREN" and sub_expression_list[x+1] not in ["Operator",";"]:
             return "Error: Subexpression Syntax Error in line "
          elif sub_expression_list[x] == "Number" and sub_expression_list[x+1] not in ["Operator","CLOSEPAREN",";"]:
             return "Error: Subexpression Syntax Error in line "
          elif sub_expression_list[x] == "Operator" and sub_expression_list[x+1] not in ["Number","Variable","OPENPAREN"]:
             return "Error: Subexpression Syntax Error in line "
          x = x + 1
    return None

file = open('SourceCode', 'r')
lines = file.readlines()

# Read Each Line Of Source Code
for line in lines:
    #Parse Line into Tokens
    tokens = line.split()
    token_code_list = []
    for x in range(len(tokens)):
        if x == len(tokens) - 1:
           if token_code_list[0] in ["Conditional","Loop"]:
              token_code_list.append(evaluate_token(tokens[x].rstrip(":")))
           else:
              token_code_list.append(evaluate_token(tokens[x].rstrip(";")))
        else:
           token_code_list.append(evaluate_token(tokens[x]))
        if x == len(tokens) - 1:
           if token_code_list[0] in ["Conditional","Loop"]:
              if line[-2] == ":":
                 token_code_list.append(":")
           elif line[-2] == ';':
              token_code_list.append(';')
    if token_code_list[0] in ["Conditional","Loop"]:
       if token_code_list[-1] != ':':
          print("Error: Colon must end Conditional or Loop in line " + line)
          continue
    elif token_code_list[-1] != ';':
       print("Error: No end of line in line " + line)
       continue
    if token_code_list[0] == "Declaration":
       if len(token_code_list) != 3:
          print("Error: Invalid Type Declaration in line " + line)
       else:
          print(line)
    elif token_code_list[1] == "Assignment":
        if token_code_list[0] != "Variable":
          print("Error: First Token Must be Variable in line " + line)
        else:
          result = evaluate_subexpression(token_code_list[2:len(token_code_list) -1])
          if result is not None:
            print(result + line)
          else:
            print(line)
    elif token_code_list[0] in ["Conditional","Loop"]:
         count_equators = token_code_list.count("Equator")
         if count_equators == 0:
            print("Error: No Equators in line " + line)
         elif count_equators > 1:
            print("Error: Too Many Equators in line " + line)
         equator_index = token_code_list.index("Equator")
         result = evaluate_subexpression(token_code_list[1:equator_index])
         if result is not None:
            print(result + line)
         result = evaluate_subexpression(token_code_list[equator_index + 1: len(token_code_list) - 1])
         if result is not None:
            print(result + line)
         else:
            print(line)
    else:
       print(token_code_list)

file.close()
