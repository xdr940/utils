import json
from path import Path
p = Path('./timelines.json')

f = open(p,encoding='utf-8')
content = f.read()

dict =json.loads(content)

print(dict)
print('ok')