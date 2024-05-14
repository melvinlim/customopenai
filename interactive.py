from customopenai import LlmModel

STREAM=True

maxRespLen=200

#assistant_url='http://192.168.68.107:8080'
assistant_url='http://192.168.68.106:8080'

assistantText="you're an AI girl. the year is 2024."

document=""""""

#messages='<|im_start|>'+document+'<|im_end|>'+'\n'
#messages=document+'\n'
#messages="<|im_start|>human:what year is it?<|im_end|>\n"
messages=""

assistant=LlmModel(assistant_url,'girl',assistantText,stream=STREAM,maxRespLen=maxRespLen,top_p=0.1)
#msg=assistant.chatresp(messages)

for i in range(5):
	msg=input()
	messages+='<|im_start|>guy:'+msg+'<|im_end|>'
	msg=assistant.chatresp(messages)
	messages+='<|im_start|>girl:'+msg+'<|im_end|>'

