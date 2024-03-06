# Udes_S2_APP5

## Mode de fonctionnement possible
1. Analyse pour chaque Auteur
   1. Ajouter une entrée dans une structure listant les auteurs et leur style d'écriture
      * À déterminer si on utilise une hashtable custom ou bien le dict de python
   2. Recherche en fonction de la profondeur maximum possible pour chaque texte.
      1. Exemple : Pour une profondeur de 3, on effectue 3 passe du texte.
         1. Première pour les uni-grammes
         2. Deuxième pour les bi-grammes
         3. Troisième pour les tri-grammes
      2. On ajoute ensuite chaque n-gramme dans une table de hachage avec une valeur de "1"
         * Si le n-gramme est déjà présent, on incrémente sa valeur.

1. Génération d'un texte 