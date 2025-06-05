import os

class Assets:
    def __init__(self):
        self._assets = load_assets()

    def get_sound_path(self, name):
        """Caso encontre o som em assets, retorna o caminho do arquivo,
        caso contrario retornara None."""
        if not name in self._assets["sounds"]: return None
        return self._assets["sounds"][name]["path"]

    def get_image_path(self, name):
        """Caso encontre a imagem em assets, retorna o caminho do arquivo,
        caso contrario retornara None."""
        if not name in self._assets["images"]: return None
        return self._assets["images"][name]["path"]

def load_assets():
    assets = {"sounds": {}, "images": {}, "fonts": {}}

    path_main = os.path.dirname(__file__)
    path_assets = os.path.join(path_main, "assets")

    path_sounds = os.path.join(path_assets, "sounds")
    path_images = os.path.join(path_assets, "images")
    path_fonts = os.path.join(path_assets, "fonts")

    for file in os.listdir(path_sounds):
        if not (file.endswith(".wav") or file.endswith(".ogg")): continue
        name = file[:-4] #Remove .wav e .ogg do nome do arquivo
        path = os.path.join(path_sounds, file)

        assets["sounds"][name] = {"path": path}

    for file in os.listdir(path_images):
        if not (file.endswith(".png") or file.endswith(".jpeg")): continue
        name = file[:-4] #Aki tem um erro que não ira remover .jpeg completamente.
        path = os.path.join(path_images, file)

        assets["images"][name] = {"path": path}

    for file in os.listdir(path_fonts):
        if not file.endswith(".ttf"): continue
        name = file[:-4]
        path = os.path.join(path_fonts, file)

        assets["fonts"][name] = {"path": path}

    return assets