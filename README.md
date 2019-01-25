Ce document est accessible sur ce lien https://camcour.github.io/PCBS-automatic_classifier/

# Automatic classifier

Ce projet suit une idée dont vous avez donnée lors de ce cours: créer un programme qui permettrait d'identifier si un texte est de langue française ou anglaise.
Pour se faire, le programme ainsi créé se base sur des statistiques d'apparition de chaque lettre de l'alphabet dans des textes. Le programme permet d'en faire le test, sur des mots, des phrases, des paragraphes et des documents entiers. Ce test est établi par une validation croisée: les textes servant de référence par langue, et les textes testés, sont bien différents.

## Préparation des textes à évaluer

  Avant d'évaluer des textes, que ce soit pour créer les fréquences de références par langue, ou que ce soit pour tester un        texte, j'ai décidé de préparer chaque texte afin d'enlever toute ponctuation et toute différence de casse.
  J'ai ainsi créé une fonction qui lit un texte selectionné, le transfomre en lettre minuscule et enlève les ponctuations (y compris les espaces).

    def simplifie_textes(texte_brut):
    #fonction qui pour un texte brut en entrée, le lit, le rend minuscule
    #et lui enlève toute ponctuation, ce qu'il retourne
        with open(texte_brut) as t:
            texte = t.read()
            texte_low = texte.lower()
            texte_lettres = re.sub(r'[^a-z]', '', texte_low)
        return texte_lettres

### Calcul des proportions de chaque lettre dans un texte

  La prochaine étape était alors de calculer pour le texte ainsi simplifié la proportion d'apparition de chaque lettre dans le texte. J'ai pris alors la décision de répertorier les fréquences des 26 lettres de l'alphabet, sans prendre en compte les caractères accentués (auxquels auraient pu être associés des fréquences propres). 
  Ne pas prendre en compte l'accentuation m'a semblé intéressant pour pouvoir travailler autour des porportions de lettres simples dans les textes, et ne pas jouer sur l'absence d'accentuation en anglais, qui aurait facilité la tâche de classification.
  La foncion créée à cette fin retourne ainsi un dictionnaire, dans lequel la fréquence d'apparition de chaque lettre est attribuée à la lettre notée dans une clé du dictionnaire.
  
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
  J'ai alors crée une fonction qui prend un texte ou un ensemble de textes, le(s) simplifie et attribue à chaque texte les frèquences d'apparition des lettres. J'ai fait le choix de faire l'usage de cette fonction aussi bien pour un texte que pour un ensemble afin de n'obtenir aucun problème dans la suite du processus pour analyser conjointement les valeurs obtenues d'un ensemble de texte, et celles obteunues par un texte unique. 
  Cette fonction a été faiet de telle sorte à obtenir toutes ces données visibles dans un dataframe. Cela permet si souhaité de voir d'un coup d'oeil les fréquences des lettres dans chaque texte évalué, mais aussi d'ordonner les données pour une future et simple analyse statistique des données présentes dans le tableau. 

  
  
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

 Ainsi, j'ai fait une deuxième fonction, qui peut grâce à ce dataframe, calculer les moyennes de fréquences de lettres, relativement à l'ensemble de textes duquel le dataframe a été créé. 

    def attribue_moyennes(tableau_prop_textes, index):
    #prend un dictionnaire de textes en entrée et
    #retourne un dictionnaire contenant les moyennes de fréquences de lettres
      dico_moyennes = tableau_prop_textes.mean(axis = 0).to_dict()
      tableau_moyennes = pd.DataFrame(dico_moyennes, index =[index])
      return tableau_moyennes
    
    
  Cette seconde fonction a un intérêt particulier pour l'éxecution du programme, où on pourra trouver les fréquences d'apparition moyennes d'un ensemble de textes, connu comme étant anglais, ou français, pour obtenir des fréquences de réferences auxquelles comparer les fréquences de lettres d'un texte inconnu.
   
## Test du programme
 
### Textes de références par langue
 
 J'ai décidé de prendre comme textes de références les oeuvres d'une poétesse et celles d'un poète. Ainsi, les textes de référence pour la langue anglaise sont un ensemble de poèmes d'Emily Dickinson. Pour les textes de référence en langue francaise, j'ai choisi un ensemble de poèmes issu du recueil Alcool, de Guillaume Apollinaire. Ces textes sont lisibles dans des fichiers .txt, et sont rangés dans deux dossiers de ce répertoire.
 
### Textes à tester
 
  Le but principal de mon programme étant de tester la langue de textes, j'ai aléatoirement choisi des textes trouvés sur internet, que j'ai rangés dans deux dossiers de textes à tester (en langue anglaise ou française), tous deux présents dans le répertoire.
  
### Comparaison des proportions entre les textes de référence et les textes à tester
  
  Afin de comparer les proportions entre les textes de référence, et le(s) texte(s) à tester, j'ai créé un dataframe dans lequel on peut observer les fréquences d'apparition moyennes de chaque lettre calculé au sein des deux receuils de textes, et les fréquences d'apparition de chaque lettre calculé pour un texte, choisi au hasard dans les deux dossiers de textes à tester.
  Grâce à ce tableau, ont ensuite été calculés deux coefficients de corrélation: l'un entre les fréquences dans le texte à tester (inconnu), et les moyennes de fréquences en anglais, et l'autre entre les fréquences dans le texte inconnu et les moyennes de fréquences en francais.
  Le coefficient de corrélation le plus grand determinera alors la langue présumée du texte testé.
  Comme le texte testé a été pioché dans un dossier présent dans le répertoire, il est ensuite possible de savoir si la langue qui a été déterminée par le programme grace aux coefficients de corrélation, est en effet la langue du texte.
 
Voici par exemple un rendu possible du terminal, après qu'un texte pris au hasard dans les dossiers du répertoire contenant des textes à tester a été évalué.

![exemple de terminal avec le texte night.txt](/exemple_rendu_sur_terminal.png)

  
## Conclusion
 
Ce fut un long travail, et je n'ai au final pas eu le temps d'analyser la performance de mon programme en fonction de la taille du texte, comme vous l'aviez suggeré. En revanche, il semble que le programme fonctionne tout de même bien pour les textes testés, ce qui est encourageant.

Mon niveau initial était très bas car je n'avais jamais programmé avant le mois de rentrée en septembre et les cours de programmation. Je considère ainsi avoir beaucoup appris lors de ce cours et grâce à ce projet. 
J'ai ainsi spécifiquement appris à avoir une vision d'ensemble d'un projet, pour pouvoir anticiper les différentes étapes, et les possibles contraintes. J'ai aussi appris l'intérêt de modules afin d'importer ceux qui pourraient être utiles, appris à bien formatter des fonctions, en faire réellement usage, que ce soit avec un ou pusieurs arguments, et un ou plusieurs éléments en sortie. J'ai appris aussi qu'il fallait à tout prix éviter les variables globales. De plus j'ai appris l'importance de bien coordonner les différents objets que l'on souhaite manipuler pour réellement utiliser les fonctions telles qu'elles sont prévues. Par exemple, j'ai trouvé que jongler entre des tableaux et des dictionnaires peut être facilitant, sans être pour autant trop problématique pour l'écriture ou la lecture du code (je pense tout de même qu'il doit s'agir d'un des problèmes de mon code, et je pense que d'autres solutions plus propres auraient pu êtres trouvées avec un peu plus de temps). J'ai aussi appris lors de ce cours l'usage des expression regulières et leur intérêt. Par ailleurs, j'ai découvert la maniere d'accéder à des fichiers sur l'ordinateur, pour les lire ou les modifier. Enfin j'ai appris à réellement faire usage des ressources de documentation des fonctions de python ou de différents modules, et surtout comprendre ce qu'elles signifiaient (pour pandas par exemple).
En somme, j'ai appris à aborder de manière plus fluide et sereine les lignes de codes que j'écris et lis.

