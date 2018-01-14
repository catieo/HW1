## HW 1
## SI 364 W18
## 1000 points

#################################

## List below here, in a comment/comments, the people you worked with on this assignment AND any resources you used to find code (50 point deduction for not doing so). If none, write "None".
## https://www.yelp.com/developers/v3/manage_app?saved_changes=True 
## https://www.yelp.com/developers/documentation/v3/business_search
## https://github.com/Yelp/yelp-fusion/blob/master/fusion/python/sample.py
## http://jsoneditoronline.org/ 


## [PROBLEM 1] - 150 points
## Below is code for one of the simplest possible Flask applications. Edit the code so that once you run this application locally and go to the URL 'http://localhost:5000/class', you see a page that says "Welcome to SI 364!"

from flask import Flask, request
import requests
import json
import api_info_template
app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_to_you():
    return 'Hello!'

#Problem 1 solution
@app.route('/class')
def hello_class():
	return 'Welcome to SI 364!'

#Problem 2 solution
@app.route('/movie/<anytitlesearch>')
def movie_search(anytitlesearch):
	baseurl = "https://itunes.apple.com/search?"
	search_query = {"term" : anytitlesearch, "entity" : "movie"}
	response = requests.get(baseurl, params=search_query)
	return str(response.json())

#Problem 3 solution 
#displays form asking user for favorite number
@app.route('/question')
def question():
	formstring = """
	<form action="/result" method='GET'>
	<h1>Enter your favorite number:</h1>
	<input type="text" name="fav_number">  
	<input type="submit" value="Submit">"""
	return formstring

#prints the result of the form which is doubling the value entered 
@app.route('/result', methods=["GET"])
def question_result():
	result_str = "Double your favorite number is "
	if request.method == "GET":
		num = request.args.get('fav_number', '0')
		return result_str + str(int(num)*2)
	return "You didn't enter a number!"

#Problem 4 solution
#accesses Yelp Search API
#form will ask for a location in the form a city name (text input)
#form will also ask for user to check boxes indicated what kind of results are wanted (kinds of restaurants)
#when submitted, results returned will display recommendations from the Yelp Search API based on input info 
@app.route('/problem4form', methods=["GET"])
def problem4():
	#html form 
	formstring = """
	<form action="/problem4form" method="GET">
	<h1>Welcome to the Restaurant Recommender!</h1>
	<h2>Please enter your location (name of a city):<h2>
	<input type="text" name="city"> <br>
	<h2>Please check which kind of restaurant you're looking for: </h2>
	<input type="checkbox" name="restaurant1" value="Breakfast"> Breakfast <br>
	<input type="checkbox" name="restaurant2" value="Brunch"> Brunch <br>
	<input type="checkbox" name="restaurant3" value="Lunch"> Lunch <br>
	<input type="checkbox" name="restaurant4" value="Dinner"> Dinner <br>
	<input type="checkbox" name="restaurant5" value="Coffee"> Coffee <br>
	<input type="checkbox" name="restaurant6" value="Ice Cream"> Ice Cream  <br><br>
	<input type="submit" value="Submit">
	<br><br>
	"""

	#secret values 
	client_id = api_info_template.client_id
	client_secret = api_info_template.client_secret
	access_token = api_info_template.access_token

	#authentication to yelp 
	base_url = "https://api.yelp.com/v3/businesses/search"
	headers = {'Authorization' : 'Bearer %s' % access_token,}

	if request.method == 'GET':
		result_str = formstring
		#determine search terms from input data 
		url_params = {} 
		url_params["limit"] = 3
		url_params["location"] = request.args.get('city', "").replace(' ', '+')
		#determine which checkboxes were selected before putting it in the url_params dict
		restaurant_type = {}
		restaurant_type["restaurant1"] = request.args.get('restaurant1')
		restaurant_type["restaurant2"] = request.args.get('restaurant2')
		restaurant_type["restaurant3"] = request.args.get('restaurant3')
		restaurant_type["restaurant4"] = request.args.get('restaurant4')
		restaurant_type["restaurant5"] = request.args.get('restaurant5')
		restaurant_type["restaurant6"] = request.args.get('restaurant6')
		#make a separate request for each restaurant type selected 
		for x in restaurant_type:
			#if the checkbox was not selected, don't make a request for that search term 
			if restaurant_type[x] != None:
				url_params["term"] = restaurant_type[x] 
		 		#make request 
				response = requests.request('GET', base_url, headers=headers, params=url_params)
				#parse through the json object and retrieve the names of each business returned
				names = ""
				for business in response.json()["businesses"]:
					names = names + business["name"] + '<br>'
				#format string to be displayed to user 
				recommendation_str = "For " + restaurant_type[x] + ", you should try: <br>" + names + "<br>"
				result_str = result_str + recommendation_str 
		return result_str
	else: 
		return formstring



if __name__ == '__main__':
    app.run()


## [PROBLEM 2] - 250 points
## Edit the code chunk above again so that if you go to the URL 'http://localhost:5000/movie/<name-of-movie-here-one-word>' you see a big dictionary of data on the page. For example, if you go to the URL 'http://localhost:5000/movie/ratatouille', you should see something like the data shown in the included file sample_ratatouille_data.txt, which contains data about the animated movie Ratatouille. However, if you go to the url http://localhost:5000/movie/titanic, you should get different data, and if you go to the url 'http://localhost:5000/movie/dsagdsgskfsl' for example, you should see data on the page that looks like this:

# {
#  "resultCount":0,
#  "results": []
# }


## You should use the iTunes Search API to get that data.
## Docs for that API are here: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
## Of course, you'll also need the requests library and knowledge of how to make a request to a REST API for data.

## Run the app locally (repeatedly) and try these URLs out!

## [PROBLEM 3] - 250 points

## Edit the above Flask application code so that if you run the application locally and got to the URL http://localhost:5000/question, you see a form that asks you to enter your favorite number.
## Once you enter a number and submit it to the form, you should then see a web page that says "Double your favorite number is <number>". For example, if you enter 2 into the form, you should then see a page that says "Double your favorite number is 4". Careful about types in your Python code!
## You can assume a user will always enter a number only.


## [PROBLEM 4] - 350 points

## Come up with your own interactive data exchange that you want to see happen dynamically in the Flask application, and build it into the above code for a Flask application, following a few requirements.

## You should create a form that appears at the route: http://localhost:5000/problem4form

## Submitting the form should result in your seeing the results of the form on the same page.

## What you do for this problem should:
# - not be an exact repeat of something you did in class
# - must include an HTML form with checkboxes and text entry
# - should, on submission of data to the HTML form, show new data that depends upon the data entered into the submission form and is readable by humans (more readable than e.g. the data you got in Problem 2 of this HW). The new data should be gathered via API request or BeautifulSoup.

# You should feel free to be creative and do something fun for you --
# And use this opportunity to make sure you understand these steps: if you think going slowly and carefully writing out steps for a simpler data transaction, like Problem 1, will help build your understanding, you should definitely try that!

# You can assume that a user will give you the type of input/response you expect in your form; you do not need to handle errors or user confusion. (e.g. if your form asks for a name, you can assume a user will type a reasonable name; if your form asks for a number, you can assume a user will type a reasonable number; if your form asks the user to select a checkbox, you can assume they will do that.)

# Points will be assigned for each specification in the problem.
