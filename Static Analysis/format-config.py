# format pytaint configure file
'''
{
  "cleaners": [
    {"merit": "ShellMerit"},
     "pipes.quote"],
  "sinks": [
    {"merit": "HtmlMerit"},
     "Handler.send_response",
    {"merit": "SecretMerit"},
     "Handler.send_response",
    {"merit": "PickleMerit"},
     "pickle.loads",
    {"merit": "ShellMerit"},
     "commands.getoutput"
     ],
  "sources": [
     "Handler.get_parameters"
    ],
  "propagators": [
     "hashlib.md5"
    ]
}
'''

def format(sink, source, bandit_id):
	f = open("test.json", "w+")
	mtmap = {1: "ShellMerit"}
	# merit = mtmap[bandit_id]
	merit = ["ShellMerit", "PickleMerit"]

	num_sinks = len(sink)
	num_srcs = len(source)


	conf = ""
	conf += """{\n\t"sinks": ["""
	for i in range(0, num_sinks):
		conf += '''\n\t{{"merit": "{}"}},\n\t "{}"'''.format(merit[0], sink[i])

		if(i != num_sinks-1):
			conf += ","
		else:
			conf += "],\n\t"

	conf += """"sources": ["""
	for j in range(0, num_srcs):
		conf += '''\n\t"{}"'''.format(source[j])

		if(j != num_srcs-1):
			conf += ","
		else:
			conf += "],\n}\n"


	# conf = '''{{\n\t"cleaners": [\n\t{{"merit": {}}},\n\t "pipes.quote"],\n\t"sinks": [\n\t{{"merit": {}}},\n\t {}],\n\t"sources": [\n\t{}]\n}}\n'''.format(merit, merit, sink, source)

	f.write(conf)
	f.close()





def test1():
	format("raw_input", "os.system", 1)

def test2():
	format(["Handler.send_response", "Handler.send_response", "pickle.loads", "commands.getoutput"], ["src1", "src2", "src3"], [2, 1, 5])



if __name__ == '__main__':
	test2()
