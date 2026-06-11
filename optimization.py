import numpy as np
import gurobipy as gp
from gurobipy import GRB
import numpy as np

N_rzedow = 10
N_slotow = 2

class Gen:   
    def __init__(self,lodka,rzad, strona):
          self.lodka = lodka
          self.rzad = rzad
          self.strona = strona

    def __repr__(self):
         
        return f'Gen ({self.lodka},{self.rzad},{self.strona})'

class Chromosom:
     
    def __init__(self, geny: list[Gen]):
        self.geny = geny
        self.fitness = 0

    def __repr__(self):
        geny_str = ','.join(str(gen) for gen in self.geny)
        return f'Chromosom([{geny_str}]\n\n)'

# id_lodek = ['A', 'B', 'C','D','E','F','G','H','I','J','K']

#dlugosci_lodek = np.array([1,2,3,1,1,3,2,1,3,2,1,3,2,2,3,1]) 

dlugosci_lodek = np.random.randint(0,3,20)
wartosc_za_lodke = {0:1, 1:6, 2:5, 3:4}
cena_za_lodke = {0:1, 1:60, 2:70, 3:90}

def optimize_and_save(dlugosci_lodek, wartosc_za_lodke, cena_za_lodke):
    
    '''
    Dodawanie wartości łódek i funkcja kary dla ograniczenia ilości łódek
    '''

    N_lodek = len(dlugosci_lodek)
    

    model = gp.Model("Optymalizacja_Macierzowa")


    M = model.addMVar(shape = (N_lodek,N_rzedow,N_slotow), vtype = GRB.BINARY, name= "Model portu do mapowania łódek")

    #Funkcja kary => Jeżeli wystąpi ograniczenie dwóch łódek nakładamy na funkcję celu karę 


    f_cel = gp.quicksum(M[b,i,s] * (1 + wartosc_za_lodke[dlugosci_lodek[b]]) for b in range(N_lodek) for i in range(N_rzedow) for s in range(N_slotow)) 

    model.setObjective(f_cel, GRB.MAXIMIZE)


    #kazda lodka w jednym slotcie

    for b in range(N_lodek):
        model.addConstr(M[b,:,:].sum() <= 1)

    #kazdy slot przyjmuje tylko jedna łódke

    for i in range(N_rzedow):
        for s in range(N_slotow):
            model.addConstr(M[:,i,s].sum() <= 1)

    #lodka 3 nie moze miec na przeciwko siebie nikogo

    for boat_3 in np.where(dlugosci_lodek == 3)[0]:
        for i in range(N_rzedow):
            
                    model.addConstr(
                        (M[boat_3,i,0] == 1) >> (M[:,i,1] == 0),
                        name = 'Zakaz stawania na przeciwko (dla lewej strony)'
                    )

                    model.addConstr(
                        (M[boat_3,i,1] == 1) >> (M[:,i,0] == 0),
                        name = 'Zakaz stawania na przeciwko (dla prawej strony)'
                    )
            
                    
    #dwie łódki 2 tworzą blokadę
    boat_2 = np.where(dlugosci_lodek == 2)[0]

    for i in range(N_rzedow - 1):
        for b1 in boat_2:
                for b2 in boat_2:
                    if b1 != b2:
                        
                        z = model.addVar(vtype=GRB.BINARY, name='Wartość blokady przez dwie łódki o długości 2')

                        model.addConstr(z == gp.and_(M[b1,i,0], M[b2,i,1]))

                        model.addConstr((z==1) >> (M[:,i+1,:].sum() == 0))

    model.setParam('PoolSearchMode', 2)
    model.setParam('PoolSolutions', 10)
    model.setParam('PoolGap', 0.9)
    model.optimize()

    populacja = []
    for sol in range(model.SolCount):       

        model.setParam('SolutionNumber', sol)

        geny = []
        for b in range(len(dlugosci_lodek)):               
            for i in range(N_rzedow):
                for j in range(N_slotow):
                    if M.Xn[b, i, j] > 0.5:   
                        geny.append(Gen(lodka=dlugosci_lodek[b], rzad= i, strona = j))


        populacja.append(Chromosom(geny))
  

    matrix_mapped = np.zeros((N_rzedow, N_slotow))

    for b in range(N_lodek):
        for i in range(N_rzedow):
            for s in range(N_slotow):
                if M[b,i,s].X > 0.5:
                    matrix_mapped[i][s] = dlugosci_lodek[b]

    print(matrix_mapped)


    return populacja

        print("Rozwiązanie metaheurystyczne 0:")
        for gen in geny:
            print(gen)

genetic_population = optimize_and_save(dlugosci_lodek, wartosc_za_lodke, cena_za_lodke)
print(genetic_population)
