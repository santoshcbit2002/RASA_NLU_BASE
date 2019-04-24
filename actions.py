from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core_sdk import Action
from rasa_core_sdk import Tracker
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.executor import CollectingDispatcher
from rasa_core_sdk.forms import FormAction
import emailpy
import zomato_utils
import zomatopy
import json

zomato = zomatopy.initialize_app()

class RestaurantForm(FormAction):

    def name(self):
        return "restaurant_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["location", "cuisine", "budget"]

    def slot_mappings(self):
        return {
			"location": self.from_entity(entity="location", intent="restaurant_search"),
			"cuisine": self.from_entity(entity="cuisine", intent="restaurant_search"),
            "budget": self.from_entity(entity="budget", intent="restaurant_search")
		}

    @staticmethod
    def cuisine_db():
        # type: () -> List[Text]
        """Database of supported cuisines"""
        return ["caribbean",
                "chinese",
                "french",
                "greek",
                "indian",
                "italian",
                "mexican"]

    def validate_cuisine(self,
                         value: Text,
                         dispatcher: CollectingDispatcher,
                         tracker: Tracker,
                         domain: Dict[Text, Any]) -> Optional[Text]:
        """Validate cuisine value."""

        if value.lower() in self.cuisine_db():
            # validation succeeded
            return value
        else:
            dispatcher.utter_template('utter_wrong_cuisine', tracker)
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return None

    def validate_num_people(self,
                            value: Text,
                            dispatcher: CollectingDispatcher,
                            tracker: Tracker,
                            domain: Dict[Text, Any]) -> Optional[Text]:
        """Validate num_people value."""

        if self.is_int(value) and int(value) > 0:
            return value
        else:
            dispatcher.utter_template('utter_wrong_num_people', tracker)
            # validation failed, set slot to None
            return None

    @staticmethod
    def validate_outdoor_seating(value: Text,
                                 dispatcher: CollectingDispatcher,
                                 tracker: Tracker,
                                 domain: Dict[Text, Any]) -> Any:
        """Validate outdoor_seating value."""

        if isinstance(value, str):
            if 'out' in value:
                # convert "out..." to True
                return True
            elif 'in' in value:
                # convert "in..." to False
                return False
            else:
                dispatcher.utter_template('utter_wrong_outdoor_seating',
                                          tracker)
                # validation failed, set slot to None
                return None

        else:
            # affirm/deny was picked up as T/F
            return value

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_template('utter_submit', tracker)
        return []

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
				index = 1
				response = "Following are top 5 restaurants matching your preference in order of average user rating on zomato:\n\n"
				for restaurant in top_5_restaurants:
					response = response + "{}. {} in {} has been rated {}\n".format(index, restaurant['name'], restaurant['address'], restaurant['user_rating'])
					index += 1
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
			response = "An email has been sent to {}.\nPlease search the inbox for subject:\n\"{}\"".format(email_address, subject)
		else:
			response = "Oops! Email could not be sent. Sorry for the inconvenience."
		
		dispatcher.utter_message(response)
