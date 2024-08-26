import os
#import youtube_dl
#from pytube import YouTube
import yt_dlp

def downloadMusic(link, name):

    directory = "./music/"

    #download_directory =  directory + "{0}.{1}".format(name, "mp3")
    download_directory =  directory + "{0}".format(name)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': download_directory,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        filenames = [link]
        ydl.download(filenames)

def downloadVideo(link, name):
    output_path = './video/'
    #yt = YouTube(link)
    #video = yt.streams.get_highest_resolution()
    #video.download(output_path)

    video_info = yt_dlp.YoutubeDL().extract_info(
		url = link, download = False
	)
    
    options = {
		'outtmpl': f'{output_path}/{name}.mp4',
        'format': 'best',  # Download the best available quality
	}
    
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])