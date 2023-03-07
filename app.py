import requests
import json
import xml.etree.ElementTree as ET
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/getCurrentWeather', methods=['POST'])
def get_current_weather():
    city = request.json.get('city')
    output_format = request.json.get('output_format')
    url = "https://weatherapi-com.p.rapidapi.com/current.json"
    querystring = {"q": city}
    headers = {
        "X-RapidAPI-Key": "your_key",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)

    # Check if city is valid
    if response.status_code == 400:
        error_message = response.json().get('error').get('message')
        return Response(json.dumps({'error': error_message}), status=400, mimetype='application/json')

    # Extract data from API response
    weather_data = response.json().get('current')
    location_data = response.json().get('location')
    temperature = weather_data.get('temp_c')
    latitude = location_data.get('lat')
    longitude = location_data.get('lon')
    city_name = location_data.get('name') + ' ' + location_data.get('country')

    # Format response based on output format
    if output_format == 'json':
        response_data = {
            'Weather': f'{temperature} C',
            'Latitude': str(latitude),
            'Longitude': str(longitude),
            'City': city_name
        }
        return Response(json.dumps(response_data), mimetype='application/json')
    elif output_format == 'xml':
        root = ET.Element('root')
        temperature_element = ET.SubElement(root, 'Temperature')
        temperature_element.text = str(temperature)
        city_element = ET.SubElement(root, 'City')
        city_element.text = city_name
        latitude_element = ET.SubElement(root, 'Latitude')
        latitude_element.text = str(latitude)
        longitude_element = ET.SubElement(root, 'Longitude')
        longitude_element.text = str(longitude)
        response_xml = ET.tostring(root, encoding='UTF-8', xml_declaration=True)
        return Response(response_xml, content_type='text/xml')
    else:
        return Response(json.dumps({'error': 'Invalid output format'}), status=400, mimetype='application/json')
    

if __name__ == '__main__':
    app.run(debug=True)
