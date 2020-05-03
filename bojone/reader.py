#! -*- coding:utf-8 -*-
import json
import numpy as np
import sys

#sys.setdefaultencoding('utf-8')
#print sys.getdefaultencoding()


complex_relation = [u"上映时间",u"饰演",u"获奖",u"配音",u"票房"]
predicate2id, id2predicate = {}, {}

#with open('/home/tsing05/bojone/data/all_50_schemas') as f:
#   for l in f:
#        #l = json.loads(l)
#        if l['predicate'] not in predicate2id:
#            id2predicate[len(predicate2id)] = l['predicate']
#            predicate2id[l['predicate']] = len(predicate2id)


filename = "./data2/relation2label.json"
with open(filename) as f:
    l = json.load(f)
    #l=json.dumps(l).decode("unicode-escape")
    #print(l)
    for (key,value) in l.items():
        if value < 2:
            continue
        id2predicate[len(predicate2id)] = key
        predicate2id[key] = len(predicate2id)
print(id2predicate)

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
                            spo_list.append((spo['subject'],rel,spo['object'][key]))
                    else:
                        spo_list.append((spo['subject'], spo['predicate'], spo['object']))
                D.append({
                    'text': l['text'],
                    'spo_list':spo_list
                })

    return D

if __name__=="__main__":
    
    D = load_data('./simple.json')
    print D
    print json.dumps(D).decode("unicode-escape")