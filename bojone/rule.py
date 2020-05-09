#! -*- coding:utf-8 -*-
from __future__ import unicode_literals
import json
import os

def rule_couple(data):
    schema = []
    #读取schema信息
    with open("./data2/schema.json", encoding='utf8') as f:
        for line in f:
            schema.append(json.loads(line))
    predicate = [x['predicate'] for x in schema]
    pre_dict = dict(zip(predicate, schema))   
    a, b, c= 0, 0, 0
    for ins in data:
        pos = [-1, -1]
        for i in range(len(ins["spo_list"])):
            spo = ins["spo_list"][i]
            if spo["predicate"] == "妻子":
                pos[0] = i
            elif spo["predicate"] == "丈夫":
                pos[1] = i

        if pos[0] >= 0 and pos[1] < 0:
            a += 1
            spo = {"object_type": pre_dict["丈夫"]["object_type"], "predicate": "丈夫", "object": {"@value": ins["spo_list"][pos[0]]["subject"]}, "subject_type":pre_dict["丈夫"]["subject_type"], "subject": ins["spo_list"][pos[0]]["object"]["@value"]}
            ins["spo_list"].append(spo)

        elif pos[1] >= 0 and pos[0] < 0:
            b += 1
            spo = {"object_type": pre_dict["妻子"]["object_type"], "predicate": "妻子", "object": {"@value": ins["spo_list"][pos[1]]["subject"]}, "subject_type":pre_dict["妻子"]["subject_type"], "subject": ins["spo_list"][pos[1]]["object"]["@value"]}
            ins["spo_list"].append(spo)

        elif pos[1] >= 0 and pos[0] >= 0:
            c += 1

    print(a, b, c)
    return data

            
if __name__ == "__main__":
    data = []
    with open("./data2/dev_result2.json", encoding='utf8') as f:
        for line in f:
            data.append(json.loads(line))
    data = rule_couple(data)
    with open('./data2/dev_result2_couple.json', 'w', encoding='utf8') as f:
        for s in data:
            s = json.dumps(s, ensure_ascii=False)
            f.write(s + "\n")

    

    