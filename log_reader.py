import re

def find_logs(log, levels=[b"DEBUG", b"INFO", b"WARN", b"ERROR"]):
    log_list = [x + b'\n' for x in log.split(b"\n")]
    new_log = []
    for i in log_list:
        for j in levels:
            if j in i:
                new_log.append(i)
    


with open("Обработка лог файла/APP_HOST.Ipint.log", "r+b") as log_f:
    log = log_f.read()

i = 1
while i < len(log):
    if not log[i].startswith(b'~'):
        log[i - 1] += log.pop(i)
    else:
        i += 1

for i in log:
    if b"INFO" in i:
        print(i)