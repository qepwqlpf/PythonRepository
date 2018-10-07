import threading,sys
import requests
import time
import os
import requests
import os,re,time,random
from contextlib import closing
import socket

from robobrowser import RoboBrowser

socket.setdefaulttimeout(20)  # 设置socket层的超时时间为20秒

class MulThreadDownload(threading.Thread):
    def __init__(self,url,startpos,endpos,f):
        super(MulThreadDownload,self).__init__()
        self.url = url
        self.startpos = startpos
        self.endpos = endpos
        self.fd = f
        self.headers = {
            'DNT': '1',
            'Host': '94.91p23.space',
            'Pragma': 'no-cache',
            'Referer': 'http://94.91p23.space/index.php',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
        requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        self.s = requests.session()
        self.s.keep_alive = False  # 关闭多余连接

    def download(self):
        print("start thread:%s at %s" % (self.getName(), time.time()))
        headers = {"Range":"bytes=%s-%s"%(self.startpos,self.endpos)}
        res = self.s.get(self.url,headers=self.headers)
        # res.text 是将get获取的byte类型数据自动编码，是str类型， res.content是原始的byte类型数据
        # 所以下面是直接write(res.content)
        self.fd.seek(self.startpos)
        self.fd.write(res.content)
        print("stop thread:%s at %s" % (self.getName(), time.time()))
        # f.close()


    def run(self):
        self.download()
def download_mp4(url,dir,filename):
    # headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name','Referer':'http://91porn.com'}
    # req=requests.get(url=url)
    # filename=str(dir)+'/1.mp4'
    # with open(filename,'wb') as f:
    #     f.write(req.content)
    # filenames = url.split('/')[-1]
    # filename = filenames.split('?')[0]
    # print(url)
    # filesize = int(requests.head(url).headers['Content-Length'])
    # print("%s filesize:%s" % (filename, filesize))
    #
    # # 线程数
    # threadnum = 3
    # # 信号量，同时只允许3个线程运行
    # threading.BoundedSemaphore(threadnum)
    # # 默认3线程现在，也可以通过传参的方式设置线程数
    # step = filesize // threadnum
    # mtd_list = []
    # start = 0
    # end = -1
    #
    # # 请空并生成文件
    # tempf = open(filename, 'w')
    # tempf.close()
    # # rb+ ，二进制打开，可任意位置读写
    # with open(filename, 'rb+') as  f:
    #     fileno = f.fileno()
    #     # 如果文件大小为11字节，那就是获取文件0-10的位置的数据。如果end = 10，说明数据已经获取完了。
    #     while end < filesize - 1:
    #         start = end + 1
    #         end = start + step - 1
    #         if end > filesize:
    #             end = filesize
    #         # print("start:%s, end:%s"%(start,end))
    #         # 复制文件句柄
    #         dup = os.dup(fileno)
    #         # print(dup)
    #         # 打开文件
    #         fd = os.fdopen(dup, 'rb+', -1)
    #         # print(fd)
    #         t = MulThreadDownload(url, start, end, fd)
    #         t.start()
    #         mtd_list.append(t)
    #
    #     for i in mtd_list:
    #         i.join()


    #
    #
    #
    with closing(requests.get(url, stream=True)) as response:
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        print(response.status_code)
        assert response.status_code == 200
        with open(filename, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
    return True


def get_video_url(url):
    br = RoboBrowser(history=True, parser='lxml')
    br.open(url)
    lang = br.get_forms()[0]
    lang['session_language'].options = ['cn_CN']
    lang['session_language'].value = 'cn_CN'
    br.submit_form(lang)

    # cn = input('请问是否要转换为中文？(y/n)')
    # if not cn:
    #    cn = 'y'
    # if cn == 'y':
    #
    #    lang = br.get_forms()[0]
    #    lang['session_language'].options = ['cn_CN']
    #    lang['session_language'].value = 'cn_CN'
    #    br.submit_form(lang)

    # get video title
    vid_title = br.find('div', {'id': 'viewvideo-title'}).text.strip()
    # print('the video you want to download is: {0}'.format(vid_title))
    # print('-----------------------------------------------------------')

    # get video id
    vid_id = re.findall(r'\d{5}', br.find('a', {'href': '#featureVideo'}).attrs['onclick'])[0]

    # get real video link
    vid_real_url = 'http://192.240.120.34//mp43/{}.mp4'.format(vid_id)
    # print(vid_real_url)
    #return vid_real_url, re.sub("""[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。|？、~@#￥%……&*（）：]+""", " ", vid_title).strip()
    return vid_real_url,re.sub("""[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。|？、~@#￥%……&*（）：]+""", " ",vid_title).strip()


def download_img(url,dir):
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接

    req=s.get(url=url,headers=headers)
    with open(str(dir),'wb') as f:
        f.write(req.content)
        req.close()
def random_ip():
    a=random.randint(1,255)
    b=random.randint(1,255)
    c=random.randint(1,255)
    d=random.randint(1,255)
    return(str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d))
flag=1
while flag<=100:
    tittle=[]
    base_url='http://94.91p23.space/view_video.php?viewkey='
    # page_url='http://91porn.com/v.php?next=watch&page='+str(flag)
    # page_url='http://91porn.com/v.php?&page='+str(flag)


    # page_url='http://91porn.com/v.php?category=tf&viewtype=basic&page='+str(flag)  #上月收藏最多
    #page_url='http://94.91p23.space/v.php?category=hd&viewtype=basic&page='+str(flag)#总收藏最多
    page_url='http://91porn.com/v.php?category=top&viewtype=basic&page='+str(flag)#本月收藏最多
    # page_url='http://91porn.com/v.php?category=hot&viewtype=basic&page='+str(flag)#当前最热
    headers = {
        'DNT': '1',
        'Host': '94.91p23.space',
        'Pragma': 'no-cache',
        'Referer': page_url,
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    get_page=s.get(url=page_url,headers=headers)

    viewkey=re.findall(r'<a target=blank href="http://94.91p23.space/view_video.php\?viewkey=(.*)&page=.*&viewtype=basic&category=.*?">\n                    <img ',str(get_page.content,'utf-8',errors='ignore'))
    for key in viewkey:
       # headers={'Accept-Language':'zh-CN,zh;q=0.9','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36','X-Forwarded-For':random_ip(),'referer':page_url,'Content-Type': 'multipart/form-data; session_language=cn_CN'}

        video_url=[]
        img_url=[]
        base_req=s.get(url=base_url+key,headers=headers)
        print(base_url+key)


       # video_url=re.findall(r'<source src="(.*?)" type=\'video/mp4\'>',str(base_req.content,'utf-8',errors='ignore'))
        video_url,tittle= get_video_url(base_url+key)
        #tittle=re.findall(r'<div id="viewvideo-title">(.*?)</div>',str(base_req.content,'utf-8',errors='ignore'),re.S)
       # print(base_req.content)
        img_url=re.findall(r'poster="(.*?)"',str(base_req.content,'utf-8',errors='ignore'))
        try:
            t=tittle
            print(t)
            # tittle[0]=t.replace('\n','')
            # t=tittle[0].replace(' ','')
            t='./posts/mp4/'+t
        except IndexError:
            pass
        if os.path.exists(str(t)+'.mp4')==False:
            try:
               # os.makedirs(str(t))
                print('开始下载:'+str(t))
                #download_img(str(img_url[0]),str(t)+'.png')
                print(str(video_url),str(t))
                if download_mp4(str(video_url),str(t),str(t)+'.mp4'):
                 print('---------------------------')
                 print('下载成功！珍惜生命，远离黄赌毒！')
                else:
                 print('下载失败')
            except:
                pass
                continue

            time.sleep(3)
        else:
            print('已经存在:'+str(t)+'.mp4')
            print('已存在文件夹,跳过')
            time.sleep(2)
    flag=flag+1
    print('此页已下载完成，下一页是'+str(flag))
