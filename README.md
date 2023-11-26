# pychatbox-Eudes-Rawad
Les participants de ce projet sont :
-kouadio bli jean eudes 
-Allam Rawad

1-Liste et fichier :
 Le code commence par définir une fonction list_of_files qui prend en paramètre un répertoire et une extension de fichier. Cette fonction utilise le module os pour 
 récupérer la liste des fichiers dans le répertoire avec l'extension spécifiée.
2-Extraction du nom du Président :
  Ensuite, le code définit une fonction extract_name qui prend une liste de noms de fichiers en entrée. Cette fonction extrait le nom du président à partir du nom du 
  fichier en supprimant les chiffres et en utilisant des délimiteurs spécifiques tels que "_". Les noms ainsi extraits sont ensuite ajoutés à une liste.
3-Association des prénoms aux noms des Présidents :
  Une fonction associer_prenom est définie pour associer les prénoms aux noms des présidents. Elle utilise des dictionnaires pour stocker ces associations.
4-Conversion en minuscules et suppression de la ponctuation :
  Le code définit deux fonctions, convert_minuscule et ponctuation_delete, qui effectuent respectivement la conversion du texte en minuscules et la suppression de la 
  ponctuation pour chaque fichier texte dans les répertoires spécifiés.
5-Calcul de TF-IDF :
  Ensuite, le code défini des fonctions liées au calcul du TF-IDF. Ces fonctions permettent de construire une matrice TF-IDF à partir des fichiers texte dans le 
  répertoire spécifié.
6-Appels de fonctions :
  Enfin, des appels de fonctions sont effectués en utilisant un répertoire spécifique (./cleaned). Ces appels incluent des opérations telles que l'affichage des 
  mots importants
7-Note sur la structure du projet :
  Le code est organisé de manière à ce qu'une fonction principale menu_principal puisse être utilisée pour interagir avec les différentes fonctionnalités du projet.
  
En résumé, ce code combine des opérations de traitement de texte (conversion en minuscules, suppression de la ponctuation) avec des analyses plus avancées telles que le calcul du TF-IDF et l'analyse des mentions de certains termes spécifiques dans les discours des présidents. Il offre une interface utilisateur simple à travers le menu principal pour explorer ces fonctionnalités.
