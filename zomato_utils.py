import zomatopy
import json

servicable_cities = [
  "bengaluru",
  "chennai",
  "delhi",
  "hyderabad",
  "kolkata",
  "mumbai",
  "agra",
  "ajmer",
  "aligarh",
  "amravati",
  "amritsar",
  "asansol",
  "aurangabad",
  "ahmedabad",
  "bareilly",
  "belgaum",
  "bhavnagar",
  "bhiwandi",
  "bhopal",
  "bhubaneswar",
  "bikaner",
  "bokaro steel city",
  "chandigarh",
  "coimbatore",
  "nagpur",
  "cuttack",
  "dehradun",
  "dhanbad",
  "durg-bhilai nagar",
  "durgapur",
  "erode",
  "delhi ncr",
  "gorakhpur",
  "gulbarga",
  "guntur",
  "guwahati",
  "gwalior",
  "hubli-dharwad",
  "indore",
  "jabalpur",
  "jaipur",
  "jalandhar",
  "jammu",
  "jamnagar",
  "jamshedpur",
  "jhansi",
  "jodhpur",
  "kannur",
  "kanpur",
  "kakinada",
  "kochi",
  "kottayam",
  "kolhapur",
  "kollam",
  "kota",
  "kurnool",
  "lucknow",
  "ludhiana",
  "madurai",
  "mathura",
  "goa",
  "mangalore",
  "meerut",
  "moradabad",
  "mysore",
  "nanded",
  "nashik",
  "nellore",
  "palakkad",
  "patna",
  "puducherry",
  "prayagraj",
  "pune",
  "raipur",
  "rajkot",
  "rajahmundry",
  "ranchi",
  "rourkela",
  "salem",
  "sangli",
  "siliguri",
  "solapur",
  "srinagar",
  "surat",
  "thiruvananthapuram",
  "thrissur",
  "trichy",
  "tirunelveli",
  "tiruppur",
  "ujjain",
  "bijapur",
  "vadodara",
  "varanasi",
  "vijayawada",
  "visakhapatnam",
  "vellore",
  "warangal"
]

cuisines = {
  'chinese': '25', 
  'mexican': '73', 
  'italian': '55', 
  'american': '1', 
  'south_indian': '85', 
  'north_indian': '50'
}

def low_budget_predicate(restaurant): 
  return restaurant['average_cost_for_two'] <= 300

def medium_budget_predicate(restaurant): 
  return 300 <= restaurant['average_cost_for_two'] <= 700

def high_budget_predicate(restaurant): 
  return restaurant['average_cost_for_two'] >= 700

budget_predicates = {
  'low': low_budget_predicate,
  'medium': medium_budget_predicate,
  'high': high_budget_predicate,
}

zomato = zomatopy.initialize_app()

def get_valid_location(location):
  location_detail = zomato.get_location(location, 1)
  location_json = json.loads(location_detail)
  location_suggestions = location_json["location_suggestions"]
  if (len(location_suggestions) > 0):
    response = location_suggestions[0]
    if response["city_name"].lower() in servicable_cities:
      response["is_valid"] = True
      return response
  return {"is_valid": False}

def get_top_restaurants_by_user_ratings(location, cuisine, budget, top_n=5):
    restaurants = []

    if location['is_valid'] and cuisine is not None and budget is not None:
      lat = location["latitude"]
      lon = location["longitude"]
      _cuisine = cuisines[cuisine.lower()]

      offset = 0
      limit = 20
      while len(restaurants) < top_n:
        results = zomato.restaurant_search("", lat, lon, _cuisine, limit=limit, offset=offset, sort={"cost":"asc"}) \
        if budget == 'low' else \
        zomato.restaurant_search("", lat, lon, _cuisine, limit=limit, offset=offset)
      
        results_json = json.loads(results)

        if results_json['results_found'] == 0:
          break

        all_restaurants = map(lambda restaurant: restaurant['restaurant'], results_json['restaurants'])
        filtered_by_budget = filter(budget_predicates[budget], all_restaurants)
        restaurants.extend(filtered_by_budget)
        offset += limit

    top_sorted = sorted(restaurants, key=lambda x: float(x['user_rating']['aggregate_rating']), reverse = True)[:top_n]
    return [{
      'name':restaurant['name'], \
      'address':restaurant['location']['address'], \
      'average_cost_for_two':restaurant['average_cost_for_two'], \
      'user_rating':restaurant['user_rating']['aggregate_rating'], \
      'url':restaurant['url'] \
    } for restaurant in top_sorted]

if __name__ == '__main__':
  location = get_valid_location('bengaluru')
  search_results = get_top_restaurants_by_user_ratings(location, 'chinese', 'low', top_n=10)
  for result in search_results:
    print(result)

