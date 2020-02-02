# -*- coding: utf-8 -*-
import os
import sys
import shutil, errno
import random
import time
import traceback
from datetime import datetime
import pathlib

DAY = 30

TARGET_DIR='P:\\precycled'

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

def parse_conf(fileName):
    with open(fileName, "rb") as f:
        txt = f.read().rstrip().lstrip()
        txt = txt.decode('utf-8')
        txt = txt.split("\n")

    newline=list()
    for line in txt:
        line = line.lstrip().rstrip()
        if line:
            info = line.split('|')
            dt=datetime.strptime(info[2], '%Y-%m-%d %H:%M:%S').timestamp()
            now=datetime.now().timestamp()
            if dt < now - DAY * 86400:
                filename = os.path.join(TARGET_DIR, info[0])
                print(filename + ' removed')
                if os.path.isdir(filename):
                    shutil.rmtree(filename, True)
                else:
                    pth = pathlib.Path(info[0])
                    shutil.rmtree(os.path.join(TARGET_DIR, pth.parts[0]), True)
            else:
                newline.append(line)
    
    if len(newline):
        with open(fileName, "w", encoding="utf-8") as f:
            f.write('\n'.join(newline) + '\n')

if __name__ == "__main__":
    if not os.path.isdir(TARGET_DIR):
        os.mkdir(TARGET_DIR)

    subdir=''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 12))
    target=os.path.join(TARGET_DIR, subdir)

    try:
        param1 = sys.argv[1]
        os.mkdir(target)
        
        with open(os.path.join(TARGET_DIR, 'record.txt'), 'ab') as f:
            basename=os.path.split(param1)[1]
            content=os.path.join(subdir, os.path.split(param1)[1]) + '|' + os.path.split(param1)[0] + '|' + time.strftime("%Y-%m-%d %X") + '\n'
            f.write(content.encode('utf-8'))


        print(param1)
        if param1[:1] == target[:1]:
            os.rename(param1, os.path.join(target, os.path.split(param1)[1]))
        else:
            copyanything(param1, os.path.join(target, os.path.split(param1)[1]))
            if os.path.isdir(param1):
                shutil.rmtree(param1)
            else:
                os.remove(param1)
    except IndexError as e:
        pass
    except Exception as e:
        print('Error:', e)
        print(traceback.format_exc())
        time.sleep(1)
    finally:
        pass

    parse_conf(os.path.join(TARGET_DIR, 'record.txt'))