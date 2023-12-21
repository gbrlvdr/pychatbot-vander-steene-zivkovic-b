import os
import math
from fonctions import calcul_tf
def presence_mot_dans_idf(contenu, idf):
    """Retourne un dictionnaire indiquant la présence ou l'absence de chaque mot du contenu dans le dictionnaire IDF"""
    presence = {}
    for mot in contenu:
        if mot != "":
            presence[mot] = False
            if mot in idf:
                presence[mot] = True
    return presence

def inverser_matrice(matrice):
    """Retourne la matrice transposée de la matrice donnée en paramètre"""
    transposition = []
    ligne = matrice[0]
    for j in range(len(ligne)):
        transposition.append([])
    i = 0

    # Remplir la transposée avec les valeurs des lignes de la matrice originale
    for ligne in matrice:
        for j in range(len(ligne)):
            transposition[j].append(matrice[i][j])
        i += 1
    return transposition

def calculer_tf_idf_question(question, idf):
    """Calculer et retourner la matrice TF-IDF en fonction du TF de la question et de l'IDF de tous les mots dans le corpus"""
    matrice_tf_idf = []
    TF = calcul_tf(question)
    
    # Créer la matrice TF-IDF
    for mot in idf:
        matrice_tf_idf.append(round(TF[mot] * idf[mot] if mot in TF else 0.0, 2))
    return matrice_tf_idf

def produit_scalaire(vecteur_a, vecteur_b):
    """Calculer et retourner le produit scalaire entre deux vecteurs"""
    # Vérifier si les deux vecteurs ont la même dimension
    if len(vecteur_a) != len(vecteur_b):
        return "Erreur ! Les vecteurs A et B sont de dimensions différentes. Veuillez réessayer avec des vecteurs de même dimension."

    # Calculer la somme des produits des éléments correspondants des deux vecteurs
    somme_produits = 0
    for i in range(len(vecteur_a)):
        somme_produits += vecteur_a[i] * vecteur_b[i]

    return somme_produits

def calculer_norme(vecteur):
    """Calculer et retourner la norme d'un vecteur"""
    # Calculer la somme des carrés des éléments du vecteur
    somme_carres = 0
    for element in vecteur:
        somme_carres += element ** 2

    # Retourner la racine carrée de la somme des carrés
    return math.sqrt(somme_carres)

def calculer_similarite(matrice_a, matrice_b):
    """Calculer et retourner la similarité entre deux matrices en utilisant le produit scalaire"""
    similarite_resultat = []
    
    # Calculer la similarité pour chaque fichier
    for i in range(len(matrice_b)):
        produit_scalaire_val = produit_scalaire(matrice_a, matrice_b[i])
        norme_a = calculer_norme(matrice_a)
        norme_b = calculer_norme(matrice_b[i])
        
        if norme_a == 0 or norme_b == 0:
            similarite_resultat.append(0)
        else:
            similarite_resultat.append(produit_scalaire_val / (norme_a * norme_b))

    return similarite_resultat

def document_plus_pertinent(similarite_scores):
    """Retourne l'indice du document le plus pertinent selon les scores de similarité calculés"""
    if max(similarite_scores) == 0:
        return False
    for i in range(len(similarite_scores)):
        if similarite_scores[i] == max(similarite_scores):
            return i

def mot_plus_important(tf_idf, idf):
    """Retourne le mot le plus important dans la matrice TF-IDF avec son indice"""
    indice_max, valeur_max = 0, 0
    for i in range(len(tf_idf)):
        if tf_idf[i] > valeur_max:
            indice_max = i
            valeur_max = tf_idf[i]
    cles_idf = list(idf.keys())
    return cles_idf[indice_max]

def generer_reponse(question, idf, matrice_tf_idf, dossier_documents):
    matrice_question = calculer_tf_idf_question(question, idf)
    scores_similarite = calculer_similarite(matrice_question, matrice_tf_idf)
    indice_document_pertinent = document_plus_pertinent(scores_similarite)
    mot_important_dans_question = mot_plus_important(matrice_question, idf)

    print("")
    for fichier in os.listdir(dossier_documents):
        if fichier == os.listdir(dossier_documents)[indice_document_pertinent]:
            chemin_fichier = os.path.join(dossier_documents, fichier)
            with open(chemin_fichier, "r") as f:
                contenu_fichier = f.read().split(".")
                for i in range(len(contenu_fichier)):
                    if mot_important_dans_question in contenu_fichier[i]:
                        return contenu_fichier[i]