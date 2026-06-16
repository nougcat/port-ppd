import random
import numpy as np
from optimization import Gen, Chromosom, cena_za_lodke, wartosc_za_lodke, N_rzedow, N_slotow
import copy
from generate_boat import stala_lista

LICZBA_CHROMOSOMOW = 20

def generate_chromosome(idx_boat, N_lodek = 21, N_rzedow = N_rzedow, N_slotow=N_slotow):
    
    gene = []
    random.shuffle(idx_boat)

    zajete_sloty = set()
    zajete_przez_trojki = set()

    for b in idx_boat:
            
        wolne = []
        for i in range(N_rzedow):
            for j in range(N_slotow):
                if (i,j) in zajete_sloty:
                    continue
                if i in zajete_przez_trojki:
                    continue
                if b == 3:
                    if (i, 1 - j) in zajete_sloty:
                        continue
                wolne.append((i,j))
        if not wolne:
            continue
    
        rzad, strona = random.choice(wolne)
        gene.append(Gen(b, rzad, strona))
        zajete_sloty.add((rzad, strona))

        if b == 3:
            zajete_przez_trojki.add(rzad)

    return Chromosom(gene)

def chromosome_to_matrix(chromosome: Chromosom, N_rzedow = N_rzedow, N_slotow = N_slotow) :
    matrix = np.zeros((N_rzedow, N_slotow), dtype=int)
    for gen in chromosome.geny:
        matrix[gen.rzad][gen.strona] = gen.lodka
    return matrix


def mutation(chromosome: Chromosom, N_rzedow: int, prob=0.1):
    '''
    Wybieramy losowy gen z chromosomu i wybieramy dla niego nowe losowe miejsce
    '''
    geny = [Gen(g.lodka, g.rzad, g.strona) for g in chromosome.geny]

    for idx in range(len(geny)):
        if random.random() > prob:
            continue

        drugi_idx = random.randint(0, len(geny) - 1)
        if drugi_idx == idx:
            continue

        geny[idx].rzad, geny[drugi_idx].rzad = geny[drugi_idx].rzad, geny[idx].rzad
        geny[idx].strona, geny[drugi_idx].strona = geny[drugi_idx].strona,  geny[idx].strona

    return Chromosom(geny)

def crossing(parent_a: Chromosom, parent_b: Chromosom):
    '''
    Crossing dzieli chromosomy na 3 części. Następnie zamienia środkową część między genami
    '''
    geny_a = parent_a.geny
    geny_b = parent_b.geny
    m = min(len(geny_a), len(geny_b))

    p1, p2 = sorted(random.sample(range(m), 2))

    segment = geny_a[p1:p2]
    zajete = {(g.rzad, g.strona) for g in segment}

    dopelnienie = [
        Gen(g.lodka, g.rzad, g.strona)
        for g in geny_b
        if (g.rzad, g.strona) not in zajete
    ]

    nowe_geny = dopelnienie[:p1] + segment + dopelnienie[p1:]

    return Chromosom(nowe_geny)

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

def f_cel_value(chromosome: Chromosom):
    value = 0
    for gene in chromosome.geny:
        value += gene.lodka
    return value

def fitness_func(chromosome: Chromosom):

    kara_blokada = 5
    kara_kolizacja = 10

    kara = 0

    pozycje = [(gen.rzad, gen.strona) for gen in chromosome.geny]

    for pos in pozycje:
        if pozycje.count(pos) > 1:
            kara += kara_kolizacja
 

    blokady = block_dock(chromosome)

    for gen in chromosome.geny:
        kara += sum(blokady[j] for j in range(gen.rzad)) * kara_blokada
 

    wartosc = sum(wartosc_za_lodke[gen.lodka] for gen in chromosome.geny)

    chromosome.fitness += wartosc - kara
 
    return chromosome.fitness

def selection(populacja: list[Chromosom], k = 3) -> Chromosom:
    
    candidates = random.sample(populacja, k)
    return max(candidates, key = lambda ch: ch.fitness)

def genetic_algorithm(population: list[Chromosom], etapy = 100, warunek_stopu = 20):
    
    populacja = copy.deepcopy(population)

    best_fit_func = float('-inf')
    best_chromosome = None
    no_changes = 0

    for gen in range(etapy):

        for chrom in populacja:
            chrom.fitness = 0
            chrom.fitness = fitness_func(chrom)

        print(f'Fitness w nowej populacji: {[ch.fitness for ch in populacja]}')
        

        #najlepsze chromosomy

        best_in_gene = max(populacja, key=lambda ch: ch.fitness)

        print(f'max_idx = {best_in_gene}')

        if best_in_gene.fitness > best_fit_func:
            best_fit_func = best_in_gene.fitness
            best_chromosome = copy.deepcopy(best_in_gene)
            no_changes = 0
        else:
            no_changes += 1
 
        print(f'Generacja {gen:3d} | fitness: {best_fit_func:.2f} | bez poprawy: {no_changes}')
        print(f'Najlepszy chromosom: {best_chromosome}')
 
        if no_changes >= warunek_stopu:
            print(f'Zbieżność w generacji {gen}')
            break
 
        # tworzenie nowej populacji
        new_population = [copy.deepcopy(best_chromosome)]  
 
        while len(new_population) < len(populacja):
 
            # selekcja turniejowa rodziców
            parent_a = selection(populacja)
            parent_b = selection(populacja)
 
            # krzyżowanie
            child = crossing(parent_a, parent_b)
 
            # mutacja
            child = mutation(child, N_rzedow)
 
            new_population.append(child)
 
        populacja = new_population

        print(f'Długości chromosomów: {[len(ch.geny) for ch in populacja]}')
 
    best_chromosome_mapped = chromosome_to_matrix(best_chromosome)

    max_value = f_cel_value(best_chromosome)
    print(f'Wartośc funkcji celu wynosi: {max_value}')

    return best_chromosome_mapped



genetic_population = []
for _ in range(LICZBA_CHROMOSOMOW):
    chromosome = generate_chromosome(stala_lista)
    genetic_population.append(chromosome)


print(genetic_algorithm(genetic_population))