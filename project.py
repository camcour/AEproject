import pandas as pd
from collections import OrderedDict
import re
import glob
import random

def simplifie_textes(texte_brut):
#fonction qui pour un texte brut en entrée, le lit, le rend minuscule et lui enlève toute ponctuation, ce qu'il retourne
    with open (texte_brut) as t:
        texte = t.read()
        texte_low = texte.lower()
        texte_lettres = re.sub(r'[^a-z]','',texte_low)
    return texte_lettres

def proportion_lettres(texte_lettres):
#fonction qui trouve la proportion de chaque lettre dans un texte donné en entrée, et retourne ces proportions dans un dictionnaire
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

def attribue_proportion (ensemble_de_textes):
#fonction qui pour un texte, ou un ensemble de textes en entrée, retourne un dictionnaire contenant les proportions des lettres dans chaque texte
    dico_prop={}
    dico_de_texte ={}
    tableau_prop_textes = pd.DataFrame()

    for texte_brut in ensemble_de_textes:
        texte_simplifie = simplifie_textes(texte_brut)
        dico_prop = proportion_lettres(texte_simplifie) #voir si on peut combiner les deux lignes
        dico_de_texte[texte_brut]= dico_prop

    for texte, distrib in dico_de_texte.items():
        tableau_prop_textes =pd.concat([tableau_prop_textes,pd.DataFrame(distrib)], sort=True)
    return tableau_prop_textes

def attribue_moyennes (tableau_prop_textes, index):
#prend un dictionnaire de textes en entrée et retourne un dictionnaire contenant les moyennes de fréquences de lettres
    dico_moyennes = tableau_prop_textes.mean(axis=0).to_dict()
    tableau_moyennes = pd.DataFrame(dico_moyennes,index=[index])
    return tableau_moyennes

poemes_anglais = glob.glob('Dickinson/*.txt')
poemes_francais = glob.glob('Apollinaire/*.txt')

textes_test_anglais = glob.glob('test_Anglais/*.txt')
textes_test_francais = glob.glob('test_Francais/*.txt')

que_tester = random.choice([ textes_test_anglais, textes_test_francais])
un_texte_inconnu = [random.choice(que_tester)]

recueils_deux_langues= [poemes_francais, poemes_anglais]

for recueil in recueils_deux_langues:
    if recueil == poemes_francais:
        tableau_prop_fr = attribue_proportion(poemes_francais)
        tableau_fr = attribue_moyennes(tableau_prop_fr, 'fr')
    if recueil == poemes_anglais:
        tableau_prop_an = attribue_proportion(poemes_anglais)
        tableau_an = attribue_moyennes(tableau_prop_an, 'an')

tableau_prop_inc= attribue_proportion(un_texte_inconnu)
tableau_prop_inc.rename(index={0:'inc'}, inplace=True)

print('Le texte testé est', un_texte_inconnu)
print('Il possède ', len(simplifie_textes(un_texte_inconnu[0])), 'lettres.', '\n')

tableau_moyennes_fr_an_inc=pd.concat([tableau_prop_inc, tableau_fr, tableau_an], sort=True).transpose() #tranpose() par souci d'esthétique, et pour bien aller avec le sens de corr
tableau_moyennes_fr_an_inc.rename(index={0:'inc'})
print("Tableau de fréquences d'apparition des lettres dans le texte à tester, et les moyennes de fréquence par langue")
print(tableau_moyennes_fr_an_inc, '\n')

correlation_fr_inc = tableau_moyennes_fr_an_inc['fr'].corr(tableau_moyennes_fr_an_inc['inc'])
correlation_an_inc = tableau_moyennes_fr_an_inc['an'].corr(tableau_moyennes_fr_an_inc['inc'])
print('correlation francais/inconnu:', correlation_fr_inc)
print('correlation anglais/inconnu:', correlation_an_inc, '\n')

#PHASE DE TEST

if (correlation_fr_inc > correlation_an_inc) and que_tester == textes_test_francais:
    print("Le texte semble être francais, et c'est vrai!")
elif (correlation_fr_inc > correlation_an_inc) and que_tester == textes_test_anglais:
    print ("Le texte semble être francais, mais malheureusement il ne l'est pas.")

if (correlation_an_inc > correlation_fr_inc) and que_tester == textes_test_anglais:
    print("Le texte semble être anglais, et c'est vrai!")
elif (correlation_an_inc > correlation_fr_inc) and que_tester == textes_test_francais:
    print ("Le texte semble être anglais, mais malheureusement il ne l'est pas.")
