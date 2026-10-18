
import math
import random
import itertools

INF = 10_000  
N = 8
D = [[INF] * N for _ in range(N)]
ARETES = {
    (1, 2): 14, (1, 3): 15, (1, 8): 17,
    (2, 3): 13, (2, 4): 14, (2, 5): 20, (2, 8): 21,
    (3, 4): 11, (3, 5): 21, (3, 6): 17, (3, 7): 9, (3, 8): 9,
    (4, 5): 11, (4, 6): 10, (4, 7): 8, (4, 8): 20,
    (5, 6): 15, (5, 7): 18,
    (6, 7): 9,
    (7, 8): 13,
}
for (a, b), v in ARETES.items():
    D[a - 1][b - 1] = D[b - 1][a - 1] = v

INITIALE = [1, 2, 3, 4, 5, 6, 7, 8]


def longueur(t):
    return sum(D[t[k] - 1][t[(k + 1) % N] - 1] for k in range(N))


def affiche(t):
    return "-".join(map(str, t + [t[0]]))

def taboue(nb_iter=30, taille_tabou=4):
    x = INITIALE[:]
    best, best_c = x[:], longueur(x)
    tabou = []
    print(f"[Taboue] initiale {affiche(x)}  L = {best_c}")
    for it in range(1, nb_iter + 1):
        cand = []
        for i, j in itertools.combinations(range(1, N), 2):  
            y = x[:]
            y[i], y[j] = y[j], y[i]
            c = longueur(y)
            if (i, j) not in tabou or c < best_c:
                cand.append((c, (i, j), y))
        c, mv, y = min(cand, key=lambda t: t[0])
        x = y
        tabou.append(mv)
        if len(tabou) > taille_tabou:
            tabou.pop(0)
        if c < best_c:
            best, best_c = y[:], c
        print(f"  it {it:2d} : echange {mv} -> {affiche(x)}  L = {c}  (best = {best_c})")
    return best, best_c

def recuit(nb_iter=5, T0=50.0, alpha=0.5, mouvements_par_palier=1, graine=1, verbose=True):
    random.seed(graine)
    x = INITIALE[:]
    c = longueur(x)
    best, best_c = x[:], c
    T = T0
    if verbose:
        print(f"[Recuit] initiale {affiche(x)}  L = {c}")
    for it in range(1, nb_iter + 1):
        for _ in range(mouvements_par_palier):
            i, j = random.sample(range(1, N), 2)
            y = x[:]
            y[i], y[j] = y[j], y[i]
            cy = longueur(y)
            delta = cy - c
            p = 1.0 if delta <= 0 else math.exp(-delta / T)
            accepte = random.random() < p
            if accepte:
                x, c = y, cy
                if c < best_c:
                    best, best_c = x[:], c
        if verbose:
            print(f"  it {it} : T = {T:6.2f}  dernier delta = {delta:+d}  p = {p:.3f}  "
                  f"{'accepté' if accepte else 'refusé'}  L courant = {c}  best = {best_c}")
        T *= alpha
    return best, best_c
def croisement_ox(p1, p2):
    a, b = sorted(random.sample(range(N), 2))
    enfant = [None] * N
    enfant[a:b + 1] = p1[a:b + 1]
    reste = [v for v in p2 if v not in enfant]
    k = 0
    for i in range(N):
        if enfant[i] is None:
            enfant[i] = reste[k]
            k += 1
    return enfant


def genetique(taille_pop=30, generations=100, p_mut=0.2, graine=2):
    random.seed(graine)
    pop = [INITIALE[:]] + [random.sample(INITIALE, N) for _ in range(taille_pop - 1)]

    def tournoi():
        return min(random.sample(pop, 3), key=longueur)

    best = min(pop, key=longueur)
    for g in range(1, generations + 1):
        nouvelle = [best[:]]  # élitisme
        while len(nouvelle) < taille_pop:
            e = croisement_ox(tournoi(), tournoi())
            if random.random() < p_mut:
                i, j = random.sample(range(N), 2)
                e[i], e[j] = e[j], e[i]
            nouvelle.append(e)
        pop = nouvelle
        cand = min(pop, key=longueur)
        if longueur(cand) < longueur(best):
            best = cand[:]
        if g % 20 == 0:
            print(f"  génération {g:3d} : meilleur = {affiche(best)}  L = {longueur(best)}")
   
    k = best.index(1)
    best = best[k:] + best[:k]
    return best, longueur(best)
def optimum_exact():
    return min(([1] + list(p) for p in itertools.permutations(range(2, N + 1))), key=longueur)


if __name__ == "__main__":
    print("1) Recherche taboue")
    t, c = taboue()
    print("=> Résultat :", affiche(t), "L =", c)

    print("\n2) Recuit simulé (5 itérations)")
    t, c = recuit()
    print("=> Résultat :", affiche(t), "L =", c)
    print("(Même schéma avec 200 mouvements par palier :)")
    t, c = recuit(mouvements_par_palier=200, verbose=False)
    print("=> Résultat :", affiche(t), "L =", c)

    print("\n3) Algorithme génétique ")
    t, c = genetique()
    print("=> Résultat :", affiche(t), "L =", c)

    opt = optimum_exact()
    print("\nOptimum exact (énumération) :", affiche(opt), "L =", longueur(opt))