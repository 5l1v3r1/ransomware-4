# -*- coding: utf-8 -*-
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import datetime

global_dict = {}
file_ext_list = [".7z", ".rar", ".m4a", ".wma", ".avi", ".wmv", ".csv", ".d3dbsp", ".sc2save", ".sie", ".sum", ".ibank", ".t13", ".t12", ".qdf", ".gdb", ".tax", ".pkpass", ".bc6", ".bc7", ".bkp", ".qic", ".bkf", ".sidn", ".sidd", ".mddata", ".itl", ".itdb", ".icxs", ".hvpl", ".hplg", ".hkdb", ".mdbackup", ".syncdb", ".gho", ".cas", ".svg", ".map", ".wmo", ".itm", ".sb", ".fos", ".mcgame", ".vdf", ".ztmp", ".sis", ".sid", ".ncf", ".menu", ".layout", ".dmp", ".blob", ".esm", ".001", ".vtf", ".dazip", ".fpk", ".mlx", ".kf", ".iwd", ".vpk", ".tor", ".psk", ".rim", ".w3x", ".fsh", ".ntl", ".arch00", ".lvl", ".snx", ".cfr", ".ff", ".vpp_pc", ".lrf", ".m2", ".mcmeta", ".vfs0", ".mpqge", ".kdb", ".db0", ".DayZProfile", ".rofl", ".hkx", ".bar", ".upk", ".das", ".iwi", ".litemod", ".asset", ".forge", ".ltx", ".bsa", ".apk", ".re4", ".sav", ".lbf", ".slm", ".bik", ".epk", ".rgss3a", ".pak", ".big", ".unity3d", ".wotreplay", ".xxx", ".desc", ".py", ".m3u", ".flv", ".js", ".css", ".rb", ".png", ".jpeg", ".txt", ".p7c", ".p7b", ".p12", ".pfx", ".pem", ".crt", ".cer", ".der", ".x3f", ".srw", ".pef", ".ptx", ".r3d", ".rw2", ".rwl", ".raw", ".raf", ".orf", ".nrw", ".mrwref", ".mef", ".erf", ".kdc", ".dcr", ".cr2", ".crw", ".bay", ".sr2", ".srf", ".arw", ".3fr", ".dng", ".jpe", ".jpg", ".cdr", ".indd", ".ai", ".eps", ".pdf", ".pdd", ".psd", ".dbfv", ".mdf", ".wb2", ".rtf", ".wpd", ".dxg", ".xf", ".dwg", ".pst", ".accdb", ".mdb", ".pptm", ".pptx", ".ppt", ".xlk", ".xlsb", ".xlsm", ".xlsx", ".xls", ".wps", ".docm", ".docx", ".doc", ".odb", ".odc", ".odm", ".odp", ".ods", ".od", ".zip", ".py", ".css", ".svg", ".dmp", ".tmp"]
limit_time = 0.1

class Watcher(FileSystemEventHandler):
    global global_dict, file_ext, limit_time

    def get_files(self, path, option):
        if option is 1:
            return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        elif option is 2:
            return len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
        else:
            return False

    def process(self, event):
        if os.path.isfile(event.src_path) and "!RecOveR!" not in event.src_path:
            time = datetime.datetime.now()
            path = event.src_path[:event.src_path.rfind("\\")]
            file_name = event.src_path[event.src_path.rfind("\\")+1:]
            file_ext = event.src_path[event.src_path.rfind("."):]
            if file_ext in file_ext_list:
                if path not in global_dict.keys(): # new path
                    global_dict[path] = [[file_name], 1, self.get_files(path, 2), time]
                else:
                    if file_name not in global_dict[path][0]:
                        global_dict[path][0].append(file_name)
                        global_dict[path][1] += 1

                        if global_dict[path][1] == global_dict[path][2]:
                            times = global_dict[path][3]
                            if (time - global_dict[path][3]).seconds < limit_time:
                                print "Found " + path
                            else:
                                global_dict[path][1] = 0
                                global_dict[path][3] = time
                        else:
                            pass
                    else:
                        pass
            else:
                pass

    def on_modified(self, event):
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