from niveles import *
from config import *

def get_diccionario_tiles(game):
    
    dict_tiles = {

            1: None,
            10: game.obtener_grafico("piso1.png"),
            20: game.obtener_grafico("agua1.png"),
            21: game.obtener_grafico("agua2.png"),
            22: game.obtener_grafico("agua3.png"),
            23: game.obtener_grafico("agua4.png"),
            30: game.obtener_grafico("nube1.png"),
            31: game.obtener_grafico("nube2.png"),
            32: game.obtener_grafico("nube3.png"),
            33: game.obtener_grafico("nube4.png"),
        }
    
    return dict_tiles



def draw_tilemap_sin_scroll(game):
    # Dibujando el escenario

    for y in range(FILAS):
        for x in range(COLUMNAS):
            index = y * COLUMNAS + x
            tile = nivel_1_1[index]
            """
            if (tile == 10):
                game.screen.blit(self.num_tile[tile][0], (x * 64, y * 64))
            """
            # Estrucura switch
            match tile:
                case 10:
                    game.screen.blit(game.num_tile[tile][0], (x * 64, y * 64))
                case 20:
                    game.screen.blit(game.num_tile[tile][0], (x * 64, y * 64))
                case 21:
                    game.screen.blit(game.num_tile[tile][0], (x * 64, y * 64))
                case 22:
                    game.screen.blit(game.num_tile[tile][0], (x * 64, y * 64))
                case 23:
                    game.screen.blit(game.num_tile[tile][0], (x * 64, y * 64))



def draw_tilemap_buena(game):

    tiles_en_pantalla_x = game.screen.get_width() // 64
    start_tile_x = game.scroll_x // 64

    for y in range(FILAS):
        for x in range(tiles_en_pantalla_x + 1): # más uno para cubrir el borde derecho
            tile_index = y * COLUMNAS + (start_tile_x + x)

            if tile_index >= len(nivel_1_1):
                continue # fuera del mapa

            tile = nivel_1_1[tile_index]

            if game.num_tile[tile] != None:
                #Calcula posición en pantalla relativa al scroll
                pantalla_x = x * 64 - (game.scroll_x % 64)
                pantalla_y = y * 64
                game.screen.blit(game.num_tile[tile][0], (pantalla_x , pantalla_y))

            