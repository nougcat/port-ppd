import numpy as np
import random
from optimization import N_lodek

boat = [0,1,2,3]
wagi = [0.10, 0.35, 0.35, 0.20] 

wylosowany = random.choices(boat, weights=wagi, k=N_lodek)

print(wylosowany)
# [1, 1, 2, 2, 1, 1, 1, 3, 3, 3, 3, 3, 1, 1, 1, 3, 1, 3, 2, 2, 2]

stala_lista = [1, 1, 2, 2, 1, 1, 1, 3, 3, 3, 3, 3, 1, 1, 1, 3, 1, 3, 2, 2, 2]