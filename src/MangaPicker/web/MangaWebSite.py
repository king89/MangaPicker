'''
Created on 2013-1-23

@author: king
'''
import WebSiteBase as webSite
import urllib, urllib2
import cookielib
import re
import os
import time
from pyquery import PyQuery as pq


class MangaWebSite(webSite.WebSite):
    '''
    classdocs
    '''

    def __init__(self,url,pageList):
        '''
        Constructor
        '''
        self.url = url;
        self.pageList = pageList; #all pageslist need to download Manga
        
##########################

class MangaPage(webSite.WebPage):
    '''
    classdocs
    '''


    def __init__(self,url,param,pattern,folder):
        '''
        Constructor
        '''
        self.url = url;
        self.param = param;
        self.startNum = 1;
        self.totalPages = 1;
        self.pattern = pattern; # a Manga Image pattern , means how to find this Image
        self.folder = folder;
        
        html = urllib2.urlopen(url).read();
        self.totalPages = int(self._GetTotalNum(html));
            
        if os.path.exists(folder) == False:
            os.makedirs(folder)
        
        cj = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        
        
    def ChangeCharSet(self,charSet):
        self.charSet = charSet;
    
    def _GetTotalNum(self,html):
        reTotalNum = 'value="[0-9]+"'
        val = re.findall(reTotalNum, html)
        reTotalNum = '[0-9]+'
        val = str(val[-1:])
        val = re.search(reTotalNum, val).group()
        return val
    
    
    def GetPageList(self):
        '''
        Return need to down pages list.
        '''
        pages = [];
        for i in range(self.startNum,self.totalPages+1):
            url = self.url + '?' + self.param + '=' + str(i);
            pages.append(url);
        return pages;
    
    def GetImageFromPage(self,startNum = 1):
        self.startNum = startNum;
        self.images = [];
        for pageUrl in self.GetPageList():
            imgUrl = self.pattern.GetImageUrl(pageUrl);
            self.DownloadImg(pageUrl, imgUrl, self.folder)
            
    def _GetImage(self,page):
        '''
        Get image from page using the pattern
        '''
        img = '';
        return img;
    
    def DownloadImg(self,pageUrl,imageUrl,folder,fileName=''):
        headers = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
        'Referer': pageUrl
        }

        cj = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        
        req = urllib2.Request(url = pageUrl, headers = headers)
        result = urllib2.urlopen(req).read()
        imgData = None;
        print('Getting ' + imageUrl);
        testTimes = 1;
        while testTimes <= 3:
            try:
                testTimes = testTimes + 1;
                req = urllib2.Request(url = imageUrl, headers = headers)
                imgData = urllib2.urlopen(req).read()
                if imgData:
                    break;
            except:
                ext = imageUrl[imageUrl.rfind('.')+1:];
                if ext == 'png':
                    imageUrl = imageUrl.replace('png','jpg');
                elif ext == 'jpg':
                    imageUrl = imageUrl.replace('jpg','png');
            
                continue;
            
        extention = imageUrl.rfind('.');
        extention = imageUrl[extention+1:];
        if fileName == '':
            fileName = imageUrl[imageUrl.rfind('/')+1:imageUrl.rfind('.')];
        path = folder + '\\' + fileName + '.' + extention;
        if not os.path.exists(path):
            if imgData:
                imgFile = open(path,'wb')
                imgFile.write(imgData);
                
        print('Done ' + imageUrl);
        time.sleep(0.5)
        
class MangaPattern(webSite.Pattern): 
        
    def __init__(self,patternDic):
        '''
        Constructor
        patternDic:
        url
        imagePrefix
        imgFormat
        '''
        self.patternDic = patternDic;
    
    def GetImageUrl(self,pageUrl):
        '''
        This is the pageUrl pattern example
        
        http://www.imanhua.com/comic/1906/list_65095.html?p=1
        http://t5.mangafiles.com/Files/Images/155/66294/JOJO_001.png
        '''
        reFirst = '/[0-9]+/'
        reSec = 'list_[0-9]+'
        firstNum = re.search(reFirst, pageUrl).group()
        firstNum = firstNum.strip('/')
        SecNum = re.search(reSec, pageUrl).group()
        SecNum = SecNum.strip('list_')
        nowNum = pageUrl[pageUrl.rfind('=')+1:];
        nowNum = '%03d'  %(int(nowNum));
        imageUrl = self.patternDic['url'].rstrip('/') + '/'+firstNum + '/' + SecNum + '/' + self.patternDic['imagePrefix'] + nowNum + '.' + self.patternDic['imgFormat'];
        return imageUrl;
        
    def _ChangeNum(self,num):
        pass
    
       
    
    
if __name__ == '__main__':
    
    patternDic = {'url':'http://t5.mangafiles.com/Files/Images','imagePrefix':'imanhua_','imgFormat':'jpg'}
    pattern = MangaPattern(patternDic);
    
#    url = 'http://www.imanhua.com/comic/1906/list_65095.html';
#    param = 'p'
#    folder = '''e:\\Manga\OnePiece\\064''';

    url = 'http://www.imanhua.com/comic/1906/list_65095.html';
    param = 'p'
    folder = '''e:\\Manga\OnePiece\\065''';
    
    myMangaPage = MangaPage(url,param,pattern,folder)
    
    myMangaPage.GetImageFromPage();
    
    print('All Done')
#    htmlData = urllib2.urlopen(url).read();
#    reTotalNum = 'value="[0-9]+"'
#    val = re.findall(reTotalNum, htmlData)
#    reTotalNum = '[0-9]+'
#    val = str(val[-1:])
#    val = re.search(reTotalNum, val).group()
#
#    print(val);

    
    