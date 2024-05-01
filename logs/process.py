import json
PATHS=['chats','fixedScripts']
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
	y=y.replace('\t',' ')
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
	y=y.lower()
	y=y.replace('<|im_start|>','')
	y=y.replace('<|im_end|>','')
	y=re.sub(r'[s]+h[h]+',r'shh',y)
	y=re.sub(r'[o]+h[h]+',r'oh',y)
	y=y.replace('"','\\"')
	y=y.replace('<','(')
	y=y.replace('>',')')
	y=y.replace('{','(')
	y=y.replace('}',')')
	y=re.sub(r'[^\x00-\x7F]+', ' ', y)
	y=y.replace('“','\\"')
	y=y.replace('”','\\"')
	y=y.replace('\t',' ')
	y=re.sub(r'[!]+','!',y)
	y=re.sub(r'[\`]+','\\"',y)
	y=re.sub(r"'[']+",'\\"',y)
	z='{"story":"'+y+'"}'
	#import pdb
	#pdb.set_trace()
	try:
		result=json.loads(z)
	except:
		import pdb
		pdb.set_trace()
		print(z)
		assert False
	return result

def processTexts(texts):
	#import pdb
	#pdb.set_trace()
	#result=[]
	#y=texts.split('\n\n')
	#for x in y:
	#	result += [processItem4(x)]
	result = [processItem4(texts)]
	return result

def readFromPath(chats,PATH):
	fl=listfiles(PATH)
	for x in fl:
		print('reading: '+x)
		chats += [{'title':x,'text':readText(x,PATH)}]
		#print(x)

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

def processSeinfeld1(script):
	script=script.replace(':','-')
	x=re.sub(r'([A-Z]+)\n[ ]+',r'\1:\n',script)
	y=re.sub(r'(  )+[ \n]*','',x)
	z=re.sub(r'[\n][ \n]+',r'<endtok>',y)
	a=re.sub('\n','',z)
	b=re.sub(':',':\n',a)
	c=re.sub('<endtok>','\n',b)
	c=re.sub(r'\([sS]cene [eE]nd.*\)','',c)
	return c

def splitAndSaveSeinfeld(filename):
	data=readText('scripts/seinfeld/'+filename)
	x=processSeinfeld1(data)
	#saveText(x,'tmp.txt')

	x=x.replace('JERRY','<SPLIT>JERRY')
	z=x.split('<SPLIT>')

	name=filename.strip('.txt')

	y=len(z)
	i=0
	while(i<y):
		data=''.join(z[i:i+10])
		saveText(data,'fixedScripts/'+name+'-'+str(i)+'.txt')
		i+=10

def processFriends(script):
	#x=re.sub(r'End\n.+\nWritten.+\n',r'EPISODEEND',z,flags=re.MULTILINE)
	#x=re.sub(r'End\n.+\nWritten.+\n\[.+\]',r'EPISODEEND',z)
	#x=re.sub(r'End\n.+\nWritten.+\n',r'EPISODEEND',z)
	script=script.lower()
	x=re.sub(r'[^\x00-\x7F]+', ' ', script)
	x=re.sub(r'end.*[\n]+.+[\n]+.+\n+.transcribe.+','',x)
	x=re.sub(r'end.*[\n]+.+[\n]+.*written.+','',x)
	x=re.sub(r'end.*[\n]+.+[\n]+.+\n+.*written.+','',x)
	x=re.sub(r'end.*[\n]+.+[\n]+.*story.+','',x)
	x=re.sub(r'end.*[\n]+.+[\n]+.+\n+aired:.+','',x)
	x=re.sub(r'\[.+\]','<SCENE>',x)
	x=re.sub(r'the end','<SCENE>',x)
	x=re.sub(r'opening credits','',x)
	x=re.sub(r'closing credits','',x)
	x=re.sub(r'ending credits','',x)
	x=re.sub(r'credits','',x)
	x=re.sub(r'thanksgiving 1915','',x)
	x=re.sub(r'commercial break','',x)
	x=re.sub(r'<SCENE>[\n]*<SCENE>','',x)
	return x

def splitAndSaveFriends(data):
	x=processFriends(data)
	#saveText(x,'tmp.txt')
	x=x.split('<SCENE>')
	x=x[1:-1]		#first and last entries are not scenes.

	i=0	
	for z in x:
		if(len(z)>1):
			i+=1
			saveText(z.strip('\n'),'fixedScripts/friends-'+str(i)+'.txt')
			#saveText(z,'friends-'+str(i)+'.txt')
	#y=len(x)
	#i=0
	#while(i<y):
	#	data=''.join(z[i:i+10])
	#	saveText(data,'friends-'+str(i)+'.txt')
	#	i+=10

def processFrasier1(script):
	#script=script.replace(':','-')
	script=script.replace('[','(')
	script=script.replace(']',')')
	#x=re.sub(r'FADE.+[\n]+.*[\n]+.cene.+\n',r'',script,flags=re.MULTILINE)
	x=re.sub(r'End.+[\n]+.*[\n]+.cene.+\n',r'<SCENE>',script,flags=re.MULTILINE)
	x=re.sub(r'FADE.*[\n]+.*[\n]+.cene.+\n',r'<SCENE>',x,flags=re.MULTILINE)
	x=re.sub(r'([A-Za-z]+):',r'<SENTENCE>\1:',x)
	x=re.sub(r'[ \n]+',r' ',x)
	x=re.sub(r'[ ]*<SENTENCE>[ ]*',' ',x)
	c=x
	#x=re.sub(r'([A-Z]+)\n[ ]+',r'\1:\n',script)
	#y=re.sub(r'(  )+[ \n]*','',x)
	#z=re.sub(r'[\n][ \n]+',r'<endtok>',y)
	#a=re.sub('\n','',z)
	#b=re.sub(':',':\n',a)
	#c=re.sub('<endtok>','\n',b)
	return c

def splitAndSaveFrasier(filename):
	data=readText('scripts/frasier/'+filename)
	x=processFrasier1(data)
	x=x.split('<SCENE>')
	name=filename.strip('.txt')
	y=len(x)
	i=0
	while(i<y):
		data=x[i]
		saveText(data,'fixedScripts/'+name+'-'+str(i)+'.txt')
		i+=1

z=listfiles('scripts/frasier')
for fn in z:
	if(len(fn)>4):
		splitAndSaveFrasier(fn)
#saveText(asdf,'tmp.txt')

z=listfiles('scripts/seinfeld')
for fn in z:
	if(len(fn)>4):
		splitAndSaveSeinfeld(fn)

z=readText('scripts/Friends_Transcript.txt')
splitAndSaveFriends(z)

chats=[]

for PATH in PATHS:
	readFromPath(chats,PATH)

jsonData=[]
for chat in chats:
	print('processing: '+chat['title'])
	if(chat['text']!=''):		#should have not added empty entries at all.  might fix this later.
		jsonData += processTexts(chat['text'])
		#jsonData += [processTexts(chat['text'])]

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

