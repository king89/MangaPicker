'''
Created on 2013-8-18

@author: KinG
'''
import MangaWebSite as webSite
import time
import localzip.myZip as zip

if __name__ == '__main__':
    downloadList = [];
    downloadList = (
            {'name' : 'chapter 1151',
               'folder':'e:\\Manga\LiarGame\\1153',
               'url':'http://www.imanhua.com/comic/200/list_43221.html'},
            )

    for dl in downloadList:
        pa = webSite.ImanhuaPattern(dl['url'])
        folder = dl['folder']
        myMangaPage = webSite.MangaPage(pa, folder)
        start = time.time();
        myMangaPage.GetImageFromPage(startNum=1, isChangeImgName=True, MultiThreadNum=4);
        time.sleep(3);
        print( dl['name'] + ' Pages Done')
        
    print('All Pages Done')
    
    for dl in downloadList:
        zip.zip_dir(dl['folder'], dl['folder']+'.zip')
        print(dl['name'] +' Zip Done')   
    print('All Zip Done') 