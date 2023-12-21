import math
import os 
from fonctions import *

# Initialisations des variables nécessaires

directory = "./speeches"
files_names = list_of_files(directory, "txt")
noms = affich_president(files_names)
lower_folder(directory, "./cleaned", files_names)
punctuation("./cleaned", files_names)
tf = calcul_tf(files_names)
idf=calcul_idf(tf)
tf_idf=calcul_tf_idf(tf,idf)
moy_tfidf=moyenne_scores_TF_IDF(tf_idf)
mots_zero=mots_score_zero(moy_tfidf)
print(tf_idf)
print("Bonjour, bienvenue dans le ChatBot. Voici les touches à utiliser pour accéder aux fonctions :\n","Appuyer sur 1 pour afficher la liste des mots les moins importants dans le corpus de documents\n","Appuyer sur 2 pour afficher le mot ayant le score TD-IDF le plus élevé")
print("Appuyer sur 3 pour indiquer le mot le plus répété par un président Chirac\n", "Appuyer sur 4 pour indiquer le nom du président qui a parlé de la « Nation » et celui qui l’a répété le plus de fois")
print("Appuyer sur 5 pour indiquer le premier président à parler du climat et/ou de l’écologie\n", "Appuyer sur 6 pour afficher les mots que tous les présidents ont évoqués.")


continuer='o'
while continuer!='n': 
    action=int(input("Action à faire : "))
    while not 0<=action<=6:
        action=int(input("Action à faire : "))
    if action == 1:
        print("Voici la liste des mots les moins importants :", mots_score_zero(moy_tfidf))
    elif action==2: 
        print("Voici le mot dont le score TF-IDF est le plus élevé :", score_TF_IDF_max(moy_tfidf))
    elif action==3: 
        print(mot_plus_repété(tf_idf, input("Saisir le nom du président pour lequel vous souhaitez connaître le mot le plus répété : ")))
    elif action==4: 
        res=parle_nation(tf_idf)
        print('Le président qui a le plus dit le mot "Nation" est',res[0],'et la liste des présidents qui ont parlé de "Nation" sont :', res[1])
    elif action==5: 
        print(écologie(files_names))
    else:
        print("Les mots dits par tous les présidents sont :",mots_tous_presidents(tf_idf,mots_zero))
    continuer=input("\nSouhaitez vous continuer à utiliser le programme ? taper \"n\" pour arrêter et n'importe quelle autre touche pour continuer : ")