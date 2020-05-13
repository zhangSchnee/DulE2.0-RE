#! -*- coding:utf-8 -*-
from __future__ import unicode_literals
import json
import os


complex_rel =  [u"上映时间",u"饰演",u"获奖",u"配音",u"票房"]

number = 0
complex_number = 0

def cal_dis(object_value,item,text):
    total_len  = len(text)
    len1 = len(object_value)
    len2 = len(item)
    item_index = 0
    o_index = 0
    for i in range(total_len):
        if text[i:i+len2] == item:
            item_index = i
            break
    for i in range(total_len):
        if text[i:i+len1] == object_value:
            o_index = i
            break
    o_index = o_index
    item_index = item_index +len2+1
    return abs(o_index-item_index)
def convert(pred):
    global number
    global complex_number
    schema = []
    
    #读取schema信息
    with open("/home/tsing05/bojone/data2/schema.json", encoding='utf8') as f:
        for line in f:
            schema.append(json.loads(line))

    predicate = [x['predicate'] for x in schema]
    pre_dict = dict(zip(predicate, schema))     
    data = []
    with open(pred, encoding='utf8') as f:
        for line in f:
            data.append(json.loads(line))
    
    #输出文件
    f = open('data/res_modified.json', 'w', encoding='utf8')
    for ins in data:
        complex_flag = 0
        text = ins["text"]
        spo_list_pred = ins["spo_list_pred"]
        spo_dict = {}
        key2_dict  = []
        property_list = []
        complex_value = []
        for p in spo_list_pred:

            if "_" in p[1]:
                pre, att = p[1].split("_")
            else:
                pre = p[1]
                att = "@value"
            
            
            if att == "@value":
                key = p[0]+pre+p[2]
                if key not in spo_dict.keys():
                    spo_dict[key] = {"o":{}, "p":pre, "s":p[0]}

                spo_dict[key]["o"][att] = p[2]
                if pre in complex_rel:
                    complex_value.append(key)
                    #spo_dict[key]["o_index"] = cal_index(p[2])
            else:

                property_list.append((pre,att,p[0],p[2]))
        if len(property_list)>0:
            #print('--------show result------:')
            #print(ins)
            complex_flag=1
            #print('--------------------------')
            #print(complex_value)
            #print(property_list)
            #print('*******************')
            for item in property_list:
                property_rel = item[0]
                property_type = item[1]
                property_subject = item[2]
                property_object = item[3]
                
                for key in complex_value:
                    if property_rel in key and property_subject in key:
                        if property_type not in spo_dict[key]['o']:
                            spo_dict[key]['o'][property_type] = [property_object]
                        else:
                            spo_dict[key]['o'][property_type].append(property_object)
            for keys in complex_value:
                object_value = spo_dict[keys]['o']['@value']
                for (key,value) in spo_dict[keys]['o'].items():
                    if key!='@value':
                        if len(value)>1:
                            min_dis = 50000
                            best_match = None
                            for item in value:
                                dis = cal_dis(object_value,item,text)
                                if dis < min_dis:
                                    min_dis = dis
                                    best_match = item
                            spo_dict[keys]['o'][key] =best_match
                        else:
                            spo_dict[keys]['o'][key] = value[0]   


            
            print(spo_dict)
        spo_list = [SPO(spo_dict[k], pre_dict) for k in spo_dict.keys()]
        s = json.dumps({"text": text, "spo_list": spo_list}, ensure_ascii=False)
        f.write(s + "\n")
    f.close()


def SPO(triple, schema):
    #if "complex" in triple:
    #print(triple)
    s = schema[triple["p"]]
    otype = {}
    for k in triple["o"].keys():
        otype.update({k:s['object_type'][k]})
        
    spo = {"object_type": otype, "predicate": triple["p"], "object": triple["o"], "subject_type":s["subject_type"], "subject": triple["s"]}
    return spo


def addrule1(input_file):
    data = []
    with open(input_file, encoding='utf8') as f:
        for line in f:
            data.append(json.loads(line))  
    f = open('data/modified.json', 'w', encoding='utf8')
    add_zhuanji = 0
    add_zuozhe = 0
    remove_toolong  =0
    remove_he = 0
    add_inwork = 0
    add_qinshu = 0
    for ins in data:  
        text = ins["text"]
        spo_list_pred = ins["spo_list_pred"]

        for p in spo_list_pred:
            if len(p[0])>15 and ("《"+p[0]+"》") not in text:
                if "，" in p[0] or "《" in p[0] or "》" in p[0]:
                    remove_toolong+=1
                    spo_list_pred.remove(p)
                    print("remove relation:too long {0}".format(p))
                    continue
            if len(p[1])>15 and ("《"+p[1]+"》") not in text:
                    remove_toolong+=1
                    spo_list_pred.remove(p)
                    print("remove relation:too long {0}".format(p))
                    continue
            # if "和" in p[0] and ("《"+p[0]+"》") not in text:
            #     sen = p[0].split('和')
            #     for p2 in spo_list_pred:
            #         if p2!=p and p[1] == p2[1]:
            #             if p2[2] in sen:
            #                 spo_list_pred.remove(p)
            #                 remove_he+=1
            #                 print("remove relation:he {0}".format(p))
            #                 continue
            #     print("split relation: {0}".format(p))
            # if "和" in p[2] and ("《"+p[2]+"》") not in text:
            #     sen = p[2].split('和')
            #     for p2 in spo_list_pred:
            #         if p2!=p and p[1] == p2[1]:
            #             if p2[0] in sen:
            #                 spo_list_pred.remove(p)
            #                 remove_he+=1
            #                 print("remove relation:he {0}".format(p))
            #                 continue
            #     print("split relation: {0}".format(p))
            if "丈夫" in p[1]:
                new_spo = [p[2],"妻子",p[0]]
                if new_spo not in spo_list_pred:
                    spo_list_pred.append(new_spo) 
                    add_qinshu+=1
                    print("add relation:妻子 {0}".format(new_spo))
            if "妻子" in p[1]:
                new_spo = [p[2],"丈夫",p[0]]
                if new_spo not in spo_list_pred:
                    spo_list_pred.append(new_spo) 
                    add_qinshu+=1
                    print("add relation:丈夫 {0}".format(new_spo)) 
            # if "所属专辑" in p[1]:
            #     gequ = p[0]
            #     zhuanji = p[2]
            #     for p2 in spo_list_pred:
            #         if p!=p2 and "歌手" in p2[1] and gequ == p2[0]:
            #             new_spo = [zhuanji,"歌手",p2[2]]
            #             if new_spo not in spo_list_pred:
            #                 spo_list_pred.append(new_spo) 
            #                 add_zhuanji +=1
            #                 print("add relation:歌手 {0}".format(new_spo))  
            if "主演" in p[1]:
                new_spo = [p[2],"饰演_inWork",p[0]]
                is_new =0 
                for p2 in spo_list_pred:
                    if "饰演" in p2[1] and p2[0] ==p[2]:
                        is_new = 1
                if new_spo not in spo_list_pred and is_new:
                    spo_list_pred.append(new_spo)
                    add_inwork+=1
                    print("add relation:inWork {0}".format(new_spo))  

            # if "编剧" in p[1]:
            #     if "《" +p[0] +"》" in text:
            #         new_spo = [p[0],"作者",p[2]]
            #         is_new = 1
            #         for p2 in spo_list_pred:
            #             if p!=p2 and "作者" in p2[1] and p[0] in p2:
            #                 is_new = 0
            #         if is_new:
            #             spo_list_pred.append(new_spo)
            #             add_zuozhe+=1
            #             print("add relation:作者 {0}".format(new_spo)) 
            

                                        
        ins["spo_list_pred"] = spo_list_pred
        s=json.dumps(ins,ensure_ascii=False)
        f.write(s + "\n")
    f.close()
    print("添加了{0}条亲属".format(add_qinshu))
    print("添加了{0}条专辑->歌手".format(add_zhuanji))
    print("添加了{0}条编剧->作者".format(add_zuozhe))
    print("添加了{0}条主演->饰演_inWork".format(add_inwork))
    print("去除了过长的{0}条关系".format(remove_toolong))
    print("去除了有和的{0}条关系".format(remove_he))
               
            

if __name__ == "__main__":
    
    addrule1('pred_threshold_att.json')
    convert("./data/modified.json")
    print('conflict number:')
    print(number)
    print(complex_number)
    
