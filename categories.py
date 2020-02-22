import detail
import meishi_requests
from utility import verify_text
from utility import verify_list
from utility import init_text
import json
from string import Template

# 爬取菜谱分类下的数据


def start():
    # 开始函数

    # 首页下分类下数据的爬取
    # get_index_categories()
    # 更加详细数据的爬取（这里爬取的是ajax的数据，每个分类爬取两页）
    # get_detail_categories()
    # 全部分类的爬取（每个分类只爬取三页，每页大概十条数据）
    get_all_categories()


def get_all_categories():
    # 获取所有分类中的菜单，其实也就获取页面前三十个，并且每个爬取3页
    print('*****start get_all_categories()开始所有分类页的爬取')
    html = meishi_requests.get('https://home.meishichina.com/recipe-type.html')
    # 下面数据不用验证了，可确定性很大
    for index, item in enumerate(html.xpath('//div[@class="category_sub clear"][1]//li')):
        data = {}
        data['categories'] = item.xpath('./a/@title')[0]
        data['recipes'] = page_category(item.xpath('./a/@href')[0])
        write_data('categories/all-categories', str(index + 1), data)
        # break
    print('*****done get_all_categories()所有分类页的爬取结束')


def page_category(url):
    print('*****start page_categorie()开始单个分类页的爬取')
    recipes = []

    base_url = url
    urls = []  # 放置页数的url,这里构造三页的page url
    # 构建url，一共为三页
    for x in range(1, 4):
        urls.append(base_url+'page/'+str(x)+'/')
    # 针对url做遍历，和发出请求
    for url in urls:
        html = meishi_requests.get(url)
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
            recipes.append(temp)
            # break 
        # break
    return recipes
    print('*****start get_all_category()开始所有分类页的爬取')


def get_detail_categories():
    # 爬取详细分类的数据
    print('*****start get_detail_categories() 开始详细分类的数据提取')
    # 请求菜谱分类页
    html = meishi_requests.get('https://home.meishichina.com/recipe.html')
    # 提取每个分类的名字(不用校验，数据可确定性已经很高)
    for index, h3 in enumerate(html.xpath('//div[@class="ui_title"]//h3')):
        data = {}
        data['categories'] = h3.xpath('./a/text()')[0]
        data['recipes'] = get_ajax_data(
            h3.xpath('./a/@data')[0], h3.xpath('./a/@order')[0])
        # 写入数据
        write_data('categories/detail-categories', str(index + 1), data)
    print('*****done get_detail_categories() 详细分类的数据提取结束')


def get_ajax_data(data, order):
    # 获取ajax的数据,只爬取一页,然后返回一个列表，对接recipes
    print('*****start get_ajax_data(data, order) 开始处理ajax数据提取')
    str_templ = 'https://home.meishichina.com/ajax/ajax.php?ac=recipe&op=getMoreDiffStateRecipeList&classid=${data}&orderby=${order}&page=1'
    ajax_url = Template(str_templ).substitute(data=data, order=order)
    # 发出请求，返回一个对象
    res = meishi_requests.get_ajax(ajax_url)
    recipes = []
    for item in res['data']:
        temp = {}
        temp['show_title'] = item['title']
        temp['show_username'] = item['username']
        temp['show_img'] = item['fcover']
        url = 'https://home.meishichina.com/recipe-'+item['id']+'.html'
        temp['detail'] = detail.parse_detail_recipe(url)
        recipes.append(temp)
    print('*****done get_ajax_data(data, order) ajax数据提取结束')
    return recipes


def get_index_categories():
    # 获取首页下分类的数据（只获取前两个）
    print('*****start index_categories() 开始首页分类数据提取')

    html = meishi_requests.get('https://www.meishichina.com/')
    # 获取分类名，装到列表中(不用验证了，可确定性很大)
    categories = html.xpath(
        '//div[@class="w5"]//h3[position() <3]/a/text()')
    # 获取列表下的食谱详细数据
    all_recipes = []
    for item in html.xpath('//div[@class="w5"]//div[@class="big4_list clear mt10"]/ul[position() < 3]'):
        recipes = []
        for i in item.xpath('./li'):
            temp = {}
            temp['show_title'] = verify_text(i.xpath('.//p/text()'))
            temp['show_username'] = verify_text(
                i.xpath('.//a[@class="u"]/text()'))
            temp['show_img'] = verify_text(i.xpath('.//img/@data-src'))
            temp['detail'] = detail.parse_detail_recipe(
                verify_text(i.xpath('.//a[1]/@href')))
            recipes.append(temp)
        all_recipes.append(recipes)
    # 整合数据
    for index, item in enumerate(all_recipes):
        data = {}
        data['categories'] = categories[index] if categories else ''
        data['recipes'] = item
        write_data('categories/index-categories', str(index + 1), data)
    # 写入数据
    print('*****done index_categories() 首页分类数据提取结束')


def write_data(dire, filename, data):
    # 把数据写到文件中
    print('*****准备写入文件')
    dire_str = Template('./${dire}/${filename}.txt')
    with open(dire_str.substitute(dire=dire, filename=filename), 'w', encoding='utf-8') as fp:
        fp.write(json.dumps(data, ensure_ascii=False))
    # 需要传入文件存储路径，文件名，待写入数据数据
    print('*****写入文件结束')
