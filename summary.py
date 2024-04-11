from customopenai import LlamaModel

STREAM=True

maxRespLen=200

assistant_url='http://192.168.68.107:8090'

assistantText="you're a helpful expert summarizer.  summarize the following document in 100 words or less without losing key information."

document=""""""

#messages='<|im_start|>'+document+'<|im_end|>'+'\n'
messages=document+'\n'

assistant=LlamaModel(assistant_url,'assistant',assistantText,stream=STREAM,maxRespLen=maxRespLen)
assistant.chatresp(messages)
