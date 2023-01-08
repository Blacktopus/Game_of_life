import pygame
import random

 
pygame.init()
 
white = (255, 255, 255)
black = (0, 0, 0)

dis_height = 700 # высота
block_size = 10

random_size = 5
random_list = ([1]* random_size)+([0]*(10 - random_size)) # создание списка заполненного 0 и 1 в соотношении random_size/10
random.shuffle(random_list) # перемешивание списка

dis1 = pygame.display.set_mode((dis_height, dis_height))
pygame.display.set_caption('Game of life')

font_style = pygame.font.SysFont(None, 50)
pause_msg = font_style.render('Pause!', True, (180, 0, 0))

rng_h = range(dis_height//block_size) # массив высоты

commands_list = ['P - for pause', 'C - for clear screen','R - for restart', 'Esc - for quit game']
for c in commands_list:
    print(c)

def rules(y, x, val_list): # функция проверки соседних клеток и правила появления клеток
    count = 0
    check_list = [[-1 , -1] , [-1 , 0] , [-1 , 1] , [0 , -1] , [0 , 1] , [1 , -1] , [1 , 0] , [1 , 1]]
    for i in check_list:
        if ((y + i[0]) in rng_h) and ((x + i[1]) in rng_h):
            if val_list[y + i[0]][x + i[1]] == 1:
                count += 1
        else:
            continue
    if 2>count>3:
        return 0
    if count == 3:
        return 1
    if count == 2 and val_list[y][x] == 1:
        return 1
def gameloop():
    game_esc = False
    clear_screen = False
    game_pause = False
    list_main1 = [[random.choice(random_list) for w1 in rng_h] for h1 in rng_h] # двумерный список со случайными значениями
    def mouse_click(pos): # функция обработки нажатий мыши
        coord = [((pos[0]-10)//block_size)+1, ((pos[1]-10)//block_size)+1] # 10 - размер курсора
        if list_main1[coord[0]][coord[1]] == 1:
            list_main1[coord[0]][coord[1]] = 0
        else:
            list_main1[coord[0]][coord[1]] = 1
    while game_esc == False:
        dis1.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_esc = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_esc = True
                if event.key == pygame.K_r: # перезапуск функции
                    gameloop()
                if event.key == pygame.K_c:
                    clear_screen = not clear_screen
                if event.key == pygame.K_p:
                    game_pause = not game_pause
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click(event.pos) # передаём в функцию координаты курсора
                    pygame.display.update()
        list_main2 = [[0 for e in rng_h] for d in rng_h] # создание пустого двумерного списка
        for i in rng_h: # заполнение экрана по значениям из list_main1
            for j in rng_h:
                if list_main1[i][j] == 1:
                    pygame.draw.rect(dis1, black, [i*block_size, j*block_size, block_size, block_size])
        pygame.display.update()
        if clear_screen == True:
            list_main1 = list_main2
            clear_screen = not clear_screen
        if game_pause == True:
            dis1.blit(pause_msg, ((dis_height/2)-30, dis_height/4))
        else:
            for i in rng_h: # заполнение экрана по значениям из list_main1
                for j in rng_h:
                    list_main2[i][j] = rules(i,j,list_main1)
            list_main1 = list_main2
        pygame.display.update()
gameloop()