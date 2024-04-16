from customopenai import LlmModel

STREAM=True

maxRespLen=5
maxRespLen=-1

#i have set capybara model to run at port 8090.
assistant_url='http://192.168.68.107:8090'

assistantText="write the name of the person the message is addressed to."

document ='<|im_start|>Bob, when did you meet up with Alice and Eve?<|im_end|>\nBob\n'
document+='<|im_start|>I just met Alice and Bob earlier.  How was your day, Eve?<|im_end|>\nEve\n'
document+="<|im_start|>Hello Eve.  Hello Bob.  What's new Alice?|im_end|>\nAlice\n"

document+="<|im_start|>Hello Eve.  Hello Alice.  What's new Bob?|im_end|>\n"

#messages='<|im_start|>'+document+'<|im_end|>'+'\n'
messages=document+'\n'

grammar='root ::= ("alice" | "bob" | "eve")'
logprobs=1
logprobs=5

assistant=LlmModel(assistant_url,'assistant',assistantText,stream=STREAM,maxRespLen=maxRespLen,grammar=grammar,logprobs=logprobs)
assistant.chatresp(messages)
