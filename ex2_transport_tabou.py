import random
import itertools

COUT = [[5, 3, 4],   
        [6, 7, 2]]  
OFFRE = [8, 9]       
DEMANDE = [4, 5, 8]  
NB_D, NB_M = len(OFFRE), len(DEMANDE)


def cout_total(x):
    return sum(COUT[i][j] * x[i][j] for i in range(NB_D) for j in range(NB_M))


def solution_initiale():
    """Règle du coin Nord-Ouest (solution réalisable)."""
    x = [[0] * NB_M for _ in range(NB_D)]
    o, d = OFFRE[:], DEMANDE[:]
    i = j = 0
    while i < NB_D and j < NB_M:
        q = min(o[i], d[j])
        x[i][j] = q
        o[i] -= q
        d[j] -= q
        if o[i] == 0:
            i += 1
        else:
            j += 1
    return x


def voisins(x):
    for i1, i2 in itertools.permutations(range(NB_D), 2):
        for j1, j2 in itertools.permutations(range(NB_M), 2):
            if x[i1][j2] > 0 and x[i2][j1] > 0:
                y = [ligne[:] for ligne in x]
                y[i1][j1] += 1
                y[i1][j2] -= 1
                y[i2][j1] -= 1
                y[i2][j2] += 1
                yield (i1, i2, j1, j2), y


def recherche_taboue(nb_iter=50, taille_tabou=5, graine=0):
    random.seed(graine)
    x = solution_initiale()
    meilleur, meilleur_cout = [l[:] for l in x], cout_total(x)
    tabou = []  
    print(f"Solution initiale : {x}  coût = {cout_total(x)}")
    for it in range(1, nb_iter + 1):
        candidats = []
        for mv, y in voisins(x):
            c = cout_total(y)
            inverse = (mv[1], mv[0], mv[3], mv[2])
            if inverse not in tabou or c < meilleur_cout:
                candidats.append((c, mv, y))
        if not candidats:
            break
        c, mv, y = min(candidats, key=lambda t: t[0])
        x = y
        tabou.append(mv)
        if len(tabou) > taille_tabou:
            tabou.pop(0)
        if c < meilleur_cout:
            meilleur, meilleur_cout = [l[:] for l in y], c
        print(f"Iter {it:2d} : mouvement {mv}  coût = {c}  (meilleur = {meilleur_cout})")
    return meilleur, meilleur_cout


if __name__ == "__main__":
    sol, c = recherche_taboue()
    print("\nMeilleure solution (lignes = dépôts, colonnes = magasins) :")
    for i, ligne in enumerate(sol, 1):
        print(f"  D{i} :", ligne)
    print("Coût total minimal trouvé :", c)