import sys,time
import pygame
import numpy as np
from grid import *
pygame.init()
clock = pygame.time.Clock()

class Start:
    def __init__(self, size):
        self.surface = pygame.Surface(size)
        self.start_b_pos = [(250,250), (500,100)]  
        self.draw_button(self.start_b_pos[0], self.start_b_pos[1], 'Start Grid', 48, (410, 280))
        self.create_b_pos = [(250,500), (500,100)] 
        self.draw_button(self.create_b_pos[0],self.create_b_pos[1], 'Create', 48,(430, 530))
        self.bounds_array={"start":self.start_b_pos,"create":self.create_b_pos}
        
        
        

    def draw_button(self, pos, size,  text, font_size, t_pos, pad =10):
        font = pygame.font.SysFont('chalkduster.ttf', font_size)
        pygame.draw.rect(self.surface, (255,255,255), (pos[0], pos[1], size[0], size[1]))
        pygame.draw.rect(self.surface, (0,0,0), (pos[0]+pad, pos[1]+pad, size[0]-(2*pad), size[1]-(2*pad)))
        self.surface.blit(font.render(text, True, (255,255,255)), t_pos)

    def check_bounds(self, pos):
        for item in self.bounds_array:
            bounds = self.bounds_array[item]
            if pos[0] > bounds[0][0] and pos[0] < bounds[0][0] + bounds[1][0]:
                if pos[1] > bounds[0][1] and pos[1] < bounds[0][1] + bounds[1][1]:
                    return item



size = w_WIDTH, w_HEIGHT = 1000, 1000
screen = pygame.display.set_mode(size)

p_size = 100

m_grid = Grid(size, p_size)
start = Start(size)
mouse_b = 0
anim =False
fps = 60

scene = 0

map = []

f = open("shapes.txt", "r")
data = f.readlines()
for line in data:

    ar = line.split(',')
    ar[-1] = ar[-1][0]
    arr = np.array(ar, int)
    map.append(arr)
f.close()
map = np.vstack(map)

print(map.shape)

for y in range(map.shape[0]):
    for x in range(map.shape[1]):
        m_grid.set_pixel(x, y, map[y, x])


while True:
    
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if anim == False:
            fps = 60
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    mouse_b = 2
                elif pygame.mouse.get_pressed()[2]:
                    mouse_b = 1
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_b = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and scene == 1:  
                anim = not anim
            if event.key == pygame.K_BACKSPACE and scene == 1:
                anim = False
                m_grid.p_grid.fill(0)
                scene = 0
    if mouse_b != 0:
        m_pos = pygame.mouse.get_pos()
        if scene == 1:
            """
            g_pos = tuple([i // p_size for i in m_pos])

            m_grid.set_pixel(g_pos[0], g_pos[1], mouse_b - 1)
            """
            pass
        elif scene == 0:
            clicked = start.check_bounds(m_pos)
            if clicked == "start":
                scene = 1
    if anim:
        fps = 200

        m_grid.update()
       
    
    m_grid.draw_grid()

    if scene == 1:
        screen.blit(m_grid.surface, (0,0))
    elif scene == 0:
        screen.blit(start.surface, (0,0))
    pygame.display.flip()
    

