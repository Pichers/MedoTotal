from searchPlus import *
import utils

parametros="T=26\nM=6\nP=10"
linha1= "= = = = = = = = = =\n"
linha2= "= @ . * . . * . . =\n"
linha3= "= . = = = = = = . =\n"
linha4= "= . = F . . . . . =\n"
linha5= "= . = . . . . . . =\n"
linha6= "= . = . . . . . . =\n"
linha7= "= . = . . . . . . =\n"
linha8= "= * . . . . . . . =\n"
linha9= "= . . . . . . . . =\n"
linha10="= = = = = = = = = =\n"
grelha=linha1+linha2+linha3+linha4+linha5+linha6+linha7+linha8+linha9+linha10
mundoStandard=parametros + "\n" + grelha

#
# Alterar o GRID para não conter espaços 
# (desnecessario excepto para o display)
#

class MedoTotal(Problem):
    
    def __init__(self, situacaoInicial = mundoStandard):
        a = situacaoInicial.split("\n")
        t, m, self.p = int(a[0][2:]), int(a[1][2:]), int(a[2][2:])

        self.grid = a[3:]
        self.f = ()

        pastilhas = []
        
        for y in range(len(self.grid) - 1): 
            self.grid[y] = utils.removeall(" ", self.grid[y])
            for x in range(len(self.grid[0]) - 1):

                c = self.grid[y][x]

                if(c != "." and c != "=" and c != " "):

                    #[posição das pastilhas]
                    if c == "*":
                        if(len(pastilhas) == 0):
                            pastilhas = [(x,y)]
                        else:
                            pastilhas.append((x,y))
                    #pos do pacman
                    elif c == "@":
                        pos = (x,y)
                    elif c == "F":
                        self.f = (x,y)
                    
                    self.grid[y] = self.grid[y][:x] + "." + self.grid[y][x + 1:]

        #estado: (pacman,pastilhas,t,m)
        self.initial = (pos, pastilhas, t, m)
        
   
    def actions(self, state):
        p = state[0]
        past = state[1]
        t = state[2]
        m = state[3]

        pastDistances = MedoTotal.dists(p, past)

        actions = []

        #instant cut
        if(len(past) == 0 and t > m):
            return []
        elif(min(pastDistances) > m):
            print(min(pastDistances))
            print("aa")
            return []
        elif(min(pastDistances) + self.p * len(past) < t):
            return []
        
        #actions (1 para N/S e 2 for each move because of spaces in the grid)
        N = (0,-1)
        W = (-1,0)
        E = (1,0)
        S = (0,1)
        
        directions = [N, W, E, S]

        for i in range(4):
            d = directions[i]

            #MAKE THIS A SWITCH CASE!!!
            if(MedoTotal.canMove(self, state, d)):
                if(d == N):
                    actions.append("N")
                elif(d == S):
                    actions.append("S")
                elif(d == E):
                    actions.append("E")
                elif(d == W):
                    actions.append("W")
        
        return actions

        
    def result(self, state, action):
        pass
    
    def path_cost(self, c, state1,action,next_state):
        pass
    
    def executa(self,state,actions):
        """Partindo de state, executa a sequência (lista) de
          acções (em actions) e devolve o último estado"""
        nstate = state
        for a in actions:
            nstate = p.result(nstate,a)
        return nstate
    
    def display(self, state):
        s = ""
        pGrid = list(self.grid)  # Make a copy of the grid

        for y in range(len(self.grid)):  # Iterate over all rows
            for x in range(len(self.grid[0])):  # Iterate over all columns
                if (x, y) in state[1]:
                    # Places the pastilhas
                    pGrid[y] = pGrid[y][:x] + "*" + pGrid[y][x + 1:]
                elif (x, y) == (state[0][0], state[0][1]):
                    # Places the pacman
                    pGrid[y] = pGrid[y][:x] + "@" + pGrid[y][x + 1:]
                elif (x, y) == self.f:
                    # Places the ghost
                    pGrid[y] = pGrid[y][:x] + "F" + pGrid[y][x + 1:]
                    
        #after each character in a string, add " "

        # Join the modified lines with spaces to form the final string
        s = "\n".join(pGrid)
        return s
    
    @staticmethod
    def snakeDistance(a,b):
        return abs((a[0] - b[0])) + abs(a[1] - b[1])
    
    @staticmethod
    def dists(x, ys):
        d = []

        for i in range(len(ys)):
            d.append(MedoTotal.snakeDistance(x, ys[i]))

        return d
    
    @staticmethod
    def canMove(self, state, d):
        p = state[0]

        newPos = (p[0] + d[0], p[1] + d[1])

        c = self.grid[newPos[1]][newPos[0]]

        canMove = (c != "=") and (newPos != self.f) 

        return canMove
