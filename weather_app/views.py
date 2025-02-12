from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import requests
from django.template.loader import get_template

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('weather')
        else:
            return HttpResponse("Invalid credentials")
    return render(request, 'weather_app/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def weather(request):
    try:
        template = get_template('weather_app/weather.html')
        print("Template found:", template)
    except Exception as e:
        print("Error loading template:", e)
    
    city = request.GET.get('city', 'Chandigarh')  # Default city
    api_key = '86d5c5c3534874ba0610c2ecf52a2a0d'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    context = {
        'weather_data': data,
        'city': city,
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'humidity': data['main']['humidity'],
        'wind_speed': data['wind']['speed'],
        'icon': data['weather'][0]['icon'],  # Weather icon
    }
    return render(request, 'weather_app/weather.html', context)







