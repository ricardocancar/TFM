#/usr/bin/python
import argparse
import requests
import subprocess ## replace os 
from bs4 import BeautifulSoup
 
'''
URL of the archive web-page which provides link to
all video lectures. It would have been tiring to
download each video manually.
In this example, we first crawl the webpage to extract
all the links and then download videos.
'''
########################################################### 
# specify the URL of the archive here
archive_url = "http://www.rtve.es/alacarta/videos/telediario/"
 
def get_video_links():
     
    # create response object
    r = requests.get(archive_url)
     
    # create beautiful-soup object
    soup = BeautifulSoup(r.content,'html5lib')
     
    # find all links on web-page
    links = soup.findAll('a')
 
    # filter the link sending with .mp4
    video_links = [archive_url + link['href'] for link in links if link['href'].endswith('mp4')]
 
    return video_links
 
 
def download_video_series(video_links):
 
    for link in video_links:
 
        '''iterate through all links in video_links
        and download them one by one'''
         
        # obtain filename by splitting url and getting 
        # last string
        file_name = link.split('/')[-1]   
 
        print("Downloading file:%s"%file_name)
         
        # create response object
        r = requests.get(link, stream = True)
         
        # download started
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size = 1024*1024):
                if chunk:
                    f.write(chunk)
         
        print("%s downloaded!\n"%file_name) 
    print("All videos downloaded!")
    return

def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename

###########################################################################

def get_args():
    desc = "Speaker Recognition Command Line Tool"
    epilog = """
transform mp4 video to audio wav

Examples:
    python video.py -f file_name 
"""
    parser = argparse.ArgumentParser(description=desc,epilog=epilog,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-f', '--file_name',
                       help='name of video you want to convert',
                       required=True)

    parser.add_argument('-o', '--out',
                       help='name out of video',
                       required=True)

    parser.add_argument('-s', '--split',
                       help='Numbres of split you do to text for batch processing',
                       required=False)

    ret = parser.parse_args()
    return ret


def video_to_audio(name, out = 'salida.wav'):
  #bashCommand = "ffmpeg -ss 00:00:00 -i tve_telediario_220518.mp4 -t 00:00:15 -ab 192000 -vn tve_telediario.wav"
  bashCommand = "ffmpeg -i {} -acodec pcm_s16le -ac 1 -ar 16000 ./audio/{}".format(name,out)
  process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
  output, error = process.communicate()

def spliter(audio, length = 1):
  if  not os.path.exists("tmp"):
      os.system("mkdir tmp")
  os.system("ffmpeg -i {} -f segment -segment_time {} -c copy ./predict/out%03d.wav".format(audio,length))

#ffmpeg -ss 00:00:00 -i audio/noticia.wav -t 00:11:26 -ab 196000 -vn noticias1.wav
 
if __name__ == "__main__":
    args = get_args()

    video_to_audio(args.file_name,args.out)

    #if args.split.isdigit():
    #   spliter(args.out, args.split)


