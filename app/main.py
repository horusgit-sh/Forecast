import requests
import pygame
import sys

def draw_button(screen, text, position, size, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(position[0], position[1], size[0], size[1])
    
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, button_rect, border_radius=12)
    else:
        pygame.draw.rect(screen, color, button_rect, border_radius=12)
    
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    
    return button_rect

def get_user_input():
    input_screen = pygame.display.set_mode((400, 100))
    pygame.display.set_caption("Enter City Name")
    
    font = pygame.font.Font(None, 32)
    input_box = pygame.Rect(50, 35, 300, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = input_box.collidepoint(event.pos)
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        
        input_screen.fill((255, 255, 255))
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        pygame.draw.rect(input_screen, color, input_box, 2)
        input_screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.display.flip()
    
    return text

def main():
    pygame.init()

    screen_width, screen_height = 600, 400
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Weather Checker")

    white = (255, 255, 255)
    black = (0, 0, 0)
    blue = (135, 206, 250)
    button_color = (70, 130, 180)
    button_hover_color = (30, 144, 255)

    pygame.font.init()
    font = pygame.font.Font(pygame.font.get_default_font(), 40)
    small_font = pygame.font.Font(pygame.font.get_default_font(), 35)

    default_city = getCity()
    weather_data = getWeather(default_city)

    is_running = True
    while is_running:
        screen.fill(blue)

        # Создаем и отрисовываем кнопку
        change_city_button = draw_button(
            screen,
            "Change City",
            (screen_width//2 - 60, 20),
            (120, 40),
            button_color,
            button_hover_color
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if change_city_button.collidepoint(event.pos):
                    new_city = get_user_input()
                    if new_city:
                        default_city = new_city
                        weather_data = getWeather(new_city)
                        # Восстанавливаем основное окно после ввода
                        screen = pygame.display.set_mode((screen_width, screen_height))
                        pygame.display.set_caption("Weather Checker")

        if weather_data:
            title = font.render(f"Weather in {default_city}", True, black)
            title_rect = title.get_rect(center=(screen_width // 2, 100))
            screen.blit(title, title_rect)

            temp = small_font.render(f"Temperature: {weather_data[0]}°C", True, black)
            temp_rect = temp.get_rect(center=(screen_width // 2, 150))
            screen.blit(temp, temp_rect)

            desc = small_font.render(f"Description: {weather_data[1]}", True, black)
            desc_rect = desc.get_rect(center=(screen_width // 2, 200))
            screen.blit(desc, desc_rect)

            humidity = small_font.render(f"Humidity: {weather_data[2]}%", True, black)
            humidity_rect = humidity.get_rect(center=(screen_width // 2, 250))
            screen.blit(humidity, humidity_rect)

            wind_speed = small_font.render(f"Wind speed: {weather_data[3]} м/с", True, black)
            wind_speed_rect = wind_speed.get_rect(center=(screen_width // 2, 300))
            screen.blit(wind_speed, wind_speed_rect)
        else:
            error_message = font.render("Error retrieving weather data.", True, black)
            error_message_rect = error_message.get_rect(center=(screen_width // 2, 320))
            screen.blit(error_message, error_message_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

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
        return [temperature, weather_description, humidity, wind_speed]
    else:
        return None

if __name__ == "__main__":
    main()