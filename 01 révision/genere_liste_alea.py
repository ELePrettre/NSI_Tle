import random

def genere_liste_aleatoire(N, n):
    """Génére une liste aléatoire de N éléments compris entre 0 et n"""
    # Créer une liste vide pour accueillir les nombres
    data = []
    # ajoute les éléments aléatoires dans la liste
    for i in range(N):
        data.append(random.randrange(n))
    return data

if __name__ == '__main__':
    # Création d'une liste de 5 valeurs comprises entre 0 et 20 à trier
    data = genere_liste_aleatoire(5, 20)
    print("Liste initiale: ", data)

