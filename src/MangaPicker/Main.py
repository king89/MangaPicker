'''
Created on 2013-8-18

@author: KinG
'''
import web.MangaWebSite as webSite
import time
import localzip.myZip as zip

if __name__ == '__main__':
    downloadList = [];
    baseFolder = 'e:\\Manga\JoJo\\'
    li = [x+115797 for x in range(1,64)]
    for i in range(6,len(li)):
        oneItem = {'name' : 'chapter ' + '%03d' % (int(i+1)),
                   'folder': baseFolder+'%03d' % (int(i+1)),
                   'url':'http://hhcomic.com/hhpage/1815553/hh'+str(li[i])+'.htm'
                   }
        downloadList.append(oneItem)
    for dl in downloadList:
        pa = webSite.HHComicPattern(dl['url'])
        folder = dl['folder']
        myMangaPage = webSite.MangaPage(pa, folder)
        start = time.time();
        myMangaPage.GetImageFromPage(startNum=1, isChangeImgName=True, MultiThreadNum=4);
        print(dl['name'] + ' Pages donwload Done')
        zip.zip_dir(dl['folder'], dl['folder']+'.zip')
        print(dl['name'] +' Zip Done') 
        time.sleep(3);
         
    print('All Pages Done')
