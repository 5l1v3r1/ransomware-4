import psutil
import datetime
import time
import os
import yara
import argh

class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)
    def added(self):
        return self.set_current - self.intersect
    def removed(self):
        return self.set_past - self.intersect
    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])

def matching(rule, target):
    compiled_rule = yara.compile(rule)
    matches = compiled_rule.match(pid=int(target))
    if len(matches) > 0:
        print "(!) " + datetime.datetime.now().strftime("%H:%M:%S") + " " + str(get_process_name(target)) + " is probably " + str(matches[0])
        print "(!) Kill " + str(get_process_name(target))
        kill_process(target)

def get_current_process():
    process_dict = {}
    for process in psutil.process_iter():
        try:
            process_info = process.as_dict(attrs=["pid", "name", "create_time"])
        except psutil.NoSuchProcess:
            pass
        else:
            process_dict[process_info["pid"]] = [process_info["name"],
                datetime.datetime.fromtimestamp(process_info["create_time"]).strftime("%d-%m-%Y %H:%M:%S")]
    return process_dict

def get_process_name(pid):
    try:
        process = psutil.Process(pid)
        return process.name()
    except psutil.NoSuchProcess:
        pass

def kill_process(pid):
    try:
        process = psutil.Process(pid)
        return process.kill()
    except psutil.NoSuchProcess:
        pass

def monitoring(rule):
    try:
        init_dict = get_current_process()
        while True:
            snap_dict = get_current_process()
            if snap_dict != init_dict:
                diff_dict = DictDiffer(snap_dict, init_dict)
                for pid in diff_dict.added():
                    matching(rule, pid)
            init_dict = snap_dict
            time.sleep(1)
    except KeyboardInterrupt:
        print "(!) Exit"

parser = argh.ArghParser()
parser.add_commands([monitoring])

if __name__ == "__main__":
    parser.dispatch()
