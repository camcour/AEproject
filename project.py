import pandas as pd
from collections import OrderedDict
import matplotlib.pyplot as plt
import glob
import string
import re


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

dico_de_textes_fr = {}
dico_de_textes_an = {}
titres_des_poemes_fr = []
titres_des_poemes_an = []

for recueil in recueils_deux_langues:
    for poeme in recueil:
        texte_simplifie = simplifie_textes(poeme)
        dico_prop = proportion_lettres(texte_simplifie)
        if recueil == poemes_francais:
            dico_de_textes_fr[poeme]= dico_prop
            titres_des_poemes_fr.append(poeme)
        if recueil == poemes_anglais:
            dico_de_textes_an[poeme]= dico_prop
            titres_des_poemes_an.append(poeme)


dico_de_texte_inc = {}

for inconnu in textes_test:
    texte_simplifie = simplifie_textes(inconnu)
    taille_texte = len(texte_simplifie)
    dico_de_texte_inc[inconnu]= proportion_lettres(texte_simplifie)

tableau_prop_fr = pd.DataFrame()
tableau_prop_an = pd.DataFrame()
tableau_prop_inc=pd.DataFrame()

for poeme, distrib in dico_de_textes_fr.items(): #changer le nom des lignes
    tableau_prop_fr =pd.concat([tableau_prop_fr,pd.DataFrame(distrib)]) #ne sert pas de mettre index=titres parce que les refait a chaque fois

for poeme, distrib in dico_de_textes_an.items():
    tableau_prop_an =pd.concat([tableau_prop_an,pd.DataFrame(distrib)])

for poeme, distrib in dico_de_texte_inc.items():
    tableau_prop_inc =pd.concat([tableau_prop_inc,pd.DataFrame(distrib)])

#print(tableau_prop_fr)
print('tableau moyennes francais')
tableau_moy_fr = tableau_prop_fr.mean(axis=0)
print(tableau_moy_fr)
dict_moy_fr= tableau_moy_fr.to_dict()
df_fr=pd.DataFrame(dict_moy_fr,index=['fr'])

print('tableau moy ang')
tableau_moy_an = tableau_prop_an.mean(axis=0)
print(tableau_moy_an)
dict_moy_an = tableau_moy_an.to_dict()
df_an = pd.DataFrame(dict_moy_an,index=['an'])

tableau_moy_inc=tableau_prop_inc.mean(axis=0)
dict_moy_inc= tableau_moy_inc.to_dict()
df_inc=pd.DataFrame(dict_moy_inc,index=['inc'])
print(tableau_moy_inc)

print('corr tout')
inc_vs_ref=[df_inc, df_fr, df_an]
tableau_moyennes_fr_an_inc=pd.concat(inc_vs_ref).transpose()
print(tableau_moyennes_fr_an_inc) #tranpose pour bien aller avec le sens de corr
print(tableau_moyennes_fr_an_inc['fr'].corr(tableau_moyennes_fr_an_inc['inc'])) #donne le coefficient de correlation entre les colonnes
print(tableau_moyennes_fr_an_inc['an'].corr(tableau_moyennes_fr_an_inc['inc']))

#VERIFIER QUE CE SONT LES BONNES VALEURS PARCE QUE CORRELATION DANS LE MAUVAIS SENS




#tableau_moyennes_fr_inc= pd.concat([tableau_moyennes_fr_inc,tableau_prop_inc])
#tableau_moyennes_fr_inc= pd.concat([tableau_moyennes_fr_inc,tableau_moy_fr])




#dico_de_moy_ref={'fr':[tableau_moy_fr],
#                 'an': [tableau_moy_an],
#                 'inc': [tableau_prop_inc]}
#for tableau, moyenne in dico_de_moy_ref.items():
#    tableau_moyennes_fr_inc = pd.concat([tableau_moyennes_fr_inc,pd.DataFrame(moyenne)])
#tableau_de_moy = pd.DataFrame.from_dict(dico_de_moy_ref)
#print(tableau_de_moy )#!!!! trop naze)

#EST CE QUE C'EST MIEUX??

tableau_prop= pd.DataFrame()
tableau_moy= pd.DataFrame()

liste_de_dico_de_textes=(dico_de_textes_fr, dico_de_textes_an, dico_de_texte_inc)

for dico in liste_de_dico_de_textes:

    if dico == dico_de_textes_fr:
        tableau_prop = tableau_prop_fr
        tableau_moy = tableau_moy_fr
    if dico == dico_de_textes_an:
        tableau_prop = tableau_prop_an
        tableau_moy = tableau_moy_an
    if dico == dico_de_texte_inc:
        tableau_prop = tableau_prop_inc
        tableau_moy = tableau_prop_inc

    for poeme, distrib in dico_de_textes_fr.items(): #changer le nom des lignes
        tableau_prop =pd.concat([tableau_prop,pd.DataFrame(distrib)])

#POUR COMPARER AVEC MATRICE DISTANCE EUCLIDIENNE This is an old question, but there is a Scipy function that does this:

tableau_moyennes_compar=pd.DataFrame()


#tableau_moyennes_compar= pd.concat([tableau_moyennes_ref,tableau_prop_inc])
#print(tableau_moyennes_compar)

from scipy.spatial.distance import pdist, squareform



## FIN

#tableau_prop_inc = pd.DataFrame.from_dict(dico_de_texte_inc)
#print('tableau prop texte inconnu')

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
