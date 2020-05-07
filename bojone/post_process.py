#! -*- coding:utf-8 -*-
from __future__ import unicode_literals
import json
import os


def convert(pred):
    schema = []
    #读取schema信息
    with open("./data2/schema.json", encoding='utf8') as f:
        for line in f:
            schema.append(json.loads(line))

    predicate = [x['predicate'] for x in schema]
    pre_dict = dict(zip(predicate, schema))     
    data = []
    with open(pred, encoding='utf8') as f:
        for line in f:
            data.append(json.loads(line))
    
    #输出文件
    f = open('./data2/dev_result.json', 'w', encoding='utf8')
    for ins in data:
        text = ins["text"]
        spo_list_pred = ins["spo_list_pred"]
        spo_dict = {}
        for p in spo_list_pred:
            if "_" in p[1]:
                pre, att = p[1].split("_")
            else:
                pre = p[1]
                att = "@value"
            key = p[0]+pre+p[2]
            if key not in spo_dict.keys():
                spo_dict[key] = {"o":{}, "p":pre, "s":p[0]}

            spo_dict[key]["o"][att] = p[2]
        spo_list = [SPO(spo_dict[k], pre_dict) for k in spo_dict.keys()]
        s = json.dumps({"text": text, "spo_list": spo_list}, ensure_ascii=False)
        f.write(s + "\n")
    f.close()


def SPO(triple, schema):
    s = schema[triple["p"]]
    otype = {}
    for k in triple["o"].keys():
        otype.update({k:s['object_type'][k]})
        
    spo = {"object_type": otype, "predicate": triple["p"], "object": triple["o"], "subject_type":s["subject_type"], "subject": triple["s"]}
    return spo



if __name__ == "__main__":
    convert("./data2/dev_pred.json")
    