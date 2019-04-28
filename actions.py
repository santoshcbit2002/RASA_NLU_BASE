from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core_sdk import Action
from rasa_core_sdk import Tracker
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.executor import CollectingDispatcher
from rasa_core_sdk.forms import FormAction
from typing import Dict, Text, Any, List, Union, Optional
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
    def validate_location(self,
                          value: Text,
                          dispatcher: CollectingDispatcher,
                          tracker: Tracker,
                          domain: Dict[Text, Any]) -> Optional[Text]:

        location = zomato_utils.get_valid_location(value)

        if location['is_valid']:
            SlotSet('lat', location["latitude"])
            SlotSet('lon', location["longitude"])
            return location["city_name"].lower()
        else:
            dispatcher.utter_template('utter_wrong_location', tracker)
            return None

    @staticmethod
    def validate_cuisine(self,
                         value: Text,
                         dispatcher: CollectingDispatcher,
                         tracker: Tracker,
                         domain: Dict[Text, Any]) -> Optional[Text]:
        cuisine = zomato_utils.get_valid_cuisine(value)
        if cuisine['is_valid']:
            return cuisine["cuisine_id"]
        else:
            dispatcher.utter_template('utter_wrong_cuisine', tracker)
            return None

    @staticmethod
    def validate_budget(self,
                        value: Text,
                        dispatcher: CollectingDispatcher,
                        tracker: Tracker,
                        domain: Dict[Text, Any]) -> Optional[Text]:
        budget = zomato_utils.get_valid_budget(value)
        if budget['is_valid']:
            return budget["type"]
        else:
            dispatcher.utter_template('utter_wrong_budget', tracker)
            return None

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict]:
        location_name = tracker.get_slot('location')
        lat = tracker.get_slot('lat')
        lon = tracker.get_slot('lon')
        cuisine = tracker.get_slot('cuisine')
        budget = tracker.get_slot('budget')

        top_5_restaurants = zomato_utils.get_top_restaurants_by_user_ratings(lat, lon, cuisine, budget)
        response = "No restaurants found in {} serving {} cuisine in {} budget".format(location_name, cuisine, budget)
        if len(top_5_restaurants) > 0:
            index = 1
            response = "Following are top 5 restaurants matching your preference in order of average user rating on zomato:\n\n"
            for restaurant in top_5_restaurants:
                response = response + "{}. {} in {} has been rated {}\n".format(index, restaurant['name'], restaurant['address'], restaurant['user_rating'])
                index += 1

        dispatcher.utter_message(response)
        return []

class ActionValidateLocation(Action):
    def name(self):
        return 'validate_location'
        
    def run(self, dispatcher, tracker, domain):

        location_name = tracker.get_slot('location')
        location = zomato_utils.get_valid_location(location_name)

        if location['is_valid']:
            return[SlotSet("lat", location["latitude"]), SlotSet("lon", location["longitude"])]
        else:
            dispatcher.utter_template('utter_wrong_location', tracker)
            return []

class ActionValidateCuisine(Action):
    def name(self):
        return 'validate_cuisine'
        
    def run(self, dispatcher, tracker, domain):
        _cuisine = tracker.get_slot('cuisine')
        cuisine = zomato_utils.get_valid_cuisine(_cuisine)
        if cuisine['is_valid']:
            return[SlotSet("cuisine_id", cuisine["cuisine_id"])]
        else:
            dispatcher.utter_template('utter_wrong_cuisine', tracker)
            return []

class ActionValidateBudget(Action):
    def name(self):
        return 'validate_budget'
        
    def run(self, dispatcher, tracker, domain):
        _budget = tracker.get_slot('budget')
        budget = zomato_utils.get_valid_budget(_budget)
        if budget['is_valid']:
            return[SlotSet("budget_type", budget["type"])]
        else:
            dispatcher.utter_template('utter_wrong_budget', tracker)
            return []

class ActionSearchRestaurants(Action):
    def name(self):
        return 'action_restaurant'
        
    def run(self, dispatcher, tracker, domain):

        location_name = tracker.get_slot('location')
        lat = tracker.get_slot('lat')
        lon = tracker.get_slot('lon')
        cuisine = tracker.get_slot('cuisine')
        cuisine_id = tracker.get_slot('cuisine_id')
        budget = tracker.get_slot('budget_type')

        top_5_restaurants = []
        if lat is not None and lon is not None and cuisine_id is not None and budget is not None:
            top_5_restaurants = zomato_utils.get_top_restaurants_by_user_ratings(lat, lon, cuisine_id, budget)
        response = "No restaurants found in {} serving {} cuisine in {} budget".format(location_name, cuisine, budget)
        is_search_successful = False
        if len(top_5_restaurants) > 0:
            index = 1
            response = "Following are top 5 restaurants matching your preference in order of average user rating on zomato:\n\n"
            for restaurant in top_5_restaurants:
                response = response + "{}. {} in {} has been rated {}\n".format(index, restaurant['name'], restaurant['address'], restaurant['user_rating'])
                index += 1
            is_search_successful = True

        dispatcher.utter_message(response)
        return[SlotSet("search_success", is_search_successful)]

class ActionSendEmail(Action):
    def name(self):
        return 'action_sendemail'
        
    def run(self, dispatcher, tracker, domain):
        location_name = tracker.get_slot('location')
        lat = tracker.get_slot('lat')
        lon = tracker.get_slot('lat')
        cuisine = tracker.get_slot('cuisine')
        cuisine_id = tracker.get_slot('cuisine_id')
        budget = tracker.get_slot('budget')
        budget_type = tracker.get_slot('budget_type')

        top_10_restaurants = zomato_utils.get_top_restaurants_by_user_ratings(lat, lon, cuisine_id, budget_type, top_n=10)

        email_address = tracker.get_slot('email_address')
        subject = "[FOODIE] Restaurant search results for {} budget restaurants serving {} cuisine in {}".format(budget, cuisine, location_name)
        success = emailpy.send_mail(email_address, subject, location_name, cuisine, budget, top_10_restaurants)

        response=""
        if success:
            response = "An email has been sent to {}.\nPlease search the inbox for subject:\n\"{}\"".format(email_address, subject)
        else:
            response = "Oops! Email could not be sent. Sorry for the inconvenience."
        
        dispatcher.utter_message(response)
