import subprocess

p = subprocess.Popen(["python3", "/home/kami/p.py"], stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE, stdin=subprocess.PIPE)
o, _ = p.communicate(b"3\n4\n5")
for s in o.split(b"\n"):
    print(s.decode())
