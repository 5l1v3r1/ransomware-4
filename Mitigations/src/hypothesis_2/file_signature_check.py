from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import datetime
import yara

global_dict = {}
rules_dir = ""

class Watcher(FileSystemEventHandler):
    global global_dict, rules_dir

    def process(self, event):
        if os.path.isfile(event.src_path):
            path = event.src_path[:event.src_path.rfind("\\")]
            file_name = event.src_path[event.src_path.rfind("\\"):]
            file_ext = event.src_path[event.src_path.rfind(".")+1:]

            if file_ext in ["JFIF", "JPE", "JPEG", "JPG", "jfif", "jpe", "jpeg", "jpg"]:
                self.check("jpeg.yar", event.src_path)
            elif file_ext in ["PDF", "FDF", "pdf", "fdf"]:
                self.check("pdf.yar", event.src_path)
            elif file_ext in ["PNG", "png"]:
                self.check("png.yar", event.src_path)
            else:
                pass

        else:
            pass

    def check(self, rule, target):
        try:
            compiled_rule = yara.compile(os.path.join(rules_dir, rule))
            matches = compiled_rule.match(target)
            if len(matches) is 0:
                print "(!) " + datetime.datetime.now().strftime("%H:%M:%S") + " " + target + " is corrupted or possibly encrypted!"
        except:
            print "(!) " + datetime.datetime.now().strftime("%H:%M:%S") + " Unable to open " + target + ". Race condition?"

    def on_modified(self, event):
		self.process(event)

if __name__ == "__main__":
    rules_dir = raw_input("(?) Yara rules directory > ")
    observer = Observer()
    observer.schedule(Watcher(), path = raw_input("(?) Path > ") , recursive = True)
    observer.start()

    try:
		while True:
			time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()