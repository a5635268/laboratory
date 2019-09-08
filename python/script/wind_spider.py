import scrapy
import json
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import os
import requests
from datetime import datetime

now = datetime.now()

root_url = '../file/news_wind'

headers_1 = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'Host': 'fd.bjx.com.cn',
    'Pragma': 'no-cache',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive'
}

# cookies = {}

headers_2 = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'Host': 'news.bjx.com.cn',
}

initialUrl = 'http://fd.bjx.com.cn/NewsList?id=89'
page = 1

security_verify_data = '&security_verify_data=313932302c31303830'


def generate_urls(url):
    urls = []
    for i in range(1):
        urls.append('{}&page={}'.format(url, i + 1))
    return urls


news_list = {
    'data': []
}


# 将获取到的content去掉最后两段p(二维码和广告文字)
def strip_p_content(content):
    soup = BeautifulSoup(content, 'lxml')

    tag_pa = soup.find_all('p')

    string_ps = []

    del_p = None

    for p in tag_pa:
        count = 0
        if del_p is not None and del_p == p:
            continue
        else:
            if '扫码关注' in str(p) and '北极星' in str(p):
                count = 1
                num = 1
                while num < 5:
                    num += 1
                    if '<img' in str(p.find_next_sibling('p')):
                        del_p = p.find_next_sibling('p')
                        break
            if count == 0:
                string_ps.append('{}'.format(p))

    return ''.join(string_ps)


# 将soup内容转为字符串:
def get_content_from_soup(soup):
    tag_ps = soup.find_all('p')
    string_ps = []

    for p in tag_ps:
        if p:
            string_ps.append('{}'.format(p))

    return ''.join(string_ps)


def error_log(type, info, date=now):
    e_type = type
    err = open("../file/error.txt", 'a')
    err.write('date: {} errorType: {} reason: {} \n\n'.format(date, e_type, info))


# 存储远程图片
def save_image(url, count, detail_url):
    try:
        if count <= 20:
            urlretrieve(url, '{}/news_images/{}'.format(root_url, get_image_name(url)))
            return True
    except BaseException as e:
        error_log('Exception', e)
        error_log('URL', url)
        error_log('detail_url', detail_url)
        if requests.get(url).status_code == 404 or requests.get(url).status_code == 403:
            return False
        count += 1
        save_image(url, count, detail_url)
    return False


# 获取图片名
def get_image_name(url):
    return url.split('/')[-1:][0]


# 获取新图片路径(用于前端页面)
def get_new_src(url):
    image_name = get_image_name(url)
    return '/file/news_wind/news_images/{}'.format(image_name)


# 获取第一段p的内容(用于描述)
def get_first_p(content):

    soup = BeautifulSoup(content, 'lxml')

    first_p = soup.find_all('p')[0]

    def strip_content(content):
        strings = []
        for i in content:
            strings_p.append(i.string)
        return ''.join(strings)

    strings_p = []
    for i in first_p:
        if i.string:
            strings_p.append(i.string)
        else:
            strings_p.append(strip_content(i))

    strings_p = strings_p[1:]

    return ''.join(strings_p)


# 通过id寻找到对应项
def get_item(list, id):
    for i, element in enumerate(list):
        if element['id'] == id:
            return element


# 判断对应id的新闻是否已经存在于列表中,如果已经存在,返回True,不存在,返回False
def already_exist(list, id):
    for i, element in enumerate(list):
        if element['id'] == id:
            return True
    return False


class NewsSpider(scrapy.Spider):
    name = "wind"

    start_urls = generate_urls(initialUrl)

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse, headers=headers_1, cookies=None)

    def parse_pagination_detail(self, response):
        print(response)
        id = response.meta['id']
        detail_url = response.meta['detail_url']
        content = ''.join(response.xpath('//div[@class="list_detail"]/div[@id="content"]//node()').extract())
        content = strip_p_content(content)
        # 保存所有图片,替换所有图片url
        content_soup = BeautifulSoup(content, 'lxml')
        images = content_soup.find_all('img')
        if len(images):
            for i in images:
                flag = save_image(i['src'], 1, detail_url)
                if flag is True:
                    i['src'] = get_new_src(i['src'])
                    if '图' in str(i.find_parent().find_previous_sibling()) or '<strong>' in str(
                            i.find_parent().find_previous_sibling()):
                        i.find_parent().find_previous_sibling()['style'] = 'text-align:center'
                else:
                    i.extract()

        # 重新获取图片地址替换后的内容
        content = get_content_from_soup(content_soup)

        data = None
        with open('{}/wind_detail_{}.json'.format(root_url, id), 'r') as of:
            text = of.read()
            data = json.loads(text)
            data['data']['content'] += content

        with open('{}/wind_detail_{}.json'.format(root_url, id), 'w') as of:
            json.dump(data, of)

    def parse_detail(self, response):
        try:
            id = response.meta['id']
            detail_url = response.meta['detail_url']
            page_list = response.meta['page_list']
            base_url = response.meta['base_url']
            title = response.xpath('//div[@class="list_detail"]/h1[1]/text()').extract_first()
            source = response.xpath('//div[@class="list_detail"]/div[@class="list_copy"]/a[1]/text()').extract_first()
            source_link = response.xpath('//div[@class="list_detail"]/div[@class="list_copy"]/a[1]/@href').extract_first()
            content = ''.join(response.xpath('//div[@class="list_detail"]/div[@id="content"]//node()').extract())
            description = get_first_p(content)[1:]

            content = strip_p_content(content)

            # 保存所有图片,获取第一张图片的url,替换所有图片url
            content_soup = BeautifulSoup(content, 'lxml')
            images = content_soup.find_all('img')
            if len(images):
                for i in images:
                    flag = save_image(i['src'], 1, detail_url)
                    if flag is True:
                        i['src'] = get_new_src(i['src'])
                        if '图' in str(i.find_parent().find_previous_sibling()) or '<strong>' in str(
                                i.find_parent().find_previous_sibling()):
                            i.find_parent().find_previous_sibling()['style'] = 'text-align:center'
                    else:
                        i.extract()
                image = get_new_src(images[0]['src'])
            else:
                image = ''

            # 重新获取图片地址替换后的内容
            content = get_content_from_soup(content_soup)

            a_detail = {
                'title': title,
                'source': source,
                'source_link': source_link,
                'content': content,
                'image': image,
                'des': description,
                'id': id
            }

            if not os.path.exists('{}/wind_detail_{}.json'.format(root_url, a_detail['id'])):
                with open('{}/wind_detail_{}.json'.format(root_url, a_detail['id']), 'w') as of:
                    data = {'data': a_detail}
                    json.dump(data, of)

            # 抓取下一级分页数据
            next_pages = response.xpath('//div[@class="list_detail"]/div[@class="page"]/a/@href')[1:-1].extract()
            next_pages = list(map(lambda i: base_url + i, next_pages))

            if len(next_pages):
                page_numbers = len(next_pages) + 1
                for i in next_pages:
                    base_url = '/'.join(i.split('/')[:-1])+'/'
                    suffix = i.split('/')[-1].split('.')[0].split('-')
                    id = suffix[0]
                    index = int(suffix[1])
                    request = scrapy.Request(i, headers=headers_2, cookies=None, callback=self.parse_pagination_detail, priority=(page_numbers - index))
                    request.meta['id'] = id
                    request.meta['detail_url'] = detail_url
                    yield request

            update_file(id, page_list)

        except BaseException as e:
            error_log('get content failed', e)
            error_log('detail_url', str(detail_url))
            data_list = None
            with open('{}/wind_list.json'.format(root_url), 'r') as of:
                text = of.read()
                if not text:
                    return
                else:
                    data_list = json.loads(text)
                    for i, element in enumerate(data_list['data']):
                        if element['id'] == id:
                            del data_list['data'][i]
            with open('{}/wind_list.json'.format(root_url), 'w') as of:
                json.dump(data_list, of)
            return

    def parse(self, response):
        response_cookies = response.headers.getlist('Set-Cookie')
        if response_cookies:
            yunsuo = response_cookies[0].split(b';')[0].split(b'=')[1]
            cookies = {'yunsuo_session_verify': yunsuo.decode('utf-8')}
            request = scrapy.Request(initialUrl + security_verify_data, headers=headers_1,
                                     cookies=cookies, callback=self.parse_with_yunsuo, dont_filter=True)
            # yield request
        else:
            print('获得数据')
            request = scrapy.Request(initialUrl + security_verify_data, headers=headers_1,
                                     cookies=None, callback=self.parse_content, dont_filter=True)
            request.meta['cookies'] = None
            # self.parse_content(response)
        yield request

    def parse_with_yunsuo(self, response):
        print('SECOND', response)
        response_cookies = response.headers.getlist('Set-Cookie')
        if response_cookies:
            security = response_cookies[0].split(b';')[0].split(b'=')[1]
            cookies = {'security_session_mid_verify': security.decode('utf-8')}
            request = scrapy.Request(initialUrl + security_verify_data, headers=headers_1,
                                     cookies=cookies, callback=self.parse_content, dont_filter=True)
            request.meta['cookies'] = cookies
            # yield request
        else:
            # self.parse_content(response)
            request = scrapy.Request(initialUrl + security_verify_data, headers=headers_1,
                                     cookies=None, callback=self.parse_content, dont_filter=True)
            request.meta['cookies'] = None
        yield request

    def parse_content(self, response):
        def extract_text(selector):
            return map(lambda i: i.extract(), response.xpath('//ul[@class="list_left_ul"]/li/' + selector + '/text()'))

        def extract_href(selector):
            return map(lambda i: i.extract(), response.xpath('//ul[@class="list_left_ul"]/li/' + selector + '/@href'))

        def extract_id(selector):
            return map(lambda i: i.extract().split('/')[-1].split('.')[0],
                       response.xpath('//ul[@class="list_left_ul"]/li/' + selector + '/@href'))

        next_pages = response.xpath('//ul[@class="list_left_ul"]/li/a/@href').extract()
        for i in next_pages:
            page_list = zip(
                extract_text('a'),
                extract_href('a'),
                extract_text('span'),
                extract_id('a')
            )
            exit_flag = False
            base_url = '/'.join(i.split('/')[:-1]) + '/'
            id = i.split('/')[-1].split('.')[0]
            response_cookies = response.meta['cookies']
            a_news = {
                'id': id
            }
            with open('{}/wind_list.json'.format(root_url), 'r') as of:
                text = of.read()
                if text:
                    data = json.loads(text)
                    if already_exist(data['data'], a_news['id']):
                        exit_flag = True
            if exit_flag:
                continue
            if response_cookies:
                request = scrapy.Request(i, headers=headers_2, cookies=response_cookies, callback=self.parse_detail)
            else:
                # self.parse_detail(response)
                request = scrapy.Request(i, headers=headers_2, cookies=None, callback=self.parse_detail)
            request.meta['id'] = id
            request.meta['base_url'] = base_url
            request.meta['detail_url'] = i
            request.meta['page_list'] = page_list
            yield request


def update_file(id, page_list):
    for title, link, date, list_id in page_list:
        if list_id == id:
            a_news = {
                'title': title,
                'link': link,
                'date': date,
                'id': list_id
            }
            data = None
            with open('{}/wind_list.json'.format(root_url), 'r') as of:
                text = of.read()
                if not text:
                    data = {'data': []}
                    print('新建list data', data)
                else:
                    data = json.loads(text)
                if not already_exist(data['data'], a_news['id']):
                    data['data'].append(a_news)

            with open('{}/wind_list.json'.format(root_url), 'w') as of:
                json.dump(data, of)

