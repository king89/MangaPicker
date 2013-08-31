'''
Created on 2013-1-23

@author: king
'''
import web.WebSiteBase as webSite
import urllib, urllib2
import cookielib
import re
import os
import time
#from pyquery import PyQuery as pq


class MangaWebSite(webSite.WebSite):
    '''
    classdocs
    '''

    def __init__(self, url, pageList):
        '''
        Constructor
        '''
        self.url = url;
        self.pageList = pageList;  # all pageslist need to download Manga
        
##########################

class MangaPage(webSite.WebPage):
    '''
    classdocs
    '''


    def __init__(self, url, folder):
        '''
        Constructor
        '''
        pattern = self.GetPattern(url)
        self.pattern = pattern  # a Manga Image pattern , means how to find this Image
        self.folder = folder

        if os.path.exists(folder) == False:
            os.makedirs(folder)
            
    def GetPattern(self,url):
        if url.find('imanhua.com') > 0:
            return ImanhuaPattern(url)
        elif url.find('hhcomic.com'):
            return HHComicPattern(url)
            
    def ChangeCharSet(self, charSet):
        self.charSet = charSet;
    
    def GetImageFromPage(self, startNum=1, isChangeImgName=False, MultiThreadNum=0):
        if MultiThreadNum == 0:
            self.pattern.DownloadImg(startNum, self.folder, isChangeImgName)
        else:
            self.pattern.DownloadImgMultiThread(startNum, self.folder, isChangeImgName, MultiThreadNum);
            
    
class ImanhuaPattern(webSite.Pattern): 
        
    def __init__(self, pageUrl):
        '''
        Constructor

        '''
        self.pageUrl = pageUrl
        self.cInfo = {}
        self.param = 'p'
        self.startNum = 1
        self.patternDic = {}
        self.patternDic['url'] = 'http://t5.mangafiles.com:88/Files/Images/'
        self.patternDic['imagePrefix'] = 'imanhua_'  # imanhua_ ,  JOJO_, no prefix  
        self.patternDic['imgFormat'] = 'jpg'
        self._InitSomeArgs();

        
    def _InitSomeArgs(self):
        pageUrl = self.pageUrl
        html = urllib2.urlopen(pageUrl).read()
        print html
        #get the var cInfo in the js
        cInfo = None
        codeRe = re.compile('(?<=var )cInfo={.+?}')
        self.code = re.search(codeRe, html)
        if not self.code is None:
            exec(self.code.group()) in globals(),locals()
            print self.cInfo
        else:
            p = re.compile('(?<=}\().+?(?=\)\))')
            result = re.search(p,html)
            if not result is None:
                result = result.group()    
                print result
                
                a = b = c = d = e = f = None
                result = 'a,b,c,d,e,f = ' + result.replace('\\','\\\\')
                exec(result) in globals(),locals()
    #             print a,b,c,d,e,f
                p = re.compile('[0-9a-zA-Z]{1,3}')
                result = p.sub(lambda m: d[GetInt(m.group(0),b)],a)
    #             print result    
                result = result[(result.find('var')+3):]
    
                exec(result) in globals(),locals()
                self.cInfo = cInfo
            
def GetInt(s,isDecimal):
    aList = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    aList = [x for x in aList]
    aDict = {}
    for i in range(0,len(aList)):
        aDict[aList[i]] = i
    if isDecimal == 10:
        return int(s)
    else:
        sList = [x for x in s]
        sList.reverse()
        total = 0
        index = 0
        for x in sList:
            total = total + (isDecimal ** index ) * aDict[x]
            index += 1
        return total

        
    def GetPageList(self):
        '''
        Return need to down pages list.
        '''
        baseUrl = self.patternDic['url'];
        imgs = self.cInfo['files']
        bid = self.cInfo['bid']
        cid = self.cInfo['cid']
        pages = [];
        for img in imgs:
            url = baseUrl + str(bid) + '/' + str(cid) + '/' + img
            pages.append(url);
        return pages;
    
    def GetImageUrl(self, pageUrl):
        '''
        This is the pageUrl pattern example
        
        http://www.imanhua.com/comic/1906/list_65095.html?p=1
        http://t5.mangafiles.com/Files/Images/155/66294/JOJO_001.png
        '''
        return pageUrl;
    
    def DownloadOnePage(self, pageUrl, folder, isChangeImgName, nowPageNum):
        imgData = None;
        imageUrl = self.GetImageUrl(pageUrl);
#        print('Getting ' + imageUrl);
        if isChangeImgName == False:
            fileName = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('.')];
        else:
            fileName = '%03d' % nowPageNum;
                            
        extention = imageUrl.rfind('.');
        extention = imageUrl[extention + 1:];
        path = folder + '\\' + fileName + '.' + extention;
        if not os.path.exists(path):
            
            try:
                cj = cookielib.LWPCookieJar()
                cookie_support = urllib2.HTTPCookieProcessor(cj)
                opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
                urllib2.install_opener(opener)
                headers = {
                'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
                'Referer':self.pageUrl,
                }
                
                req = urllib2.Request(
                url=imageUrl,
                headers=headers
                )
                print imageUrl
                imgData = urllib2.urlopen(req).read()
                if not imgData:
                    imgData = '';
            except:
                print('Error ' + imageUrl);
                
            if imgData:
                imgFile = open(path, 'wb')
                imgFile.write(imgData);
                    
#        print('Done ' + imageUrl);
        time.sleep(0.5)



class Comic131Pattern(webSite.Pattern):
    
    def __init__(self, pageUrl):
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
        baseUrl = self.pageUrl[:self.pageUrl.rfind('/') + 1];
        for i in range(self.startNum, self.totalNum + 1):
            
            url = baseUrl + str(i) + '.html';
            pages.append(url);
        return pages;
    
    def GetImageUrl(self, pageUrl):
        '''
        pattern:
        <img id="comicBigPic" src="http://res6.comic.131.com/38/b5/5be37d62ea991612fe9af771e78d2350b90c.jpg"
        '''
        html = urllib2.urlopen(pageUrl).read();

        reImg = '<img id="comicBigPic" src=.+" alt'
        result = re.search(reImg, html).group();
        reImg = 'src=.*"';
        result = re.search(reImg, result).group();
        result = result.replace('src="', '').replace('"', '');
        
        return result;
        # print(result);
     

    
    def DownloadOnePage(self, pageUrl, folder, isChangeImgName, nowPageNum):
        headers = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
        'Referer': pageUrl
        }

        imgData = None;
        imageUrl = self.GetImageUrl(pageUrl);
#        print('Getting ' + imageUrl);

        try:
            req = urllib2.Request(url=imageUrl, headers=headers)
            imgData = urllib2.urlopen(req).read()
            if not imgData:
                imgData = '';
        except:
            print('Error ' + imageUrl);
            
            
        extention = imageUrl.rfind('.');
        extention = imageUrl[extention + 1:];

        if isChangeImgName == False:
            fileName = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('.')];
        else:
            fileName = '%03d' % nowPageNum;
        path = folder + '\\' + fileName + '.' + extention;
        if not os.path.exists(path):
            if imgData:
                imgFile = open(path, 'wb')
                imgFile.write(imgData);
                
#        print('Done ' + imageUrl);
        time.sleep(0.5)
       
class HHComicPattern(webSite.Pattern):
    ServerList = ['http://61.164.109.162:5458/dm01/', 'http://61.164.109.141:9141/dm02/', 'http://61.164.109.162:5458/dm03/', 'http://61.164.109.141:9141/dm04/', 'http://61.164.109.162:5458/dm05/', 'http://61.164.109.141:9141/dm06/', 'http://61.164.109.162:5458/dm07/', 'http://61.164.109.141:9141/dm08/', 'http://61.164.109.162:5458/dm09/', 'http://61.164.109.162:5458/dm10/', 'http://61.164.109.141:9141/dm11/', 'http://61.164.109.162:5458/dm12/', 'http://61.164.109.162:5458/dm13/', 'http://8.8.8.8:99/dm14/', 'http://61.164.109.141:9141/dm15/', 'http://142.4.34.102/dm16/']
    def __init__(self, pageUrl):
        webSite.Pattern.__init__(self);
        self.pageUrl = pageUrl;
        self.server = self.GetServer(pageUrl)
        html = urllib2.urlopen(pageUrl).read()
        codeRe = re.compile('(?<=PicListUrl = ").+?(?=")')
        self.code = re.search(codeRe, html)
        if not self.code is None:
            self.code = self.code.group()
            self.key = 'tahficoewrm'
        else:
            codeRe = re.compile('(?<=PicLlstUrl = ").+?(?=")')
            self.code = re.search(codeRe, html).group()  
            self.key = 'tavzscoewrm'
#         print self.code
        self.imgList = self.decode(); 
        self.totalNum = len(self.imgList)
        
    def GetServer(self,url):
        p = re.compile('(?<=s=)[0-9]{1,2}')
        result = re.search(p,url).group()
        return int(result)
    
    def decode(self):
        code = self.code
        result = ''
        key = self.key
        spliter = key[-1]
        key = key[:-1]
        i = 0
        for k in key:
            code = code.replace(k, str(i));
            i = i + 1
        code = code.split(spliter)
#         print code
        
        for c in code:
            result = result + chr(int(c))
        
        result = result.split('|')
        
        resultList = []
        baseUrl = HHComicPattern.ServerList[self.server-1]
        for p in result:
            p = baseUrl + p
            resultList.append(p)
            
        return resultList
    
    def GetPageList(self):
        '''
        http://hhcomic.com/hhpage/184295/hh118645.htm?s=3
        '''
        pages = self.imgList
        return pages;
    
    def GetImageUrl(self, pageUrl):
        return pageUrl
      
    def DownloadOnePage(self, pageUrl, folder, isChangeImgName, nowPageNum): 
        imgData = None;
        imageUrl = self.GetImageUrl(pageUrl);
#        print('Getting ' + imageUrl);
        if isChangeImgName == False:
            fileName = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('.')];
        else:
            fileName = '%03d' % nowPageNum;
                            
        extention = imageUrl.rfind('.');
        extention = imageUrl[extention + 1:];
        path = folder + '\\' + fileName + '.' + extention;
        if not os.path.exists(path):
            
            try:
                cj = cookielib.LWPCookieJar()
    
                cookie_support = urllib2.HTTPCookieProcessor(cj)
            
                opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
            
                urllib2.install_opener(opener)
                
                headers = {
                'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
                'Referer':self.pageUrl,
                }
                
                req = urllib2.Request(
                url=imageUrl,
                headers=headers
                )
                print imageUrl
                imgData = urllib2.urlopen(req).read()
                if not imgData:
                    imgData = '';
            except:
                print('Error ' + imageUrl);
                
            if imgData:
                imgFile = open(path, 'wb')
                imgFile.write(imgData);
                    
#        print('Done ' + imageUrl);
        time.sleep(0.5)
    
if __name__ == '__main__':
    pa = 'http://www.imanhua.com/comic/176/list_8220.html'
    folder = '''e:\\Manga\htg1\\001''';
    myMangaPage = MangaPage(pa, folder)
    start = time.time();
    myMangaPage.GetImageFromPage(startNum=1, isChangeImgName=True, MultiThreadNum=4);
    time.sleep(1);
    print('Pages All Done')
    print('total use time :' + str(time.time() - start) + 's');  

       
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
    
