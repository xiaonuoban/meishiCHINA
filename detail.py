import meishi_requests
import json
from utility import verify_text
from utility import verify_list
from utility import init_text
# 专门用来处理详细页面的数据提取和解析


def parse_slider_recipes_pages(lis):
    # 参数为带有li的xpth对象，返回一个列表，为当前li下所有菜谱的解析
    print('*****start parse_slider_recipes_pages(lis)分标题下食谱提取')
    recipes = []
    for li in lis:
        # 这里处理每个分标题下每个菜谱的数据
        temp = {}
        temp['show_title'] = verify_text(
            li.xpath('.//a[1]/span[last()]/text()'))
        temp['show_username'] = verify_text(li.xpath('.//a[last()]/text()'))
        temp['show_imgs'] = verify_text(li.xpath('.//a[1]/img/@data-src'))
        temp['detail'] = parse_detail_recipe(
            verify_text(li.xpath('.//a[1]/@href')))
        recipes.append(temp)
        # print(json.dumps(temp,ensure_ascii=False))
    print('*****done parse_slider_recipes_pages(lis)分标题下食谱提取结束')
    return recipes


def parse_detail_recipe(url):
    # 处理食谱页面，返回一个详细食谱模型字典
    print('*****start parse_detail_recipe()详细食谱提取')
    recipe = {}
    html = meishi_requests.get(url)
    # 食谱名
    recipe['title'] = verify_text(html.xpath('//a[@id="recipe_title"]/text()'))
    print('当前处理食谱: %s' % recipe['title'])
    # 用户名
    recipe['username'] = verify_text(html.xpath(
        '//span[@id="recipe_username"]/text()'))
    recipe['avatar'] = verify_text(html.xpath('//a[@class="uright"]/img/@src'))
    recipe['showphoto'] = verify_text(
        html.xpath('//a[@class="J_photo"]/img/@src'))
    # 把开头的回车去掉
    recipe['desc'] = init_text(verify_list(
        html.xpath('//div[@id="block_txt1"]/text()')))
    # print(recipe['title'])
    # print(recipe['username'])
    # print(recipe['avatar'])
    # print(recipe['showphoto'])
    # print(recipe['desc'])
    # 获取食材材料
    recipe['material'] = {
        'main': [],
        'subsidiary': [],
        'category': []
    }
    for index, i in enumerate(verify_list(html.xpath('//div[@class="recipeCategory_sub_R clear"]'))):
        if index == 0:

            main_temp = {}
            main_temp['name'] = verify_text(i.xpath('.//li//b/text()'))
            main_temp['gram'] = verify_text(
                i.xpath('.//li/span[@class="category_s2"]/text()'))
            recipe['material']['main'].append(main_temp)
        else:
            main_temp = {}
            main_temp['name'] = verify_text(i.xpath('.//li//b/text()'))
            main_temp['gram'] = verify_text(
                i.xpath('.//li/span[@class="category_s2"]/text()'))
            recipe['material']['subsidiary'].append(main_temp)

    for i in verify_list(html.xpath('//div[@class="recipeCategory_sub_R mt30 clear"]//li')):
        temp = {}
        temp['desc'] = verify_text(i.xpath('.//a/text()'))
        temp['name'] = verify_text(
            i.xpath('./span[@class="category_s2"]/text()'))
        recipe['material']['category'].append(temp)

    # 获取步骤
    recipe['step'] = []
    for li in verify_list(html.xpath('//div[@class="recipeStep"]//li')):
        temp = {}
        temp['content'] = verify_text(
            li.xpath('./div[@class="recipeStep_word"]/text()'))
        temp['step_img'] = verify_text(li.xpath(
            './div[@class="recipeStep_img"]/img/@src'))
        recipe['step'].append(temp)

    print('*****done parse_detail_recipe()详细食谱提取结束')
    return recipe
