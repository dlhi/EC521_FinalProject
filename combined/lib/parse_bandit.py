#!/usr/bin/env python3
"""
This script  extracts relevant information from a text file that contains output from bandit
"""
import os

def parse_output():
    vulnerabilities = ['B102', 'B608', 'B605']
    path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.dirname(path) + "/b_output.txt"
    file = open(filename, "r")

    vuln_ids = []
    sinks = []
    sources = []
    paths = []
    line_numbers = []

    new_id = 0
    for line in file:
        if "Issue" in line:
            if line[11:15] in vulnerabilities:
                vuln_ids.append(line[11:15])
                new_id = 1
            continue

        if "exec(" in line and new_id or "exec (" in line and new_id:
            ind_exec = line.find("exec")
            ind_par = line.find(')', ind_exec)
            sinks.append("exec")
            sources.append(line[ind_exec+5:ind_par])
            new_id = 0
            continue


        if "execute(" in line and new_id or "execute (" in line and new_id:
            ind_execute = line.find("execute")
            ind_last_space = line.rfind(' ', 0, ind_execute)
            sinks.append(line[ind_last_space+1:ind_execute] + "execute")
            sources.append(line[line.rfind('%', ind_execute)+1:line.find(')')])
            new_id = 0
            continue

        if "os.system(" in line and new_id or "os.system (" in line and new_id:
            sinks.append("os.system")
            ind_first_par = line.find("(", line.find("os.system"))
            ind_sec_par = line.find(")", ind_first_par)
            sources.append(line[ind_first_par+1:ind_sec_par])
            new_id = 0
            continue

        if "Location" in line and new_id:
            ind_location = line.find("Location")
            paths.append(line[ind_location+10:line.find(':', ind_location+10)])
            line_numbers.append(line[line.find(':', ind_location+10)+1:-1])
            continue

        # print(line.split('('))


    list_vulns = []    # (ID, Source, Sink, Path, Line #)
    print(sources)
    for i in range(len(vuln_ids)):
        if sources[i].__contains__("("):
            sources[i] = sources[i].replace("(", "")

        if sources[i].__contains__(" "):
            sources[i] = sources[i].replace(" ", "")

        list_vulns.append((vuln_ids[i], sources[i], sinks[i], paths[i], line_numbers[i]))

    # print(list_vulns)
    return list_vulns



if __name__ == '__main__':
    parse_output()
