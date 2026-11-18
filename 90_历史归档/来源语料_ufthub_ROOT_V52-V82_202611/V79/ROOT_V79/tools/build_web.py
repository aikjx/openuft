import csv,json,pathlib
p=pathlib.Path(__file__).resolve().parents[1]
f=p/'web/index.html'; s=f.read_text(encoding='utf-8')
data=[]
with (p/'data/equation_catalog.csv').open(encoding='utf-8-sig',newline='') as h:
    for row in csv.reader(h):
        if row and row[0]!='id': data.append(row)
if 'const EQ_DATA = __EQUATION_DATA__;' in s:
    s=s.replace('__EQUATION_DATA__',json.dumps(data,ensure_ascii=False))
    f.write_text(s,encoding='utf-8')
print('Embedded equations:',len(data))
