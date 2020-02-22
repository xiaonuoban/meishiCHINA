import detail
import meishi_requests
from utility import verify_text
from utility import verify_list
from utility import init_text
from utility import init_time
import json
# 爬取首页菜单数据
INDEX = 1


def start():
    # 爬取首页的菜单数据，此为开始函数
    data_temp = get_menus_URL()
    for item in data_temp:
        parse_menu_pages(item)


def parse_menu_pages(temporary_data):
    # 处理每个菜单页面中的数据
    print('*****start parse_menu_pages(temporary_data) 开始菜单的页面数据处理')
    data = {}
    # 提取首页显示的数据
    data['home_title'] = temporary_data['home_title']
    data['home_content'] = temporary_data['home_content']
    data['username'] = temporary_data['username']
    # 发起请求
    html = meishi_requests.get(temporary_data['url'])
    # 解析数据
    data['page_data'] = {}
    # 标题
    data['page_data']['title'] = html.xpath(
        '//a[@id="collect_title"]/text()')[0].strip()
    # 创建时间
    data['page_data']['creation_time'] = init_time(
        html.xpath('//div[@class="collect_dp"]/span/text()')[0])
    # 用户名
    data['page_data']['username'] = temporary_data['username']
    # 页面中的食谱信息
    data['page_data']['recipes'] = []
    for item in html.xpath('//div[@id="J_list"]//li'):
        temp = {}
        temp['show_img'] = verify_text(
            item.xpath('./div[@class="pic"]//img/@data-src'))
        temp['show_title'] = verify_text(item.xpath(
            './div[@class="detail"]//a/text()'))
        temp['show_username'] = verify_text(item.xpath(
            './div[@class="detail"]//p[@class="subline"]/a/text()'))
        temp['material'] = verify_text(
            item.xpath('.//p[@class="subcontent"]/text()'))
        temp['detail'] = detail.parse_detail_recipe(
            item.xpath('./div[@class="detail"]//a/@href')[0])
        data['page_data']['recipes'].append(temp)
        # temp['detail']
    # 格式化数据
    # 把数据写入到文件
    global INDEX
    with open('./menu_data/'+str(INDEX)+'.txt', 'w', encoding='utf-8') as fp:
        print('开始写入文件')
        fp.write(json.dumps(data, ensure_ascii=False))
        print('写入文件结束')
    INDEX += 1
    print('*****done parse_menu_pages(temporary_data) 菜单的页面数据处理完毕')


def get_menus_URL():
    # 获取首页菜单的各个url
    print('*****start get_menus_URL() 开始提取首页的菜单url')
    data_temp = []
    # 发起请求
    html = meishi_requests.get('https://www.meishichina.com/')
    # 底下不要做验证，这边出错是得到数据致命性错误的，不能让程序修正
    for item in html.xpath('//div[@id="w2_slider"]//li'):
        temp = {}
        temp['url'] = item.xpath('.//a/@href')[0]
        temp['home_title'] = item.xpath('.//a/text()')[0].strip()
        temp['home_content'] = init_text(item.xpath('./p/text()'))
        temp['username'] = item.xpath('./p/span/text()')[0].strip()
        data_temp.append(temp)
        # print(json.dumps(temp,ensure_ascii=False))

    print('*****done get_menus_URL() 提取首页的菜单url结束')
    # 返回解析到的url,和首页中展示的数据
    return data_temp
