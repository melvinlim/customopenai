import json
x=open('data00.json','r')
x=open('data01.json','r')
y=x.read()
z=json.loads(y)
for t in z:
	#import pdb
	#pdb.set_trace()
	#print(t['story'])
	if(t['story'].find('JERRY')>=0):
		print(t['story'])
		input()
