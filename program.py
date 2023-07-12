grille_taux = [
    # années, taux
    (12.0, 2.9),
    (15.0, 3.2),
    (20.0, 3.8),
    (22.0, 3.8),
    (25.0, 4.4)
]
    
def main():
    emprunt = 160000.0
    duree = grille_taux[4][0] * 12
    taux = grille_taux[4][1] / 100 / 12

    # Pour un pret simple
    mensualite = mensualite_classique(emprunt, taux, duree)
    interets = calcul_interets(taux, duree, emprunt, mensualite)
    interets_bis = calcul_interets_bis(taux, duree, emprunt, mensualite)

    print(f'Pour un pret simple d\'un montant de {emprunt} sur une durée de {duree / 12} ans à un taux de {taux * 100 * 12}% :')
    print(f'Mensualité : {mensualite}')
    print(f'Interets par soustraction : {interets}')
    print(f'Interets par addition : {interets_bis} \n')

    # Calcul du ratio
    taux1 = grille_taux[0][1] / 100 / 12
    duree1 = grille_taux[0][0] * 12
    taux2 = grille_taux[3][1] / 100 / 12
    duree2 = grille_taux[3][0] * 12
    r = ratio(taux1, duree1, taux2, duree2)
    print(f'taux1 = {taux1 * 100 * 12}% \n duree1 = {duree1 / 12} ans \n taux2 = {taux2 * 100 * 12}% \n duree2 = {duree2 / 12} ans')
    print(f'Le ratio est : {r} \n')

    # Optimisation du pret gigogne
    best_interets, best_montant1, best_duree1 = optimisation_gigogne(duree, emprunt)
    print('Pour un pret gigogne optimisé :')
    print(f'Les plus faibles interets sont de : {best_interets}')
    print(f'Pour un montant de ligne 1 de : {best_montant1}')
    print(f'Pour un duree de ligne 1 de : {best_duree1} mois, soit {best_duree1 / 12} ans')

    return

def calcul_interets(taux, mois, montant, mensualite):
    interets = mensualite * mois - montant
    return interets

def calcul_interets_bis(taux, mois, montant, mensualite):
    interets = 0
    if mois == 0 : 
        interets += montant * taux
    else :
        interets = interets + montant * taux
        montant -= (mensualite - montant * taux)
        mois -= 1
        interets += calcul_interets_bis(taux, mois, montant, mensualite)
    return interets

def ratio(taux1, duree1, taux2, duree2):
    # Chercher le meilleur ratio entre ligne 1 et ligne 2
    # Le premier mois, la mensualité lissée ne rembourse que les intérêts de la ligne longue (ligne 2)
    
    pt2d2 = p(taux2, duree2)
    pt1d1 = p(taux1, duree1)
    pt2d1 = p(taux2, duree1)

    a = pt2d2 - taux2 
    b = pt1d1 - ((pt1d1 * pt2d2) / pt2d1)
    c = a / b
    r = c / (1 + c)

    return r

def p(t, d):
    result = t / (1 - (1+t)**(-d))
    return result

def mensualite_classique(montant, taux, duree):
    m = montant * p(taux, duree)
    return m

def mensualite_lissee(montant1, taux1, duree1, montant2, taux2, duree2):
    mensualite1 = mensualite_classique(montant1, taux1, duree1)
    m = (montant2 + mensualite1 / p(taux2, duree1)) * p(taux2, duree2)
    return m

def interets_gigogne(montant1, taux1, duree1, montant2, taux2, duree2):
    i = mensualite_lissee(montant1, taux1, duree1, montant2, taux2, duree2) * duree2 - (montant1 + montant2)
    return i

def optimisation_gigogne(duree, montant):
    # Recherche du taux pour la ligne longue
    taux2 = 0
    for ligne in grille_taux:
        if ligne[0] * 12 == duree:
            taux2 = ligne[1] / 100 / 12
    if taux2 == 0:
        return 1

    # variables pour les résultats
    best_interets = 0
    best_montant1 = 0
    best_duree1 = 0

    # Pour chaque duréee de ligne 1 depuis la grille de taux
    for i in range(len(grille_taux)):
        duree1 = grille_taux[i][0] * 12 
        if duree > duree1:
            taux1 = grille_taux[i][1] / 100 / 12
        else:
            return best_interets, best_montant1, best_duree1
        
        # Montant max de la ligne 1
        montant_max = ratio(taux1, duree1, taux2, duree) * montant
        montant_max_int = int(round(montant_max))

        # Pour chaque montant de 0 au montant max déterminé grace au ratio.
        for j in range(0, montant_max_int):
            a = interets_gigogne(j, taux1, duree1, (montant - j), taux2, duree)
            if best_interets == 0:
                best_interets = a
                best_montant1 = j
                best_duree1 = duree1
            elif a < best_interets:
                best_interets = a
                best_montant1 = j
                best_duree1 = duree1

    return best_interets, best_montant1, best_duree1

main()