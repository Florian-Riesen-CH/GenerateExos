import openai
from pptx import Presentation
import json
import regex

def getEnonceExos(response, n):
    # Parsez la chaîne de caractères JSON pour obtenir un dictionnaire
    print("Série n° ", n)
    openAiAnswer = json.loads(str(response))

    # Accédez à l'élément 'content'
    content = openAiAnswer['choices'][n]['message']['content']

    #print(content)

    exercicesDecode = pattern.findall(str(content).replace('\\\\n', '').replace('\\n', ''))

    print(exercicesDecode[0])

    exercicesJson = json.loads(str(exercicesDecode[0]))
    # Accédez à l'élément 'content'
    exercices = exercicesJson['exercices']
    for element in exercicesJson['exercices']:
        print(element["difficulte"])
        print(element["enonce"])
        print(element["reponse"])
        print("------------------------------------------")



pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}')
# # Load your API key from an environment variable or secret management service
openai.api_key = "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"

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Tu es un programme qui génères des exerices python pour des élèves conaissant les base de la programmation"},
        {"role": "system", "content": "Tu es seulement capable de répondre des fichiers JSON"},
        {"role": "system", "content": "Aujourd'hui, les élèves ont appris les variables et leur différent type, les conditions et les fonctions mathématiques de base"},
        {"role": "system", "content": "Les élèves ne conaissent pas les liste ou les boucles, ne pose donc aucune question en lien avec"},
        {"role": "system", "content": "Le texte que tu génèreras sera directement envoyé aux élèves, il faut donc éviter tout texte superflu, ne donne que les exercices, ne confirme pas que tu as compris ma demande"},
        {"role": "user", "content": "Peux-tu me générer 5 exercices complet théorique ou pratique de niveau moyen à très difficilesur la leçon vue aujourd'hui ainsi que les corrigés ?"},
        {"role": "user", "content": "Format moi cela en JSON dans un tableau nommé 'exercices' contenant les élément 'difficulte', 'enonce', 'reponse'"}
    ], 
    n=1
) 

print(response)

for n in range(0,2):
    getEnonceExos(response, n)
