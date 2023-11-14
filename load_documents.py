import os


def load_documents() -> list:
    texts = []
    carpeta = "files"
    if os.path.exists(carpeta):
        archivos_en_carpeta = os.listdir(carpeta)
        for archivo in archivos_en_carpeta:
            ruta_archivo = os.path.join(carpeta, archivo)
            if os.path.isfile(ruta_archivo):
                with open(ruta_archivo, 'r',encoding='utf-8') as file:
                    contenido = file.read()
                    texts.append(contenido)
    else:
        print("La carpeta especificada no existe")

    return texts