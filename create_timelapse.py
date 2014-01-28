#!/usr/bin/python
# Cross platform timelapse creation of picture taken at certian hours.
# Author : Gilad Fride
#os.system("mencoder -nosound mf://@%s -mf w=640:h=480:type=jpg:fps=15 -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=2160000:mbd=2:keyint=132:v4mv:vqmin=3:lumi_mask=0.07:dark_mask=0.2:mpeg_quant:scplx_mask=0.1:tcplx_mask=0.1:naq -o %s"%(file_list_path,output_path))
import os
import sys
import glob
from datetime import time,date, timedelta


#defaults
LIST_FILENAME = "files.txt"
NIGHT_START = 20
NIGHT_END = 6
is_linux = False

if sys.platform != 'win32':
    is_linux = True

if is_linux:
    MENCODER_LOCATION = "mencoder"
else:
    #Change accordingly
    MENCODER_LOCATION = "d:\\IPCamPics\\mencoder.exe"

MENCODER_COMMAND = "%s -nosound -ovc lavc -lavcopts vcodec=mpeg4 -o %s -mf type=jpeg:fps=20 mf://@%s"
TAG_COMMAND = 'convert -font helvetica -fill blue -draw \'text 24,24 "%s"\' "%s" "%s"'


def create_movie(file_list_path,output_path):
    os.system(MENCODER_COMMAND%(MENCODER_LOCATION,output_path,file_list_path))


# Only works on linux 
def time_stamp_images():
    lf = open(LIST_FILENAME)
    for line in lf.readlines():
        file = line.strip()
        text = os.path.basename(file)
        os.system(TAG_COMMAND%(text,file,file))

    lf.close()



def add_files(dir,file_handle):
    base_dir = os.getcwd()
    os.chdir(dir)
    files = glob.glob("*.jpg")
    files.sort()
    for file in files:
        full_path = os.path.join(dir,file)
        file_handle.write(full_path + "\n")
    os.chdir(base_dir)


def add_last_night(today = date.today()):
    of = open("files.txt","a")
    #today = date.today()
    yesterday = today - timedelta(1)
    yesterday_dir = yesterday.strftime("%m.%d.%Y")
    today_dir = today.strftime("%m.%d.%Y")
    base_dir = os.getcwd()
    for hour in range(NIGHT_START,24):
        dir = os.path.join(yesterday_dir,"%02d"%hour)
        add_files(dir,of)
    for hour in range(0,NIGHT_END):
        dir =  os.path.join(today_dir,"%02d"%hour)
        add_files(dir,of)
    of.close()


def create_last_night():
    try:
        os.remove(LIST_FILENAME)
    except:
        pass
    add_last_night()
    # timestamping images only works on linux
    if is_linux:
        time_stamp_images()
    create_movie(LIST_FILENAME,date.today().strftime("Timelapse_%d_%m_%Y-Night")+".avi")



if __name__ == "__main__":
    #print("Python Movie Creator\n")
    if len(sys.argv) != 1:
        os.chdir(sys.argv[1])
    
    create_last_night()


    #get_last_night_files()
