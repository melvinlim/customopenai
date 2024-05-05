from customopenai import LlmModel

STREAM=True

maxRespLen=5
maxRespLen=-1

#i have set capybara model to run at port 8090.
explorer_url='http://192.168.68.107:8090'

explorerText="explore the environment"
#explorerText="find a way into the castle"

document ="""You stand at a point of decision on a road which makes a wide fork to the
northeast and southeast, circling the base of the Lonely Mountain, which looms
high overhead to the east. A very long and winding road starts here and
stretches out of sight to the west through low, smoky hills.
The sun is rising over the lands to the east."""
#document ="""Outside Gate
#You are outside the western entrance to the castle. To the east stands an iron
#gate which is closed and chained. A winding road starts here and proceeds to the
#west.\n"""
#document+="<|im_start|>explorer:east|im_end|>\n"
#document+="The iron gate is locked.\n"
#document+="<|im_start|>explorer:you find a small key on the ground|im_end|>\n"
#document+="There was nothing on the ground.\n"

#messages='<|im_start|>'+document+'<|im_end|>'+'\n'
messages=document+'\n'

grammar='root ::= ("alice" | "bob" | "eve")'
grammar=None
logprobs=1
logprobs=5
logprobs=None

explorer=LlmModel(explorer_url,'explorer',explorerText,stream=STREAM,maxRespLen=maxRespLen,grammar=grammar,logprobs=logprobs)
result=explorer.chatresp(messages)

print(result)
