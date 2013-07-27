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


    def __init__(self,pattern,folder):
        '''
        Constructor
        '''

        self.pattern = pattern; # a Manga Image pattern , means how to find this Image
        self.folder = folder;

            
        if os.path.exists(folder) == False:
            os.makedirs(folder)

        
    def ChangeCharSet(self,charSet):
        self.charSet = charSet;
    
    def GetImageFromPage(self,startNum = 1,isChangeImgName=False,MultiThreadNum=0):
        if MultiThreadNum == 0:
            self.pattern.DownloadImg(startNum, self.folder, isChangeImgName)
        else:
            self.pattern.DownloadImgMultiThread(startNum, self.folder, isChangeImgName,MultiThreadNum);
            
    
class ImanhuaPattern(webSite.Pattern): 
        
    def __init__(self,pageUrl):
        '''
        Constructor

        '''
        self.pageUrl = pageUrl;
        self.param = 'p';
        self.startNum = 1;
        self.patternDic = {};
        self.patternDic['url'] = 'http://t5.mangafiles.com/Files/Images';
        self.patternDic['imagePrefix'] = 'imanhua_';    #imanhua_ ,  JOJO_, no prefix  
        self.patternDic['imgFormat'] = 'jpg'; 
        self._InitSomeArgs();

        
    def _InitSomeArgs(self):
        pageUrl = self.pageUrl
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
        self.totalNum = int(self._GetTotalNum(result));
        
        imgData = None;
        
        testPrefix = ('imanhua_','JOJO_','')
        testFormat = ('jpg','png');
        for prefix in testPrefix:
            for myFormat in testFormat:
                self.patternDic['imagePrefix'] = prefix;  
                self.patternDic['imgFormat'] = myFormat;
                imageUrl = self.GetImageUrl(pageUrl);
                try:
                    req = urllib2.Request(url = imageUrl, headers = headers)
                    imgData = urllib2.urlopen(req).read()
                    if imgData:
                        print('ok: ' + prefix + ' + ' + myFormat);
                        return;
                except:
                    print('error: ' + prefix + ' + ' + myFormat);
                
    def GetPageList(self):
        '''
        Return need to down pages list.
        '''
        pages = [];
        for i in range(self.startNum,self.totalNum+1):
            url = self.pageUrl + '?' + self.param + '=' + str(i);
            pages.append(url);
        return pages;
    
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
        if nowNum == pageUrl:
            nowNum = 1;
        nowNum = '%03d'  %(int(nowNum));
        imageUrl = self.patternDic['url'].rstrip('/') + '/'+firstNum + '/' + SecNum + '/' + self.patternDic['imagePrefix'] + nowNum + '.' + self.patternDic['imgFormat'];
        return imageUrl;
    
    def DownloadOnePage(self,pageUrl,folder,isChangeImgName,nowPageNum):
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
        
        imageUrl = self.GetImageUrl(pageUrl);
#        print('Getting ' + imageUrl);
        testTimes = 1;
        while testTimes <= 3:
            try:
                testTimes = testTimes + 1;
                req = urllib2.Request(url = imageUrl, headers = headers)
                imgData = urllib2.urlopen(req).read()
                if imgData:
                    break;
            except:
                ext = self.patternDic['imgFormat'];
                if ext == 'png':
                    imageUrl = imageUrl.replace('png','jpg');
                    self.patternDic['imgFormat'] = 'jpg';
                elif ext == 'jpg':
                    imageUrl = imageUrl.replace('jpg','png');
                    self.patternDic['imgFormat'] = 'png';
                
                continue;
            
        extention = imageUrl.rfind('.');
        extention = imageUrl[extention+1:];

        if isChangeImgName == False:
            fileName = imageUrl[imageUrl.rfind('/')+1:imageUrl.rfind('.')];
        else:
            fileName = '%03d' %nowPageNum;
        path = folder + '\\' + fileName + '.' + extention;
        if not os.path.exists(path):
            if imgData:
                imgFile = open(path,'wb')
                imgFile.write(imgData);
                
#        print('Done ' + imageUrl);
        time.sleep(0.5)



class Comic131Pattern(webSite.Pattern):
    
    def __init__(self,pageUrl):
        webSite.Pattern.__init__(self);
        self.pageUrl = pageUrl;
        html = urllib2.urlopen(pageUrl).read()
        self.totalNum = self.GetTotalNum(html);
        
    def GetPageList(self):
        '''
        Return need to down pages list.
        http://comic.131.com/content/2104/188362/1.html
        '''
        pages = [];
        baseUrl = self.pageUrl[:self.pageUrl.rfind('/')+1];
        for i in range(self.startNum,self.totalNum+1):
            
            url = baseUrl + str(i) + '.html';
            pages.append(url);
        return pages;
    
    def GetImageUrl(self,pageUrl):
        '''
        pattern:
        <img id="comicBigPic" src="http://res6.comic.131.com/38/b5/5be37d62ea991612fe9af771e78d2350b90c.jpg"
        '''
        html = urllib2.urlopen(pageUrl).read();

        reImg = '<img id="comicBigPic" src=.+" alt'
        result = re.search(reImg,html).group();
        reImg = 'src=.*"';
        result = re.search(reImg,result).group();
        result = result.replace('src="','').replace('"','');
        
        return result;
        #print(result);
     

    
    def DownloadOnePage(self,pageUrl,folder,isChangeImgName,nowPageNum):
        headers = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
        'Referer': pageUrl
        }

        imgData = None;
        imageUrl = self.GetImageUrl(pageUrl);
#        print('Getting ' + imageUrl);

        try:
            req = urllib2.Request(url = imageUrl, headers = headers)
            imgData = urllib2.urlopen(req).read()
            if not imgData:
                imgData = '';
        except:
            print('Error ' + imageUrl);
            
            
        extention = imageUrl.rfind('.');
        extention = imageUrl[extention+1:];

        if isChangeImgName == False:
            fileName = imageUrl[imageUrl.rfind('/')+1:imageUrl.rfind('.')];
        else:
            fileName = '%03d' %nowPageNum;
        path = folder + '\\' + fileName + '.' + extention;
        if not os.path.exists(path):
            if imgData:
                imgFile = open(path,'wb')
                imgFile.write(imgData);
                
#        print('Done ' + imageUrl);
        time.sleep(0.5)
       
class HHManPattern(webSite.Pattern):
    def __init__(self,pageUrl):
        webSite.Pattern.__init__(self);
        self.pageUrl = pageUrl;
        html = urllib2.urlopen(pageUrl).read()
        codeRe = re.compile('(?<=PicLlstUrl = ").+?(?=")')
        self.code = re.search(codeRe,html).group()
        print self.code
        self.imgList = self.decode(); 
        self.totalNum = len(self.imgList)
        
    def decode(self):
        code = self.code
        result = ''
        key = 'tavzscoewrm'
        spliter = key[-1]
        key = key[:-1]
        i = 0
        for k in key:
            code = code.replace(k,str(i));
            i = i + 1
        code = code.split(spliter)
        print code
        
        for c in code:
            result = result + chr(int(c))
        
        result = result.split('|')
        
        resultList = []
        baseUrl = 'http://61.164.109.162:5458/dm03/'
        for p in result:
            p = baseUrl + p
            resultList.append(p)
            
        return resultList
    
    def GetPageList(self):
        '''
        http://hhcomic.com/hhpage/184295/hh118645.htm?s=3*v=1
        '''

        pages = [];
        baseUrl = self.pageUrl[:-1];
        for i in range(self.startNum,self.totalNum+1):
            url = baseUrl + str(i)
            pages.append(url);
            
        return pages;
    
    def GetImageUrl(self,pageUrl):
        num = pageUrl[pageUrl.rfind('=')+1:]
        number = (int)(num)
        return self.imgList[number-1];
      
    def DownloadOnePage(self,pageUrl,folder,isChangeImgName,nowPageNum): 
        imgData = None;
        imageUrl = self.GetImageUrl(pageUrl);
#        print('Getting ' + imageUrl);

        try:
            cj = cookielib.LWPCookieJar()

            cookie_support = urllib2.HTTPCookieProcessor(cj)
        
            opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        
            urllib2.install_opener(opener)
            
            headers = {
            'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
            'Referer':pageUrl,
            'Host':'61.164.109.162:5458'
            }
            
            req = urllib2.Request(
            url = imageUrl,
            headers = headers
            )
            print imageUrl
            imgData = urllib2.urlopen(req).read()
            if not imgData:
                imgData = '';
        except:
            print('Error ' + imageUrl);
            
            
        extention = imageUrl.rfind('.');
        extention = imageUrl[extention+1:];

        if isChangeImgName == False:
            fileName = imageUrl[imageUrl.rfind('/')+1:imageUrl.rfind('.')];
        else:
            fileName = '%03d' %nowPageNum;
        path = folder + '\\' + fileName + '.' + extention;
        if not os.path.exists(path):
            if imgData:
                imgFile = open(path,'wb')
                imgFile.write(imgData);
                
#        print('Done ' + imageUrl);
        time.sleep(0.5)
    
if __name__ == '__main__':
    
    pa = HHManPattern('http://hhcomic.com/hhpage/184295/hh118645.htm?s=3*v=1')
    folder = '''e:\\Manga\OnePiece\\068''';
    myMangaPage = MangaPage(pa,folder)
    start = time.time();
    myMangaPage.GetImageFromPage(startNum = 1,isChangeImgName = True,MultiThreadNum=4);
    time.sleep(1);
    print('Pages All Done')
    print('total use time :' + str(time.time() - start) + 'ms');     
#    myMangaPage.ZipFolder();
#    url = 'http://www.imanhua.com/comic/1906/list_65095.html';
#    pattern = ImanhuaPattern(url);
#    folder = '''e:\\Manga\OnePiece\\065''';
#
#    myMangaPage = MangaPage(pattern,folder)
#    myMangaPage.GetImageFromPage();
#    
#    print('All Done')
    
#    url = 'http://www.imanhua.com/comic/479/list_77967.html';
#    pattern = ImanhuaPattern(url);
#    folder = '''e:\\Manga\Chaodiancipao\\001''';
#
#    myMangaPage = MangaPage(pattern,folder)
#    myMangaPage.GetImageFromPage();
#    
#    print('All Done')
    
    