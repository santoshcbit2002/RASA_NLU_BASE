from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
import emailpy
import zomato_utils
import zomatopy
import json

zomato = zomatopy.initialize_app()

class ActionSearchRestaurants(Action):
	def name(self):
		return 'action_restaurant'
		
	def run(self, dispatcher, tracker, domain):

		location_name = tracker.get_slot('location')
		cuisine = tracker.get_slot('cuisine')
		budget = tracker.get_slot('budget')

		location = zomato_utils.get_valid_location(location_name)

		response = ""
		if location['is_valid']:
			top_5_restaurants = zomato_utils.get_top_restaurants_by_user_ratings(location, cuisine, budget)
			if len(top_5_restaurants) == 0:
				response = "No restaurants found in {} serving {} cuisine in {} budget".format(location_name, cuisine, budget)
			else:
				for restaurant in top_5_restaurants:
					response=response+ "{} in {} has been rated {}\n".format(restaurant['name'], restaurant['address'], restaurant['user_rating'])
		else:
			response = "We do not operate in that area yet"
		
		dispatcher.utter_message(response)

class ActionSendEmail(Action):
	def name(self):
		return 'action_sendemail'
		
	def run(self, dispatcher, tracker, domain):
		location_name = tracker.get_slot('location')
		cuisine = tracker.get_slot('cuisine')
		budget = tracker.get_slot('budget')

		location = zomato_utils.get_valid_location(location_name)
		top_10_restaurants = zomato_utils.get_top_restaurants_by_user_ratings(location, cuisine, budget, top_n=10)

		email_address = tracker.get_slot('email_address')
		subject = "[FOODIE] Restaurant search results for {} budget restaurants serving {} cuisine in {}".format(budget, cuisine, location_name)
		success = emailpy.send_mail(email_address, subject, location_name, cuisine, budget, top_10_restaurants)

		response=""
		if success:
			response = "An email has been sent to {}. Please search the inbox for subject {}".format(email_address, subject)
		else:
			response = "Oops! Email could not be sent. Sorry for the inconvenience."
		
		dispatcher.utter_message(response)
