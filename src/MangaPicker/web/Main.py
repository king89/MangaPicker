'''
Created on 2013-8-18

@author: KinG
'''
import MangaWebSite as webSite
import time
import localzip.myZip as zip

if __name__ == '__main__':
    downloadList = [];
    for i in range(15,17):
        oneItem = {'name' : 'chapter ' + '%03d' % (int(i)),
                   'folder':'e:\\Manga\KaXiu\\'+'%03d' % (int(i)),
                   'url':'http://hhcomic.com/hhpage/186596/hh'+str(57292+i)+'.htm'
                   }
        downloadList.append(oneItem)
    for dl in downloadList:
        pa = webSite.HHManPattern(dl['url'])
        folder = dl['folder']
        myMangaPage = webSite.MangaPage(pa, folder)
        start = time.time();
        myMangaPage.GetImageFromPage(startNum=1, isChangeImgName=True, MultiThreadNum=4);
        time.sleep(3);
        print( dl['name'] + ' Pages Done')
        
    print('All Pages Done')
    
    for i in range(15,17):
        dl = {'name' : 'chapter ' + '%03d' % (int(i)),
                   'folder':'e:\\Manga\KaXiu\\'+'%03d' % (int(i))}
        zip.zip_dir(dl['folder'], dl['folder']+'.zip')
        print('All Zip Done')
    print(dl['name'] +' Zip Done')    