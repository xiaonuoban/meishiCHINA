import pymysql
import json
import hashlib
# 把文件中的数据存储到数据库


def start():
    # 入口
    # 保存轮播图的数据（已经写入）(有瑕疵，分类少一最后重新搞)
    save_slider_data()
    # 保存菜单的数据
    save_menu_data()
    # 保存首页常用分类的菜单
    save_index_type()
    # 保存全部分类的数据
    save_all_type()


def save_all_type():
    # 保存详细分类和全部分类
    code = add_type_code()
    file_paths = []
    for index in range(1, 11):
        temp_str = './categories/detail-categories/'+str(index)+'.txt'
        file_paths.append(temp_str)

    for index in range(1, 17):
        temp_str = './categories/all-categories/'+str(index)+'.txt'
        file_paths.append(temp_str)
    # 读取数据库
    conn = pymysql.connect(host='localhost', user='root',
                           password='654742', database='micro_recipes', port=3306)
    cursor = conn.cursor()
    recipes_all_type_sql = '''
        insert into recipes_all_type(r_a_id, r_a_type, r_a_r_id, r_a_show_title, r_a_u_id, r_a_show_user_name, r_a_avatar, r_a_show_img) values(null,%s,%s,%s,%s,%s,%s,%s)
    '''

    # 存数据
    for index, path in enumerate(file_paths):
        # 读取文件
        data = read_file(path)
        type_temp = data['categories']
        for recipe in data['recipes']:
            ids = save_user_and_recipes(recipe, conn, cursor)
            temp_tupple = (code[type_temp], ids['r_id'],
                           recipe['show_title'], ids['u_id'], recipe['show_username'],
                           recipe['detail']['avatar'], recipe['show_img'])
            cursor.execute(recipes_all_type_sql, temp_tupple)
            conn.commit()
    conn.close()


def add_type_code():
    # 这个字典存放着类型码
    code = {}
    code['最新推荐'] = 1
    code['最新发布'] = 2
    code['热菜'] = 3
    code['凉菜'] = 4
    code['汤羹'] = 5
    code['主食'] = 6
    code['小吃'] = 7
    code['家常菜'] = 8
    code['泡酱腌菜'] = 9
    code['西餐'] = 10
    code['烘焙'] = 11
    code['烤箱菜'] = 12
    code['饮品'] = 13
    code['零食'] = 14
    code['火锅'] = 15
    code['自制食材'] = 16
    code['海鲜'] = 17
    code['宴客菜'] = 18
    return code


def save_index_type():
    # 保存首页常用分类的菜单
    file_paths = []
    for index in range(1, 3):
        temp_str = './categories/index-categories/'+str(index)+'.txt'
        file_paths.append(temp_str)
    # 读取数据库
    conn = pymysql.connect(host='localhost', user='root',
                           password='654742', database='micro_recipes', port=3306)
    cursor = conn.cursor()
    recipes_index_type_sql = '''
        insert into recipes_index_type(r_i_id, r_i_type, r_i_r_id, r_i_show_title, r_i_u_id, r_i_show_user_name, r_i_avatar, r_i_show_img) values(null,%s,%s,%s,%s,%s,%s,%s)
    '''
    # recipes_pages_data_sql = '''
    #     insert into recipes_pages_data(r_pd_id, r_pd_type, r_pd_title, r_pd_content, r_pd_user_name, r_pd_menu_data) values(null,%s,%s,%s,%s,%s)
    # '''

    # 存数据
    categories = {
        '新秀菜谱': 'xxcp',
        '一周热门': 'yzrm'
    }
    for index, path in enumerate(file_paths):
        # 读取文件
        data = read_file(path)
        type_temp = data['categories']
        for recipe in data['recipes']:
            ids = save_user_and_recipes(recipe, conn, cursor)
            temp_tupple = (categories[type_temp], ids['r_id'],
                           recipe['show_title'], ids['u_id'], recipe['show_username'],
                           recipe['detail']['avatar'], recipe['show_img'])
            cursor.execute(recipes_index_type_sql, temp_tupple)
            conn.commit()
    conn.close()


def save_menu_data():
    # 保存菜单的数据
    # 构造文件路径
    file_paths = []
    for index in range(1, 19):
        temp_str = './menu_data/'+str(index)+'.txt'
        file_paths.append(temp_str)

    # 读取数据库
    conn = pymysql.connect(host='localhost', user='root',
                           password='654742', database='micro_recipes', port=3306)
    cursor = conn.cursor()
    recipes_index_type_sql = '''
        insert into recipes_index_type(r_i_id, r_i_type, r_i_r_id, r_i_show_title, r_i_u_id, r_i_show_user_name, r_i_avatar, r_i_show_img, r_i_materials) values(null,%s,%s,%s,%s,%s,%s,%s,%s)
    '''
    recipes_pages_data_sql = '''
        insert into recipes_pages_data(r_pd_id, r_pd_type, r_pd_title, r_pd_content, r_pd_user_name, r_pd_menu_data) values(null,%s,%s,%s,%s,%s)
    '''

    # 存数据
    for index, path in enumerate(file_paths):
        # 读取文件
        data = read_file(path)
        page_data = data['page_data']
        menu_data = {}
        menu_data['title'] = page_data['title']
        menu_data['creation_time'] = page_data['creation_time']
        menu_data['username'] = page_data['username']
        for recipe in page_data['recipes']:
            ids = save_user_and_recipes(recipe, conn, cursor)
            temp_tupple = ('menu_'+str(index+1), ids['r_id'],
                           recipe['show_title'], ids['u_id'], recipe['show_username'],
                           recipe['detail']['avatar'], recipe['show_img'], recipe['material'])
            cursor.execute(recipes_index_type_sql, temp_tupple)
            conn.commit()
        temp_tupple = ('menu_'+str(index+1), data['home_title'],
                       data['home_content'], data['username'], json.dumps(menu_data, ensure_ascii=False))
        cursor.execute(recipes_pages_data_sql, temp_tupple)
        conn.commit()

    conn.close()


def save_slider_data():
    # 保存轮播图的数据
    file_paths = []
    for index in range(1, 6):
        temp_str = './slider_data/'+str(index)+'.txt'
        file_paths.append(temp_str)

    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root',
                           password='654742', database='micro_recipes', port=3306)
    cursor = conn.cursor()
    recipes_index_type_sql = '''
        insert into recipes_index_type(r_i_id, r_i_type, r_i_r_id, r_i_show_title, r_i_u_id, r_i_show_user_name, r_i_avatar, r_i_show_img) values(null,%s,%s,%s,%s,%s,%s,%s)
    '''
    recipes_pages_data_sql = '''
        insert into recipes_pages_data(r_pd_id, r_pd_type, r_pd_img, r_pd_desc, r_pd_data) values(null,%s,%s,%s,%s)
    '''

    # 读取文件
    for index, path in enumerate(file_paths):
        data = read_file(path)
        page_t_c = []
        for index_2, item in enumerate(data['list']):
            temp = {}
            temp['title'] = item['title']
            temp['content'] = item['content']
            page_t_c.append(temp)
            avatar = None
            for recipe in item['recipes']:
                avatar = recipe['detail']['avatar']
                ids = save_user_and_recipes(recipe, conn, cursor)
                temp_tupple = ('slider_'+str(index+1)+'_'+str(index_2+1), ids['r_id'],
                               recipe['show_title'], ids['u_id'], recipe['show_username'],
                               recipe['detail']['avatar'], recipe['show_imgs'])
                cursor.execute(recipes_index_type_sql, temp_tupple)
                conn.commit()
        temp_tupple = ('slider_'+str(index+1), data['img_url'],
                       data['desc'], json.dumps(page_t_c, ensure_ascii=False))
        cursor.execute(recipes_pages_data_sql, temp_tupple)
        conn.commit()
    # 存取页面数据
    conn.close()


def save_user_and_recipes(recipe, conn, cursor):
    # 接受一个recipe,保存详细食谱和用户信息

    # 密码统一设置为12345678，然后进行md5加密后塞数据库
    m = hashlib.md5()
    m.update('12345678'.encode(encoding='utf-8'))
    password_md5 = m.hexdigest()

    search_sql = '''
        SELECT u_id FROM user WHERE u_user_name=%s
    '''
    save_user_sql = '''
        insert into user(u_id, u_user_name, u_password, u_avatar, u_gender, u_individual_desc, u_area) values(null,%s,%s,%s,%s,%s,%s)
    '''
    save_recipe_sql = '''
        insert into recipes(r_id, r_title, r_u_id, r_user_name, r_avatar, r_show_photo, r_desc, r_materials, r_step) values(null,%s,%s,%s,%s,%s,%s,%s,%s)
    '''
    # print(item['detail'])
    detail = recipe['detail']
    ids = {}

    cursor.execute(search_sql, (detail['username']))
    result = cursor.fetchone()
    # 用户入库
    if(result == None):
        # 说明还此用户名未在加入数据库
        temp_tupple = (detail['username'], password_md5,
                       detail['avatar'], 0, '', '')
        cursor.execute(save_user_sql, temp_tupple)
        ids['u_id'] = cursor.lastrowid
        # print(ids['u_id'])
        conn.commit()
        print('用户名：'+detail['username'])
    else:
        # 说明之前已经有用户，就取出这个id
        print('用户名：'+detail['username']+'已存在')
        ids['u_id'] = result[0]

    # 菜谱入库
    temp_tupple = (detail['title'], ids['u_id'], detail['username'], detail['avatar'],
                   detail['showphoto'], detail['desc'], json.dumps(
        detail['material'], ensure_ascii=False),
        json.dumps(detail['step'], ensure_ascii=False))
    cursor.execute(save_recipe_sql, temp_tupple)
    ids['r_id'] = cursor.lastrowid
    conn.commit()
    print('菜谱名：'+detail['title'])

    return ids


def read_file(path):
    # 传入要打开的文件路径，返回一个对象
    data = {}
    with open(path, 'r', encoding='utf-8') as fp:
        data = json.loads(fp.read())
    return data


def connect_mysql():
    # 进行数据库的连接操作
    temp = {}
    conn = pymysql.connect(host='localhost', user='root',
                           password='654742', database='micro_recipes', port=3306)
    cursor = conn.cursor()
    temp['conn'] = conn
    temp['cursor'] = cursor
    return temp
