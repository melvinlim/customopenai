from customopenai import LlmModel

STREAM=True

maxRespLen=5
maxRespLen=-1

storyteller_url='http://192.168.68.107:8080'
storytellerText="you are telling a story to the explorer. you allow him to act after each sentence."

#i have set capybara model to run at port 8090.
explorer_feelings_url='http://192.168.68.107:8090'
explorer_feelingsText="you are an explorer's feelings. respond with one sentence describing your feelings."

explorer_thought_url='http://192.168.68.107:8090'
explorer_thoughtText="you are an explorer's thought process. respond with one sentence describing what your thoughts."

explorer_action_url='http://192.168.68.107:8090'
explorer_actionText="you are an explorer's actions. respond with one sentence describing your action."

#document ="storyteller:you're relaxing on the bed in your apartment\n"
#document ="storyteller:you're relaxing on a beach in hawaii."
#document ="storyteller:you're relaxing on a hammock between two palm trees on a tropical island."
document ="storyteller:you're exploring a cruise ship."
messages='<|im_start|>'+document+'<|im_end|>'+'\n'

grammar='root ::= ("alice" | "bob" | "eve")'
grammar=None
logprobs=1
logprobs=5
logprobs=None

explorer_feelings=LlmModel(explorer_feelings_url,'explorer_feelings',explorer_feelingsText,stream=STREAM,maxRespLen=maxRespLen,grammar=grammar,logprobs=logprobs)
explorer_thought=LlmModel(explorer_thought_url,'explorer_thought',explorer_thoughtText,stream=STREAM,maxRespLen=maxRespLen,grammar=grammar,logprobs=logprobs)
explorer_action=LlmModel(explorer_action_url,'explorer_action',explorer_actionText,stream=STREAM,maxRespLen=maxRespLen,grammar=grammar,logprobs=logprobs)
storyteller=LlmModel(storyteller_url,'storyteller',storytellerText,stream=STREAM,maxRespLen=maxRespLen,grammar=grammar,logprobs=logprobs)

for i in range(5):
	msg=explorer_feelings.chatresp(messages)
	messages+='<|im_start|>explorer_feelings:'+msg+'<|im_end|>'+'\n'
	msg=explorer_thought.chatresp(messages)
	messages+='<|im_start|>explorer_thought:'+msg+'<|im_end|>'+'\n'
	msg=explorer_action.chatresp(messages)
	messages+='<|im_start|>explorer_action:'+msg+'<|im_end|>'+'\n'
	msg=storyteller.chatresp(messages)
	messages+='<|im_start|>storyteller:'+msg+'<|im_end|>'+'\n'

print(messages,flush=True)
