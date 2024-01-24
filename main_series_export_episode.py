import requests
import re
from bs4 import BeautifulSoup
import json
import os

def clean_filename(title):
    # Remplacer les caractères non autorisés dans les noms de fichier Windows
    illegal_chars = '<>:"/\\|?*'
    for char in illegal_chars:
        title = title.replace(char, '_')
    # Supprimer les sauts de ligne et les espaces en début et fin de chaîne
    title = title.strip().replace('\n', '').replace('\r', '')
    return title

# Remplacez l'URL par l'adresse de la page que vous souhaitez analyser

# url = "https://wookafr.site/titles/825/lupin/season/1"
url = input("Indiquer le lien de la serie avec la saison : exemple : https://wookafr.site/titles/825/lupin/season/1 \n >>>")

# Récupérer le contenu de la page web
response = requests.get(url)
html_content = response.text

# Utiliser BeautifulSoup pour extraire le titre de la page
soup = BeautifulSoup(html_content, 'html.parser')
page_title = soup.title.string

# Utiliser une expression régulière pour trouver les occurrences de "episode_num" suivies d'un nombre
matches_episode_num = re.findall(r'"episode_num"\s*:\s*(\d+)', html_content)

# Utiliser une expression régulière pour trouver les occurrences de "path" suivies d'une chaîne de caractères
matches_path = re.findall(r'"path"\s*:\s*"([^"]+)"', html_content)

# Convertir les valeurs trouvées en entiers
episode_num_values = list(map(int, matches_episode_num))

# Trouver le nombre le plus grand parmi les valeurs de episode_num
max_episode_num = max(episode_num_values, default=None)

if max_episode_num is not None:
    print(f"Le nombre le plus grand de 'episode_num' trouvé sur la page est : {max_episode_num}")
else:
    print("Aucune valeur de 'episode_num' n'a été trouvée dans le code source.")

# Créer le nom de fichier en utilisant le titre nettoyé de la page
cleaned_title = clean_filename(page_title)
file_name = f"{cleaned_title}_results.txt"

# Enregistrer les valeurs associées à la clé "path" avec la partie dynamique dans le fichier
if matches_path:
    with open(file_name, 'w') as file:
        # file.write("Les valeurs associées à la clé 'path' sont :\n")
        for path_value in matches_path:
            for episode_number in range(1, max_episode_num + 1):
                file.write(path_value.replace("\\", "") + f"/episode/{episode_number}\n")
    print(f"Les résultats ont été sauvegardés dans le fichier : {file_name}")
else:
    print("Aucune valeur de 'path' n'a été trouvée dans le code source.")
