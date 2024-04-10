import json
import requests

startTok='<|im_start|>'
endTok='<|im_end|>'

responseLength=50
responseLength=100

class LlamaModel():
	def __init__(self,url,name,sysmsg,grammar=None):
		self.headers={"Content-type": "application/json"}
		self.url=url+'/completion'
		self.name=name
		self.sysmsg=sysmsg
		self.sysmsg=startTok+'system\n'+sysmsg+endTok+'\n'
		self.trailer=startTok+self.name+'\n'
		self.jsondata={
			'prompt':'',
			'n_predict':responseLength,
			'stream':True,
			'stop':[startTok,endTok],
		}
		if(grammar):
			print('added grammar.')
			self.jsondata['grammar']=grammar
			self.jsondata['n_probs']=4
			print(self.jsondata)
	def chatresp(self,messages,grammar=None):
		if(grammar):
			self.jsondata['grammar']=grammar
		#self.jsondata['prompt']=messages
		self.jsondata['prompt']=self.sysmsg+messages+self.trailer
		strdata=json.dumps(self.jsondata)
		response=requests.post(self.url, data=strdata, headers=self.headers, stream=True)

		result=''

		print(self.name+': ')
		for line in response.iter_lines():
			if line:
				#print(line)
				x=json.loads(line[6:])
				content=x['content']
				print(content,end='',flush=True)
				try:
					y=x['prompt']
					print(y,end='',flush=True)
					#y=x['completion_probabilities']
					#print(y,end='',flush=True)
				except:
					pass
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

#grammar='root ::= ("alice" | "bob" | "eve")'
grammar1='root ::= ("bob" | "eve")'
grammar2='root ::= ("eve" | "alice")'
grammar3='root ::= ("bob" | "alice")'

#chatOrderChooser=LlamaModel(capybara_url,'orderChooser',"respond with the next speaker's name.  do not allow anyone to speak twice.  ensure everyone has a chance to speak.",grammar)
chatOrderChooser=LlamaModel(capybara_url,'orderChooser',"respond with the next speaker's name.  ensure everyone has a chance to speak.",grammar1)

def chatOnce(llmmodel,messages,grammar=None):
	nextToSpeak=None

	result=llmmodel.chatresp(messages,grammar)
	resultl=result.lower()

#should compare indexes and set nextToSpeak to greatest index (last mentioned)
	if(resultl.find('bob')>=0):
		nextToSpeak=1
		#nextToSpeak=capybara
	elif(resultl.find('eve')>=0):
		nextToSpeak=2
		#nextToSpeak=airoboros
	elif(resultl.find('alice')>=0):
		nextToSpeak=0
		#nextToSpeak=dolphin

	messages+=startTok+llmmodel.name+'\n'+result+'\n'
	return messages,nextToSpeak

models=[dolphin,capybara,airoboros]
modelindex=0

#import pdb
#pdb.set_trace()

chatrounds=2
for i in range(chatrounds):
	messages,nextToSpeak=chatOnce(models[modelindex],messages)
	speaker,nts=chatOnce(chatOrderChooser,messages,grammar1)
	if(speaker.find('alice')>=0):
		modelindex=0
	elif(speaker.find('bob')>=0):
		modelindex=1
	elif(speaker.find('eve')>=0):
		modelindex=2
	#if(nextToSpeak==None):
	#	modelindex=(modelindex+1)%3
	#else:
	#	modelindex=nextToSpeak
	#messages=chatOnce(dolphin,messages)
	#messages=chatOnce(capybara,messages)
	#messages=chatOnce(airoboros,messages)

#print()
#print(result)
