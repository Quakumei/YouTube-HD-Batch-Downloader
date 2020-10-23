import argparse
from pytube import YouTube
import os
import subprocess

def getExt(k):
    res=[]
    for i in range(len(k)-1, -1, -1):
    	if k[i]==".":
    		break
    	else:
    		res.append(k[i])
    return "".join(res)[::-1]
    
def downloadAudioVideo(url):
    streams = YouTube(url).streams
    video = streams.filter(progressive=False).order_by('resolution').desc().first().download()
    audio = streams.get_audio_only().download()
    
    new_video = video.replace(" ", "_")
    new_audio = audio.replace(" ", "_")
    os.rename(video, new_video)
    os.rename(audio, new_audio)
    print(new_video)
    print(new_audio)
    return new_video, new_audio
    
def glueVideoAudio(video, audio):
    ext = getExt(video)
    command = "ffmpeg -i " +video+" -i " +audio+" -map 0:v -map 1:a -c:v copy -shortest "+video+"."+ext
    subprocess.call(command, shell=True)
    return

def process_batch(lol):
    #List of links - lol
    #Txt file, each line is a link to the youtube video
    
    #Get list of strings of links
    shindlers_list = []
    f = open(lol, 'r')
    line = f.readline()
    while line:
    	line = line.rstrip()
    	shindlers_list.append(line)
    	line = f.readline()
    f.close()
    
    for link in shindlers_list:
    	a = downloadAudioVideo(link)
    	glueVideoAudio(a[0], a[1])
    	os.remove(a[0])
    	os.remove(a[1])
    

parser = argparse.ArgumentParser(description='Downloads a batch of high quality youtube videos for free. From a file which contains of links.')    
parser.add_argument('--list', type=str,  help='schindlers_list file')
args = parser.parse_args()

process_batch(args.list)

