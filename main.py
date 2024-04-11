from customopenai import LlamaModel, chatOnce

STREAM=False
STREAM=True

startTok='<|im_start|>'
endTok='<|im_end|>'

messages=startTok+'eve\nhi alice.'+endTok+'\n'
dolphin_url='http://192.168.68.107:8080'
capybara_url='http://192.168.68.107:8090'
airoboros_url='http://192.168.68.107:8070'

#dolphin=LlamaModel(dolphin_url,'alice','you are alice.  you\'re role playing being a wizard at hogwarts with your friends bob and eve.  respond with ... to allow someone else to speak.')
#capybara=LlamaModel(capybara_url,'bob','you are bob.  you\'re role playing being a wizard at hogwarts with your friends alice and eve.  respond with ... to allow someone else to speak.')
#airoboros=LlamaModel(airoboros_url,'eve','you are eve.  you\'re role playing being a wizard at hogwarts with your friends alice and bob.  respond with ... to allow someone else to speak.')

aliceText="you are alice.  a college student.  you're chatting with your friends bob and eve at a coffee shop."
bobText="you are bob.  a college student.  you're chatting with your friends alice and eve at a coffee shop."
eveText="you are eve.  a college student.  you're chatting with your friends alice and bob at a coffee shop."

dolphin=LlamaModel(dolphin_url,'alice',aliceText)
capybara=LlamaModel(capybara_url,'bob',bobText)
airoboros=LlamaModel(airoboros_url,'eve',eveText)

models=[dolphin,capybara,airoboros]
modelindex=0

chatrounds=6
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
