## Generated Story 2427997638656963262
* restaurant_search
    - restaurant_form
    - form{"name": "restaurant_form"}
    - slot{"requested_slot": "location"}
* form: restaurant_search{"location": "pune"}
    - slot{"location": "pune"}
    - form: restaurant_form
    - slot{"location": "pune"}
    - slot{"requested_slot": "cuisine"}
* form: restaurant_search{"cuisine": "north indian"}
    - slot{"cuisine": "north indian"}
    - form: restaurant_form
    - slot{"cuisine": "north indian"}
    - slot{"requested_slot": "budget"}
* form: restaurant_search{"budget": "> 700"}
    - slot{"budget": "> 700"}
    - form: restaurant_form
    - slot{"budget": "> 700"}
    - slot{"lat": 18.520469}
    - slot{"lon": 73.85662}
    - slot{"cuisine_id": "50"}
    - slot{"budget_type": "high"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - utter_ask_sendmail
* affirm
    - utter_ask_emailaddress
* send_email{"email_address": "keensam04@gmail.com"}
    - slot{"email_address": "keensam04@gmail.com"}
    - action_sendemail
    - utter_goodbye
    - action_restart

## Generated Story -6786567558800845662
* restaurant_search{"location": "pune"}
    - slot{"location": "pune"}
    - restaurant_form
    - form{"name": "restaurant_form"}
    - slot{"location": "pune"}
    - slot{"location": "pune"}
    - slot{"requested_slot": "cuisine"}
* form: restaurant_search{"cuisine": "south indian"}
    - slot{"cuisine": "south indian"}
    - form: restaurant_form
    - slot{"cuisine": "south indian"}
    - slot{"requested_slot": "budget"}
* form: restaurant_search{"budget": "< 300"}
    - slot{"budget": "< 300"}
    - form: restaurant_form
    - slot{"budget": "< 300"}
    - slot{"lat": 18.520469}
    - slot{"lon": 73.85662}
    - slot{"cuisine_id": "85"}
    - slot{"budget_type": "low"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - utter_ask_sendmail
* goodbye
    - utter_goodbye
    - action_restart

## Generated Story 6164329005245683105
* greet
    - utter_greet
* restaurant_search{"location": "banglore", "cuisine": "italian"}
    - slot{"cuisine": "italian"}
    - slot{"location": "banglore"}
    - restaurant_form
    - form{"name": "restaurant_form"}
    - slot{"location": "banglore"}
    - slot{"cuisine": "italian"}
    - slot{"location": "banglore"}
    - slot{"cuisine": "italian"}
    - slot{"requested_slot": "budget"}
* form: restaurant_search{"budget": "between 300 - 700"}
    - slot{"budget": "between 300 - 700"}
    - form: restaurant_form
    - slot{"budget": "between 300 - 700"}
    - slot{"lat": 18.548498}
    - slot{"lon": 73.773357}
    - slot{"cuisine_id": "55"}
    - slot{"budget_type": "medium"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - utter_ask_sendmail
* goodbye
    - utter_goodbye
    - action_restart

## Generated Story -3998450245614700542
* greet
    - utter_greet
* restaurant_search{"location": "bengaluru"}
    - slot{"location": "bengaluru"}
    - restaurant_form
    - form{"name": "restaurant_form"}
    - slot{"location": "bengaluru"}
    - slot{"location": "bengaluru"}
    - slot{"requested_slot": "cuisine"}
* form: restaurant_search{"cuisine": "thai"}
    - slot{"cuisine": "thai"}
    - form: restaurant_form
    - slot{"cuisine": null}
    - slot{"requested_slot": "cuisine"}
* form: restaurant_search{"cuisine": "chinese"}
    - slot{"cuisine": "chinese"}
    - form: restaurant_form
    - slot{"cuisine": "chinese"}
    - slot{"requested_slot": "budget"}
* form: restaurant_search{"budget": "around 300"}
    - slot{"budget": "around 300"}
    - form: restaurant_form
    - slot{"budget": null}
    - slot{"requested_slot": "budget"}
* form: restaurant_search{"budget": "more then 700"}
    - slot{"budget": "more then 700"}
    - form: restaurant_form
    - slot{"budget": "more then 700"}
    - slot{"lat": 12.971606}
    - slot{"lon": 77.594376}
    - slot{"cuisine_id": "25"}
    - slot{"budget_type": "high"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - utter_ask_sendmail
* goodbye
    - utter_goodbye
    - action_restart

## Generated Story -5093960693092854837
* goodbye
    - utter_goodbye
    - action_restart

## Generated Story -5093960693092854837
* irrelevant_intent
    - utter_default
    - action_restart