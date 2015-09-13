#coding=utf-8
import requests

url = 'http://127.0.0.1:5000'

#get all countries
r = requests.post(url+'/cities/search', {'action': 'countries', 'language': 'cn'})
if r.status_code == 200:
    print r.text
else:
    print r.status_code
#get all provinces
r = requests.post(url+'/cities/search', {'action': 'provinces', 'language': 'cn', 'c_id': 1})
if r.status_code == 200:
    print r.text
else:
    print r.status_code

#get all cities
r = requests.post(url+'/cities/search', {'action': 'cities', 'language': 'cn', 'c_id': 1, 'p_id': 32})
if r.status_code == 200:
    print r.text
else:
    print r.status_code

#get one city
r = requests.post(url+'/cities/search', {'action': 'city', 'language': 'cn', 'c_id': 1, 'p_id': 32, 'i_id': 8})
if r.status_code == 200:
    print r.text
else:
    print r.status_code