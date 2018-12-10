import parse_bandit
from pytaint_test import ast_trace

bandit_output = parse_bandit.parse_output()

d, list_line_numbers, list_functions = ast_trace.parseAST(bandit_output[0][3], bandit_output[0][1])

for item in range(len(list_line_numbers)):
    list_line_numbers[item] = list_line_numbers[item] - 1

print(list_line_numbers)

variable_functions = []


with open(bandit_output[0][3]) as fp:
    for i, line in enumerate(fp):
        if i not in list_line_numbers:
            continue
        else:
            for func in list_functions:
                print(i, line)
                if func in line:
                    variable_functions.append(func)


print(variable_functions)