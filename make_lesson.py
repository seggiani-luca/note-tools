# 2024 - Luca Seggiani
# Questo file è uno script per la generazione automatica di lezioni in latex

import os
import shared_utils as su
from datetime import datetime


def make_lesson(directory):
    # trova il template lesson
    template_file = os.path.join(directory, "templates/lesson_template.tex")
    if not os.path.isfile(template_file):
        print("No lesson_template.tex found, skipping")
        return

    # genera la directory dalla data corrente
    current_date = datetime.now().strftime("%m-%d")
    lesson_directory = os.path.join(directory, current_date)

    # se non c'è, creala
    if not os.path.exists(lesson_directory):
        os.makedirs(lesson_directory)
    else:
        # altrimenti esci
        print("Lesson already exists")
        quit(1)

    lesson_file = os.path.join(lesson_directory, "main.tex")

    # crea il file e aprilo
    with open(lesson_file, "w") as lesson:
        # crea un preambolo popolando i tag del template
        preamble = su.replace_tags(template_file, su.get_tags(os.path.basename(
            directory)))

        # scrivi il preambolo sul file
        lesson.write(preamble)

        # chiudi il file
        lesson.write("\\end{document}")
        print(f"Wrote to lesson in {directory}")

        # libera il file e aspetta che sia pronto
        lesson.flush()
        os.fsync(lesson.fileno())

        # compila il file
        su.compile_tex(lesson_file)


# presentati
print("2024 - Luca Seggiani")

# crea una nuova lezione nella directory corrente
current = os.getcwd()
make_lesson(current)
