import requests
import pygame
import sys


def display_weather():
    pygame.init()

    screen_width, screen_height = 600, 400
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Weather Checker")

    white = (255, 255, 255)
    black = (0, 0, 0)
    blue = (135, 206, 250)

    pygame.font.init()
    font = pygame.font.Font(pygame.font.get_default_font(), 28)
    small_font = pygame.font.Font(pygame.font.get_default_font(), 20)

    default_city = getCity()
    if not default_city or 'Error' in default_city:
        default_city = "London"
    weather_data = getWeather(default_city)

    is_running = True
    while is_running:
        screen.fill(blue)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    user_city = input("Введите название города: ")
                    weather_data = getWeather(user_city)

        if weather_data:
            title = font.render(f"Weather in {default_city}", True, black)
            screen.blit(title, (20, 20))

            temp = small_font.render(f"Temperature: {weather_data['temperature']}", True, black)
            screen.blit(temp, (20, 80))

            desc = small_font.render(f"Description: {weather_data['description']}", True, black)
            screen.blit(desc, (20, 120))

            humidity = small_font.render(f"Humidity: {weather_data['humidity']}", True, black)
            screen.blit(humidity, (20, 160))

            wind_speed = small_font.render(f"Wind speed: {weather_data['wind_speed']}", True, black)
            screen.blit(wind_speed, (20, 200))
        else:
            error_message = font.render("Error retrieving weather data.", True, black)
            screen.blit(error_message, (20, 80))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    display_weather()
class Weather:
    @staticmethod
    def output():
        welcome_message ="""
       .--.  
      |o_o |    
      |:_/ |    
     //   \ \   
    (|     | )  
   /'\_   _/`|
   \___)=(___/  
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
              Welcome to WeatherChecker! 🌦️ 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
        print(welcome_message)
        userResp = input(f"Your city: {getCity()}. Do you want to check weather in your city?(yes/no)")
        if userResp == "no":
            userCity = input("Set your city: ")
            getWeather(userCity)
        else:
            userCity1 = getCity()
            getWeather(userCity1)



def getCity():
    ip = getIP()

    if ip == "Error":
        return "Can't get IP"

    urlRequest = f"https://ipinfo.io/{ip}/json"

    try:
        response = requests.get(urlRequest)
        if response.status_code == 200:
            data = response.json()
            city = data.get("city")
            return city
        else:
            return "Can't get your city"
    except Exception as e:
        return f"Error: {e}"


def getIP():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            ip_data = response.json()
            return ip_data['ip']
        else:
            return None
    except requests.exceptions.RequestException as e:
        return f"Error {e}"



def getWeather(city):
        api = "2fa5df369c1451870b1611145da84896"
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            temperature = data['main']['temp']
            weather_description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            return temperature, weather_description, humidity, wind_speed

        else:
            return None


Weather.output()