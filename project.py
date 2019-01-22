import pandas as pd
from collections import OrderedDict
import re
import glob
import random

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

textes_test_anglais = glob.glob('test_Anglais/*.txt')
textes_test_francais = glob.glob('test_Francais/*.txt')

que_tester = random.choice([ textes_test_anglais, textes_test_francais])
un_texte_inconnu = [random.choice(que_tester)]

recueils_deux_langues= [poemes_francais, poemes_anglais]

dico_de_textes_fr = {}
dico_de_textes_an = {}
titres_des_poemes_fr = []
titres_des_poemes_an = []

def attribue_proportion (ensemble_de_textes):
#faire docsting
    dico_prop={}
    dico_de_texte ={}
    for texte_brut in ensemble_de_textes:
        texte_simplifie = simplifie_textes(texte_brut)
        dico_prop = proportion_lettres(texte_simplifie) #voir si on peut combiner les deux lignes
        dico_de_texte[texte_brut]=dico_prop
    return dico_de-texte

def dico_moyennes (dico_de_texte):
#faire docstring
    tableau_prop = pd.DataFrame()
    for texte, distrib in dico_de_texte.items():
        tableau_prop =pd.concat([tableau_prop, pd.DataFrame(distrib)])
    dico_moyennes = tableau_prop.mean(axis=0).to_dict()
    return dico_moyennes



for recueil in recueils_deux_langues:
    #if recueil == poemes_francais:
    #    dico_de_textes_fr_test={}
    #    dico_de_textes_fr_test = attribue_proportion(poeme, recueil)
    #if recueil == poemes_anglais:
    #    dico_de_textes_an_test={}
    #    dico_de_textes_an_test=  attribue_proportion(poeme, recueil)

    #if recueil == inconnu:
            #prend un texte au hasard dans la liste des textes inconnu
    #    dico_de_texte_inc_test = attribue_proportion(poeme, recueil)

    #apres ca c'est ok, juste avant et apres les deux points qui suivent recueils deux langues c'est un test
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

for inconnu in un_texte_inconnu:
    texte_simplifie = simplifie_textes(inconnu)
    taille_texte = len(texte_simplifie)
    dico_de_texte_inc[inconnu]= proportion_lettres(texte_simplifie)

tableau_prop_fr = pd.DataFrame()
tableau_prop_an = pd.DataFrame()
tableau_prop_inc=pd.DataFrame()

for poeme, distrib in dico_de_textes_fr.items(): #changer le nom des lignes
    tableau_prop_fr =pd.concat([tableau_prop_fr,pd.DataFrame(distrib)], sort=True) #ne sert pas de mettre index=titres parce que les refait a chaque fois

for poeme, distrib in dico_de_textes_an.items():
    tableau_prop_an =pd.concat([tableau_prop_an,pd.DataFrame(distrib)], sort=True)

for poeme, distrib in dico_de_texte_inc.items():
    tableau_prop_inc =pd.concat([tableau_prop_inc,pd.DataFrame(distrib)], sort=True)


dict_moy_fr = tableau_prop_fr.mean(axis=0).to_dict()
#tableau_moy_fr = tableau_prop_fr.mean(axis=0)
#dict_moy_fr= tableau_moy_fr.to_dict()
df_fr=pd.DataFrame(dict_moy_fr,index=['fr'])

dict_moy_an = tableau_prop_an.mean(axis=0).to_dict()
df_an = pd.DataFrame(dict_moy_an,index=['an'])

dict_moy_inc=tableau_prop_inc.mean(axis=0).to_dict()
df_inc = pd.DataFrame(dict_moy_inc,index=['inc'])

print('Le texte testé était', inconnu, '\n')

print("tableau de correlation entre les fréquences d'apparition des lettres par langue, et celles du texte à tester ")
tableau_moyennes_fr_an_inc=pd.concat([df_inc, df_fr, df_an], sort=True).transpose()
print(tableau_moyennes_fr_an_inc, '\n') #tranpose pour bien aller avec le sens de corr

correlation_fr_inc = tableau_moyennes_fr_an_inc['fr'].corr(tableau_moyennes_fr_an_inc['inc']) #donne le coefficient de correlation entre les colonnes
correlation_an_inc = tableau_moyennes_fr_an_inc['an'].corr(tableau_moyennes_fr_an_inc['inc'])
print('correlation francais/inconnu:',correlation_fr_inc) #donne le coefficient de correlation entre les colonnes
print('correlation anglais/inconnu:', correlation_an_inc, '\n')


#PHASE DE TEST


if (correlation_fr_inc > correlation_an_inc) and que_tester == textes_test_francais:
    print("Il semble être francais, et c'est vrai!")
elif (correlation_fr_inc > correlation_an_inc) and que_tester == textes_test_francais:
    print ("Il semble être francais, mais malheureusement il ne l'est pas")

if (correlation_an_inc > correlation_fr_inc) and que_tester == textes_test_anglais:
    print("Il semble être anglais, et c'est vrai!")
elif (correlation_fr_inc > correlation_an_inc) and que_tester == textes_test_anglais:
    print ("Il semble être anglais, mais malheureusement il ne l'est pas")




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

#for dico in liste_de_dico_de_textes:

#    if dico == dico_de_textes_fr:
#        tableau_prop = tableau_prop_fr
#        tableau_moy = tableau_moy_fr
#    if dico == dico_de_textes_an:
#        tableau_prop = tableau_prop_an
#        tableau_moy = tableau_moy_an
#    if dico == dico_de_texte_inc:
#        tableau_prop = tableau_prop_inc
#        tableau_moy = tableau_prop_inc

#    for poeme, distrib in dico_de_textes_fr.items(): #changer le nom des lignes
#        tableau_prop =pd.concat([tableau_prop,pd.DataFrame(distrib)], sort=True)



#PHASE DE TEST


if que_tester == textes_test_anglais :
    anglais = True
    francais = False
if que_tester == textes_test_francais :
    anglais = False
    francais = True


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
