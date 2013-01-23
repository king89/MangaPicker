'''
Created on 2013-1-23

@author: king
'''
import WebSiteBase as webSite
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


    def __init__(self,url,param,startNum,totalPages,pattern,folderName):
        '''
        Constructor
        '''
        self.url = url;
        self.param = param;
        self.startNum = startNum;
        self.totalPages = totalPages;
        self.pattern = pattern; # a Manga Image pattern , means how to find this Image
        self.folderName = folderName;
        
    def ChangeCharSet(self,charSet):
        self.charSet = charSet;
    
    def GetPageList(self):
        '''
        Return need to down pages list.
        '''
        self.pages = [];
        for i in range(self.startNum,self.totalPages):
            url = self.url + '?' + self.param + '=' + str(i);
            self.pages.append(url);
        return self.pages;
    
    def GetImageFromPage(self,folderPath):
        self.images = [];
        for page in self.pages:
            img = self._GetImage(page);
            self.images.append(img);
            
    def _GetImage(self,page):
        '''
        Get image from page using the pattern
        '''
        img = '';
        return img;
    

class MangaPattern(webSite.Pattern): 
        
    def __init__(self):
        '''
        Constructor
        '''
    
    def GetImageUrl(self):
        '''
        This is the pattern example
        
        <img id="mangaFile" onload="imh.imgLoad.success(this)" alt="海贼王单行本 第064卷" 
        onerror="imh.imgLoad.error(this)" class="mangaFile" 
        src="http://t5.mangafiles.com/Files/Images/1906/65095/imanhua_054.png">
        '''
        
    
    
if __name__ == '__main__':
    
    url = 'http://www.imanhua.com/comic/1906/list_65095.html';
    param = 'p';
    ImangaPages = MangaPage(url,param,1,111);
    
    print (ImangaPages.GetPageList())
    
    
    
    