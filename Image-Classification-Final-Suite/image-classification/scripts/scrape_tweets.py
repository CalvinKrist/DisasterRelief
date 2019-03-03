import re
import os
import subprocess

def scrape(): 
    subprocess.call("./scrapeTweets.sh")

    PIC_REGEX = re.compile(r'pic.twitter.com/[^\s"]+')
    TEXT_REGEX = re.compile(r'"text": "[^",]+')
    TIME_REGEX = re.compile(r'"datetime": "[^",]+')
    URL_REGEX = re.compile(r'"url": "[^",]+')

    PIC_URLS = []
    TEXTS = []
    TIMES = []
    URLS = []

    DATA_PATH = os.path.join(os.getcwd(), 'TweetScraper/Data/tweet')
    for file in os.listdir(DATA_PATH):
        with open(os.path.join(DATA_PATH, file), 'rt') as f:
            PIC_URLS.append(PIC_REGEX.findall(f.read())[0])
            TEXTS.append(TEXT_REGEX.findall(f.read())[0])
            TIMES.append(TIME_REGEX.findall(f.read())[0])
            URLS.append(URL_REGEX.findall(f.read())[0])

    PIC_REGEX = re.compile(r'data-image-url="[^\s"]+')
    i = 1
    for url in PIC_URLS:
        subprocess.check_call(['./curlHTML.sh', url, str(i)])
        with open(os.path.join(os.getcwd(), 'output.txt'), 'rt') as f:
            try:
                PIC = PIC_REGEX.findall(f.read())[0]
                PIC = PIC.split("=\"")[1]
                subprocess.check_call(['./curlImage.sh', PIC, str(i)])
            except IndexError:
                pass
        i += 1

    RESP = []
    for i in range(0, len(PIC_URLS)):
        RESP[i] = {
            "pic": "img" + str(i) + ".jpg",
            "text": TEXTS[i],
            "time": TIMES[i],
            "url": URLS[i],
            "media_type": "Twitter"
        }

    return RESP






    # subprocess.call('./deleteImages.sh')
