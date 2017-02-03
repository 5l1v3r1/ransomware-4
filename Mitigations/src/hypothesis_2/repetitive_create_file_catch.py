from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import datetime
import hashlib
import sys

global_dict = {}
limit = 3

class Watcher(FileSystemEventHandler):
    global global_dict, limit

    def check(self):
        counter = 0 # others hash_data repetition?
        for hash_data in global_dict.keys():
            if global_dict[hash_data][1] is limit:
                counter += 1
        if counter is not 3: # png, txt, html must be exceeded limit at the same time
            return False
        else:
            return True

    def hashing(self, file_name):
        try:
            hasher = hashlib.md5()
            with open(file_name, "rb") as target:
                buf = target.read()
                hasher.update(buf)
            return hasher.hexdigest()
        except IOError:
            pass

    def process(self, event):
        if os.path.isfile(event.src_path):
            hash_path = hashlib.md5(event.src_path[:event.src_path.rfind("\\")]).hexdigest()
            hash_data = self.hashing(event.src_path)
            if not hash_data in global_dict.keys():
                global_dict[hash_data] = [[hash_path], 1]
            else:
                if not hash_path in global_dict[hash_data][0]:
                    global_dict[hash_data][0].append(hash_path)
                    global_dict[hash_data][1] = len(global_dict[hash_data][0])
                else:
                    pass
            if self.check():
                print "(!) " + datetime.datetime.now().strftime("%H:%M:%S") + " Possibly repetitive files created!"
                print "(!) File(s): " + event.src_path[event.src_path.rfind("\\")+1:]
                sys.exit(0)
        else:
            pass

    def on_created(self, event):
		self.process(event)

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(Watcher(), path = raw_input("(?) Path > ") , recursive = True)
    observer.start()

    try:
		while True:
			time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()