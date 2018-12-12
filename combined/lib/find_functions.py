import parse_bandit
import ast_trace
import os, sys

def find():

    bandit_output = parse_bandit.parse_output()
    print(bandit_output)
    dict_return = {}
    var_return = {}

    for ind in range(len(bandit_output)):
        d = ast_trace.parseAST(bandit_output[ind][3], bandit_output[ind][1])
        # print(d)
        # for item in range(len(list_line_numbers)):
        #     list_line_numbers[item] = list_line_numbers[item] - 1

        # variable_functions = []


        # with open(bandit_output[ind][3]) as fp:
        #     for i, line in enumerate(fp):
        #         if i not in list_line_numbers:
        #             continue
        #         else:
        #             for func in list_functions:
        #                 if func in line:
        #                     ind_first = line.find(func)
        #                     variable_functions.append(func)

        # dict_return[bandit_output[ind][3]] = variable_functions
        if bandit_output[ind][3] not in dict_return:
            dict_return[bandit_output[ind][3]] = set()
        for i in d:
            dict_return[bandit_output[ind][3]].add(i)


        if bandit_output[ind][3] not in var_return:
            var_return[bandit_output[ind][1]] = set()
        for i in d:
            var_return[bandit_output[ind][1]].add(i)


    print(dict_return)
    print(var_return)
    return dict_return, var_return

def get_sanitizers():
    path = os.path.dirname(os.path.abspath(__file__))
    file = path + '/sanitizers.txt'
    sanitizers = []
    with open(file, 'r') as f:
        content = f.readlines()
        sanitizers = [x.strip() for x in content] 
    return sanitizers



if __name__ == "__main__":
    find()
