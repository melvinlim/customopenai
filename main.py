from customopenai import LlamaModel

STREAM=False
STREAM=True

maxRespLen=200

startTok='<|im_start|>'
endTok='<|im_end|>'

dolphin_url='http://192.168.68.107:8080'
capybara_url='http://192.168.68.107:8090'
airoboros_url='http://192.168.68.107:8070'

messages=startTok+'eve\nhi alice.'+endTok+'\n'

aliceText="you are alice.  a college student.  you're chatting with your friends bob and eve at a coffee shop during spring break."
bobText="you are bob.  a college student.  you're chatting with your friends alice and eve at a coffee shop during spring break."
eveText="you are eve.  a college student.  you're chatting with your friends alice and bob at a coffee shop during spring break."

dolphin=LlamaModel(dolphin_url,'alice',aliceText,stream=STREAM,maxRespLen=maxRespLen)
capybara=LlamaModel(capybara_url,'bob',bobText,stream=STREAM,maxRespLen=maxRespLen)
airoboros=LlamaModel(airoboros_url,'eve',eveText,stream=STREAM,maxRespLen=maxRespLen)

models=[dolphin,capybara,airoboros]
modelindex=0

chatrounds=6
for i in range(chatrounds):
	model=models[modelindex]
	messages,nextToSpeak=model.chatOnce(messages)
	if(nextToSpeak==None):
		modelindex=(modelindex+1)%3
	else:
		modelindex=nextToSpeak
	#messages=chatOnce(dolphin,messages)
	#messages=chatOnce(capybara,messages)
	#messages=chatOnce(airoboros,messages)

