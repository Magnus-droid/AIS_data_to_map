import requests
import json
import folium


def get_new_access_token():

	url = 'https://id.barentswatch.no/connect/token'

	headers = {
		'Content-Type':'application/x-www-form-urlencoded'
	}

	#Bad idea to just have the credentials in line, maybe put in a different file and import?
	response = requests.post(url, headers=headers, data='client_id=magnuskrumbacher%40gmail.com%3ATestMagnus&scope=ais&client_secret=Orngejuice100!&grant_type=client_credentials')
	print(response.json()['access_token'])
	return response.json()['access_token']


def check_access_token(access_token):
	
	url = 'https://live.ais.barentswatch.no/v1/latest/combined'

	headers = {
		'Authorization':f'Bearer {access_token}',
		'Content-Type':'application/json'
    }

	test_response = requests.get(url, headers=headers)
	print("Test_response.status_code: ",test_response.status_code)
	if test_response.status_code == 401:
		print("Getting new access token")
		global bearer_access_token 
		bearer_access_token = get_new_access_token()



bearer_access_token = '' 



check_access_token(bearer_access_token)

url = 'https://live.ais.barentswatch.no/v1/latest/combined'

headers = {
	'Authorization':f'Bearer {bearer_access_token}',
	'Content-Type':'application/json'
}

all_ship_data = requests.get(url, headers=headers)	
print(all_ship_data.status_code)
ship_list = json.loads(all_ship_data.text)
relevant = [ship for ship in ship_list if ship['mmsi'] == 258219000]
#print(relevant)
latitude = relevant[0].get('latitude')
longitude = relevant[0].get('longitude')
name = relevant[0].get('name')
m = folium.Map(location=[latitude, longitude], zoom_start = 12)
folium.Marker([latitude, longitude], popup=name).add_to(m)
m.save("testmap.html")

