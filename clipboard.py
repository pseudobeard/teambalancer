import sys
import subprocess

def copyToClipboard(s):
    s = bytes(s, 'utf-8')
    if sys.platform == 'win32' or sys.platform == 'cygwin':
        subprocess.Popen(['clip'], stdin=subprocess.PIPE).communicate(s)
    else:
        raise Exception('Platform not supported')