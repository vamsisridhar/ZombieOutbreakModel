import pygame, sys
import numpy as np
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

        for dir in self.a_dir:
            dots.append(np.dot(np.array(dir), np.array(u_dir)))

        return np.array(dots)    


        



        

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
                    for z in zombies:
                        dx = - z[0] + i
                        dy = - z[1] + j
                        
                        unit = np.array([dx, dy])
                        r_move += unit
                    r_move_mag  = (r_move[0]**2 + r_move[1]**2)**(1/2)
                    r_unit = (1/r_move_mag)*r_move
                    
                    moves = self.movement(r_unit)
                    moves_ordered = np.sort(moves)
                    print(moves_ordered)
                    #r_pref_move = np.round(self.a_dir[moves.argmax()])


                    for k in range(len(moves_ordered)):

                        r_pref_move = np.round(self.a_dir[np.where(moves == moves_ordered[-1-k])[0][0]])
                        print(int(self.p_grid[j+int(r_pref_move[1])][i+int(r_pref_move[0])]))
                        if int(self.p_grid[j+int(r_pref_move[1])][i+int(r_pref_move[0])]) == 0:
                            print(r_pref_move)
                            print("Case 3")
                            ##print(self.p_grid[j+int(r_pref_move[1])][i+int(r_pref_move[0])])
                            break
                        else:
                            print("Case 2")
                            if k == len(moves_ordered):
                                r_pref_move = [0,0]
                                break
                            else:
                            
                            
                                print("CASE 1")
                                continue
                            continue
                    print("Case 4")
                    

                    self.s_grid[j+int(r_pref_move[1])][i+int(r_pref_move[0])] = 2

                elif self.p_grid[j][i] == 3:
                    r_move = np.array([0,0], dtype= np.float64)
                    for z in people:
                        dx =  z[0] - i
                        dy =  z[1] - j
                        
                        unit = np.array([dx, dy])
                        r_move += unit
                    r_move_mag  = (r_move[0]**2 + r_move[1]**2)**(1/2)
                    r_unit = (1/r_move_mag)*r_move
                    
                    moves = self.movement(r_unit)
                    moves_ordered = np.sort(moves)
                    #r_pref_move = np.round(self.a_dir[moves.argmax()])


                    for k in range(len(moves_ordered)):

                        r_pref_move = np.round(self.a_dir[np.where(moves == moves_ordered[-1-k])[0][0]])
                        ##print(self.p_grid[j+int(r_pref_move[1])][i+int(r_pref_move[0])])
                        if self.p_grid[j+int(r_pref_move[1])][i+int(r_pref_move[0])] == 0:
                            #print(r_pref_move)
                            ##print(self.p_grid[j+int(r_pref_move[1])][i+int(r_pref_move[0])])
                            break
                        else:
                                
                            
                            if k == len(moves_ordered) - 1:
                                r_pref_move = [0,0]
                                break
                            continue

                    

                    self.s_grid[j+int(r_pref_move[1])][i+int(r_pref_move[0])] = 3
                else:
                    pass

        
        self.p_grid = np.copy(self.s_grid)
        self.s_grid.fill(0)
        