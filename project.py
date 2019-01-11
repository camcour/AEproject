import pandas as pd
from collections import OrderedDict
import matplotlib.pyplot as plt
import glob
import string
import re

#texte = list(albatros) #mis en liste pour travailler sur les chaines de caracteres et les modifier
# "".join(texte) rétablit en texte


def proportion_lettres(texte_lettres):
#faire docstring donne la proportion de chaque lettre dans le texte, et retourne un dictionnaire
    dico_prop={}
    for lettre in texte_lettres:
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
        dico_prop[lettre] = [(texte_lettres.count(lettre))/len(texte_lettres)]
    return dico_prop


def simplifie_textes(texte_brut):
#faire une docstring: prend un texte brut, le lie, le rend minuscule et lui enlève toute ponctuation
    with open (texte_brut) as t:
        texte = t.read()
        texte_low = texte.lower()
        texte_lettres = re.sub(r'[^a-z]','',texte_low)
    return texte_lettres


poemes_anglais = glob.glob('Dickinson/*.txt')
poemes_francais = glob.glob('Apollinaire/*.txt')
textes_test = glob.glob('Testables/*.txt')

recueils_deux_langues= [poemes_francais, poemes_anglais]

dico_de_textes_fr={}
dico_de_textes_an={}

for recueil in recueils_deux_langues:
    for poeme in recueil:
        texte_simplifie = simplifie_textes(poeme)
        dico_prop = proportion_lettres(texte_simplifie)
        if recueil== poemes_francais:
            dico_de_textes_fr[poeme]= dico_prop
        if recueil== poemes_anglais:
            dico_de_textes_an[poeme]= dico_prop

tableau_prop_fr = pd.DataFrame()
tableau_prop_an = pd.DataFrame()


for poeme, distrib in dico_de_textes_fr.items():
    #changer le nom des lignes
    tableau_prop_fr=pd.concat([tableau_prop_fr,pd.DataFrame(distrib)])

for poeme, distrib in dico_de_textes_an.items():
    tableau_prop_an=pd.concat([tableau_prop_an,pd.DataFrame(distrib)])

print("Voici un tableau avec les proportions de lettres pour une base de textes français,puis les moyennes d'apparitions de chaque lettre")
print(tableau_prop_fr)
print(tableau_prop_fr.mean(axis=0))

print("Voici un tableau avec les proportions de lettres pour une base de textes anglais, puis les moyennes d'apparitions de chaque lettre")
print(tableau_prop_an)
print(tableau_prop_an.mean(axis=0)) 


dico_de_texte_inc = {}

for inconnu in textes_test:
    texte_simplifie = simplifie_textes(poeme)
    dico_prop = proportion_lettres(texte_simplifie)
    taille_texte = len(texte_simplifie)
    dico_de_texte_inc[inconnu]= dico_prop

tableau_prop_inc = pd.DataFrame.from_dict(dico_de_texte_inc)
print(tableau_prop_inc)



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



def remove_punctuation(chaine):
#faire docstring
    newchaine=''
    for caractere in chaine:
        if not (caractere in [',','.',':',';','!','?','=','+','-', '_', '/', '(', ')', "'",'"',"{","}", '<', '>', '\n',' ']): #probleme parce que \n est deux caracteress:
        #or in string.punctuation
            newchaine += caractere
    return newchaine
