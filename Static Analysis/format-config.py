"""
This module automatically formats a pytaint configure file, given processed bandit output as input
"""
def format(bandit_out):
	mtmap = {"B605": "ShellMerit", "B608": "SQLiMerit", "bandit_id3" : "HtmlMerit", "B102": "ShellMerit"}
	f = open("test.json", "w+")

	merit = []
	source = []
	sink = []

	for i in bandit_out:
		merit.append(mtmap[i[0]])
		source.append(i[1])
		sink.append(i[2])

	num_sinks = len(sink)
	num_srcs = len(source)


	conf = ""
	conf += '''{\n\t"sinks": ['''
	for i in range(0, num_sinks):
		conf += '''\n\t{{"merit": "{}"}},\n\t "{}"'''.format(merit[i], sink[i])

		if(i != num_sinks-1):
			conf += ","
		else:
			conf += "],\n\t"

	conf += '''"sources": ['''
	for j in range(0, num_srcs):
		conf += '''\n\t"{}"'''.format(source[j])

		if(j != num_srcs-1):
			conf += ","
		else:
			conf += "],\n}\n"


	# conf = '''{{\n\t"cleaners": [\n\t{{"merit": {}}},\n\t "pipes.quote"],\n\t"sinks": [\n\t{{"merit": {}}},\n\t {}],\n\t"sources": [\n\t{}]\n}}\n'''.format(merit, merit, sink, source)

	f.write(conf)
	f.close()


"""
Test function - input is a list of tuples of strings

Example Output Config file:
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


"""
def test():
	format([("B605", "src1", "os.system", "/home", "45"), ("B608", "src2", "sql_something", "/hom/ls", "812")])


if __name__ == '__main__':
	test()