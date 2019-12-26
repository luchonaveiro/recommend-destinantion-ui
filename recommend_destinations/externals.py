import requests
import json
import pandas as pd

def parse_json_name(df):
    return df['name']

def get_possible_destinations():
    req = requests.get('https://recommend-destination.herokuapp.com/destinations')
    req = json.loads(req.text)
    df_req = pd.DataFrame(req)
    possible_cities = df_req['name']
    continent = df_req['continent'].apply(parse_json_name)
    country = df_req['country'].apply(parse_json_name)
    label = possible_cities + ', ' + country + ', ' + continent
    possible_cities = pd.concat([possible_cities, country, continent, label], axis=1)
    possible_cities = possible_cities.sort_values(['continent', 'country', 'name'], ascending=[True, True, True])
    possible_cities.columns = ['value','country','continent','label']
    possible_cities = possible_cities[['value', 'label']]
    
    return json.loads(possible_cities.to_json(orient='records'))

def recommend_cities(cities_list):
    body = {'cities':cities_list}
    req = requests.post('https://recommend-destination.herokuapp.com/recommend', data=json.dumps(body), headers = {'Content-Type': "application/json"})
    req = json.loads(req.text)

    return req
    
