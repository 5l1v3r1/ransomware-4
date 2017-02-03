import sys
import time
import hashlib
import os
import datetime
import psutil
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

god_dict = {}
malicious_list = []
ignored_process = ["System Idle Process",
"System",
"smss.exe",
"csrss.exe",
"SearchIndexer.exe",
"wininit.exe",
"winlogon.exe",
"services.exe",
"lsass.exe",
"lsm.exe",
"svchost.exe"
"VBoxService.exe",
"spoolsv.exe"
]
counter_alert = 0

class Watcher(FileSystemEventHandler):
	global god_dict, malicious_list
	def process(self, event):
		global counter_alert
		time = datetime.datetime.now()
		if "." in str(event.src_path):
			path = str(event.src_path)[:str(event.src_path).rfind("\\")]
			path_with_file = str(event.src_path)
			path_md5 = hashlib.md5(path).hexdigest()
			if not path_md5 in god_dict:
				god_dict[path_md5] = [str(path), 1, calculate_red_flag(str(path)), time]
			else:
				god_dict[path_md5][1] += 1
				if god_dict[path_md5][1] is god_dict[path_md5][2]: # Problem
					diff_time = time - god_dict[path_md5][3]
					if diff_time.microseconds < 0.3 and diff_time.seconds == 0:
						print "Suspicious files modified on " + path
						if counter_alert == 10:
							find_them_kill_them(get_current_process())
						else:
							counter_alert += 1
					else:
						god_dict[path_md5][1] = 0
				else:
					pass
			god_dict[path_md5][3] = time
		else:
			# path = str(event.src_path)
			pass

	def on_modified(self, event):
		self.process(event)

def calculate_red_flag(abs_path):
		red_flag = 0
		for root, dirs, files in os.walk(abs_path):
			if not files:
				red_flag += 1
			else:
				red_flag += 1
				for each_file in files:
					red_flag +=1
		return int(red_flag)

# def is_sigcheck_setup():
# 	if os.listdir(".").find("sigcheck.exe") or os.listdir(".").find("sigcheck64.exe"):
# 		return True
# 	else:
# 		return False

# def sigcheck(file_path):
# 	if is_sigcheck_setup():
# 		# print "(*) Verify program's digital signature"
# 		output = subprocess.check_output(["sigcheck.exe", filepath])
# 		output = output.split()
# 		if output[output.index("Verified:")+1] is "Signed":
# 			return True
# 		if output[output.index("Verified:")+1] is "Unsigned":
# 			return False
# 	else:
# 		print "(!) sigcheck.exe or sigcheck64.exe not found!"
# 		sys.exit(0)

def get_readable_time_format(unreadable_time):
	return datetime.datetime.fromtimestamp(unreadable_time).strftime("%d-%m-%Y %H:%M:%S")

def get_current_process():
	process_dict = {}
	for processes in psutil.process_iter():
		try:
			process_info = processes.as_dict(attrs=["pid", "name", "create_time"])
		except psutil.NoSuchProcess:
			pass
		else:
			process_dict[process_info["pid"]] = [process_info["name"], get_readable_time_format(process_info["create_time"])]
	return process_dict

def find_them_kill_them(process_dict):
	for key, value in process_dict.iteritems():
		if not value[0] in ignored_process:
			malicious_list.append([key, value[0], value[1]])
	malicious_list.sort(key=lambda x: x[2])
	print "(*) Suspicious processes"
	print
	print "PID".ljust(20, ' ') + "Name".ljust(20, ' ') + "Create Time".ljust(20, ' ')
	print "="*52
	for index in xrange(0, len(malicious_list)-1):
		print str(malicious_list[index][0]).ljust(20, ' ') + str(malicious_list[index][1]).ljust(20, ' ') + str(malicious_list[index][2]).ljust(20, ' ')
	print
	kills = input("(?) Kill any process? [PID] > ")
	try:
		process = psutil.Process(kills)
		process.kill()
		sys.exit(0)
	except psutil.NoSuchProcess:
		pass
		sys.exit(1)

if __name__ == "__main__":
	observer = Observer()
	path = raw_input("(?) Input path to monitor > ")
	# if is_sigcheck_setup():
	# 	pass
	# else:
	# 	print "(!) sigcheck.exe or sigcheck64.exe are not found on running directories, some feature will not work"
	observer.schedule(Watcher(), path, recursive = True)
	observer.start()

	try:
		while True:
			# print god_dict
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()

	observer.join()
