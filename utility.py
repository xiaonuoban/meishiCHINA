import re
# 自定义工具类，注意验证函数的使用场合


def verify_text(xpath_obj):
    # 校验获取的文本是否为空
    try:
        text = xpath_obj[0].strip()
        return text
    except:
        print('提取的文本列表为空，已设置为空字符串')
        write_erro()
        return ''


def verify_list(xpath_obj):
    # 校验传来的xpath list对象是否为空
    try:
        xpath_obj[0]
        return xpath_obj
    except:
        print('提取列表有错，已设置为空列表')
        write_erro()
        return []


def init_text(str_list):
    # 格式化字符串，把下xpth提取出的字符列表回车给去掉
    str_temp = ''
    for x in str_list:
        if(x != '\n'):
            str_temp += x.strip()
    return str_temp


def init_time(str_temp):
    return re.search('\d*-\d*-\d*', str_temp).group()


def write_erro():
    # 有字符串错误时候调用,相当于错误日记
    with open('erro.txt', 'a', encoding='utf-8') as fp:
        fp.write('有提取到的段落或者文字为空\r\n')
