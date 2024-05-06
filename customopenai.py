import json
from urllib.request import Request, urlopen

startTok='<|im_start|>'
endTok='<|im_end|>'

def decodeStream(req,logprobs=False):
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
		if(logprobs):
			print('\n')
			print(x['completion_probabilities'])
			print('\n')
		result+=content

def getPreMsg(name):
		#return name+':'+startTok
		return startTok+name+':\n'

class LlmModel():
	def __init__(self,url,name,sysmsg,stream=None,maxRespLen=None,grammar=None,logprobs=None,top_k=None,ONESENTENCE=False):
		self.stream=False
		self.logprobs=False
		self.headers={"Content-type": "application/json"}
		self.url=url+'/completion'
		self.name=name
		self.sysmsg=sysmsg
		self.sysmsg=getPreMsg('system')+sysmsg+endTok+'\n'
		self.trailer=getPreMsg(self.name)
		self.jsondata={
			#'beam_width':5,
			'prompt':'',
			#'stop':[startTok,endTok,'.'],
		}
		if(ONESENTENCE):
			self.jsondata['stop']=[startTok,endTok,'.']
		else:
			self.jsondata['stop']=[startTok,endTok]
		#import pdb
		#pdb.set_trace()
		if(stream):
			self.stream=True
			self.jsondata['stream']=stream
		if(maxRespLen):
			self.jsondata['n_predict']=maxRespLen
		if(top_k):
			self.jsondata['top_k']=top_k
		if(grammar):
			self.jsondata['grammar']=grammar
		if(logprobs):
			self.logprobs=True
			#self.jsondata['logprobs']=logprobs
			self.jsondata['n_probs']=logprobs
	def chatresp(self,messages):
		#self.jsondata['prompt']=messages
		self.jsondata['prompt']=self.sysmsg+messages+self.trailer
		print(self.jsondata['prompt'])
		strdata=json.dumps(self.jsondata)
		if(self.stream):
			request=Request(method='POST', data=strdata.encode('utf-8'), headers=self.headers, url=self.url)
			req=urlopen(request)

			print(self.name+': ')
			result=decodeStream(req,self.logprobs)
		else:
			request=Request(method='POST', data=strdata.encode('utf-8'), headers=self.headers, url=self.url)
			response=urlopen(request).read().decode('utf-8')

			result=''

			print(self.name+': ')
			x=json.loads(response)
			content=x['content']
			print(content,end='',flush=True)
			result+=content
			if(self.logprobs):
				print('\n')
				print(x['completion_probabilities'])
		print('\n--------')
		#import pdb
		#pdb.set_trace()
		return result

	def chatOnce(self,messages):
		nextToSpeak=None

		result=self.chatresp(messages)
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

		#messages+=startTok+self.name+':'+result+endTok+'\n'
		#messages+=self.name+':'+startTok+result+endTok+'\n'
		messages+=getPreMsg(self.name)+result+endTok+'\n'
		return messages,nextToSpeak
