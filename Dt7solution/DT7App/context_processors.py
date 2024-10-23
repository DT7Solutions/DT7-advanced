# context_processors.py
import requests

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_geolocation(ip):
    url = f'http://ip-api.com/json/{ip}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        city = data['city']
        return city


def location_data(request):
    user_ip = get_client_ip(request)
    location_data = get_geolocation(user_ip)

    city = 'guntur'
    if location_data:
        city = location_data
    return {
        'city': city
    }
