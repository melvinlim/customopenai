from customopenai import LlmModel

STREAM=False
STREAM=True

maxRespLen=200

startTok='<|im_start|>'
endTok='<|im_end|>'

dolphin_url='http://192.168.68.107:8080'		#great at discussing quantum physics and philosophy.
airoboros_url='http://192.168.68.107:8070'	#seems to perform better at functions.  also knowledgeable of fantasy books.
raven_url='http://192.168.68.107:8060'

#messages=startTok+'bob:Hi Alice!'+endTok+'\n'
#messages=startTok
messages='alice'+startTok

#aliceText="you are alice, a college student. you're chatting with your friend bob about philosophy and quantum physics."
#aliceText="you are alice and you're trying to get to know your friend bob at a coffee shop."
#aliceText="you are alice and you're exploring the grand bazaar with your friend bob.  you discuss the items for sale at various stalls."
aliceText="you are alice and you're exploring disneyland with your friend bob."
#bobText="you are bob and you're chatting with your friend alice. you enjoy role playing as a psychic."
#bobText="you are bob and you're chatting with your friend alice. you're paranoid and you think the illuminati is after you."
#bobText="you are bob and you're chatting with your friend alice. you just did acid and are really high."
#bobText="you are bob and you're exploring the grand bazaar with your friend alice.  you discuss the items for sale at various stalls."
bobText="you are bob and you're exploring disneyland with your friend alice."

dolphin=LlmModel(dolphin_url,'alice',aliceText,stream=STREAM,maxRespLen=maxRespLen)
airoboros=LlmModel(raven_url,'bob',bobText,stream=STREAM,maxRespLen=maxRespLen)

models=[dolphin,airoboros]
modelindex=0

chatrounds=6
for i in range(chatrounds):
	model=models[modelindex]
	messages,nextToSpeak=model.chatOnce(messages)
	modelindex=(modelindex+1)%2
	#messages=chatOnce(dolphin,messages)
	#messages=chatOnce(capybara,messages)
	#messages=chatOnce(airoboros,messages)

fd=open('latestchat.txt','w')
fd.write(messages)
fd.close()
