#!/usr/bin/env python3
import subprocess, sys

msg = " ".join(sys.argv[1:]) or "update document, update joints and walk path"
subprocess.run(f'git add -A && git commit -m "{msg}" && git push origin main', shell=True, check=True)
