#encoding:utf-8

import json
id2predicate ={}
predicate2id = {}

rel = []
filename = "/home/tsing05/bojone/data2/relation2label.json"
with open(filename) as f:
    l = json.load(f)
    #l=json.dumps(l).decode("unicode-escape")
    #print(l)
    for (key,value) in l.items():
        if value < 2:
            continue
        rel.append(key)
        id2predicate[len(predicate2id)] = key
        predicate2id[key] = len(predicate2id)
print(id2predicate)
rel_high = ['所属专辑', '上映时间_@value', '上映时间_inArea', '国籍', '总部地点', '制片人', '获奖_onDate', '获奖_period', '配音_@value', '配音_inWork', '创始人', '董事长', '人口数量', '票房_@value', '票房_inArea', '气候', '改编自', '官方语言', '首都']
rel_med = ['注册资本', '作者', '歌手', '饰演_@value', '成立日期', '毕业院校', '作词', '面积', '占地面积', '嘉宾', '出品公司', '所在城市', '祖籍', '朝代']
rel_low = ['饰演_inWork', '简称', '获奖_@value', '代言人']
complex_relation = [u"上映时间",u"饰演",u"获奖",u"配音",u"票房"]
def load_data(filename):
    D = []
    with open(filename) as f:
        for l in f:
            l = json.loads(l)
            spos = l.get('spo_list')
            if spos == None:  # test file
                D.append({
                    'text': l['text'],
                    'spo_list':[]
                })
            else:
                spo_list = []
                for spo in spos:
                    if spo['predicate'] in complex_relation:
                        #print json.dumps(spo).decode("unicode-escape")
                        #print spo
                        #print spo['object']
                        for (key,value) in spo["object"].items():
                            if key == "@value":
                                rel = spo['predicate']+'_@value'
                            else:
                                rel = spo['predicate']+'_'+key
                            assert rel in predicate2id
                            spo_list.append([spo['subject'],rel,spo['object'][key]])
                    else:
                        spo_list.append([spo['subject'], spo['predicate'], spo['object']['@value']])
                D.append({
                    'text': l['text'],
                    'spo_list':spo_list
                })

    return D

test = load_data('processed_test1.json')
data = []
with open('pred_with_high_threshold2.json', encoding='utf8') as f:
    for line in f:
        data.append(json.loads(line))


f = open('new_combined2.json', 'w', encoding='utf8')

num  =0 
still_void =0
for i in range(len(test)):

    combine  = []
    test1 = test[i]['spo_list']
    text = test[i]['text']
    for j in test1:
        if j[1] not in rel_high:
            if j not in combine:
                combine.append(j)
    data_test = data[i]['spo_list_pred']
    for j in data_test:
        #if j[1] in rel_high or j[1] in rel_med:
        if j not in combine and j[1] not in rel_low:
            combine.append(j)
    if(len(combine)==0):
        num+=1
        combine = test[i]['spo_list']
        if len(combine) ==0:
            
            combine = data[i]['spo_list_pred']
            if len(combine)==0:
                still_void+=1
    s = json.dumps({
        'text': text,
        'spo_list': [],
        'spo_list_pred': combine,
        'new':[],
        'lack':[]
    }, ensure_ascii=False)
    f.write(s + '\n')
    #f.write(s)       
print(num) 
print(still_void)



