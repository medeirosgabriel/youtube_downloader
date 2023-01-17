import os
import youtube_dl
from pytube import YouTube

def downloadMusic(link, name):

    directory = "./music/"

    download_directory =  directory + "{0}.{1}".format(name, "mp3")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': download_directory,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            filenames = [link]
            ydl.download(filenames)
    except:
        os.system("clear")

def downloadVideo(link):
    yt = YouTube(link)
    video = yt.streams.get_highest_resolution()
    video.download('./video/')
    return yt.title