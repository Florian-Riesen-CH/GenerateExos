import openai
import json
import regex
import webbrowser
import os
import pathlib
import mail
import random
import utils
nbSerie = 1
continueProcess = True;
gptModel = "gpt-3.5-turbo-1106"
noCours = 1
exoFolderPath = str(pathlib.Path().resolve())+'\\Exos'
studentMails = ['florian.riesen@eduvaud.ch','florian.riesen@outlook.com']
#studentMails = ['sylvain.berset@eduvaud.ch','jean-amedee.bosch@eduvaud.ch','sifedine.bouras@eduvaud.ch','yoan.corradini@eduvaud.ch','axel.dereymaeker@eduvaud.ch','sebastien.duruz@eduvaud.ch','theo.mayoraz@eduvaud.ch','manuel.oro@eduvaud.ch','sebastien.voide@eduvaud.ch']
mappingExosWithMail = {}
messageIntroduction = "Bonjour,\n\nComme annoncé lors du dernier cours.\nVoici une série d'exercices vous permettant de vous entraîner.\nVous retrouverez en pièce jointe les corrections"

def requestChatGPT():
    # # Load your API key from an environment variable or secret management service
    openai.api_key = "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"
    print("'\033[92m'", "Send powerPoint", "'\033[0m'")
    
    response = openai.ChatCompletion.create(
        response_format={ "type": "json_object" },
        model=gptModel,
        messages=[
            {"role": "system", "content": "You are an API who genarate python's exercises for advenced french student, the format of your answer must be JSON"},
            {"role": "system", "content": "The JSON must be formated like: { \"exercises\":[ { \"number\": \"...\", \"type\": \"...\", \"difficulty\": \"...\", \"question\": \"...\", \"answer\": \"...\", }, { \"number\": \"...\", \"type\": \"...\", \"difficulty\": \"...\", \"question\": \"...\", \"answer\": \"...\", } ] }"},
            {"role": "system", "content": "Python use indentation and not ';' to determine end of line"},
            {"role": "system", "content": "Students only know about: -variable  -condition  -math  -function  -loop"}, 
            {"role": "system", "content": "Difficulty has to be a number from 1 to 5"},
            {"role": "user", "content": "The file I share to you is the course material"},
            {"role": "user", "content": "Based on that file, can you generate 4 tehorical exercises, 5 \"What print this code\" and 7 pratical exercices in french ? "},
            {"role": "user", "content": "The question has to have at least 2 sentences"}
        ], 
        n=nbSerie
    )
    # Retirer les \n qui ne sont pas entre guillemets
    json_content_one_line:str = str(response)
    json_content_one_line = utils.remove_newlines_not_inside_quotes(json_content_one_line)

    #print(response)
    #print(json_content_one_line)

    print("Analyse des réponses ...")
    for n in range(0,nbSerie):
        getEnonceExos(json_content_one_line, n)

def getEnonceExos(response, no):
    # Parsez la chaîne de caractères JSON pour obtenir un dictionnaire
    print("Série n° ", no)
    print("'\033[92m'", "Read openAi reponse", "'\033[0m'")
    openAiAnswer = json.loads(str(response))

    # Accédez à l'élément 'content'
    content = openAiAnswer['choices'][no]['message']['content']

    #
    print("'\033[92m'", "Extract JSON", "'\033[0m'")
    try:
        pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}')
        exercisesDecode = pattern.findall(str(content).replace('```',''))[0]
        print("'\033[92m'", "Display exos", "'\033[0m'")
        stringexercisesDecode:str = str(exercisesDecode).replace('\\\'','\\\\\'')
        exercisesJson = json.loads(stringexercisesDecode)
    except  json.decoder.JSONDecodeError as e:
        print("'\033[91m'", "Error happend ", e.msg, "'\033[0m'")
        print("'\033[91m'", str(content), "'\033[0m'")
        return

    #print(str(exercisesDecode))

    # Accédez à l'élément 'content'
    
    GenerateHTML(exercisesJson, no)  
    GenerateCorrectedTxt(exercisesJson, "Série n°"+str(no)+"-Corrigés")
    
def GenerateHTML(exercisesJson, serieNo):
    html = '<a>'+messageIntroduction.replace('\n', '<br>').replace('.','.<br>')+'</a>'
    for element in exercisesJson['exercises']:
        html += '<h3>Exercice: '+str(element['number'])+'</h3>'
        html += '<a>'+str(element['question']).replace('\n', '<br>').replace(' ', '&nbsp')+'</a>'
    openFile(html, "Série n°"+str(serieNo)+"-exercices")

def openFile(html, fileName):
    filePath = exoFolderPath + '\\Cours n°'+str(noCours)+'\\'+str(fileName+".html")
    print("'\033[92m'", filePath, "'\033[0m'")
    path = os.path.abspath(filePath)
    url = 'file://' + path

    with open(path, 'w') as f:
        f.write(html)
    webbrowser.open(url)

def GenerateCorrectedTxt(exercisesJson, fileName):
    print("'\033[92m'", "Genarate correction file", "'\033[0m'")
    txt = "Corrections exercises" + "\n\n"
    for element in exercisesJson['exercises']:
        txt += "Exercice: " + str(element['number']) + "\n"
        txt += element['question'] + "\n\n"
        txt += element['answer'] + "\n\n\n"

    filePath = exoFolderPath + '\\Cours n°'+str(noCours)+'\\'+str(fileName+".txt")
    path = os.path.abspath(filePath)
    with open(path, 'w') as f:
        f.write(txt)

def sendEmails():
    smptPassword = input("Quel est le mot du passe du SMTP: ")
    for i in studentMails:
        print("'\033[92m'", "Send emails ...", "'\033[0m'")
        exerciceNo = random.randint(0, nbSerie-1)
        mappingExosWithMail[i] = exerciceNo
        # Ouvrir le fichier en mode lecture
        with open(exoFolderPath+"\\Cours n°"+str(noCours)+"\\Série n°"+str(exerciceNo)+"-exercices.html", 'r') as fichier:
            # Lire tout le contenu du fichier
            contenu = fichier.read()
            # Afficher le contenu lu
            mail.sendEmail('Exercices du cours n°'+str(noCours),i, smptPassword, contenu,"Corrections.txt",exoFolderPath+"\\Cours n°"+str(noCours)+"\\Série n°"+str(exerciceNo)+"-Corrigés.txt")
        

    filePath = exoFolderPath + '\\Cours n°'+str(noCours)+'\\Mapping.txt'
    path = os.path.abspath(filePath)
    with open(path, 'w') as f:
        for map in mappingExosWithMail:
            f.write(map+": "+ str(mappingExosWithMail[map]) + '\n')

while continueProcess:
    choixUser = input("Que souhaitez-vous faire ?\n1 - Générer des séries d'exercices \n2 - Envoyer les séries aux élèves\n >>> ")
    if choixUser == "1":
        requestChatGPT()
    elif choixUser == "2":
        sendEmails()
    else:  
        print("Merci de rentrer une valeur valide (1 ou 2)")

    continueProcessUser = input("Souhaitez-vous quitter (o => oui) ?\n >>> ")
    if continueProcessUser.lower() == "o":
        continueProcess = False