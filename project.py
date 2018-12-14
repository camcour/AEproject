import pandas as pd
from collections import OrderedDict
import matplotlib.pyplot as plt
import glob


#texte = list(albatros) #mis en liste pour travailler sur les chaines de caracteres et les modifier
# "".join(texte) rétablit en texte



def remove_punctuation(chaine):
#faire docstring
    newchaine=''
    for caractere in chaine:
        if not (caractere in [',','.',':',';','!','?','=','+','-', '_', '/', '(', ')', "'",'"',"{","}", '<', '>', '\n',]):
            newchaine += caractere
    return newchaine

dico={}
def proportion_lettres(texte_lettres):
#faire docstring donne la proportion de chaque lettre dans le texte, et retourne un dictionnaire
    for lettre in texte:
        if lettre in ['à','â']:
            lettre = 'a'
        if lettre in ['è','é','ê','ë']:
            lettre = 'e'
        if lettre in ['ô','ö']:
            lettre ='o'
        if lettre in ['î', 'ï']:
            lettre = 'i'
        if lettre in ['û','ü']:
            lettre = 'u'
        dico[lettre] = [(texte.count(lettre))/len(texte)]
    return dico


poemes_anglais = glob.glob('Dickinson/*.txt')
poemes_francais = glob.glob('Apollinaire/*.txt')

#un peu inutile comme on a mis les textes dans un fichier; à modifier
#print ('est-ce un texte à tester? (y/n)')
#rep_test= input()
#if rep_test == 'y':
#    print('ok testons le') #faire suite
#else:
#    print('les textes pour enregistrer des données sont-il francais ou anglais? (f/a)')
#    rep_langue= input()
#    if rep_langue == 'f':
#        poemes = poemes_francais
#    if rep_langue == 'a':
#        poemes = poemes_anglais


dico_de_textes={}

for poeme in poemes_francais:
    with open (poeme) as t:
        texte = t.read()
        texte_low = texte.lower()
        texte_lettres = remove_punctuation(texte_low)#jusqu'ici ok mais apres compte des majuscules
        dico_prop = proportion_lettres(texte_lettres)# puis met les mproportions du dernier texte pour tous les textes dans le dico_de_textes, 
        dico_de_textes['{}'.format(poeme)]= dico_prop


#print(dico_de_textes)
tableau_prop = pd.DataFrame.from_dict(dico_de_textes)
#print(tableau_prop)
