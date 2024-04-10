import json

try:
	import requests
	REQUESTS=True
	STREAM=True
except:
	from urllib.request import Request, urlopen
	REQUESTS=False
	STREAM=False

startTok='<|im_start|>'
endTok='<|im_end|>'

responseLength=50
responseLength=100

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
		#response=requests.post(self.url, data=strdata, headers=self.headers, stream=True)
		request=Request(method='POST', data=strdata.encode('utf-8'), headers=self.headers, url=self.url)
		response=urlopen(request).read().decode('utf-8')

		result=''

		print(self.name+': ')
		if(STREAM):
			for line in response.iter_lines():
				if line:
					x=json.loads(line[6:])
					content=x['content']
					print(content,end='',flush=True)
					result+=content
		else:
			x=json.loads(response)
			content=x['content']
			print(content,end='',flush=True)
			result+=content
		print('\n--------')
		return result

#messages=startTok+'bob\nhi alice.'+endTok+'\n'
messages=startTok+'eve\nhi alice.'+endTok+'\n'
dolphin_url='http://192.168.68.107:8080'
capybara_url='http://192.168.68.107:8090'
airoboros_url='http://192.168.68.107:8070'

#dolphin=LlamaModel(dolphin_url,'alice','you are alice.  you\'re role playing being a wizard at hogwarts with your friends bob and eve.  bob will speak after you.')
#capybara=LlamaModel(capybara_url,'bob','you are bob.  you\'re role playing being a wizard at hogwarts with your friends alice and eve.  eve will speak after you.')
#airoboros=LlamaModel(airoboros_url,'eve','you are eve.  you\'re role playing being a wizard at hogwarts with your friends alice and bob.  alice will speak after you.')
#dolphin=LlamaModel(dolphin_url,'alice','you are alice.  you\'re role playing being a wizard at hogwarts with your friends bob and eve.  respond with ... to allow someone else to speak.')
#capybara=LlamaModel(capybara_url,'bob','you are bob.  you\'re role playing being a wizard at hogwarts with your friends alice and eve.  respond with ... to allow someone else to speak.')
#airoboros=LlamaModel(airoboros_url,'eve','you are eve.  you\'re role playing being a wizard at hogwarts with your friends alice and bob.  respond with ... to allow someone else to speak.')
dolphin=LlamaModel(dolphin_url,'alice','you are alice.  you\'re role playing being a wizard at hogwarts with your friends bob and eve.  respond with ... to allow someone else to speak.')
capybara=LlamaModel(capybara_url,'bob','you are bob.  you\'re role playing being a wizard at hogwarts with your friends alice and eve.  respond with ... to allow someone else to speak.')
airoboros=LlamaModel(airoboros_url,'eve','you are eve.  you\'re role playing being a wizard at hogwarts with your friends alice and bob.  respond with ... to allow someone else to speak.')

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

models=[dolphin,capybara,airoboros]
modelindex=0

chatrounds=4
for i in range(chatrounds):
	messages,nextToSpeak=chatOnce(models[modelindex],messages)
	if(nextToSpeak==None):
		modelindex=(modelindex+1)%3
	else:
		modelindex=nextToSpeak
	#messages=chatOnce(dolphin,messages)
	#messages=chatOnce(capybara,messages)
	#messages=chatOnce(airoboros,messages)

#print()
#print(result)
