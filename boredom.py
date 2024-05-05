from customopenai import LlmModel

STREAM=True

maxRespLen=5
maxRespLen=-1

storyteller_url='http://192.168.68.107:8080'
storytellerText="you are telling a story to the explorer.  he decides what action to take every 1 to 2 sentences."

#i have set capybara model to run at port 8090.
explorer_url='http://192.168.68.107:8090'
explorerText="you are listening to a story.  you respond with a brief action you want to take."

#document ="storyteller:you're relaxing on the bed in your apartment\n"
document ="storyteller:you're relaxing on a beach in hawaii."
messages='<|im_start|>'+document+'<|im_end|>'+'\n'

grammar='root ::= ("alice" | "bob" | "eve")'
grammar=None
logprobs=1
logprobs=5
logprobs=None

explorer=LlmModel(explorer_url,'explorer',explorerText,stream=STREAM,maxRespLen=maxRespLen,grammar=grammar,logprobs=logprobs)
storyteller=LlmModel(storyteller_url,'storyteller',storytellerText,stream=STREAM,maxRespLen=maxRespLen,grammar=grammar,logprobs=logprobs)

for i in range(5):
	msg=explorer.chatresp(messages)
	messages+='<|im_start|>explorer:'+msg+'<|im_end|>'+'\n'
	msg=storyteller.chatresp(messages)
	messages+='<|im_start|>storyteller:'+msg+'<|im_end|>'+'\n'

print(messages,flush=True)
