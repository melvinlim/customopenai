import json
PATH='chats'
PATH='fixedScripts'
def readDataJson():
	a=open('data49.json','r')
	b=a.read()
	c=json.loads(b)
	d=c[:3]
	return d

def readText(filename,PATH=None):
	#import pdb
	#pdb.set_trace()
	try:
		if(PATH):
			filename = PATH+'/'+filename
		z=open(filename,'r')
		x=z.read()
		#y=json.dumps(x)
		return x
	except:
		return ''

import re

#y=re.sub(':[\n]+',': ',x)
#w=re.sub('[\n]+','\n',y)

#y=re.sub(':[\n]+','":"',x)
#w=re.sub('[\n]+','","',y)

def readJson():
	fd=open('zxcv.json','r')
	z=fd.read()
	x=json.loads(z)
	return x

#x=readText()

#y=re.sub(':[\n]+',': ',x)
#w=re.sub('[\n]+','\n',y)

import subprocess
def listfiles(PATH=''):
	x=subprocess.check_output(['ls',PATH])
	y=x.decode('ascii')
	z=y.split('\n')
	return z

def processItem1(item):
	item=item.strip('\n')
	x=item.replace(':\n','":"')
	y=x.replace('\n','"},{"')
	z='[{"'+y+'"}]'
	try:
		result=json.loads(z)
	except:
		print(z)
		assert False
	return result

def processItem2(item):
	item=item.strip('\n')
	x=item.replace(':\n',':')
	y=x.replace('\n','","')
	z='["'+y+'"]'
	try:
		result=json.loads(z)
	except:
		print(z)
		assert False
	return result

def processItem3(item):
	item=item.strip('\n')
	y=item.replace('\n',' ')
	z='{"story":"'+y+'"}'
	try:
		result=json.loads(z)
	except:
		print(z)
		assert False
	return result

def processItem4(item):
	item=item.strip('\n')
	y=item.replace('\n',' ')
	y=y.replace('<|im_start|>','')
	y=y.replace('<|im_end|>','')
	y=y.replace('"','\\"')
	z='{"story":"'+y+'"}'
	#import pdb
	#pdb.set_trace()
	try:
		result=json.loads(z)
	except:
		print(z)
		assert False
	return result

def processTexts(texts):
	#import pdb
	#pdb.set_trace()
	result=[]
	y=texts.split('\n\n')
	for x in y:
		result += [processItem4(x)]
	return result

chats=[]

def readFromPath(chats,PATH):
	fl=listfiles(PATH)
	for x in fl:
		print('reading: '+x)
		chats += [{'title':x,'text':readText(x,PATH)}]
		#print(x)

readFromPath(chats,PATH)

jsonData=[]
for chat in chats:
	print('processing: '+chat['title'])
	if(chat['text']!=''):		#should have not added empty entries at all.  might fix this later.
		jsonData += processTexts(chat['text'])
		#jsonData += [processTexts(chat['text'])]

def saveText(data,outputfile):
	fd=open(outputfile,'w')
	fd.write(data)
	fd.close()

def saveData(jsonData,outputfile):
	jsonString=json.dumps(jsonData)
	fd=open(outputfile,'w')
	fd.write(jsonString)
	fd.close()

def processSentence1(sent):
	result = '{"story":"'+sent+'"}'
	return result

finalData=[]

for conv in jsonData:
	#print(conv)
	for sentence in conv:
		#print(sentence)
		finalData += [processSentence1(sentence)]
		
#saveData(jsonData,'result.json')
mid=int(len(jsonData)/2)
saveData(jsonData[:mid],'data00.json')
saveData(jsonData[mid:],'data01.json')

z=readText('scripts/seinfeld-ep1.txt')

def processSeinfeld1(script):
	script=script.replace(':','-')
	x=re.sub(r'([A-Z]+)\n[ ]+',r'\1:\n',script)
	y=re.sub(r'(  )+[ \n]*','',x)
	z=re.sub(r'[\n][ \n]+',r'<endtok>',y)
	a=re.sub('\n','',z)
	b=re.sub(':',':\n',a)
	c=re.sub('<endtok>','\n',b)
	return c

def splitAndSaveSeinfeld(data):
	x=processSeinfeld1(data)
	#saveText(x,'tmp.txt')

	x=x.replace('JERRY','<SPLIT>JERRY')
	z=x.split('<SPLIT>')

	y=len(z)
	i=0
	while(i<y):
		data=''.join(z[i:i+10])
		saveText(data,'seinfeld-ep1-'+str(i)+'.txt')
		i+=10

splitAndSaveSeinfeld(z)
