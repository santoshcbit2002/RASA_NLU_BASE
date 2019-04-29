import global_config
from rasa_core.channels.slack import SlackInput
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.utils import EndpointConfig


nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/restaurantnlu')
actionendpoint = EndpointConfig(url="http://localhost:5055/webhook")
agent = Agent.load('./models/dialogue', interpreter = nlu_interpreter,action_endpoint = actionendpoint)

input_channel = SlackInput(global_config.get_config('slack','bot_access_token'))
 # global_config.get_config('slack','bot_access_token'), 
 #						   global_config.get_config('slack','verification_token'))

s = agent.handle_channels([input_channel], 5004, serve_forever=True)