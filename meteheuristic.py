import random
import numpy as np
from optimization import genetic_population, Gen, Chromosom

def mutation(chromosome: Chromosom, N_rzedow: int, prob=0.1):
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
    p1,p2 = sorted(random.sample(range(1,m), 2))

    middle_b = parent_b.geny[p1:p2]
    rest_a = [g for g in parent_a.geny if g.lodka not in {g.lodka for g in middle_b}]

    return Chromosom(parent_a[:p1] + middle_b + rest_a[p1:])

def genetic_algorithm(genetic_population: list[Chromosom]):
    pass