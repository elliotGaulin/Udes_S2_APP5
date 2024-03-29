#!/usr/bin/env python3
# -*- coding: utf-8 -*-


""" Ce fichier contient la classe TextAn, à utiliser pour résoudre la problématique.
    C'est un gabarit pour l'application de traitement des fréquences de mots dans les oeuvres d'auteurs divers.

    Les méthodes apparaissant dans ce fichier définissent une API qui est utilisée par l'application
    de test test_textan.py
    Les paramètres d'entrée et de sortie (Application Programming Interface, API) sont définis,
    mais le code est à écrire au complet.
    Vous pouvez ajouter toutes les méthodes et toutes les variables nécessaires au bon fonctionnement du système

    La classe TextAn est invoquée par la classe TestTextAn (contenue dans test_textan.py) :

        - Tous les arguments requis sont présents et accessibles dans args (dans le fichier test_textan.py)
        - Note : vous pouvez tester votre code en utilisant les commandes :
            + "python test_textan.py"
            + "python test_textan.py -h" (donne la liste des arguments possibles)
            + "python test_textan.py -v" (mode "verbose", qui indique les valeurs de tous les arguments)

    Copyright 2018-2023, F. Mailhot et Université de Sherbrooke
"""
import random

from textan_common import TextAnCommon
from operator import itemgetter
import math


class TextAn(TextAnCommon):
    """Classe à utiliser pour coder la solution à la problématique :

        - La classe héritée TextAnCommon contient certaines fonctions de base pour faciliter le travail :
            - recherche des auteurs
            - ouverture des répertoires
            - et autres (voir la classe TextAnCommon pour plus d'information)
            - La classe ParsingClassTextAn est héritée par TextAnCommon et lit la ligne de commande
        - Les interfaces du code à développer sont présentes, mais tout le code est à écrire
        - En particulier, il faut compléter les fonctions suivantes :
            - dot_product_dict (dict1, dict2)
            - dot_product_aut (auteur1, auteur2)
            - doct_product_dict_aut (dict, auteur)
            - find_author (oeuvre)
            - gen_text (auteur, taille, textname)
            - get_nth_element (auteur, n)
            - analyze()

    Copyright 2018-2023, F. Mailhot et Université de Sherbrooke
    """

    # Signes de ponctuation à retirer (compléter cette liste incomplète)
    PONC = ["!", "?", ".", ",", ";", ":", "(", ")", "[", "]", "{", "}", "<", ">", "'", '"', "«", "»", "“", "”", "‘",
            "’", "/", '—']
    PONC_A_GARDER = ['-']

    def __init__(self) -> None:
        """Initialize l'objet de type TextAn lorsqu'il est créé

        Args :
            (void) : Utilise simplement les informations fournies dans la classe TextAnCommon

        Returns :
            (void) : Ne fait qu'initialiser l'objet de type TextAn
        """

        # Initialisation des champs nécessaires aux fonctions fournies
        super().__init__()

        # Au besoin, ajouter votre code d'initialisation de l'objet de type TextAn lors de sa création

        return

    # Ajouter les structures de données et les fonctions nécessaires à l'analyse des textes,
    #   la production de textes aléatoires, la détection d'oeuvres inconnues,
    #   l'identification des n-ièmes mots les plus fréquents
    #
    # If faut coder les fonctions find_author(), gen_text(), get_nth_element() et analyse()
    # La fonction analyse() est appelée en premier par test_textan.py
    # Ensuite, selon ce qui est demandé, les fonctions find_author(), gen_text() ou get_nth_element() sont appelées

    @staticmethod
    def dot_product_dict(
            dict1: dict, dict2: dict, dict1_size: int, dict2_size: int
    ) -> float:
        """Calcule le produit scalaire NORMALISÉ de deux vecteurs représentés par des dictionnaires

        Args :
            dict1 (dict) : le premier vecteur
            dict2 (dict) : le deuxième vecteur

        Returns :
            dot_product (float) : Le produit scalaire normalisé de deux vecteurs

        Copyright 2023, F. Mailhot et Université de Sherbrooke
        """

        dot_product = 0.0

        # Permuter les dictionnaires pour réduire le nombre d'opérations
        if len(dict1) > len(dict2):
            dict1, dict2 = dict2, dict1

        for key in dict1:
            if key in dict2:
                dot_product += dict1[key] * dict2[key]

        if dict1_size != 0 and dict2_size != 0:
            dot_product = dot_product / (dict1_size * dict2_size)

        if dot_product > 1:
            dot_product = 1

        return dot_product

    def dot_product_aut(self, auteur1: str, auteur2: str) -> float:
        """Calcule le produit scalaire normalisé entre les oeuvres de deux auteurs, en utilisant dot_product_dict()

        Args :
            auteur1 (str) : le nom du premier auteur
            auteur2 (str) : le nom du deuxième auteur

        Returns :
            dot_product (float) : Le produit scalaire normalisé des n-grammes de deux auteurs

        Copyright 2023, F. Mailhot et Université de Sherbrooke
        """

        dict_auteur1 = self.mots_auteurs[auteur1]
        dict_auteur2 = self.mots_auteurs[auteur2]

        dict1_size = int(math.sqrt(sum(value ** 2 for value in dict_auteur1.values())))

        dict2_size = int(math.sqrt(sum(value ** 2 for value in dict_auteur2.values())))

        dot_product = self.dot_product_dict(dict_auteur1, dict_auteur2, dict1_size, dict2_size)

        return dot_product

    def dot_product_dict_aut(self, dict_oeuvre: dict, auteur: str) -> float:
        """Calcule le produit scalaire normalisé entre une oeuvre inconnue et les oeuvres d'un auteur,
           en utilisant dot_product_dict()

        Args :
            dict_oeuvre (dict) : la liste des n-grammes d'une oeuvre inconnue
            auteur (str) : le nom d'un auteur

        Returns :
            dot_product (float) : Le produit scalaire normalisé des n-grammes de deux auteurs

        Copyright 2023, F. Mailhot et Université de Sherbrooke
        """

        dict_auteur = self.mots_auteurs[auteur]

        dict1_size = int(math.sqrt(sum(value ** 2 for value in dict_oeuvre.values())))

        dict2_size = int(math.sqrt(sum(value ** 2 for value in dict_auteur.values())))

        dot_product = self.dot_product_dict(dict_oeuvre, dict_auteur, dict1_size, dict2_size)

        return dot_product

    def find_author(self, oeuvre: str) -> []:
        """Après analyse des textes d'auteurs connus, retourner la liste d'auteurs
            et le niveau de proximité (un nombre entre 0 et 1) de l'oeuvre inconnue
            avec les écrits de chacun d'entre eux

        Args :
            oeuvre (str) : Nom du fichier contenant l'oeuvre d'un auteur inconnu

        Returns :
            resultats (Liste[(string, float)]) : Liste de tuples (auteurs, niveau de proximité),
            où la proximité est un nombre entre 0 et 1)
        """

        # # Les lignes suivantes ne servent qu'à éliminer un avertissement.
        # # Il faut les retirer lorsque le code est complété
        # print(self.auteurs, oeuvre)
        # resultats = [
        #     ("Premier_auteur", 0.1234),
        #     ("Deuxième_auteur", 0.1123),
        # ]  # Exemple du format des sorties

        # Ajouter votre code pour déterminer la proximité du fichier passé en paramètre avec chacun des auteurs
        # Retourner la liste des auteurs, chacun avec sa proximité au fichier inconnu
        # Plus la proximité est grande, plus proche l'oeuvre inconnue est des autres écrits d'un auteur
        #   Le produit scalaire entre le vecteur représentant les oeuvres d'un auteur
        #       et celui associé au texte inconnu pourrait s'avérer intéressant...
        #   Le produit scalaire devrait être normalisé avec la taille du vecteur associé au texte inconnu :
        #   proximité = (A dot product B) / (|A| |B|)   où A est le vecteur du texte inconnu et B est celui d'un auteur,
        #           "dot product" est le produit scalaire, et |X| est la norme (longueur) du vecteur X

        resultats = []

        file = open(oeuvre, 'r', encoding="utf-8")
        texte_oeuvre = file.read()

        dict_oeuvre = self.create_dict(texte_oeuvre, {})

        for auteur in self.auteurs:
            resultats.append((auteur, self.dot_product_dict_aut(dict_oeuvre, auteur)))

        return resultats

    def write_words_to_file(self, words: [str], textname: str) -> None:
        f = open(textname, 'w', encoding='utf-8')
        word_count = 0
        for word in words:
            if word_count != 0 and word not in self.PONC:
                if word_count % 10 == 0:
                    f.write('\n')
                else:
                    f.write(' ')
            f.write(word)
            word_count += 1

        f.close()

    def gen_text_all(self, taille: int, textname: str) -> None:
        """Après analyse des textes d'auteurs connus, produire un texte selon des statistiques de l'ensemble des auteurs

        Args :
            taille (int) : Taille du texte à générer
            textname (str) : Nom du fichier texte à générer.

        Returns :
            void : ne retourne rien, le texte produit doit être écrit dans le fichier "textname"
        """

        # Ce print ne sert qu'à éliminer un avertissement. Il doit être retiré lorsque le code est complété
        markov_dict = {}
        mots_tout_auteurs = {}
        for auteur in self.auteurs:
            for ngram, freq in self.mots_auteurs[auteur].items():
                if ngram not in mots_tout_auteurs:
                    mots_tout_auteurs[ngram] = 0
                mots_tout_auteurs[ngram] += freq
                prefix = ngram[:len(ngram) - 1]
                suffix = ngram[-1]
                if prefix not in markov_dict:
                    markov_dict[prefix] = {}

                markov_dict[prefix][suffix] = freq

        first_n_gram = random.choices(list(mots_tout_auteurs.keys()), weights=list(mots_tout_auteurs.values()))[0]
        words = list(first_n_gram)
        for i in range(0, taille - self.ngram):
            if self.ngram == 1:
                next_word = random.choices(list(mots_tout_auteurs.keys()), weights=list(mots_tout_auteurs.values()))[0][
                    0]
            else:
                last_prefix = tuple(words[-self.ngram + 1:])
                if last_prefix not in markov_dict:
                    break
                possible_next_words = markov_dict[last_prefix]
                next_word = \
                    random.choices(list(possible_next_words.keys()), weights=list(possible_next_words.values()))[0]
            words.append(next_word)

        self.write_words_to_file(words, textname)
        return

    def gen_text_auteur(self, auteur: str, taille: int, textname: str) -> None:
        """Après analyse des textes d'auteurs connus, produire un texte selon des statistiques d'un auteur

        Args :
            auteur (str) : Nom de l'auteur à utiliser
            taille (int) : Taille du texte à générer
            textname (str) : Nom du fichier texte à générer.

        Returns :
            void : ne retourne rien, le texte produit doit être écrit dans le fichier "textname"
        """

        # Ce print ne sert qu'à éliminer un avertissement. Il doit être retiré lorsque le code est complété

        markov_dict = {}
        for ngram, freq in self.mots_auteurs[auteur].items():
            prefix = ngram[:len(ngram) - 1]
            suffix = ngram[-1]
            if prefix not in markov_dict:
                markov_dict[prefix] = {}

            markov_dict[prefix][suffix] = freq

        sorted_prefixes = sorted(markov_dict.items(), key=lambda key: len(key[1]), reverse=True)
        first_n_gram = \
            random.choices(list(self.mots_auteurs[auteur].keys()), weights=list(self.mots_auteurs[auteur].values()))[0]
        words = list(first_n_gram)
        for i in range(0, taille - self.ngram):
            if self.ngram == 1:
                next_word = random.choices(list(self.mots_auteurs[auteur].keys()),
                                           weights=list(self.mots_auteurs[auteur].values()))[0][0]
            else:
                last_prefix = tuple(words[-self.ngram + 1:])
                if last_prefix not in markov_dict:
                    break
                possible_next_words = markov_dict[last_prefix]
                next_word = \
                    random.choices(list(possible_next_words.keys()), weights=list(possible_next_words.values()))[0]
            words.append(next_word)

        self.write_words_to_file(words, textname)
        return

    def get_nth_element(self, auteur: str, n: int) -> [[str]]:
        """Après analyse des textes d'auteurs connus, retourner le n-ième plus fréquent n-gramme de l'auteur indiqué

        Args :
            auteur (str) : Nom de l'auteur à utiliser
            n (int) : Indice du n-gramme à retourner

        Returns :
            ngram (List[Liste[string]]) : Liste de liste de mots composant le n-gramme recherché
            (il est possible qu'il y ait plus d'un n-gramme au même rang)
        """

        if auteur not in self.auteurs:
            return []

        dict = self.mots_auteurs[auteur]

        # Fonction lambda pour trier le dictionnaire par valeur
        # dict.items() retourne une liste de tuples (clé, valeur)
        # key=itemgetter(1) trie la liste par la fréquence (valeur)
        # reverse=True trie en ordre décroissant

        ngram_sorted = sorted(dict.items(), key=itemgetter(1), reverse=True)

        # On retourne le n-ème élément de la liste triée
        # Si un ou plusieurs n-grammes ont la même fréquence, on les retourne tous

        if n > len(ngram_sorted):
            return []
        if n < 1:
            n = 1

        frequency = 0

        ngram = []

        all_same_frequency = True

        ## Trouver le n-ème élément (Si ex: [1, 2, 2, 3, 4, 4, 4, 5, 6] et n = 3, retourner [3])
        for i in range(len(ngram_sorted)):
            if ngram_sorted[i][1] != ngram_sorted[i - 1][1]:
                n -= 1
                all_same_frequency = False
            if all_same_frequency and n != 0:
                n = 0
            if n == 0:
                ngram = [list(ngram_sorted[i][0])]
                frequency = ngram_sorted[i][1]
                n = i
                break

        for i in range(n + 1, len(ngram_sorted)):
            # On vérifie si le n-gramme suivant a la même fréquence que le n-gramme actuel
            if ngram_sorted[i][1] == frequency:
                # On ajoute le n-gramme à la liste
                ngram.append(list(ngram_sorted[i][0]))
            else:
                break

        # # Les lignes suivantes ne servent qu'à éliminer un avertissement.
        # # Il faut les retirer lorsque le code est complété
        # print(self.auteurs, auteur, n)
        # ngram = [["un", "roman"]]  # Exemple du format de sortie d'un bigramme
        return ngram

    def create_dict(self, text: str, existing_dict: dict) -> dict:
        result_dict = existing_dict
        text = text.lower()
        for PONC_sign in self.PONC:
            if self.keep_ponc:
                text = text.replace(PONC_sign, ' ' + PONC_sign + ' ')
            else:
                text = text.replace(PONC_sign, '')
        for PONC_sign in self.PONC_A_GARDER:
            text = text.replace(PONC_sign, ' ' + PONC_sign + ' ')

        mots = text.split()
        if self.remove_word_1:
            mots = [mot for mot in mots if (len(mot) > 1)]
        if self.remove_word_2:
            mots = [mot for mot in mots if (len(mot) > 2)]

        for i in range(0, len(mots) - self.ngram):
            ngram = self.get_empty_ngram(self.ngram)
            for j in range(0, self.ngram):
                ngram[j] = mots[i + j]
            ngram_tuple = tuple(ngram)
            if ngram_tuple in result_dict:
                result_dict[ngram_tuple] += 1
            else:
                result_dict[ngram_tuple] = 1
        return result_dict

    def analyze(self) -> None:
        """Fait l'analyse des textes fournis, en traitant chaque oeuvre de chaque auteur

        Args :
            void : toute l'information est contenue dans l'objet TextAn

        Returns :
            void : ne retourne rien, toute l'information extraite est conservée dans des structures internes
        """

        # Ajouter votre code ici pour traiter l'ensemble des oeuvres de l'ensemble des auteurs
        # Pour l'analyse :  faire le calcul des fréquences de n-grammes pour l'ensemble des oeuvres
        #   d'un certain auteur, sans distinction des oeuvres individuelles,
        #       et recommencer ce calcul pour chacun des auteurs
        #   En procédant ainsi, les oeuvres comprenant plus de mots auront un impact plus grand sur
        #   les statistiques globales d'un auteur.
        # Il serait possible de considérer chacune des oeuvres d'un auteur comme ayant un poids identique.
        #   Pour ce faire, il faudrait faire les calculs de fréquence pour chacune des oeuvres
        #       de façon indépendante, pour ensuite les normaliser (diviser chaque vecteur par sa norme),
        #       avant de les additionner pour obtenir le vecteur complet d'un auteur
        #   De cette façon, les mots d'un court poème auraient une importance beaucoup plus grande que
        #   les mots d'une très longue oeuvre du même auteur. Ce n'est PAS ce qui vous est demandé ici.

        for auteur in self.auteurs:
            print(auteur)
            oeuvres = self.get_aut_files(auteur)
            for oeuvre in oeuvres:
                file = open(oeuvre, 'r', encoding="utf-8")
                texte_oeuvre = file.read()
                self.mots_auteurs[auteur] = self.create_dict(texte_oeuvre, self.mots_auteurs[auteur])
        return
