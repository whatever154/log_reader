import re

def find_logs(log, levels=[b"DEBUG", b"INFO", b"WARN", b"ERROR"]):
    new_log = []
    for i in log:
        for j in levels:
            if j in i:
                new_log.append(i)
