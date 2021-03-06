from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px

'''
 Note: If running from Pycharm, will need to Edit Run Configurations and change the Working Directory
       to start from /src instead of this current folder
       
 Bar Graph API Doc: https://plotly.com/python-api-reference/generated/plotly.express.bar.html
'''
class ViewsBot:

    def __init__(self):
        # 1. Setup Edge Web Driver and grab the Website
        edgeDriver = Service('Drivers\\edgedriver_win64\\msedgedriver.exe')
        self.edge = webdriver.Edge(service=edgeDriver)
        # self.edge.get('https://www.youtube.com/c/mkbhd/videos')
        self.edge.get('https://www.youtube.com/user/EthosLab/videos')

        # 2. Create BeautifulSoup for Html Parser
        self.soup = BeautifulSoup(self.edge.page_source, features="html.parser")

    def processVideos(self):
        # 3. Grab the list of Youtube Videos
        videos = self.soup.find_all("ytd-grid-video-renderer", {"class": "style-scope ytd-grid-renderer"})

        # 4. Extract fields from the videos:
        #       - Title
        #       - View Count
        videosProcessed = []
        for video in videos:
            videoMetaData = []
            videoTitle = video.find("a", {"id": "video-title"}).text
            videoViewCount = video.find("span", {"class": "style-scope ytd-grid-video-renderer"}).text

            # Only want the view numbers: 1.6M vs 1.6M views
            videoViewCountValue = self.parseViewCount(videoViewCount.split(' ')[0])
            videoViewCountFormatted = format(videoViewCountValue,',')

            videoMetaData.append(videoTitle)
            videoMetaData.append(videoViewCountValue)
            videoMetaData.append(videoViewCountFormatted)

            # print(videoMetaData)
            # print(video.find("a", {"id": "video-title"}).text)

            videosProcessed.append(videoMetaData)

        # Tabularize the results
        pd.set_option('display.max_rows', 100)
        self.df = pd.DataFrame.from_records(videosProcessed, columns=["Title", "Views", "Views Formatted"])
        print(self.df)
        self.edge.close()

    def plotData(self):
        titles = self.df.loc[:, "Title"]
        views = self.df.loc[:, "Views"]
        fig = px.line(x=titles,
                     y=views,
                     title='Video vs View Count',
                     color_discrete_sequence =['mediumturquoise']*len(self.df),
                     labels=dict(x="Title", y="Views"))

        fig.show()

    def parseViewCount(self, viewCount=''):
        lastChar = viewCount[len(viewCount)-1]
        viewCount = viewCount.replace(',','')
        if lastChar.upper() == 'K':
            return int(float(viewCount[:-1]) * 1000)
        elif lastChar.upper() == 'M':
            return int(float(viewCount[:-1]) * 1000000)
        else:
            int(viewCount)

viewsBot = ViewsBot()
viewsBot.processVideos()
viewsBot.plotData()