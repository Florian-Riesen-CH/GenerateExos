import re

def remove_newlines_not_inside_quotes(json_string):
    # Pour suivre si on est à l'intérieur de guillemets
    in_quotes = False
    json_result = ""

    # Parcourir chaque caractère dans la chaîne
    for char in json_string:
        if char == "\"":
            # Bascule l'état de 'in_quotes'
            in_quotes = not in_quotes
        # Si on trouve un newline et qu'on n'est pas à l'intérieur de guillemets, on continue sans l'ajouter
        if char == "\n" and not in_quotes:
            continue
        if char == "\\n" and not in_quotes:
            continue
        
        # Sinon, on ajoute le caractère au résultat
        json_result += char

    return json_result