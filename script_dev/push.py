#!/usr/bin/env python3
import subprocess, sys

msg = " ".join(sys.argv[1:]) or "update"
subprocess.run(f'git add -A && git commit -m "{msg}" && git push origin V2', shell=True, check=True)
