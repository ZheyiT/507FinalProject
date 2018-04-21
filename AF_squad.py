from requests_oauthlib import OAuth1
from requests_oauthlib import OAuth1Session
import json
import plotly.plotly as py
import requests
from bs4 import BeautifulSoup
import secrets

###Global Variables
base_url = "https://en.wikipedia.org"

Squad_Web_File = 'AF_squad_webpage.json'
Squad_JSON_Name = 'AF_squad.json'
Base_JSON_Name = 'AF_base.json'
Aircraft_JSON_Name = 'AF_plane.json'


###CACHING
def caching_list_page():
    global page_store
#	global all_squad_dic
#	global all_base_dic

	#JSON CACHE of whole webpage, in case of too frequent access.
	try:
		with open(Squad_Web_File) as f:
			cache_contents = f.read()
			Squad_CD = json.loads(cache_contents)
			page_store = Squad_CD["result"]
	except:
		Squad_CD = {}
		squad_url = "https://en.wikipedia.org/wiki/List_of_active_United_States_Air_Force_aircraft_squadrons"
		page_store = requests.get(squad_url).text
		Squad_CD["result"] = page_store

		dumped_json_cache = json.dumps(Squad_CD)
		fw = open(Squad_Web_File,"w")
		fw.write(dumped_json_cache)
		fw.close()

###Instrumental Functions

#Convert degree-tude to decimal-tude
def tude_convert(tude):
	ls1 = tude.split('°')
	du = ls1[0]
	ls2 = ls1[1].split('′')
	fen = ls2[0]
	if len(ls2[1]) == 1:
		miao = 0
		direction = ls2[1]
	else:
		ls3 = ls2[1].split('″')
		miao = ls3[0]
		direction = ls3[1]
	multiplier = 1 if direction in ['N', 'E'] else -1
	result_output = multiplier * sum(float(x) / 60 ** n for n, x in enumerate([du, fen, miao]))
	return round(result_output, 6)

#Convert geo_dec-tude to decimal-tude
def geo_dec_convert(tude):
	tude_var = tude[:-2]
	direction = tude[-1]
	multiplier = 1 if direction in ['N', 'E'] else -1
	result_output = multiplier * float(tude_var)
	return round(result_output, 6)

###MAIN FUNCTIONS To GENERATE/UPDATE JSON FILE

def get_AF_Squad():
	global all_squad_dic

	caching_list_page()
	all_squad_dic = []

	soup = BeautifulSoup(page_store, 'html.parser')

	table_subpage = soup.find('div', attrs={'class':'mw-parser-output'})
	table_list = table_subpage.find_all('table', attrs={'class':'wikitable sortable'})

	

	for single_table in table_list:
		table_rows = single_table.find_all('tr')[1:]
		for single_row in table_rows:
			squad_dic = {}
			columns = single_row.find_all('td')
			squad_name = columns[0].find('a').string
			squad_dic["squad_nm"] = squad_name

			try:
				squad_dic["command_nm"] = columns[3].find('a').string
			except:
				squad_dic["command_nm"] = "NO INFO"

			try:
				squad_dic["wing_nm"] = columns[5].find('a').string
			except:
				squad_dic["wing_nm"] = "NO INFO"
			
			try:
				squad_dic["base_nm"] = columns[8].find('a').string
			except:
				squad_dic["base_nm"] = "NO INFO"
			
			try:
				squad_dic["aircraft_nm"] = columns[9].find('a').string
			except:
				squad_dic["aircraft_nm"] = "NO INFO"

			try:
				squad_dic["command_url"] = columns[3].find('a')['href']
			except:
				squad_dic["command_url"] = ""

			try:
				squad_dic["base_url"] = columns[8].find('a')['href']
			except:
				squad_dic["base_url"] = ""

			try:
				squad_dic["aircraft_url"] = columns[9].find('a')['href']
			except:
				squad_dic["aircraft_url"] = ""

			all_squad_dic.append(squad_dic)

	dumped_json_cache = json.dumps(all_squad_dic)
	fw = open(Squad_JSON_Name,"w")
	fw.write(dumped_json_cache)
	fw.close()


def get_Air_Base():

	#JSON Dict for base info	
	try:
		with open(Squad_JSON_Name) as f:
			cache_contents = f.read()
			all_squad_dic = json.loads(cache_contents)
	except:
		get_AF_Squad()

	all_base_dic = []
	distinct_base_list = []
	for squad_dic in all_squad_dic:
		single_base = {}
		if squad_dic["base_nm"] not in distinct_base_list:
			single_base["base_nm"] = squad_dic["base_nm"]
			single_base["url"] = squad_dic["base_url"]

			if single_base["url"] == "":
				single_base["lat"] = ""
				single_base["lon"] = ""

			elif squad_dic["base_nm"] in ["Homestead ARB", "Seymour Johnson AFB"]:
				single_base["lat"] = ""
				single_base["lon"] = ""

			else:
				airbase_url = base_url + squad_dic["base_url"]
				airbase_page = requests.get(airbase_url).text
				soup = BeautifulSoup(airbase_page, 'html.parser')

				if squad_dic["base_nm"] == "Mountain Home AFB":
					geo_info = soup.find('span', attrs={'class':'geo-dec'}).string
					lat_str = geo_info.split()[0]
					lon_str = geo_info.split()[1]
					lat = geo_dec_convert(lat_str)
					lon = geo_dec_convert(lon_str)

				else:
					geo_subpage = soup.find('span', attrs={'class':'geo-default'})
					lat_str = geo_subpage.find('span', attrs={'class':'latitude'}).string
					lat = tude_convert(lat_str)
					lon_str = geo_subpage.find('span', attrs={'class':'longitude'}).string
					lon = tude_convert(lon_str)

				single_base["lat"] = lat
				single_base["lon"] = lon

			
			distinct_base_list.append(squad_dic["base_nm"])
			all_base_dic.append(single_base)

	dumped_json_cache = json.dumps(all_base_dic)
	fw = open(Base_JSON_Name,"w")
	fw.write(dumped_json_cache)
	fw.close()

get_AF_Squad()
get_Air_Base()









