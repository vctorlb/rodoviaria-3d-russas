from OpenGL.GL import *
from PIL import Image
import numpy as np

class TextureLoader:
    @staticmethod
    def load(filepath, repeat=True):
        """
        Carrega uma imagem e converte-a para uma textura OpenGL.
        Retorna o ID da textura ou None se o ficheiro não for encontrado.
        """
        try:
            img = Image.open(filepath).convert("RGBA")
            img_data = np.array(list(img.getdata()), np.uint8)
            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            
            # Define como a textura se comporta quando as coordenadas estão fora do intervalo [0, 1]
            wrap_param = GL_REPEAT if repeat else GL_CLAMP_TO_EDGE
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrap_param)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrap_param)
            
            # Define como a textura é filtrada ao ser ampliada ou reduzida
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            
            # Envia os dados da imagem para a GPU e gera mipmaps para melhor qualidade
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
            glGenerateMipmap(GL_TEXTURE_2D)
            
            return texture_id
        except FileNotFoundError:
            print(f"Aviso: Arquivo de textura não encontrado em '{filepath}'")
            return None
