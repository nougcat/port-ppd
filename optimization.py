import numpy as np
import gurobipy as gp
from gurobipy import GRB


id_lodek = ['A', 'B', 'C','D','E','F','G','H','I']

dlugosci_lodek = np.array([1,2,3,1,1,3,2,1,3]) 

N_lodek = len(id_lodek)
N_rzedow = 5
N_slotow = 2

model = gp.Model("Optymalizacja_Macierzowa")


M = model.addMVar(shape = (N_lodek,N_rzedow,N_slotow), vtype = GRB.BINARY, name= "Model portu do mapowania łódek")


f_cel = gp.quicksum(dlugosci_lodek[b] * M[b,i,s]
                    for b in range(N_lodek)
                    for i in range(N_rzedow)
                    for s in range(N_slotow))

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


model.optimize()

matrix_mapped = np.zeros((N_rzedow, N_slotow))

for b in range(N_lodek):
    for i in range(N_rzedow):
        for s in range(N_slotow):
             if M[b,i,s].X > 0.5:
                   matrix_mapped[i][s] = dlugosci_lodek[b]

print(matrix_mapped)