import pygame, sys
import numpy as np
import pandas as pd
class Grid:
    shapes={}
    a_dir = np.array([[1,0], [-1,0],
        [0, 1], [0, -1],
        [1/np.sqrt(2),1/np.sqrt(2)], [1/np.sqrt(2), -1/np.sqrt(2)], 
        [-1/np.sqrt(2), 1/np.sqrt(2)], [-1/np.sqrt(2),-1/np.sqrt(2)]])
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
        ##print(self.p_grid)
        self.p_grid[y, x] = val

    def draw_object(self, name, x, y):
        for pt in self.shapes[name]:
            if pt[0] + x < self.resolution[0] and pt[1] + y < self.resolution[1]:
                self.set_pixel(pt[0] + x, pt[1] + y, 1)
    
    def movement(self, u_dir):
        

        dots = []
        ref_dirs = []
        for dir in self.a_dir:
            dots.append(np.dot(np.array(dir), np.array(u_dir)))
            ref_dirs.append(dir)

        dir_df = pd.DataFrame({"dots": dots, "dirs": ref_dirs})
        return dir_df.sort_values("dots")    


        



        

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

                walls_w = np.where(self.p_grid == 1)
                people_w = np.where(self.p_grid == 2)
                zombies_w = np.where(self.p_grid == 3)

                walls = np.array((walls_w[1], walls_w[0])).T
                people = np.array((people_w[1], people_w[0])).T
                zombies = np.array((zombies_w[1], zombies_w[0])).T

                ##print(f"Walls: {walls}")
                ##print(f"People: {people}")
                ##print(f"Zombies: {zombies}")



                """
                
                0 - empty
                1 - wall
                2 - person
                3 - zombie

                """

                if self.p_grid[j][i] == 0:
                    self.s_grid[j][i] = 0

                elif self.p_grid[j][i] == 1:
                    self.s_grid[j][i] = 1

                elif self.p_grid[j][i] == 2:
                    r_move = np.array([0,0], dtype= np.float64)
                    pos = [i, -j]
                    print("PERSON")
                    for z in zombies:
                        # i is correct dir
                        # j is opposite dir
                        
                        dx = z[0] - pos[0]
                        dy = - z[1] - pos[1]

                        
                        unit = np.array([dx, dy])
                        r_move += unit
                    r_move_mag  = (r_move[0]**2 + r_move[1]**2)**(1/2)
                    r_unit = (1/r_move_mag)*r_move
                    pref_dir_df = self.movement( np.array([-r_unit[0], -r_unit[1]]))
                    pref_dirs = pref_dir_df["dirs"].values
                    pref_dots = pref_dir_df["dots"].values

                    for k in range(1, len(pref_dots)):
                        pref_dir_vec = pref_dirs[-k]
                        if (self.s_grid[j - round(pref_dir_vec[1])][i+ round(pref_dir_vec[0])] == 0) and (self.p_grid[j - round(pref_dir_vec[1])][i+ round(pref_dir_vec[0])] == 0):


                            self.s_grid[j - round(pref_dir_vec[1])][i+ round(pref_dir_vec[0])] = 2
                            #self.s_grid[j][i] = 0
                            break
                        else:
                            print("No CASE")
                            if k == len(pref_dots) - 1:
                                self.s_grid[j][i] = 2


                elif self.p_grid[j][i] == 3:
                    r_move = np.array([0,0], dtype= np.float64)
                    pos = [i, -j]
                    print("ZOMBIE")
                    for z in people:
                        
                        # i is correct dir
                        # j is opposite dir
                        
                        dx = z[0] - pos[0]
                        dy = - z[1] - pos[1]

                        
                        unit = np.array([dx, dy])
                        r_move += unit
                    r_move_mag  = (r_move[0]**2 + r_move[1]**2)**(1/2)
                    r_unit = (1/r_move_mag)*r_move
                    pref_dir_df = self.movement( np.array([r_unit[0], r_unit[1]]))
                    pref_dirs = pref_dir_df["dirs"].values
                    pref_dots = pref_dir_df["dots"].values

                    for k in range(1, len(pref_dots)):
                        pref_dir_vec = pref_dirs[-k]
                        if (self.s_grid[j - round(pref_dir_vec[1])][i+ round(pref_dir_vec[0])] == 0) and (self.p_grid[j - round(pref_dir_vec[1])][i+ round(pref_dir_vec[0])] == 0):

                            self.s_grid[j - round(pref_dir_vec[1])][i+ round(pref_dir_vec[0])] = 3
                            #self.s_grid[j][i] = 0
                            break
                        else:
                            if k == len(pref_dots) - 1:
                                self.s_grid[j][i] = 3
                else:
                    pass

        
        self.p_grid = np.copy(self.s_grid)
        self.s_grid.fill(0)
        