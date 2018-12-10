import pandas as pd
from collections import OrderedDict

texte="""Souvent, pour s’amuser, les hommes d’équipage
Prennent des albatros, vastes oiseaux des mers,
Qui suivent, indolents compagnons de voyage,
Le navire glissant sur les gouffres amers.

À peine les ont-ils déposés sur les planches,
Que ces rois de l'azur, maladroits et honteux,
Laissent piteusement leurs grandes ailes blanches
Comme des avirons traîner à côté d'eux.

Ce voyageur ailé, comme il est gauche et veule !
Lui, naguère si beau, qu'il est comique et laid !
L'un agace son bec avec un brûle-gueule,
L'autre mime, en boitant, l'infirme qui volait !

Le Poète est semblable au prince des nuées
Qui hante la tempête et se rit de l'archer ;
Exilé sur le sol au milieu des huées,
Ses ailes de géant l'empêchent de marche"""

#texte = list(albatros) #mis en liste pour travailler sur les chaines de caracteres et les modifier
# "".join(texte) rétablit en texte

texte_low=texte.lower()

def remove_punctuation(chaine):
#faire docstring
    newchaine=''
    for caractere in chaine:
        if not (caractere in [',','.',':',';','!','=','+','-', '_', '/', '(', ')', "'",'"',"{","}"]):
            newchaine += caractere
    return newchaine

texte=remove_punctuation(texte_low)

dico={}



def prop_lettres(texte):
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

dico_prop = prop_lettres(texte)

tableau_prop = pd.DataFrame.from_dict(dico_prop)

print(tableau_prop)
