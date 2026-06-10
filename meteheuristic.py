import random
import numpy as np
from optimization import genetic_population, Gen, Chromosom, dlugosci_lodek, cena_za_lodke, wartosc_za_lodke, N_rzedow



def mutation(chromosome: Chromosom, N_rzedow: int, prob=0.3):
    '''
    Wybieramy losowy gen z chromosomu i wybieramy dla niego nowe losowe miejsce
    '''
    mutated_genes = []
    for gen in chromosome.geny:
        if random.random() < prob:
            new_gene = Gen(
                lodka = gen.lodka,
                rzad = random.randint(0, N_rzedow - 1),
                strona = random.randint(0,1)
            )
            mutated_genes.append(new_gene)
        else:
            mutated_genes.append(gen)

    return Chromosom(mutated_genes)

def crossing(parent_a: Chromosom, parent_b: Chromosom):
    '''
    Crossing dzieli chromosomy na 3 części. Następnie zamienia środkową część między genami
    '''
    m = len(parent_a.geny)
    p1, p2 = sorted(random.sample(range(1, m), 2))

    middle_b = parent_b.geny[p1:p2]

  
    left_a  = parent_a.geny[:p1]
    right_a = parent_a.geny[p2:]

    return Chromosom(left_a + middle_b + right_a)

def block_dock(chromosome):

    occ = [[0,0] for _ in range(N_rzedow)]

    for gen in chromosome.geny:
        rozmiar = gen.lodka
        occ[gen.rzad][gen.strona] = rozmiar

    blokady = []
    for j in range(N_rzedow):
        suma = occ[j][0] + occ[j][1]
        three = occ[j][0]==3 or occ[j][1] ==3
        blokady.append(1 if suma >=4 or three else 0)

    return blokady

def fitness_func(chromosome: Chromosom, dlugosci_lodek:list, wartosci_za_lodke:dict):

    kara_blokada = 50
    kara_kolizacja = 100

    kara = 0

    pozycje = [(gen.rzad, gen.strona) for gen in chromosome.geny]
    for pos in pozycje:
        if pozycje.count(pos) > 1:
            kara += kara_kolizacja
 

    blokady = block_dock(chromosome)

    for gen in chromosome.geny:
        kara += sum(blokady[j] for j in range(gen.rzad)) * kara_blokada
 

    wartosc = sum(wartosc_za_lodke[gen.lodka] for gen in chromosome.geny)
 
    return wartosc - kara

def selection(populacja: list[Chromosom], oceny, k = 3):
    
    candidates = random.sample(range(len(populacja)), k)
    best_candidates = max(candidates, key = lambda i: oceny[i])

    return populacja[best_candidates]

def genetic_algorithm(genetic_population: list[Chromosom], etapy = 100, warunek_stopu = 20):
    
    populacja = genetic_population.copy()

    best_fit_func = float('-inf')
    best_chromosome = None
    no_changes = 0

    for gen in range(etapy):

        oceny = [
            fitness_func(chrom, dlugosci_lodek,wartosc_za_lodke) for chrom in populacja
        ]

        #najlepsze chromosomy

        max_idx = int(np.argmax(oceny))
        if oceny[max_idx] > best_fit_func:
            best_fit_func = oceny[max_idx]
            best_chromosome = populacja[max_idx]
            no_changes = 0
        else:
            no_changes += 1
 
        print(f'Generacja {gen:3d} | fitness: {best_fit_func:.2f} | bez poprawy: {no_changes}')
 
        if no_changes >= warunek_stopu:
            print(f'Zbieżność w generacji {gen}')
            break
 
        # tworzenie nowej populacji
        new_population = [best_chromosome]  
 
        while len(new_population) < len(populacja):
 
            # selekcja turniejowa rodziców
            parent_a = selection(populacja, oceny)
            parent_b = selection(populacja, oceny)
 
            # krzyżowanie
            child = crossing(parent_a, parent_b)
 
            # mutacja
            child = mutation(child, N_rzedow)
 
            new_population.append(child)
 
        populacja = new_population
 
    return best_chromosome

print(genetic_population)
print(genetic_algorithm(genetic_population))