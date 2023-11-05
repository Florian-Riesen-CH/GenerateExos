import openai
import json
import regex
import webbrowser
import os
import pathlib

noCours = 1


def getEnonceExos(response, n):
    # Parsez la chaîne de caractères JSON pour obtenir un dictionnaire
    print("Série n° ", n)
    print("'\033[91m'", "Read openAi reponse", "'\033[0m'")
    openAiAnswer = json.loads(str(response))

    # Accédez à l'élément 'content'
    content = openAiAnswer['choices'][n]['message']['content']

    #
    print("'\033[91m'", "Extract JSON", "'\033[0m'")
    try:
        pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}')
        exercicesDecode = pattern.findall(str(content).replace('```',''))[0]
    except  json.decoder.JSONDecodeError :
        print("'\033[91m'", str(content), "'\033[0m'")
        exit()

    #print(str(exercicesDecode).replace('\n', ''))
    
    print("'\033[91m'", "Display exos", "'\033[0m'")

    exercicesJson = json.loads(str(exercicesDecode).strip('\n').strip())
    
    html = ""
    # Accédez à l'élément 'content'
    for element in exercicesJson['exercices']:
        html = html + GenerateHTML(element)
        
    openFile(html, "Cours n°"+str(noCours)+"-Série n°"+str(n)+"-Exercices")
    
def openFile(html, fileName):
    filePath = str(pathlib.Path().resolve())+'\\Exos\\'+str(fileName+".html")
    print("'\033[91m'", filePath, "'\033[0m'")
    path = os.path.abspath(filePath)
    url = 'file://' + path

    with open(path, 'w') as f:
        f.write(html)
    webbrowser.open(url)
    
def GenerateHTML(element):
    html = '<h3>Exercice: '+str(element['numero'])+'</h3><h4> ('+str(element['difficulte'])+')</h4>'
    html = html + '<p>'+str(element['question'])+'</p>'
    return html
    

n = 3
# # Load your API key from an environment variable or secret management service
openai.api_key = "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"
print("'\033[91m'", "Envoie de la demande à l'assistant ...", "'\033[0m'")
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Tu es un programme qui génères des exerices python pour des élèves conaissant les base de la programmation"},
        {"role": "system", "content": "Le format final est un JSON, dans un tableau nommé 'exercices' contenant les élément 'type','difficulte', 'numero','question', 'reponse', ta réponse ne doit contenir aucun retour à la ligne (\n) et aucune lettre avec des accents"},
        {"role": "system", "content": "Tu parles que le français"},
        {"role": "system", "content": "Tu es seulement capable de répondre des fichiers JSON"},
        {"role": "system", "content": "Aujourd'hui, les élèves ont appris les variables et leur différent type, les conditions et les fonctions mathématiques de base"},
        {"role": "system", "content": "Les élèves ne conaissent pas les liste ou les boucles, ne pose donc aucune question en lien avec"},
        {"role": "system", "content": "Le texte que tu génèreras sera directement envoyé aux élèves, il faut donc éviter tout texte superflu, ne donne que les exercices, ne confirme pas que tu as compris ma demande"},
        {"role": "user", "content": "Peux-tu me générer 5 exercices théorique et 5 exercices pratiques de niveau moyen à très difficilesur la leçon vue aujourd'hui ainsi que les corrigés ?"}
    ], 
    n=n
)

print("Analyse des réponses ...")

for n in range(0,n):
    getEnonceExos(response, n)
