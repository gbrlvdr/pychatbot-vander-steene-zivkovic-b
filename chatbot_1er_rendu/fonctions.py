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
    if not os.path.exists(exit_dir):  # Crée le dossier s'il n'existe pas
        os.makedirs(exit_dir)
    for e in files:
        with open(os.path.join(entry_dir, e), 'r') as f:
            content = f.read()
        content_end = ''
        for j in content:
            char = ord(j)
            if 65 <= char <= 90:  # A <= char <= Z
                char += 32
            content_end += chr(char)
        with open(os.path.join(exit_dir, e), 'w') as f2:
            f2.write(content_end)

def punctuation(directory, files):
    '''
    Supprime la ponctuation des fichiers du répertoire "directory" (donner les noms de fichier dans la liste "files").
    '''
    for e in files:
        with open(os.path.join(directory, e), 'r') as f:
            content = f.read()
        ponctu = '''!()[];:\",<>./?%^&*'''
        for j in ponctu:
            content = content.replace(j, '')
        content = content.replace("'", ' ')
        content = content.replace('-', ' ')
        with open(os.path.join(directory, e), 'w') as f2:
            f2.write(content)

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

def calcul_tf(files_names, directory="./cleaned"):
    '''
    Retourne la matrice associant à chaque clé le nom du fichier et à chaque valeur le nombre d'occurrences de chaque mot dans chaque fichier.
    '''
    matrice = {}

    # Parcourir chaque fichier
    for e in files_names:
        with open(os.path.join(directory, e), 'r') as f:
            contenu = f.read()
        occurrences = nb_occurences(contenu)
        #nb_mots=len(contenu.split())
        for mot,occ in occurrences.items():
            occurrences[mot]=occ
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
            idf_fich[mot] = math.log((Nb_fich / nb_fichiers_contenant_mot))
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
        if score == 0.0:
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

def écologie(files_names, directory="./cleaned"):
    '''
    Trouve le mot ecologie dans texte
    '''
    L=['écologie','climat']
    cont=9999999999999
    nom_pres=''
    for e in files_names:
        with open(os.path.join(directory, e), 'r') as f:
            contenu = f.read()
        contenu=contenu.split()
        for i in range(len(contenu)):
            if contenu[i] in L:
                if i < cont:
                    nom_pres=e
                    cont=i
    if cont<9999999999999:
        return nom_pres, cont

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

#### Partie 2

def tokenize_question(text) :
    # convertit texte en lettre minuscule
    tokenized_text = text.lower()

    # enleve la ponctuation
    ponctu = '''!()[];:",<>./?%^&*'''
    for j in ponctu:
        tokenized_text = tokenized_text.replace(j, '')
    tokenized_text = tokenized_text.replace("'", ' ')
    tokenized_text = tokenized_text.replace('-', ' ')

    # convertit le texte en str dans une liste
    return tokenized_text.split()

def norme(A) :
    s = 0
    for i in range(len(A)) :
        s += A[i]**2
    s = math.sqrt(s)
    return s

def prod_scal(A, B):
    sommeAB = 0
    for i in range(len(A)):
        sommeAB += A[i]*B[i]
    return sommeAB


def similarite(A, B) :
    sc = prod_scal(A, B)
    div = norme(A) * norme(B)
    if div != 0 :
        sc /= div
        return sc
    sc = 0
    return sc

def pertin(tfidf, TFIDF_qu, files) :
    max=0
    for i in range(len(tfidf)):
        a=similarite(tfidf[i],TFIDF_qu)
        if a>=max:
            max=a
            nom=files[i]
    return nom
