

def create_text_file(file_name):
    try:
        file = open(file_name, "x")
        file.close()
    except FileExistsError:
        pass