def écologie(files_names):
    '''
    Trouve le mot ecologie dans texte
    '''
    L=['écologie','climat']
    cont=9999999999999
    nom_pres=''
    for e in files_names:
        f = open('./cleaned/' + e, 'r')
        contenu=f.read()
        f.close()
        contenu=contenu.split()
        for i in range(len(contenu)):
            if contenu[i] in L:
                if i < cont:
                    nom_pres=e
                    cont=i
    if cont<9999999999999:
        return nom_pres, cont