'''
Created on 2013-1-23

@author: king
'''


import urllib, urllib2
import cookielib
import re
import threading 
import time
from Queue import Queue
from time import sleep
import localzip.myZip as zip

###############################################
# WebSite
class WebSite:
    '''
    classdocs
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
#################################################
# WebPage
class WebPage:
    '''
    classdocs
    '''
    
    
    
    def __init__(self):
        '''
        Constructor
        '''
        self.pattern = 'pattern';  # a Manga Image pattern , means how to find this Image
        self.folder = 'folder';
        self.charSet = 'utf-8';
    
    def ZipFolder(self):
        folder = self.folder;
        zipFolder = folder
        zipName = folder + '.zip'
        zip.zip_dir(folder, zipName);
##################################################
class Pattern:
    '''
    classdocs
    '''
    global lock
    def __init__(self):
        '''
        Constructor
        '''
        self.pageUrl = '';
        self.startNum = 1;
        self.totalNum = 1;
        
    def GetTotalNum(self, html):
        reTotalNum = 'value="[0-9]+"'
        val = re.findall(reTotalNum, html)
        reTotalNum = '[0-9]+'
        val = str(val[-1:])
        val = re.search(reTotalNum, val).group()
        return int(val);
    
    def DownloadImg(self, startNum, folder, isChangeImgName):
        self.NowPageNum = startNum;
        nowPageNum = 1;
        for pageUrl in self.GetPageList():
            self.DownloadOnePage(pageUrl, folder, isChangeImgName, nowPageNum);
            nowPageNum = nowPageNum + 1;
#         print('All Done')    
        
    def GetPageList(self):
        assert 0; raise NoimplementError;
    def GetImageUrl(self, pageUrl):
        assert 0; raise NoimplementError;
    def DownloadOnePage(self, pageUrl, folder, isChangeImgName, nowPageNum):
        assert 0; raise NoimplementError;
        
    def DownloadImgMultiThread(self, startNum, folder, isChangeImgName, ThreadNum=2):

        self.urlQueue = Queue();
        nowPageNum = startNum;
        pageList = self.GetPageList()[nowPageNum - 1:];
        for pageUrl in pageList:
            argDic = {'pageUrl':pageUrl, 'folder':folder, 'isChangeImgName':isChangeImgName, 'nowPageNum':nowPageNum};
            self.urlQueue.put(argDic)
            nowPageNum += 1;
        threadList = [];
        for i in range(ThreadNum):
            t = threading.Thread(target=self._working)
            t.setDaemon(True)
            t.start()
            threadList.append(t);
        self.urlQueue.join();

        
    def _working(self):
        while True:
            start = time.time();
            arguments = self.urlQueue.get()
            pageUrl = arguments['pageUrl'];
            folder = arguments['folder'];
            isChangeImgName = arguments['isChangeImgName'];
            nowPageNum = arguments['nowPageNum'];
            self.DownloadOnePage(pageUrl, folder, isChangeImgName, nowPageNum)
            print('finished pic ' + str(nowPageNum));
            print('use time :' + str(time.time() - start) + 's');
            self.urlQueue.task_done()    
        
###############################################
class NoimplementError(Exception):
    pass;



if __name__ == '__main__':
    url1 = 'http://www.imanhua.com/comic/155/list_77873.html?p=3'
    url2 = 'http://t5.mangafiles.com/Files/Images/155/77873/JOJO_003.png';
    folder = 'd:\\';
    

    cj = cookielib.LWPCookieJar()

    cookie_support = urllib2.HTTPCookieProcessor(cj)

    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)

    urllib2.install_opener(opener)
    
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
    'Referer':'http://www.imanhua.com/comic/155/list_77873.html?p=3'
    }
    
    req = urllib2.Request(
    url=url1,
    headers=headers
    )
    
    result = urllib2.urlopen(req).read()
    
    req = urllib2.Request(
    url=url2,
    headers=headers
    )
    data2 = urllib2.urlopen(req).read()
    file1 = open('d:\\data.png', 'wb');
    file1.write(data2);
    

    
    # Downloader.DownloadImg(url2,folder);



    
