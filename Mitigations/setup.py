from distutils.core import setup
import py2exe

setup(
	console = ["src/hypothesis_1/hypothesis_1_process_monitoring.py"],
	options = {
		'py2exe': {
			'bundle_files': 1,
			'compressed': True,
			'dll_excludes': ['msvcr71.dll', "IPHLPAPI.DLL", "NSI.dll",  "WINNSI.DLL",  "WTSAPI32.dll"]
		}
	},
	zipfile = None
)