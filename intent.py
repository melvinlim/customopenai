from customopenai import LlmModel

STREAM=True

maxRespLen=200

#assistant_url='http://192.168.68.107:8080'
assistant_url='http://192.168.68.102:8080'

assistantText="you're a college girl."

document=""""""

#messages='<|im_start|>'+document+'<|im_end|>'+'\n'
#messages=document+'\n'
messages="would you like to do nothing, browse websites, listen to music, or dance?"

assistant=LlmModel(assistant_url,'girl',assistantText,stream=STREAM,maxRespLen=maxRespLen,top_p=0.1)
assistant.chatresp(messages)
