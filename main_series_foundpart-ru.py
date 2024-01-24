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
            found_part = code_source[max(0, start_index - 50): min(len(code_source), end_index + 50)]

            # Utiliser une expression régulière pour extraire l'URL avec "https://"
            url_pattern = r'https:[^"]+'
            url_match = re.search(url_pattern, found_part)

            if url_match:
                extracted_url = url_match.group().replace('\\', '')
                return extracted_url
            else:
                return f"Impossible d'extraire l'URL avec 'https://'"

        else:
            return f"La variable '{variable}' n'a pas été trouvée dans le code source JavaScript."

    except requests.exceptions.RequestException as e:
        return f"Une erreur s'est produite lors de la récupération de la page : {e}"

def traiter_fichier(input_filename):
    output_filename = "output-ru" + input_filename

    try:
        with open(input_filename, 'r') as file:
            lines = file.readlines()

        with open(output_filename, 'w') as output_file:
            for line in lines:
                url = line.strip()
                variable_a_chercher = "video.sibnet.ru"
                result = chercher_variable(url, variable_a_chercher)
                output_file.write(f"{url}\n{result}\n\n")
                print(f"Traitement terminé pour {url}")

        print(f"Les résultats ont été enregistrés dans le fichier {output_filename}")

    except FileNotFoundError:
        print(f"Le fichier {input_filename} n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

# Exemple d'utilisation avec une boucle
while True:
    input_file = input("Entrez le nom du fichier texte (ou 'exit' pour quitter) : ")
    
    if input_file.lower() == 'exit':
        break

    traiter_fichier(input_file)
