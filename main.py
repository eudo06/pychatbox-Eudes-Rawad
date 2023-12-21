import os
import string

files_name = []

# Récupérer la liste des fichiers d'un répertoire
def list_of_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

# Extraire le nom du Président d'un fichier
def extract_name(files_names):
    president = []
    for filename in files_names:
        extract_nomination = filename.rsplit("_", 1) [1]
        extract_nom = extract_nomination.rsplit(".",1) [0]
        nom_president = ''.join([i for i in extract_nom if not i.isdigit()])
        president.append(nom_president)
    final_president = set(president)
    return sorted(final_president)
print(extract_name)

# Associer le prénom du Président à son nom
def associer_prenom(liste_nom) :

    Chirac = {}
    Mitterand = {}
    Hollande = {}
    Macron = {}
    Sarkozy = {}
    Giscard = {}

    for nom in liste_nom:
        if nom == "Chirac" :
            Chirac = {'Chirac':'Jacques'}
        elif nom == "Mitterrand" :
            Mitterand = {"Mitterand":"François"}
        elif nom == "Hollande" :
            Hollande = {"Hollande":"François"}
        elif nom == "Macron" :
            Macron = {"Macron":"Emmanuel"}
        elif nom == "Sarkozy" :
            Sarkozy = {"Sarkozy":"Nicolas"}
        elif nom == "Giscard dEstaing" :
            Giscard = {"Giscard dEstaing":"Valéry"}

    president_complet = {**Chirac, **Mitterand,**Hollande, **Macron, **Sarkozy, **Giscard }
    return president_complet

# Ecriture de nouveaux fichiers dans le dossier "cleaned"
def convert_minuscule() :
    file_names = []
    file_names = list_of_files("./speeches", "txt")
    try:
        for filename in file_names:
            fichier_source = "./speeches/" + filename
            destination = "./cleaned/" + filename

            # Ouvrir le fichier source en mode lecture
            with open(fichier_source, 'r') as fichier_source:
                # Lire le contenu du fichier
                contenu = fichier_source.read()
                contenu = contenu.lower()

            # Ouvrir le fichier destination en mode écriture
            with open(destination, 'w') as fichier_destination:
                # Écrire le contenu dans le fichier destination
                fichier_destination.write(contenu)
        print("La conversion du texte en miniscule est réussie")
    except ValueError:
        print("erreur de coversion")



# Supprimer la ponctuation des textes
def ponctuation_delete():
    file_names = []
    file_names = list_of_files("./cleaned", "txt")

    for filename in file_names:
        fichier = "./cleaned/" + filename
        with open(fichier, 'r') as fichier_source:
            # Lire le contenu du fichier
            contenu = fichier_source.read()

            #Supprimer la ponctuation du texte
            ponctuation = string.punctuation
            for i in ponctuation:
                contenu = contenu.replace(i, "")
                contenu = contenu.replace("'", " ").replace("-"," ")

            # Ouvrir le fichier destination en mode écriture (le créer s'il n'existe pas)
            with open(fichier, 'w') as fichier_destination:
                # Écrire le contenu sans ponctuation dans le fichier destination
                fichier_destination.write(contenu)


# fonction de la partie idf et tf 

import os
import math
def calculer_tf(texte):
    mots = texte.split()
    tf_dict = {}

    for mot in mots:
        tf_dict[mot] = tf_dict.get(mot, 0) + 1

    return tf_dict



def calculer_idf(repertoire):
    nb_documents = len(os.listdir(repertoire))
    idf_dict = {}

    for fichier in os.listdir(repertoire):
        with open(os.path.join(repertoire, fichier), 'r') as file:
            contenu = file.read().split()
            unique_mots = set(contenu)

            for mot in unique_mots:
                idf_dict[mot] = idf_dict.get(mot, 0) + 1

    for mot, count in idf_dict.items():
        idf_dict[mot] = math.log((nb_documents / count))

    return idf_dict


def calculer_tfidf(tf, idf):
    tfidf_dict = {}

    for mot, tf_score in tf.items():
        tfidf_dict[mot] = tf_score * idf.get(mot, 0) if isinstance(tf_score, int) else 0

    return tfidf_dict


def construire_matrice_tfidf(repertoire):
    mots_uniques = set()
    tf_matrix = []

    for fichier in os.listdir(repertoire):
        with open(os.path.join(repertoire, fichier), 'r') as file:
            contenu = file.read()
            tf = calculer_tf(contenu)
            mots_uniques.update(tf.keys())
            tf_matrix.append(tf)

    idf = calculer_idf(repertoire)

    tfidf_matrix = []
    for tf_dict in tf_matrix:
        tfidf_row = tfidf_row = [int(tf_dict.get(mot, 0) * idf.get(mot, 0)) for mot in mots_uniques]
        tfidf_matrix.append(tfidf_row)

    return tfidf_matrix, list(mots_uniques)

# Calculer la similarité avec chaque document dans le corpus




def mots_non_importants(repertoire):
    tfidf_matrix, mots_uniques = construire_matrice_tfidf(repertoire)

    mots_non_importants = [mot for i, mot in enumerate(mots_uniques) if all(ligne[i] == 0 for ligne in tfidf_matrix)]

    print("Mots les moins importants :", mots_non_importants)


def mots_plus_importants(repertoire):
    tfidf_matrix, mots_uniques = construire_matrice_tfidf(repertoire)

    max_tfidf_scores = [max(ligne) for ligne in tfidf_matrix]
    index_max_tfidf = max_tfidf_scores.index(max(max_tfidf_scores))

    mot_plus_importants = mots_uniques[index_max_tfidf]

    print("Mot(s) ayant le score TF-IDF le plus élevé :", mot_plus_importants)


def mots_plus_repetes_par_president(repertoire, president):
    tf_matrix, mots_uniques = construire_matrice_tfidf(repertoire)

    # Index du président dans la liste des fichiers
    index_president = None
    for i, fichier in enumerate(os.listdir(repertoire)):
        if president.lower() in fichier.lower():
            index_president = i
            break

    if index_president is not None:
        mots_president = {mot: tf_matrix[index_president][j] for j, mot in enumerate(mots_uniques)}
        mots_plus_repetes = [mot for mot, score in mots_president.items() if score == max(mots_president.values())]

        print(f"Mot(s) le(s) plus répété(s) par le président {president} :", mots_plus_repetes)
    else:
        print(f"Le président {president} n'a pas de discours dans le répertoire fourni.")


def analyse_mentions_nation(repertoire):
    tf_matrix, mots_uniques = construire_matrice_tfidf(repertoire)


    mentions_nation_par_president = {}

    # Parcourir chaque président
    for i, fichier in enumerate(os.listdir(repertoire)):
        president = fichier.split("_")[1]  # Extrait le nom du président du nom du fichier
        mentions_nation_par_president[president] = sum(
            tf_matrix[i][j] for j, mot in enumerate(mots_uniques) if mot.lower() == "nation")


    president_max_mentions = max(mentions_nation_par_president, key=mentions_nation_par_president.get)

    print(f"Président(s) ayant parlé de la «Nation» : {list(mentions_nation_par_president.keys())}")
    print(
        f"Président ayant répété le plus de fois le mot «Nation» : {president_max_mentions} avec {mentions_nation_par_president[president_max_mentions]} mentions.")


def premier_president_a_parler_climat_ecologie(repertoire):
    tf_matrix, mots_uniques = construire_matrice_tfidf(repertoire)


    premier_occurrence_par_president = {}

    # Parcourir chaque président
    for i, fichier in enumerate(os.listdir(repertoire)):
        president = fichier.split("_")[1]  # Extrait le nom du président du nom du fichier
        for j, mot in enumerate(mots_uniques):
            if mot.lower() in ["climat", "écologie"]:
                if tf_matrix[i][j] > 0:
                    premier_occurrence_par_president.setdefault(president, mot.lower())
                    break

    print(f"Premier président à parler du climat et/ou de l'écologie : {premier_occurrence_par_president}")


def mots_evoques_par_tous_presidents(repertoire):
    tf_matrix, mots_uniques = construire_matrice_tfidf(repertoire)


    mots_evoques_par_tous = set(
        mot for j, mot in enumerate(mots_uniques) if all(tf_matrix[i][j] > 0 for i in range(len(tf_matrix))))

    print(
        f"Mot(s) évoqué(s) par tous les présidents (à l'exception des mots dits 'non importants') : {list(mots_evoques_par_tous)}")


#dernière partie du projet
import os

def list_of_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names







#partie 2 du projet
import string

def tokenize_question(question):
    # Convertir la question en minuscules
    question = question.lower()

    # Supprimer la ponctuation du texte
    ponctuation = string.punctuation
    for char in ponctuation:
        question = question.replace(char, "")

    # Diviser la question en mots individuels
    mots_question = question.split()

    return mots_question

def find_common_terms(question_words, corpus_words):
    # Identifie les termes communs entre la question et le corpus
    common_terms = set(question_words) & set(corpus_words)
    return list(common_terms)

def calculate_tfidf_vector(question_words, tf_dict, idf_dict):
    tfidf_vector = []

    for mot in question_words:
        # Score TF du mot dans la question
        tf_score = question_words.count(mot)

        # Score IDF du mot dans le corpus
        idf_score = idf_dict.get(mot, 0)

        # Calcul du score TF-IDF pour le mot
        tfidf_score = tf_score * idf_score

        tfidf_vector.append(tfidf_score)

    return tfidf_vector

def calculate_tf_for_corpus(repertoire):
    tf_matrix = []

    for fichier in os.listdir(repertoire):
        with open(os.path.join(repertoire, fichier), 'r') as file:
            contenu = file.read()
            tf = calculer_tf(contenu)
            tf_matrix.append(tf)

    return tf_matrix

# Partie 2 du projet

# ...

def calculate_tfidf_vector(question_words, tf_dict, idf_dict):
    tfidf_vector = []

    for mot in question_words:
        # Score TF du mot dans la question
        tf_score = question_words.count(mot)

        # Score IDF du mot dans le corpus
        idf_score = idf_dict.get(mot, 0)

        # Calcul du score TF-IDF pour le mot
        tfidf_score = tf_score * idf_score

        tfidf_vector.append(tfidf_score)

    return tfidf_vector

    return tf_matrix









#Menu principal
if __name__ == "__main__":
    repertoire_corpus = "./cleaned"
    directory = "./speeches"
    files_names = list_of_files(directory, "txt")
    mots_uniques = construire_matrice_tfidf(repertoire_corpus)[1]
    idf_dict = calculer_idf(repertoire_corpus)
    tf_matrix_corpus = calculate_tf_for_corpus(repertoire_corpus)

    while True:
        print("\nMenu Principal:")
        print("1. Accéder aux fonctionnalités de la partie 1")
        print("2. Accéder au mode Chatbot (partie 2)")
        print("3. Quitter")

        choix = input("Choisissez une option (1-3): ")

        if choix == "1":
            print("\nFonctionnalités de la Partie 1:")
            print("1. Convertir texte en minuscule")
            print("2. Afficher les mots les moins importants dans le corpus de documents")
            print("3. Afficher le(s) mot(s) ayant le score TF-IDF le plus élevé")
            print("4. Afficher le(s) mot(s) le(s) plus répété(s) par le président Chirac")
            print("5. Analyser les mentions de la «Nation» par les présidents")
            print("6. Trouver le(s) premier(s) président(s) à parler du climat et/ou de l'écologie")
            print("7. Trouver le(s) mot(s) évoqué(s) par tous les présidents")
            print("8. Retour au menu principal")

            choix_partie1 = input("Choisissez une option (1-8): ")

            if choix_partie1 == "1":
                convert_minuscule()
                ponctuation_delete()
            elif choix_partie1 == "2":
                mots_non_importants(repertoire_corpus)
            elif choix_partie1 == "3":
                mots_plus_importants(repertoire_corpus)
            elif choix_partie1 == "4":
                president_chirac = "Chirac"
                mots_plus_repetes_par_president(repertoire_corpus, president_chirac)
            elif choix_partie1 == "5":
                analyse_mentions_nation(repertoire_corpus)
            elif choix_partie1 == "6":
                premier_president_a_parler_climat_ecologie(repertoire_corpus)
            elif choix_partie1 == "7":
                mots_evoques_par_tous_presidents(repertoire_corpus)
            elif choix_partie1 == "8":
                continue
            else:
                print("Option non valide. Veuillez choisir une option entre 1 et 8.")
        elif choix == "2":
            # Mode Chatbot (Partie 2)
            question_utilisateur = input("Posez une question : ")
            mots_question = tokenize_question(question_utilisateur)
            termes_communs = find_common_terms(mots_question, mots_uniques)
            tfidf_vector_question = calculate_tfidf_vector(mots_question, tf_matrix_corpus[0], idf_dict)
            print("\nRésultats du Chatbot:")
            print("Termes communs avec le corpus :", termes_communs)
            print("Vecteur TF-IDF de la question :", tfidf_vector_question)
        elif choix == "3":
            print("Programme terminé.")
            break
        else:
            print("Option non valide. Veuillez choisir une option entre 1 et 3.")
















# appel des fonctions 1
directory = "./speeches"
files_names = list_of_files(directory, "txt")
nom_president = extract_name(files_names)
liste_complete = associer_prenom(nom_president)
print(liste_complete)
convert_minuscule()
ponctuation_delete()

#appel des fonctions  2
repertoire_corpus = "./cleaned"
mots_non_importants(repertoire_corpus)
repertoire_corpus = "./cleaned"
mots_plus_importants(repertoire_corpus)
repertoire_corpus = "./cleaned"
president_chirac = "Chirac"
mots_plus_repetes_par_president(repertoire_corpus, president_chirac)
repertoire_corpus = "./cleaned"
analyse_mentions_nation(repertoire_corpus)
repertoire_corpus = "./cleaned"
premier_president_a_parler_climat_ecologie(repertoire_corpus)
repertoire_corpus = "./cleaned"
mots_evoques_par_tous_presidents(repertoire_corpus)







