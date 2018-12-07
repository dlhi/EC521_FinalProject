#!/Users/andregonzaga/Desktop/pytaint/Python-2.7.5-pytaint/python.exe
"""
This script  extracts relevant information from a text file that contains output from bandit
"""
vulnerabilities = ['B102', 'B608']
filename = "b_output.txt"
file = open(filename, "r")

vuln_ids = []
sinks = []
sources = []
new_id = 0
for line in file:
    if "Issue" in line:
        if line[11:15] in vulnerabilities:
            vuln_ids.append(line[11:15])
            new_id = 1
        continue

    if "exec(" in line and new_id:
        ind_exec = line.find("exec(")
        ind_par = line.find(')', ind_exec)
        sinks.append("exec")
        sources.append(line[ind_exec+5:ind_par])
        new_id = 0
        continue


    if "execute(" in line and new_id:
        ind_execute = line.find("execute(")
        ind_last_space = line.rfind(' ', 0, ind_execute)
        sinks.append(line[ind_last_space+1:ind_execute] + "execute")
        sources.append(sinks[-1][0:sinks[-1].find('.')])
        new_id = 0
        continue

print "IDs"
print vuln_ids
print ""
print "Sources"
print sources
print  ""
print "Sinks"
print sinks
