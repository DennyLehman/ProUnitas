# mapping for Albert
import gmplot
import os
from geopy.geocoders import Nominatim
import pandas as pd
import requests
import json
import folium
print(os.getcwd())
path = r'C:\Users\slin2\Documents\ProUnitas\maps'

def test_requests():
	#this test needs an api key from google maps
	response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA')
	resp_json_payload = response.json()
	print(resp_json_payload)
	#print(resp_json_payload['results'][0]['geometry']['location'])

def test_requests2():
	GOOGLE_MAPS_API_URL = 'http://maps.googleapis.com/maps/api/geocode/json'

	params = {
	    'address': 'oshiwara industerial center goregaon west mumbai',
	    'sensor': 'false',
	    'region': 'india'
	}

	# Do the request and get the response data
	req = requests.get(GOOGLE_MAPS_API_URL, params=params)
	res = req.json()

	print(res)

	# Use the first result
	result = res['results'][0]

	print(result)
	geodata = dict()
	geodata['lat'] = result['geometry']['location']['lat']
	geodata['lng'] = result['geometry']['location']['lng']
	geodata['address'] = result['formatted_address']


	print('{address}. (lat, lng) = ({lat}, {lng})'.format(**geodata))

def test_gmplot():

	gmap = gmplot.GoogleMapPlotter(37.428, -122.145, 16)

	gmap.marker(1,11)
	gmap.marker(2,22)
	gmap.points[0][0]
	gmap.draw(os.path.join(path,'test_map.html'))


def test_geolocator():

	geolocator = Nominatim(user_agent="my_app_name")
	#location = geolocator.geocode("175 5th Avenue NYC")
	# location = geolocator.geocode("260 North Sam Houston Parkway East Houston Texas")
	location = geolocator.geocode('415 Mission St San Francisco CA')
	print(location.address)
	print((location.latitude, location.longitude))
	print(location.raw)

def test_marker():

	gmap = gmplot.GoogleMapPlotter(location.latitude, location.longitude, 15)

	gmap.marker(location.latitude, location.longitude, 'cornflowerblue', title='My House')

	gmap.draw(os.path.join(path,'test_map.html'))

def test_from_geocode():
	gmap2 = gmplot.GoogleMapPlotter.from_geocode( "Dehradun, India" ) 
	  
	gmap2.draw(os.path.join(path,'test_india.html')) 

def load_data():
	csv_path =r'C:\Users\slin2\Documents\ProUnitas\Service_Provider_Mapping.csv'
	# error in encoding 
	# https://stackoverflow.com/questions/18171739/unicodedecodeerror-when-reading-csv-file-in-pandas-with-python
	df = pd.read_csv(csv_path,sep=',',encoding="ISO-8859-1")

	df = df[['Program: Program Name','Partner Status','Billing Street','Billing City','Billing State/Province', 'Billing Zip/Postal Code']]
	# fix nan's in billing state
	df['Billing State/Province'] = 'TX'
	
	# fix bad addresses in other places
	df = df.fillna('')

	# Fix \n in street address here
	df['Billing Street'] = df['Billing Street'].str.replace(pat='\n', repl=' ',case=False)

	df['address'] = df['Billing Street'] +' '+ df['Billing City'] + ' ' + df['Billing State/Province'] + ' ' + df['Billing Zip/Postal Code'].map(str)
	

	df.address = df.address.str.replace(pat='\n', repl=' ',case=False)

	return df

def get_lat_long(address):
	try:
		geolocator = Nominatim(user_agent="my_rap_name")
		location = geolocator.geocode(address)
		#print(type(location))
		return [location.latitude, location.longitude, True]
	except Exception as e:
		#print('Address didn\'t work...')
		geolocator = Nominatim(user_agent="my_rap_name")
		location = geolocator.geocode('415 Mission St San Francisco CA')
		#print('Using Salesforce Tower Address')
		return [location.latitude, location.longitude, False]
	
def add_lat_long_to_df():
	lat = []
	lon = []
	success = []
	for i in range(0,len(df.address)):
		_lat , _lon, _success = get_lat_long(df.address[i])
		lat.append(_lat)
		lon.append(_lon)
		success.append(_success)
		
	df['latitude'] = lat
	df['longitude'] = lon
	df['success'] = success
	return df

def gmplot_map_df(df):
	# make list of successful lat/long coordinates
	df = df[df['success']==True]
	lat_list = df['latitude']
	lon_list = df['longitude']
	gmap = gmplot.GoogleMapPlotter(29.7106415,-95.4970872, 12)
	# Yeallow:'#ccff00' Red: Blue: 'cornflowerblue'
	gmap.scatter(lat_list, lon_list, 'red', size=100, marker=False)
	#gmap.plot(lat_list, lon_list, 'cornflowerblue')
	#gmap.heatmap(lat_list,lon_list)
	gmap.draw(os.path.join(path,'gmplot_map.html'))

def folium_map_df(df): 
	# make list of successful lat/long coordinates
	df = df[df['success']==True]
	lat_list = df['latitude']
	lon_list = df['longitude']
	pop_up_name = df['Program: Program Name']
	# Map method of folium return Map object 

	# Here we pass coordinates of Gfg 
	# and starting Zoom level = 12 
	my_map1 = folium.Map(location = [29.7106415,-95.4970872], 
											zoom_start = 12 ) 

	folium.Marker([29.7106415,-95.4970872], 
               popup = 'school stuff here ').add_to(my_map1)

	for i in range(0,len(lat_list)):
		folium.Marker([lat_list.iloc[i], lon_list.iloc[i]], popup = pop_up_name.iloc[i]).add_to(my_map1)


	# save method of Map object will create a map 
	my_map1.save(os.path.join(path,'folium_map.html')) 


def load_and_clean_data():
	df = load_data()
	df = add_lat_long_to_df()
	df.to_csv(r'C:\Users\slin2\Documents\ProUnitas\output.csv')

def test_run():
	print('hello world')
	# test_geolocator()
	geolocator = Nominatim(user_agent="my_app_name")
	#location = geolocator.geocode("175 5th Avenue NYC")
	# location = geolocator.geocode("260 North Sam Houston Parkway East Houston Texas")
	location = geolocator.geocode('415 Mission St San Francisco CA')
	#print(location.address)
	#print((location.latitude, location.longitude))
	#print(location.raw)

	df = load_data()
	add = df.address[10]

	print(add)
	for i in range(0,2):
		add = df.address[i]
		lat , lon, success = get_lat_long(add)
		print(i,": ",success,'  ', lat, ' ' , lon)

	df = add_lat_long_to_df()

	print(df.head())

	df.to_csv(r'C:\Users\slin2\Documents\ProUnitas\output.csv')

def testerino():
	df = pd.read_csv(r'C:\Users\slin2\Documents\ProUnitas\output.csv')
	print(df.head())
	folium_map_df(df)
	gmplot_map_df(df)

testerino()