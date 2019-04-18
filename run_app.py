import global_config
from rasa_core.channels import HttpInputChannel
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_slack_connector import SlackInput


nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/restaurantnlu')
agent = Agent.load('./models/dialogue', interpreter = nlu_interpreter)

input_channel = SlackInput(global_config.get_config('slack','access_token'), #app verification token
						   global_config.get_config('slack','bot_access_token'), # bot verification token
						   global_config.get_config('slack','verification_token'), # slack verification token
						   True)

agent.handle_channel(HttpInputChannel(5004, '/', input_channel))