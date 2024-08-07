import ollama

output_format = 'JSON'

def ask(requests, text, csv):
    query = (f"Vous êtes un modèle linguistique extrêmement précis et méticuleux chargé d'extraire des informations "
             f"spécifiques à partir de texte extrait par OCR. Le texte est fourni aux formats texte brut et CSV. "
             f"Votre objectif est d'extraire uniquement les données suivantes : \n{requests}\n"
             f"Ne rien extraire de plus ou de moins et ne pas ajouter de détails ou d'informations supplémentaires non demandées "
             f"à partir des fichiers suivants :\ncsv:\n{csv}\ntext:\n{text}\n"
             f"Vous devez extraire les données demandées et seulement celles demandées de manière concise et précise sous format "
             f"{output_format}. Aucune donnée ou valeur ne doit être modifiée. Le résultat final doit être concis et "
             f"ne contenir que l'information demandée, telle qu'elle est spécifiée dans les textes donnés. "
             f"Si une donnée demandée n'est pas trouvée, indiquer explicitement 'introuvable'. "
             f"Ne pas mentionner vos connaissances linguistiques et ne pas ajouter de contexte. "
             f"Assurez-vous que les données extraites sont précises et correspondent exactement à celles présentes dans le texte.")

    response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': query, },])

    response = response['message']['content']
    return response