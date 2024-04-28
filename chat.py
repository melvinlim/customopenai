from customopenai import LlmModel

STREAM=False
STREAM=True

maxRespLen=200

startTok='<|im_start|>'
endTok='<|im_end|>'

dolphin_url='http://192.168.68.107:8080'		#great at discussing quantum physics and philosophy.
airoboros_url='http://192.168.68.107:8070'	#seems to perform better at functions.  also knowledgeable of fantasy books.
raven_url='http://192.168.68.107:8060'

messages=startTok+'bob:Hi Alice!'+endTok+'\n'

aliceText="you are alice, a college student. you're chatting with your friend bob about philosophy and quantum physics."
bobText="you are bob, a college student.  you're chatting with your friend alice about philosophy and quantum physics."

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
