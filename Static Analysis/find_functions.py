
def find():
    import parse_bandit
    from pytaint_test import ast_trace

    bandit_output = parse_bandit.parse_output()
    dict_return = {}

    for ind in range(len(bandit_output)):
        d, list_line_numbers, list_functions = ast_trace.parseAST(bandit_output[ind][3], bandit_output[ind][1])

        for item in range(len(list_line_numbers)):
            list_line_numbers[item] = list_line_numbers[item] - 1

        variable_functions = []


        with open(bandit_output[ind][3]) as fp:
            for i, line in enumerate(fp):
                if i not in list_line_numbers:
                    continue
                else:
                    for func in list_functions:
                        if func in line:
                            count = 0
                            ind_first = line.find(func)
                            if line[ind_first-1] == '.':
                                for x in range(10):
                                    if line[ind_first-x] != ' ' and line[ind_first-x] != '(':
                                        count += 1
                                    else:
                                        break
                                variable_functions.append(line[ind_first - count + 1:ind_first + len(func)])
                            else:
                                variable_functions.append(func)

        dict_return[bandit_output[ind][3]] = variable_functions
    print(dict_return)
    return dict_return



if __name__ == "__main__":
    find()