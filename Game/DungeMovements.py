import requests
import pygame

address_ll = "133.795384,-25.694768"

delta = "0.001"
screen = pygame.display.set_mode((600,450))
screen.fill((0, 0, 0))

map_params = {
        "ll": address_ll, # позиционируем карту центром на наш исходный адрес
        "spn": ",".join([delta, delta]),
        "l": "sat",
}
running = True
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
with open('result.jpg', 'wb') as f:
    f.write(response.content)
hero_x,hero_y = 0,0
text = "down"
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    img = pygame.image.load('result.jpg')
    hero = pygame.image.load('hero.jpg')
    hero = pygame.transform.scale(hero,(50,50))
    screen.blit(img, (0, 0))
    for i in range(6):
        pygame.draw.line(screen, (0, 0, 0), (i * 100, 0), (i * 100, 450),3)
    for i in range(6):
        pygame.draw.line(screen, (0, 0, 0), (0, i*75), (600, i*75),3)
    if(text == "left" and (hero_x-100 >= 0)):
        hero_x -= 100
    if (text == "right" and (hero_x+100 <= 600)):
        hero_x += 100
    if (text == "up" and (hero_y-75 >= 0)):
        hero_y -= 75
    if (text == "down" and (hero_y+75 <=450)):
        hero_y += 75
    text = ""
    screen.blit(hero, (hero_x + 25,hero_y + 12.5))
    pygame.display.flip()
with open("Quest.txt", "r") as file:
    s = file.readlines()
    temp = s[0].split()#random 0
    quest = temp[1]
    #выод пользователю
