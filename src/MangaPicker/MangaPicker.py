'''
Created on Aug 28, 2013

@author: v-qilia
'''

import web.MangaWebSite as webSite
import time
import localzip.myZip as zip

if __name__ == '__main__':
    downloadList = []
    dlList = open('download.txt').read()
    dlList = dlList.split('\n')
    dlList = [x for x in dlList if x.strip()]
    for i in range(0,len(dlList)):
        url, folder = dlList[i].split(',') 
        oneItem = {'name' : 'file ' + '%03d' % (int(i+1)),
                   'folder': folder,
                   'url':url
                   }
        downloadList.append(oneItem)
    for dl in downloadList:
        folder = dl['folder']
        myMangaPage = webSite.MangaPage(dl['url'], folder)
        start = time.time();
        myMangaPage.GetImageFromPage(startNum=1, isChangeImgName=True, MultiThreadNum=4);
        print(dl['name'] + ' Pages donwload Done')
        zip.zip_dir(dl['folder'], dl['folder']+'.zip')
        print(dl['name'] +' Zip Done') 
        time.sleep(3);
         
    print('All Pages Done')
