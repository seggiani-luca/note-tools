# 2024 - Luca Seggiani
# Questo file implementa alcune funzioni condivise dagli script per la
# generazione di appunti

import os
from datetime import datetime

author = "luca seggiani"


# trova se un file è latex
def is_latex(path):
    return os.path.splitext(path)[1] == ".tex"


# compila il file .tex indicato da @path
def compile_tex(path):
    if not is_latex(path):
        print("file given to compile isn't a .tex file")
        return

    # spostati nella cartella del file e compilalo
    prev_directory = os.getcwd()

    os.chdir(os.path.dirname(path))
    os.system(f"pdflatex {os.path.basename(path)}")
    os.chdir(prev_directory)


# genera il dizionario dei tag; si definiscono i seguenti tag:
# title-tag: il nome della cartella degli appunti (.../questa/09-25/main.tex)
# author-tag: il nome trovato in @author
# date-tag: la data di oggi in formato dd-mm-yy
# year-tag: l'anno corrente
def get_tags(title):
    tags = {}

    # titolo, estrai il nome della cartella degli appunti
    tags["title-tag"] = os.path.basename(title)

    # autore
    tags["author-tag"] = author

    # data, trova la data di oggi
    today = datetime.now()
    tags["date-tag"] = today.strftime("%d-%m-%y")

    # anno, trova l'anno corrente
    tags["year-tag"] = today.strftime("%y")

    return tags


# rimpiazza ogni tag trovato file indicato da @path confrontandolo con @tags
def replace_tags(path, tags):
    with open(path, "r") as file:
        content = file.read()
        for tag, value in tags.items():
            content = content.replace(tag, value)
    return content


# ottieni tutte le subdirectory di @path
def get_directories(path):
    return [
                f for f in os.listdir(path)
                if os.path.isdir(os.path.join(path, f))
            ]
