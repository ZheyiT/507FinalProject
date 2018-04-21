#507 Final Project README
#####Name: Zheyi Tian
#####E-mail: tzheyi@umich.edu
#####UMID: 36521510
#####Winter 2018
#####GSI: Deahan


###Data Source
The data is scraping and crawling from Wikipedia, [List of active United States Air Force aircraft squadrons](https://en.wikipedia.org/wiki/List_of_active_United_States_Air_Force_aircraft_squadrons) No API needed.


###Other Information to run the program
#####PLotly

The project use plotly combined with Flask, so you need to have a plotly account and have basic plotly setting. Besides, scattermapbox tool in plotly is used. That require a [Mapbox Access Token](https://www.mapbox.com/studio/). Please click the link and get your own access token.

When you get the token, please make a python file called "secrets.py" in the project folder. In side, please write:

mapbox_access_token = "Write your tokens here"

#####Virtual Environment(If you need)

All the packages the project used is used in this semester, so I believe GSI can run them smoothly. If not, please run the virtual environment.


###The structure of code.
#####Scraping and crawling - AF_squad.py
-Scraps and crawls information from wikipedia, stores dictionaries in AF_squad.json and AF_base.json.

#####Update Json File - Aircraft_Update_Json.py
-Update AF_squad.json, add a new attribute "BattlePlaneType" for each squad.

#####Write into Database - BuildDatabase.py
-Build the database by 2 json files.
-The database has 3 tables

#####Tests - projecttest.py
-Test the class.
-Test each table
-Test table join

#####Draw four plots - DrawAirbase.py
-class AirBase() is defined here.
-plot_all_air_base(): draw map for airbases around the world
-plot_command_pie(): draw pie plots for USAF commands
-plot_wing_bar(): draw bar plot for USAF wings
-plot_fight_range(BaseId, hour): get the input value BaseId and hour, draw the reaction range of certain base in certain time.

#####Run the flask - app.py
-index(): Homepage
-map(): Draw global base map
-pie(): Draw pie plot
-bar(): Draw bar plot
-range(): Draw reaction range

#####Templates
otherplotly.html: normal webpage
rangeplotly.html: webpage with variable input and interaction


###User Guide
#####Basic Version
All the json files and python files are submitted.

To run the flask app, you only need to get a plotly mapbox access token. The instructions are in the "Other Information to run the program" section above.

Then run the app.py, copy the url to your web browser, click the subpage link in the homepage, and you can return to the homepage by the link in each subpage.

On "reaction range" page, you need to input base id and hour, tips are also showed in that page.

#####If you want to use virtual environment
In command window, go to your folder.

Input:
source venv/bin/activate

Then run app.py

When you are done, input:
deactivate


#####If you want yo run the whole project from the beginning
Please the following python file in the following order:
1. AF_squad.py
2. Aircraft_Update_Json.py
3. BuildDatabase.py
4. app.py


Thank you for reading and thank you Deahan, for your help and instruction through this semester. I learned a lot!