from bs4 import BeautifulSoup
import requests
import re
import os
from bs4 import BeautifulSoup
import requests
import re
import os
import lxml

#
# from GetUrlSet import GetPostUrlSet
# from GetPicWithinPost import GetPics
class GetPostUrlSet:
    def __init__(self, url):
        self.url = url

    def get_urls_set(self):
        req = requests.get(self.url)
        req.encoding = 'utf-8'
        soup = BeautifulSoup(req.text, 'lxml')
        post_url_set = set()
        post_url_list = soup.find_all(href=re.compile("viewthread.php\?tid=(\d+?)&extra=page%([\d\w]{3})%26amp%3Bfilter%3Ddigest$"))
        for post_url in post_url_list:
            relative_url = post_url.get('href')
            real_post_url = 'http://f.p03.space/' + relative_url
            post_url_set.add(real_post_url)
        return post_url_set

class GetPics:
    def __init__(self, url, post_number):
        self.url = url
        self.post_number = post_number
        self.img_number = 1

    def getpic(self):
        raw_page = requests.get(self.url)
        raw_page.encoding = 'utf-8'
        soup = BeautifulSoup(raw_page.text, 'lxml')
        img_tags = soup.find_all('img', file=re.compile("attachments/.*?\.jpg"))

        describe_tag = soup.find('td',class_='t_msgfont')
        post_title = soup.find('title')

        titles= re.findall(r"(.+?)-", post_title.text)[0].replace(' ','')
        print(titles)
        if not os.path.exists('posts/{}'.format(titles)):
            os.makedirs('posts/{}'.format(titles))
        f = open('posts/{}/{}.txt'.format(titles, self.post_number), 'w', encoding='utf-8')
        f.write(self.url+'\n')
        f.write(post_title.text+'\n\n\n\n\t\t\t')
        for string in describe_tag.stripped_strings:
            f.write(string+'\n')
        f.close()
        for img_tag in img_tags:
            img_url = img_tag.get('file')
            real_url = 'http://f.p03.space/'+img_url
            raw_img = requests.get(real_url)
            img_file = open('posts/{}/{}.jpg'.format(titles, self.img_number), 'wb')
            img_file.write(raw_img.content)
            print(titles+'downing {}'.format(self.img_number))
            img_file.close()
            self.img_number +=1

if __name__ == '__main__':

    url_set = set()
    counter = 1
    for n in range(1, 10):
        page = 'http://f.p03.space/forumdisplay.php?fid=19&filter=digest&page={}'.format(n)
        print(page)
        urlsgetter = GetPostUrlSet(page)
        url_set.clear()
        url_set = urlsgetter.get_urls_set()
        for post_url in url_set:
            picgetter = GetPics(post_url, counter)
            counter +=1
            picgetter.getpic()
