# 2024 - Luca Seggiani
# Questo file è uno script per la generazione automatica di master in latex

import os
from datetime import datetime

author = "Luca Seggiani"


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
    tags["year-tag"] = today.strftime("%Y")

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


# genera il master dai @tex_files in @directory
def make_master(tex_files, directory):
    # trova la cartella master
    master_directory = os.path.join(directory, "master")

    # se non c'è, creala
    if not os.path.isdir(master_directory):
        os.makedirs(master_directory)

    # trova il template master
    template_file = os.path.join(directory, "templates/master_template.tex")
    if not os.path.isfile(template_file):
        print("No master_template.tex found, skipping")
        return

    # trova il file master
    master_file = os.path.join(master_directory, "master.tex")

    # apri il file master
    with open(master_file, "w") as master:
        # crea un preambolo popolando i tag del template
        preamble = replace_tags(template_file, get_tags(directory))

        # scrivi il preambolo sul file
        master.write(preamble)

        # scrivi tutti i tex_file sul file
        for file, containing in tex_files:
            master.write(f"\\input{{../{containing}/{file}}}\n")

        # chiudi il file
        master.write("\\end{document}")
        print(f"Wrote to master in {directory}")

        # libera il file e aspetta che sia pronto
        master.flush()
        os.fsync(master.fileno())

        # compila il file
        compile_tex(master_file)


# inverti gli elementi della tupla @tup
def swap(tup):
    if len(tup) > 1:
        return (tup[1], tup[0])
    return tup


# ottieni una chiave di ordinamento per file latex @x, determinata dalla data
def get_sort_key(x):
    if x[1].find("-T") != -1:
        # -D è un tag che pone il file sempre in fondo all'ordine
        tup = tuple(map(lambda y: int(y) + 99, x[1].replace("-D", "")
                                                   .split("-")[::-1]))
        return swap(tup)
    else:
        tup = tuple(map(int, x[1].split("-")[::-1]))
        return swap(tup)


# ottieni tutte le coppie file-cartella di file .tex validi in @directory
def find_tex_files(directory):
    tex_files = []

    # esplora la cartella sul primo livello per trovare file validi
    for root, dirs, files in os.walk(directory):
        level = root.replace(directory, '').count(os.sep)
        if level <= 1:
            for file in files:
                dirname = os.path.basename(root)
                if is_latex(file):
                    try:
                        get_sort_key(dirname)
                    except ValueError:
                        continue
                    tex_files.append((file, dirname))
                    continue
    return tex_files


# presentati
print("2024 - Luca Seggiani")

directory = os.getcwd()
# cerca file tex opportuni nella directory
print(f"Looking into directory {directory}")

tex_files = find_tex_files(directory)

# ordina i file
tex_files.sort(key=get_sort_key)

# riporta tutti i file, ordinati
for file, containing in tex_files:
    print(f"Found: {file} in {containing}")

# crea il master
make_master(tex_files, directory)
