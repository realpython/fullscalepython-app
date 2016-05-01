# project/server/bathroom/geodata.py


import requests


URL = "https://maps.googleapis.com/maps/api/geocode/json"


def get_geodata(address):
    payload = {'address': address}
    response = requests.get(URL, params=payload)
    return response.json()
