import os
import requests
import re

def chercher_variable(url, variable):
    try:
        # Obtenir le code source de la page
        response = requests.get(url)
        response.raise_for_status()
        code_source = response.text

        # Rechercher la variable dans la partie JavaScript du code source
        pattern = r'\b' + re.escape(variable) + r'\b'
        match = re.search(pattern, code_source)

        if match:
            start_index = match.start()
            end_index = match.end()

            # Rechercher "https" à gauche de la variable
            start_http_index = code_source.rfind('https', 0, start_index)
            if start_http_index == -1:
                start_http_index = 0

            # Rechercher ".mp4" à droite de la variable (y compris)
            end_mp4_index = code_source.find('.mp4', end_index)
            if end_mp4_index == -1:
                end_mp4_index = len(code_source)

            found_part = code_source[start_http_index:end_mp4_index + 4]  # Ajout de 4 caractères pour inclure ".mp4"

            # Supprimer les barres obliques inverses
            found_part = found_part.replace('\\', '')

            return found_part

        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"Une erreur s'est produite lors de la récupération de la page : {e}")
        return None

def traiter_liens(input_file_path, variable_a_chercher):
    try:
        # Créer le chemin du fichier de sortie avec "output_" ajouté devant le nom
        output_file_path = "output_" + os.path.basename(input_file_path)

        with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
            for line in input_file:
                url = line.strip()
                if url:
                    result = chercher_variable(url, variable_a_chercher)
                    if result:
                        # output_file.write(f"URL: {url}\n")
                        output_file.write(f"{result}\n")
                        # output_file.write("="*30 + "\n")

        print(f"Les informations ont été enregistrées dans le fichier : {output_file_path}")

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

# Indiquez le chemin du fichier d'entrée contenant les liens
input_file_path = input("Veuillez indiquer le chemin du fichier d'entrée : ")

# Remplacez la variable_a_chercher selon votre besoin
variable_a_chercher = "iptvfrenchforyou"

traiter_liens(input_file_path, variable_a_chercher)
