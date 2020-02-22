# 轮播图的数据模型
slider_pages_data = [
    {
        'img_url': 'xxx',  #轮播图那里的数据
        'desc': 'xxx',
        'list': [
            #  放分标题,比如五个，每个标题下还有详细的食谱
                {'title': 'xxx', 'content': 'xxx', 'recipes': [
                    # 可能二十几个
                    {'show_title': xxx,
                     'show_username': xxx,
                     'show_imgs': xxx,
                     'detail': {  # 详细食谱

                     }
                     }
                ]}
        ]
    }
]

# 详细食谱detail的数据模型
{
    'title': 'xxx',
    'username': 'xxx',
    'avatar': 'xxx',
    'show-photo': 'xxx',  # 做好的菜谱的展示图片
    'desc': 'xxx',
    'material': {  # 食材明细
        'main': [
            {'name': 'xxx', 'gram': 'xxx'},
            {'name': 'xxx', 'gram': 'xxx'},
            ...
        ],
        'subsidiary': [...],
        'category': [
            {'name': 'xxx', 'desc': 'xxx'},
            {'name': 'xxx', 'desc': 'xxx'},
            ...
        ],
    }
    'step': [{'content': 'xxx', 'step_img': ''}, {'content': 'xxx', 'step_img': ''}, ...]
}
