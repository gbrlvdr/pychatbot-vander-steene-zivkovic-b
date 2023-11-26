import os
import math

def list_of_files(directory, extension):
    '''
    Retourne une liste de noms de fichiers ayant l'extension spécifiée dans le répertoire donné.
    '''
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

def affich_president(files_names):
    '''
    Affiche le nom des présidents sans doublon à partir des noms de fichiers donnés.
    '''
    lst_tempo = []
    str_tempo = ""
    for e in files_names:
        if '1' in e or '2' in e:
            str_tempo = e[11:-5]
        else:
            str_tempo = e[11:-4]
        if str_tempo not in lst_tempo:
            lst_tempo.append(str_tempo)
    return lst_tempo

def trouve_prenom(nom):
    '''
    Retourne une liste des présidents correspondant aux noms donnés.
    '''
    res = []
    lst = ['François Mitterrand', 'Jacques Chirac', 'Charles de Gaulle', 'Jules Grévy', 'Georges Pompidou',
           'Valéry Giscard dEstaing', 'Nicolas Sarkozy', 'François Hollande', 'Emmanuel Macron']
    for e in nom:
        for j in lst:
            if e in j:
                res.append(j)
    return res

def lower_folder(entry_dir, exit_dir, files):
    '''
    Met en minuscule le contenu des fichiers txt du dossier entry_dir et les enregistre dans exit_dir.
    "files" contient le nom des fichiers dans une liste.
    '''
    if not os.path.exists('./' + exit_dir):  # Crée le dossier ./cleaned s'il n'existe pas
        os.makedirs('./' + exit_dir)
    for e in files:
        f = open(entry_dir + '/' + e, 'r')
        content = f.read()
        f.close()
        content_end = ''
        for j in content:
            char = ord(j)
            if 65 <= char <= 90:  # A <= char <= Z
                char += 32
            content_end += chr(char)
        f2 = open(exit_dir + '/' + e, 'w')
        f2.write(content_end)
        f2.close()

def punctuation(directory, files):
    '''
    Supprime la ponctuation des fichiers du répertoire "directory" (donner les noms de fichier dans la liste "files").
    '''
    for e in files:
        f = open(directory + "/" + e, 'r')
        content = f.read()
        f.close()
        ponctu = '''!()[];:",<>./?%^&*'''
        for j in ponctu:
            content = content.replace(j, '')
        content = content.replace("'", ' ')
        content = content.replace('-', ' ')
        f2 = open(directory + "/" + e, 'w')
        f2.write(content)
        f2.close()

def nb_occurences(s):
    '''
    Retourne un dictionnaire contenant tous les mots du texte et leurs nombres d'occurrences.
    '''
    dico = {}
    s = s.split()
    for mot in s:
        if mot not in dico:
            dico[mot] = 1
        else:
            dico[mot] += 1
    return dico

def calcul_tf(files_names):
    '''
    Retourne la matrice associant à chaque clé le nom du fichier et à chaque valeur le nombre d'occurrences de chaque mot dans chaque fichier.
    '''
    matrice = {}

    # Parcourir chaque fichier
    for e in files_names:
        with open('./cleaned/' + e, 'r') as f:
            # Utiliser un dictionnaire pour stocker le nombre d'occurrences de chaque mot dans le fichier
            occurrences = nb_occurences(f.read())
            matrice[e] = occurrences

    return matrice

def calcul_idf(matrice_mots):
    idf = {}
    nb_mots_fich = {}
    Nb_fich = len(matrice_mots)

    # Initialiser le dictionnaire IDF avec des fréquences nulles pour tous les mots
    for dico in matrice_mots.values():
        for mot in dico:
            nb_mots_fich[mot] = 0

    # Calculer le nombre de fichiers contenant chaque mot
    for dico in matrice_mots.values():
        for mot in dico:
            nb_mots_fich[mot] += 1

    # Calculer IDF pour chaque mot et fichier
    for nom_fich, dico in matrice_mots.items():
        idf_fich = {}
        for mot in dico:
            nb_fichiers_contenant_mot = nb_mots_fich[mot]
            idf_fich[mot] = math.log((Nb_fich / nb_fichiers_contenant_mot) + 1)
        idf[nom_fich] = idf_fich

    return idf

def calcul_tf_idf(tf, idf):
    '''
    Retourne la matrice TF-IDF où chaque ligne représente un mot et chaque colonne représente un document.
    '''
    matrice_tf_idf = {}

    # Parcourir la matrice TF
    for nom_fich, dico_tf in tf.items():
        dico_tf_idf = {}
        # Parcourir le dictionnaire TF pour chaque fichier
        for mot, freq_tf in dico_tf.items():
            # Récupérer la valeur IDF correspondante
            valeur_idf = idf[nom_fich][mot]
            # Calculer TF-IDF
            tf_idf = freq_tf * valeur_idf
            dico_tf_idf[mot] = tf_idf
        # Ajouter le dictionnaire TF-IDF pour ce fichier à la matrice finale
        matrice_tf_idf[nom_fich] = dico_tf_idf

    return matrice_tf_idf

def moyenne_scores_TF_IDF(tf_idf):
    """
    Calcule et retourne un dictionnaire contenant la moyenne des scores TF-IDF de chaque mot sur tous les fichiers.
    """
    moyenne_scores_par_mot = {}

    # Dictionnaire pour stocker le nombre de fichiers contenant chaque mot
    nb_fichiers_contenant_mot = {}

    # Parcourir la matrice TF-IDF
    for dico_tf_idf in tf_idf.values():
        # Parcourir le dictionnaire TF-IDF pour chaque fichier
        for mot, score in dico_tf_idf.items():
            # Mise à jour du nombre de fichiers contenant chaque mot
            nb_fichiers_contenant_mot[mot] = nb_fichiers_contenant_mot.get(mot, 0) + 1

            # Mise à jour de la somme des scores TF-IDF pour chaque mot
            moyenne_scores_par_mot[mot] = moyenne_scores_par_mot.get(mot, 0) + score

    # Calculer la moyenne pour chaque mot
    for mot, somme_scores in moyenne_scores_par_mot.items():
        moyenne_scores_par_mot[mot] = somme_scores / nb_fichiers_contenant_mot[mot]

    return moyenne_scores_par_mot


def mots_score_zero(moy_tfidf):
    """
    Retourne le tableau de tous les mots dont le score TF-IDF est de 0.
    """
    liste_finale=[]
    # Parcourir la matrice TF-IDF
    for mot, score in moy_tfidf.items():
        # Vérifier si le score est égal à 0
        if score < 0.5:
            liste_finale.append(mot)
    return liste_finale

def score_TF_IDF_max(moyennne_tfidf):
    max=0
    mot_max=''
    for mot,score in moyennne_tfidf.items():
        if score >= max :
            mot_max=mot
            max=score
    return mot_max

def mot_plus_repété(tf_idf, president):
    '''Retourne le mot le plus répété parmi les discours d'un président'''
    # Initialisation du score maximum à 0
    score_max = 0
    # Initialisation de la liste des mots les plus répétés
    mot_plus_repété = ""

    # Pour chaque fichier et son dictionnaire de scores TF-IDF
    for file_name, tfidf_scores in tf_idf.items():
        # Vérifier si le fichier correspond au président spécifié
        if president in file_name:
            # Pour chaque mot et son score TF-IDF dans le dictionnaire
            for mot, score in tfidf_scores.items():
                if score >= score_max:
                    score_max = score
                    mot_plus_repété = mot
    return mot_plus_repété

def parle_nation(tf_idf):
    noms=[]
    max=0
    nom_max=""
    for nom_pres, dico_score in tf_idf.items():
        for mot,score in dico_score.items():
            if mot=="nation":
                if score>=max:
                    max=score
                    if "1" in nom_pres or "2" in nom_pres:
                        nom_max=nom_pres[11:-5]
                        if nom_max not in noms:
                            noms.append(nom_max)
                    else: 
                        nom_max=nom_pres[11:-4]
                        if nom_max not in noms:
                            noms.append(nom_max)
                else:
                    if "1" in nom_pres or "2" in nom_pres:
                        if nom_pres[11:-5] not in noms :
                            noms.append(nom_pres[11:-5])
                    else: 
                        if nom_pres not in noms: 
                            noms.append(nom_pres[11:-4])
    return nom_max, noms

def mots_tous_presidents(tfidf, mots_score_zero=[]):
    '''Retourne les mots que tous les présidents ont dit dans leur discours'''
    dico_cpt={}
    liste_finale=[]
    presence_requise=len(tfidf)

    for dico_tfidf in tfidf.values():
        for mot in dico_tfidf.keys():
            if mot not in mots_score_zero:
                if mot not in dico_cpt:dico_cpt[mot]=1 #remplit le dictionnaire dico_cpt et incrémente pour qu'il contienne le nombre de documents où le mot apparait
                else: dico_cpt[mot]+=1

    for mot,nb_presence in dico_cpt.items():
        if nb_presence==presence_requise: #regarde si le mot apparait dans tous les fichiers et l'ajoute à la liste_finale si tel est le cas
            liste_finale.append(mot)
    return liste_finale