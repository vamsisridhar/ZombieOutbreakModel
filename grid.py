import pygame, sys
import numpy as np
class Grid:
    shapes={}
    
    def __init__(self, size: tuple, p_size: int):
        self.resolution = tuple([i // p_size for i in size]) # res
        self.p_grid = np.zeros(self.resolution) #Primary
        self.s_grid = np.zeros(self.resolution)#Secondary
        self.surface = pygame.Surface(size) 
        self.p_size = p_size

    def draw_grid(self):
        self.surface.fill((0,0,0))
        for i in range(self.resolution[0]):
            for j in range(self.resolution[1]):
                if self.p_grid[j][i] == 1:
                    p_color = (255, 255, 255)
                elif self.p_grid[j][i] == 2:
                    p_color = (0, 255, 0)
                elif self.p_grid[j][i] == 3:
                    p_color = (255, 0, 0)
                else:
                    p_color = (0,0,0)
                pygame.draw.rect(self.surface, p_color, tuple([i * self.p_size for i in [i, j, 0.8, 0.8]]))
    
    def set_pixel(self, x, y, val:int):
        print(self.p_grid)
        self.p_grid[y, x] = val

    def draw_object(self, name, x, y):
        for pt in self.shapes[name]:
            if pt[0] + x < self.resolution[0] and pt[1] + y < self.resolution[1]:
                self.set_pixel(pt[0] + x, pt[1] + y, 1)
                


        

    def update(self):


        for i in range(self.resolution[0]):
            for j in range(self.resolution[1]):
                n_count = 0
                
                for x in range(i-1, i+2):
                    for y in range(j-1, j+2):

                        if x > 0 and y > 0 and x < self.resolution[0] and y < self.resolution[1]:
                            
                            if (x, y) != (i,j):
                                if self.p_grid[y][x]:
                                    n_count += 1


                """
                
                0 - empty
                1 - wall
                2 - person
                3 - zombie

                """
                if self.p_grid[j][i] == 0:
                    pass

                elif self.p_grid[j][i] == 1:
                    pass

                elif self.p_grid[j][i] == 2:
                    pass
                elif self.p_grid[j][i] == 3:
                    pass

        
        
        self.p_grid = np.copy(self.s_grid)
        self.s_grid.fill(0)
        