from readmdict import MDD

mdd = [*MDD("C:\\Users\\limuzhi\\Desktop\\[MDict电子词典资源合辑].CALD3_v1.4.mdd")]
items = [*MDD("C:\\Users\\limuzhi\\Desktop\\[MDict电子词典资源合辑].CALD3_v1.4.mdd").items()]

q = input()
result = items[mdd.index(q.encode())]
with open(f'tmp{q}', 'wb') as f:
    f.write(result[1])
""" 
for k,v in mdd.items():
    k = k.decode('utf-8')
    if 'z_test' in k:
        print(k)
        with open('./tmp/z_test.spx', 'wb') as f:
            f.write(v) """