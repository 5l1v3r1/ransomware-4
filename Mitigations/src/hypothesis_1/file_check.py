import yara
import argh

def callback_func(data):
	print
	print "(*) Tags: " + str(data['tags'])
	print "(*) Matches: " + str(data['matches'])
	print "(*) Namespace: " + str(data["namespace"])
	print "(*) Rule: " + str(data["rule"])
	print "(*) Meta: " + str(data["meta"])
	print "(*) Strings: " + str(data["strings"])
	yara.CALLBACK_CONTINUE

def matching(rule, target):
	compiled_rule = yara.compile(rule)
	if target.isdigit():
		matches = compiled_rule.match(pid=int(target), callback=callback_func)
	else:
		matches = compiled_rule.match(target, callback=callback_func)

parser = argh.ArghParser()
parser.add_commands([matching])

if __name__ == "__main__":
	parser.dispatch()
