# Automatic classifier

Ce projet suit une idée dont vous avez donnée lors de ce cours: créer un programme qui permettrait d'identifier si un texte est de langue français ou anglaise.
Pour se faire, le programme ainsi créé se base sur des statistiques d'apparition de chaque lettre de l'alphabet dans le(s) texte(s). Le programme que j'ai ainsi créé permet d'en faire le test, sur des mots, des phrases, des paragraphes et des documents entiers. Ce test est établi par une validation croisée: les textes servant de référence par langue, et les textes testés sont bien différents.

  ## Préparation des textes à évaluer

  Avant d'évaluer des textes, que ce soit pour créer les références de proportion par langue, ou que ce soit pour tester un               texte, j'ai décidé de préparer chaque texte afin d'enlever toute ponctuation et toute difference de casse
  J'ai ainsi créé une fonction qui lit un texte selectionné, et enlève les ponctuations (y compris les espaces).

    def simplifie_textes(texte_brut):
    #fonction qui pour un texte brut en entrée, le lit, le rend minuscule
    #et lui enlève toute ponctuation, ce qu'il retourne
        with open(texte_brut) as t:
            texte = t.read()
            texte_low = texte.lower()
            texte_lettres = re.sub(r'[^a-z]', '', texte_low)
        return texte_lettres

  ### Calcul des proportions de chaque lettre dans un texte

  La prochaine étape était alors de calculer pour le texte ainsi simplifié la propotion d'apparition de chaque lettre dans le texte. J'ai pris alors la décision de répertorier les fréquences des 26 lettres de l'alphabet, sans prendre en compte les caractères accentués (auxquels auraient pu être associés des fréquences propres). 
  Ne pas prendre en compte l'accentuation m'a semblé intéressant pour pouvoir travailler autour des porportions de lettres simples dans les textes, et ne pas jouer sur l'absence d'accentuation en anglais, qui aurait facilité la tâche de classification.
  La foncion créée à cette fin retourne ainsi un dictionnaire, dans lequel la fréquence d'apparition de chaque lettre est attribué à la lettre notée dans une clé du dictionnaire.
  
    def proportion_lettres(texte_lettres):
    #fonction qui trouve la proportion de chaque lettre dans un texte donné
    # en entrée, et retourne ces proportions dans un dictionnaire
      dico_prop = {}
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
          dico_prop[lettre] = [(texte_lettres.count(lettre)) / len(texte_lettres)]
      return dico_prop
      
  ### Attribution de proportions à plusieurs textes en une fois
  
  Il a été ensuite question d'évaluer un ensemble de textes, d'attribuer à chacun des textes les proportions d'apparition de lettres, et d'ordonner ces données.
  J'ai alors crée une fonction qui prend un texte ou un ensemble de textes, le(s) simplifie et attribue à chaque texte les frèquences d'apparition des textes. Cela a été fait de telle sorte à obtenir toutes ces données visibles dans un dataframe. 
  Cela permet si souhaité de voir d'un coup d'oeil les fréquences des lettres de chaque texte évalué, mais aussi d'ordonner les données pour une future et simple analyse statistiques des données presentes dans le tableau. 
  Ainsi, j'ai fait une deuxième fonction, qui peut grâce à ce dataframe, calculer les moyennes de frequences de textes, relativement à l'ensemble de textes duquel le dataframe a été créé. 
  
  
    def attribue_proportion(ensemble_de_textes):
    #fonction qui pour un texte, ou un ensemble de textes en entrée,
    #retourne un tableau contenant les proportions des lettres dans chaque texte
      dico_prop = {}
      dico_de_texte = {}
      tableau_prop_textes = pd.DataFrame()

      for texte_brut in ensemble_de_textes:
          texte_simplifie = simplifie_textes(texte_brut)
          dico_prop = proportion_lettres(texte_simplifie)
          dico_de_texte[texte_brut]= dico_prop

      for texte, distrib in dico_de_texte.items():
          tableau_prop_textes = pd.concat([tableau_prop_textes,
                                         pd.DataFrame(distrib, index =[texte])],
                                        sort = True)
      return tableau_prop_textes



    def attribue_moyennes(tableau_prop_textes, index):
    #prend un dictionnaire de textes en entrée et
    #retourne un dictionnaire contenant les moyennes de fréquences de lettres
      dico_moyennes = tableau_prop_textes.mean(axis = 0).to_dict()
      tableau_moyennes = pd.DataFrame(dico_moyennes, index =[index])
      return tableau_moyennes
    
    
  Cette seconde fonction a un intérêt particulier pour l'execution du programme, où on pourra trouver les fréquences d'apparition moyennes dans un ensemble de textes, connu comme étant anglais, ou français, pour obtenir des fréquences de réferences auxquelles comparer les fréquence d'un texte inconnu.
   
 

## Journal de bord 


