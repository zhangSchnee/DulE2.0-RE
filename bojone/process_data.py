import json
import numpy as np
from copy import deepcopy
import io


def split_chupingongsi( objs ):
    cc = 0
    index = []
    count = 0
    for idx,obj in enumerate(objs):
        temp_spos = []
        
        for spo in obj['spo_list']:
            k = list(spo['object'].keys())[0]
            if '、' in spo['object'][k] and spo['predicate'] == '出品公司':
                new_objects = spo['object'][k].split('、')
                for ob in new_objects:
                    new_spo = deepcopy(spo)
                    new_spo['object'][k] = ob
                    temp_spos.append(new_spo)
                    count+=1
                    # print(new_spo)
                # print(obj['text'])
                # print("-")
                cc+=1
                index.append(idx)
            else:
                temp_spos.append(spo)
        obj['spo_list'] = temp_spos
    print('本次共清理错误出品公司数据{}条'.format(cc))
    #print(count)
    return index


def split_renwu( objs ):
    cc = 0
    index = []
    count = 0
    for idx,obj in enumerate(objs):
        temp_spos = []
        for spo in obj['spo_list']:
            k = list(spo['object'].keys())[0]
            if '、' in spo['object'][k] and spo['predicate'] in ['主演','创始人','嘉宾','作曲','作者','主角','作词','歌手','编剧','制片人','导演','']:
                new_objects = spo['object'][k].split('、')
                for ob in new_objects:
                    new_spo = deepcopy(spo)
                    new_spo['object'][k] = ob
                    temp_spos.append(new_spo)
                    # print(new_spo)
                    count+=1
                # print(obj['text'])
                # print('-')
                cc+=1
                index.append(idx)
                obj['spo_list'] = temp_spos
            else:
                temp_spos.append(spo)
    print('本次共清理错误人物数据{}条'.format(cc))
    #print(count)
    return index

#查看spo用 sub,obj空格开头结尾的
def find_wrong_spo1(result):
    count = 0
    index = []
    for idx,data in enumerate(result):
        spo_list = data['spo_list']
        temp_spo = []
        for spo in spo_list:
            k = list(spo['object'].keys())[0]
            obj = spo['object'][k]
            sbj = spo['subject']
            if obj != '' and sbj != '':
                if obj[0] == ' ' and sbj[0] != ' ':
                    new_spo = deepcopy(spo)
                    new_spo['object'][k] = spo['object'][k][1:-1]
                    temp_spo.append(new_spo)
                    # print(new_spo)
                    # print(data['text'])
                    # print('-')
                    count+=1
                elif sbj == ' ' and obj != ' ':
                    new_spo = deepcopy(spo)
                    new_spo['subject']['@value'] = spo['subject']['@value'][1:-1]
                    temp_spo.append(new_spo)
                    # print(new_spo)
                    # print(data['text'])
                    # print('-')
                    count+=1
                elif sbj == ' ' and obj == ' ':
                    new_spo = deepcopy(spo)
                    new_spo['subject']['@value'] = spo['subject']['@value'][1:-1]
                    new_spo['object'][k] = spo['object'][k][1:-1]
                    temp_spo.append(new_spo)
                    count+=1
                    # print(new_spo)
                    # print(data['text'])
                    # print('-')
                else:
                    temp_spo.append(spo)

        if temp_spo != spo_list:
            index.append(idx)
        data['spo_list'] = temp_spo
    print('一共修复subject,object开头为空格的样本{}条,spo {} 个'.format(len(index),count))
    return index


# 作词作曲 ，作曲标漏，做词标漏
def find_wrong_spo2(result):
    index = []
    count = []
    for idx, data in enumerate(result):
        flag = 0
        spo_list = data["spo_list"]
        predicate = []
        temp_spo = []
        for spo in spo_list:
            predicate.append(spo['predicate'])

        if '作词作曲' in data['text'] or '作词、作曲' in data['text'] or '作曲作词' in data['text'] or '作曲、作词' in data['text'] or '':

            if '作曲' in predicate and '作词' not in predicate:
                temp_spo = spo_list
                # 找到作曲spo的subject 和object
                for spo in spo_list:
                    if spo['predicate'] == '作词':
                        new_spo = {}
                        new_spo['object'] = spo['object']
                        new_spo['object_type'] = 'xx'
                        new_spo['predicate'] = '作词'
                        new_spo['subject'] = spo['subject']
                        new_spo['subject_type'] = 'xx'
                        # print(new_spo)
                        # print(data['text'])
                        # print('-')
                        temp_spo.append(new_spo)
                        flag = 1
                        break

            elif '作词' in predicate and '作曲' not in predicate:
                temp_spo = spo_list
                # 找到作词spo的 subject和object
                for spo in spo_list:
                    if spo['predicate'] == '作词':
                        new_spo = {}
                        new_spo['object'] = spo['object']
                        new_spo['object_type'] = 'xx'
                        new_spo['predicate'] = '作曲'
                        new_spo['subject'] = spo['subject']
                        new_spo['subject_type'] = 'xx'
                        # print(new_spo)
                        # print(data['text'])
                        # print('-')
                        temp_spo.append(new_spo)
                        flag = 1
                        break
        if flag == 1:
            index.append(idx)
    print('作词作曲修复{}条spo'.format(len(index)))
    return index

def time_fix(result):
    """
    对data类型的时间结果进行修复
    :param result:
    :return:
    """
    count = 0
    for data in result:
        for spo in data['spo_list']:
            k = list(spo['object'].keys())[0]
            if '上映时间' == spo['predicate'] or '出生日期' == spo['predicate'] or '成立日期' == spo['predicate']:
                if '年' not in spo['object'][k] and spo['object'][k] + '年' in data['text']:
                    spo['object'][k] += '年'
                    # print(spo)
                    count+=1
    print('时间一共修复{}条'.format(count))

def space_and_superscript_process(result):
    """
    把括号里面的上标1，和空格删去
    :param result:
    :return:
    """
    special_sampls= []
    index = []
    count = 0
    for idx,data in enumerate(result):
        spo_list = data['spo_list']
        for spo in spo_list:
            object_flag = 0
            subject_flag = 0
            k = list(spo['object'].keys())[0]
            #清除spo里面前后的括号。
            if spo['object'] and spo['subject']:
                if spo['object'][k][0] == ' ':
                    spo['object'][k] = spo['object'][k][1:]
                    count+=1
                elif spo['subject'][0] == ' ':
                    spo['subject'] = spo['subject'][1:]
                    count+=1
                elif spo['object'][k][-1] == ' ':
                    spo['object'][k] = spo['object'][k][:-1]
                    count+=1
                elif spo['subject'][-1] == ' ':
                    spo['subject'] = spo['subject'][:-1]
                    count+=1
                #清除括号的下标
                for samples in special_sampls:
                    if samples in spo['object'][k]:
                        object_flag = 1
                        break
                if spo['predicate'] != '成立日期' and spo['predicate'] != '上映日期' and spo['predicate'] != '出生日期' :  # object是日期类的时候不做清洗
                    if object_flag == 0 and spo['object'][k][-1] == '1': #object 不包含special_samples里面的内容
                        spo['object'][k] = spo['object'][k][:-1]
                        count+=1
                for samples in special_sampls:
                    if samples in spo['subject']:
                        subject_flag = 1
                        break
                if subject_flag == 0 and spo['subject'][-1] == '1': #subject 不包含
                    spo['subject'] = spo['subject'][:-1]
                    count+=1
    print('括号，上标处理{}条'.format(count))


def gongsi_fix(result):
    """
    对公司后缀进行修复
    1,有限责任公司
    2，实业有限公司
    3，股份有限公司
    4，投资有限公司
    5，有限公司
    6，投资发展有限公司
    :param result:
    :return:
    """
    count = 0
    name_list = ['有限责任公司','实业有限公司','股份有限公司','投资有限公司','有限公司','投资发展有限公司']
    for data in result:
        for spo in data['spo_list']:
            if spo['predicate'] in ['董事长','成立日期','创始人']:
                for name in name_list:
                    if spo['subject'] + name in data['text']:
                        spo['subject'] += name
                        count+=1
                        #print(spo)
                        #print(data['text'])
                        #print('-')
                        break
            elif spo['predicate'] == '出品公司':
                k = list(spo['object'].keys())[0]
                for name in name_list:

                    if spo['object'][k] + name in data['text']:
                        spo['object'][k] += name
                        #print(spo)
                        #print(data['text'])
                        #print('-')
                        count+=1
                        break
    print("公司：", count)

def didian_fix(result):
    """
    1，地点截取到人
    2，地点没截取全 （市，县，区）
    :param result:
    :return:
    """
    count = 0
    for data in result:
        for spo in data['spo_list']:
            k = list(spo['object'].keys())[0]
            if spo['predicate'] in ['祖籍','出生地']:
                if spo['object'][k][-1] == '人':
                    spo['object'][k] = spo['object'][k][:-1]
                    count+=1
    for data in result:
        flag = 1
        for spo in data['spo_list']:
            k = list(spo['object'].keys())[0]
            if spo['predicate'] in ['祖籍','总部地点','出生地']:
                if spo['object'][k]+'省' in data['text']:
                    spo['object'][k]+='省'
                    count+=1
                    flag=  0
                elif spo['object'][k]+'市' in data['text']:
                    spo['object'][k]+='市'
                    count+=1
                    flag = 0
                elif spo['object'][k]+'县' in data['text']:
                    spo['object'][k]+='县'
                    count+=1
                    flag=  0
                elif spo['object'][k]+'区' in data['text']:
                    spo['object'][k]+='区'
                    count+=1
                    flag=0
                elif spo['object'][k]+'镇' in data['text']:
                    spo['object'][k]+='镇'
                    count+=1
                    flag =0
    for data in result:
        flag = 1
        for spo in data['spo_list']:
            k = list(spo['object'].keys())[0]
            if spo['predicate'] in ['首都','所在城市']:
                if spo['object'][k]+'市' in data['text']:
                    spo['object'][k]+='市'
                    count+=1
                    flag = 0
                elif spo['object'][k]+'县' in data['text']:
                    spo['object'][k]+='县'
                    count+=1
                    flag=  0
                elif spo['object'][k]+'区' in data['text']:
                    spo['object'][k]+='区'
                    count+=1
                    flag=0
                elif spo['object'][k]+'镇' in data['text']:
                    spo['object'][k]+='镇'
                    count+=1
                    flag =0

def renkou_fix(result):
    """
    按照官方的说法，人口数量不能带单位’人‘，这里做修复
    :param result:
    :return:
    """
    count = 0
    for data in result:
        for spo in data['spo_list']:
            k = list(spo['object'].keys())[0]
            if spo['predicate'] == '人口数量':
                if spo['object'][k][-1] == '人':
                    spo['object'][k] = spo['object'][k][:-1]
                    count+=1
                    #print(data['text'])
    print("人口修复:", count)

def guoji_fix(result,or_objs):
    """
    对国籍进行修复
    :param result:
    :return:
    """
    count = 0
    for idx,data in enumerate(result):
        or_obj = or_objs[idx]
        temp_spos = []
        for spo in data['spo_list']:
            rm_flag = False
            if spo['predicate'] == '国籍' and spo['object'] =='中国':
                china_ents = [x for x in
                              filter(lambda x: x != '中国' and '中国' in x, [pos['word'] for pos in or_obj['postag']])]
                cur_text = data['text']
                for ent in china_ents:
                    cur_text = cur_text.replace(ent, '')
                if '中国' not in cur_text:
                    print(data['text'])
                    rm_flag =True
                    count+=1
            if not rm_flag:
                temp_spos.append(spo)

        data['spo_list'] = temp_spos
    print(count)


def load_data(file):
    predict = []
    with open(file, encoding='utf8') as f:
        for line in f:
            predict.append(json.loads(line))
    return predict

def cd_fix(result):
    count = 0
    for data in result:
        for spo in data['spo_list']:
            if spo['predicate'] == '朝代':
                if spo['object'] +'末年' in data['text']:
                    spo['object']+='末年'
                    count+=1
                    #print(spo)
                elif spo['object'] + '时期' in data['text']:
                    spo['object'] += '时期'
                    count+=1
                    print(spo)
                elif spo['object'] + '代' in data['text']:
                    spo['object'] += '代'
                    count+=1
                    print(spo)
                elif spo['object'] + '朝' in data['text']:
                    spo['object'] += '朝'
                    count+=1
                    print(spo)
    print(count)

    """
    数据后处理过程
    1，将顿号没隔开的出品公司，人物隔开，
    2，将‘1’，‘ ’为结尾的so,删去
    3，最长字符串匹配，删去投票带来的误差
    4，用规则修复明显的作词，作曲应该是同时出现的样本
    5，用字典的方式修复连载网站。
    6，利用同名专辑修复填充 专辑，歌曲
    7，利用主演修复出品公司
    8，修复总部地点
    9，曾的代码部分。简称，改编自，出版社，书名号，
    10，地点，公司，人口，单位处理
    11，
    """

def result_process(result,save_file):

    train_data = load_data('./data/train.json')
    dev_data = load_data('./data/dev.json')

    train_data += dev_data
    index0 = split_chupingongsi(result)
    _= split_renwu(result)
    # 开头为空格，结尾为空格
    index1 = find_wrong_spo1(result)
    
    index2 = find_wrong_spo2(result) #作词作曲同时出现
    time_fix(result) #时间
    didian_fix(result)
    gongsi_fix(result)
    renkou_fix(result)

    # cd_fix(result) #朝代 5/19

    space_and_superscript_process(result)

    # 最终得spo数量
    count = 0
    for data in result:
        count+=len(data['spo_list'])
    print('总spo得个数为{}'.format(count))
    print(len(result))

    f = io.open(save_file,'w',encoding='utf-8')
    for data in result:
        f.write(json.dumps(data,ensure_ascii=False)+'\n')
    return result

if __name__ == "__main__":
    result = load_data("./data/test_result.json")
    result_process(result, "./data/processed_result.json")