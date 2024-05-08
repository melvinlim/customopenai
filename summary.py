from customopenai import LlmModel

STREAM=True

maxRespLen=200

#assistant_url='http://192.168.68.107:8090'
assistant_url='http://192.168.68.102:8090'

assistantText="you're a helpful expert summarizer.  summarize the following document in 100 words or less without losing key information."

assistant2Text=""

document=""""""

document='ALICE was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, "and what is the use of a book," thought Alice, "without pictures or conversations?"'

document="""
alice:
Hello Eve. How was your day?
eve:
It was good, thanks for asking. How about you?
"""

x=open('logs/chats/disneyland3.txt','r')
x=x.read()
document=x
#import pdb
#pdb.set_trace()

#messages='<|im_start|>'+document+'<|im_end|>'+'\n'
messages=document+'\n'

assistant=LlmModel(assistant_url,'assistant',assistantText,stream=STREAM,maxRespLen=maxRespLen)
assistant2=LlmModel(assistant_url,'assistant',assistantText,stream=STREAM,maxRespLen=maxRespLen)

assistant.chatresp(messages)
assistant2.chatresp('summarize:'+messages)
