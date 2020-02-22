# from lxml import etree
import detail
import meishi_requests
from utility import verify_text
from utility import verify_list
import json


# 用来处理首页轮播图中数据的模块
#本来函数用驼峰命名的，
INDEX = 1  # 用来命名


def start():
    slider_pages_data = []
    data = get_slider_URL()
    for index, item in enumerate(data['slider_pages_url']):
        # 处理每个轮播图页面
        parse_slider_pages(item, data['imgs_url'][index])
        


def parse_slider_pages(slider_page_url, slpage_img_url):
    # 处理进入每个轮播图中的网页数据
    print('*****start parse_slider_pages(slider_page_url)提取轮播图页面数据')
    page_data = {}  # slider_pages_data下的{}
    page_data['img_url'] = slpage_img_url
    html = meishi_requests.get(slider_page_url)

    # 获取页面描述
    page_data['desc'] = verify_text(html.xpath('//p[@id="mof_desc"]/text()'))
    # 获取分标题和其内容
    page_data['list'] = []  # slider_pages_data下的{}的list[]
    # 标题
    mo_result = verify_list(html.xpath(
        '//div[@class="mo" and position() < last()-1]/h2/text()'))
    # 内容
    p_list = verify_list(html.xpath('//div[@class="msb"]/p/text()'))
    for index, p in enumerate(p_list):
        p_list[index] = p.replace('\n', '').strip('')

    # 每部分的菜谱
    recipes_result = []  # slider_pages_data下的{}的list[]的对象下的recipes[]
    msb_ul = verify_list(html.xpath('//div[@class="msb_list clear"]/ul'))
    for item in msb_ul:
        # 得到每个包含详细的菜谱li集合，丢给detail模块处理，然后返回一个列表
        # print(item.xpath('.//li'))
        recipes_result.append(
            detail.parse_slider_recipes_pages(item.xpath('./li')))

    # 把相对应的标题，内容，菜谱集合进行数据重组
    for index, item in enumerate(recipes_result):
        temp = {}
        temp['title'] = mo_result[index] if mo_result else ''
        temp['content'] = p_list[index] if p_list else ''
        temp['recipes'] = recipes_result[index]
        page_data['list'].append(temp)

    global INDEX
    with open('./slider_data/'+str(INDEX)+'.txt', 'w', encoding='utf-8') as fp:
        print('开始写入文件')
        fp.write(json.dumps(page_data, ensure_ascii=False))
    INDEX += 1
    # print(json.dumps(page_data, ensure_ascii=False))
    print('*****done parse_slider_pages(slider_page_url)提取轮播图页面数据结束')


def get_slider_URL():
    # 获取首页轮播图那里的url
    print('*****start get_slider_URL()提取轮播图url')
    data = {}
    html = meishi_requests.get('https://www.meishichina.com/')
    slider_pages_url = html.xpath(
        '//div[@id="home_index_slider"]/ul/li/a[@title != "2020，人人都是美食家"]/@href')
    imgs_url = html.xpath(
        '//div[@id="home_index_slider"]/ul/li/a[@title != "2020，人人都是美食家"]/img/@src')
    data['slider_pages_url'] = slider_pages_url
    data['imgs_url'] = imgs_url
    print('*****done get_slider_URL()提取轮播图url结束')
    return data
