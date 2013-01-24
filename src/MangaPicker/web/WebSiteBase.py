'''
Created on 2013-1-23

@author: king
'''


import urllib, urllib2
import cookielib



###############################################
#WebSite
class WebSite:
    '''
    classdocs
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
#################################################
#WebPage
class WebPage:
    '''
    classdocs
    '''
    
    
    
    def __init__(self):
        '''
        Constructor
        '''
        self.charSet = 'utf-8';
        
##################################################
class Pattern:
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        
        
###############################################
class Downloader:
    
    @staticmethod
    def DownloadImg(imageUrl,folder,fileName=''):
        extention = imageUrl.rfind('.');
        extention = imageUrl[extention+1:];
        if fileName == '':
            fileName = imageUrl[imageUrl.rfind('/')+1:imageUrl.rfind('.')];
        path = folder + '\\' + fileName + '.' + extention;




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
    url = url1,
    headers = headers
    )
    
    result = urllib2.urlopen(req).read()
    
    req = urllib2.Request(
    url = url2,
    headers = headers
    )
    data2 = urllib2.urlopen(req).read()
    file1 = open('d:\\data.png', 'wb');
    file1.write(data2);
    

    
    #Downloader.DownloadImg(url2,folder);



    
