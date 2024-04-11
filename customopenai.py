import json
from urllib.request import Request, urlopen

STREAM=False
STREAM=True

startTok='<|im_start|>'
endTok='<|im_end|>'

responseLength=50
responseLength=100

def decodeStream(req):
	response=''
	result=''
	READSZ=20

	#import pdb
	#pdb.set_trace()

	while(True):
		datatag = -1
		while(datatag<0):
			nextresponse=req.read(READSZ).decode('utf-8')
			if(nextresponse==''):
				return result
			response+=nextresponse
			datatag=response.find('data: ')
		response=response[datatag+6:]
		datatag = -1
		while(datatag<0):
			nextresponse=req.read(READSZ).decode('utf-8')
			if(nextresponse==''):
				return result
			response+=nextresponse
			datatag=response.find('data: ')
		data=response[:datatag]
		x=json.loads(data)
		content=x['content']
		print(content,end='',flush=True)
		result+=content

class LlamaModel():
	def __init__(self,url,name,sysmsg):
		self.headers={"Content-type": "application/json"}
		self.url=url+'/completion'
		self.name=name
		self.sysmsg=sysmsg
		self.sysmsg=startTok+'system\n'+sysmsg+endTok+'\n'
		self.trailer=startTok+self.name+'\n'
		self.jsondata={
			'beam_width':5,
			'prompt':'',
			'n_predict':responseLength,
			'stream':STREAM,
			'stop':[startTok,endTok],
		}
	def chatresp(self,messages):
		#self.jsondata['prompt']=messages
		self.jsondata['prompt']=self.sysmsg+messages+self.trailer
		strdata=json.dumps(self.jsondata)
		if(STREAM):
			request=Request(method='POST', data=strdata.encode('utf-8'), headers=self.headers, url=self.url)
			req=urlopen(request)

			print(self.name+': ')
			result=decodeStream(req)
		else:
			request=Request(method='POST', data=strdata.encode('utf-8'), headers=self.headers, url=self.url)
			response=urlopen(request).read().decode('utf-8')

			result=''

			print(self.name+': ')
			x=json.loads(response)
			content=x['content']
			print(content,end='',flush=True)
			result+=content
		print('\n--------')
		return result

def chatOnce(llmmodel,messages):
	nextToSpeak=None

	result=llmmodel.chatresp(messages)
	resultl=result.lower()

	greatestIndex=-1
	nextIndex=resultl.find('bob')
	if(nextIndex>greatestIndex):
		greatestIndex=nextIndex
		nextToSpeak=1
	nextIndex=resultl.find('eve')
	if(nextIndex>greatestIndex):
		greatestIndex=nextIndex
		nextToSpeak=2
	nextIndex=resultl.find('alice')
	if(nextIndex>greatestIndex):
		nextToSpeak=0
	if(resultl.find('bob,')>=0):
		nextToSpeak=1
	elif(resultl.find('eve,')>=0):
		nextToSpeak=2
	elif(resultl.find('alice,')>=0):
		nextToSpeak=0

	messages+=startTok+llmmodel.name+'\n'+result+'\n'
	return messages,nextToSpeak
