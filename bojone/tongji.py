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

dev_data = load_data('/home/tsing05/bojone/data2/dev.json')

dev2 = load_data('processed_dev.json')

res_count = {}
res ={}
for re in rel:
    res_count[re] = [1e-9,1e-9,1e-9,1e-9]
    res[re] = [0,0,0]


print('---------------------------------------------------------')
with open('final_balanced.json') as f:
    for l in f:
        l = json.loads(l)
        lack = l["lack"]
        pred = l["spo_list_pred"]
        right = l["spo_list"]
        new = l["new"]
        for item in right:
            re = item['predicate']
            res_count[re][2] +=1
        for item in pred:
            re = item['predicate']
            res_count[re][0] +=1
            res_count[re][3] +=1
        for item in new:
            re = item['predicate']
            res_count[re][0] -=1
        for item in lack:
            re = item['predicate']
            res_count[re][1] +=1       
print(res_count)   
print('---------------------------------------------------------')
res_f1 = {}
for (key,value) in res_count.items():
    pre = value[0]/value[3]
    recall = 1-value[1]/value[2]
    f1 = (2*pre*recall)/(pre+recall)
    res[key] = [round(pre,4),round(recall,4),round(f1,4)]
    res_f1[key] = [round(f1,4)]
print(res)
print('---------------------------------------------------------')
print(res_f1)

print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
res_count = {}
res ={}

for re in rel:
    res_count[re] = [1e-9,1e-9,1e-9,1e-9]
    res[re] = [0,0,0]

for  i in range(len(dev_data)):
    #print( dev[i]['spo_list'])
    #print(type(dev[i]))
    dev = dev_data[i]['spo_list']
    dev_pred = dev2[i]['spo_list']
    #dev_pred = dev_pred["spo_list"]
    #print(dev_pred)


    devset = set(tuple(spo) for spo in dev)
    dev_predset = set(tuple(spo) for spo in dev_pred)
    
    lack = [spo for spo in devset-dev_predset]
    pred = [spo for spo in dev_predset]
    right = [spo for spo in devset]
    new = [spo for spo in dev_predset-devset]
    for item in right:
        re = item[1]
        res_count[re][2] +=1
    for item in pred:
        re = item[1]
        res_count[re][0] +=1
        res_count[re][3] +=1
    for item in new:
        re = item[1]
        res_count[re][0] -=1
    for item in lack:
        re = item[1]
        res_count[re][1] +=1     

#print(res_count)   
print('---------------------------------------------------------')
res_f12 = {}
for (key,value) in res_count.items():
    pre = value[0]/value[3]
    recall = 1-value[1]/value[2]
    f1 = (2*pre*recall)/(pre+recall)
    res[key] = [round(pre,4),round(recall,4),round(f1,4)]
    res_f12[key] = [round(f1,4)]
print(res)
print('---------------------------------------------------------')
print(res_f12)


high = [] 
med = [] 
low  = []
for (key,value) in res_f1.items():
    #print(value)
    #print(res_f12[key])
    if value[0]>res_f12[key][0]+0.05:
        high.append(key)
    elif value[0]-res_f12[key][0] > 0 or res_f12[key][0]-value[0]<0.05:
        med.append(key)
    else:
        low.append(key)
print(len(high))
print(high)
print(len(med))
print(med)
print(len(low))
print(low)

