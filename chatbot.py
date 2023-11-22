import os

def list_of_files(directory, extension):
 
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

def affich_president(files_names):
    '''Affiche le nom des présidents sans doublon'''
    lst_tempo=[]
    str_tempo=""
    for e in files_names: 
        if '1' in e or '2' in e : 
            str_tempo=e[11:-5]
        else: 
            str_tempo=e[11:-4]
        if str_tempo not in lst_tempo: 
            lst_tempo.append(str_tempo)
    return lst_tempo

def trouve_prenom(nom):
    res=[]
    lst=['François Mitterrand','Jacques Chirac','Charles de Gaulle','Jules Grévy','Georges Pompidou','Valéry Giscard dEstaing','Nicolas Sarkozy','François Hollande','Emmanuel Macron']
    for e in nom:
        for j in lst:
            if e in j:
                res.append(j)
    return res

def lower_folder(entry_dir,exit_dir, files):
    '''Met en minsucule le contenu des fichiers txt du dossier entry_dir et les enregistre dans exit_dir
       "files" contient le nom des fichiers dans une liste'''
    if not os.path.exists('./'+exit_dir): #créer le dossier ./cleaned s'il n'existe pas
        os.makedirs('./'+exit_dir)
    for e in files: 
        f=open(entry_dir+'/'+e,'r')
        content=f.read()
        f.close()
        content_end=''
        for j in content: 
            char=ord(j)
            if 65<=char<=90:
                char+=32
            content_end+=chr(char)
        f2=open(exit_dir+'/'+e,'w')
        f2.write(content_end)
        f2.close()

def punctuation(directory,files):
    '''Supprime la ponctuation des fichiers du directoire "directory" (donner les nom de fichier dans la liste "files")'''
    for e in files: 
        f=open(directory+"/"+e,'r')
        content=f.read()
        f.close()
        ponctu='''!()[];:",<>./?%^&*'''
        for j in ponctu:
            content=content.replace(j,'')
        content=content.replace("'", ' ')
        content=content.replace('-',' ')
        f2=open(directory+"/"+e,'w')
        f2.write(content)
        f2.close()

def nb_occurences(s):
    '''Retourne un dictionnaire contenant tous les mots du texte et leurs nombres d'occurences'''
    dico={}
    s=s.split()
    for e in s:   
        if e not in dico:
            dico[e]=1
        else: 
            dico[e]+=1
    return dico

def tf(files_names):
    matrice={}
    for e in files_names:
        f=open('./cleaned/'+e,'r')
        matrice[e]=nb_occurences(f.read())
    return matrice


#def idf(directory):
    

directory = "./speeches"
files_names = list_of_files(directory, "txt")
noms=affich_president(files_names)
print(trouve_prenom(noms))
lower_folder(directory, "./cleaned",files_names)
punctuation("./cleaned", files_names)
a=(tf(files_names))
for e in a.values():
    print(e)