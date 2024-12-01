import pygame
from package.constantes import *
from pygame import *
import csv

# Generales
def convertir_csv_a_lista_diccionarios(path:str) -> list:
    """
    ¿Que hace?-> Recibe la ruta de un csv lee sus lineas y las convierte en una lista de diccionarios, 
    entre las cabezeras y cada linea

    ¿Que parametros acepta?
        -path:str -> ruta del csv

    ¿Que retorna?-> list: Una lista de diccionarios formados por las cabezeras y 
                los datos linea a linea del csv
    """
    lista_diccionarios = []
    
    with open(path, mode='r', encoding='utf-8') as archivo:
        lineas = archivo.readlines()
        encabezados = lineas[0].strip().split(',')
    
        for linea in lineas[1:]:
            valores = linea.strip().split(',')

            for i in range(len(valores)):
                valores[i] = valores[i].strip('"')

            fila_diccionario = dict(zip(encabezados, valores))
            lista_diccionarios.append(fila_diccionario)
    
    return lista_diccionarios

def convertir_lista_diccionarios_a_csv(lista_diccionarios: list, path: str):
    """
    ¿Qué hace? -> Convierte una lista de diccionarios a un archivo CSV.

    ¿Qué parámetros acepta?
        - lista_diccionarios: list -> Lista de diccionarios que se quiere guardar en CSV.
        - path: str -> Ruta donde se guardará el archivo CSV.

    ¿Qué retorna? -> Nada
    """
    if len(lista_diccionarios) > 0:
        encabezados = lista_diccionarios[0].keys()

        with open(path, mode='w', encoding='utf-8', newline='') as archivo:
            archivo.write(','.join(encabezados) + '\n')
            for diccionario in lista_diccionarios:
                fila = []
                for i in diccionario.values():
                    fila.append(i)
                archivo.write(','.join(fila) + '\n')

def crear_botones(opciones: list, alto: int, ancho:int , espaciado: int, opcional:int = 0 ) -> list:
    '''
    ¿Que hace? Recibe una lista con opciones y crea los botones acordes a cada elemento de la lista,
    acomodando su posición y tamaño

    ¿Que parametros acepta?
        -opciones:list -> lista con las opciones a crear botones
        -alto:int -> alto del boton a crear
        -ancho:int -> ancho del boton a crear
        -espaciado:int -> espacio entre botones

    ¿Que retorna? -> Lista de botones(tupla y texto del boton)
    '''
    botones = []
    
    # Calculo espacio total a ocupar por botones + espaciado
    espacio_total_botones = (alto + espaciado) * len(opciones)

    espacio_restante = DIMENSIONES_VENTANA[1] - espacio_total_botones
    margen_superior = espacio_restante // 2 + opcional
    x_inicial = (DIMENSIONES_VENTANA[0] - ancho) // 2
    y_inicial = margen_superior

    for i in range(len(opciones)):
        # la posicion en y se calcula (alto+espacio) espacio total a ocupar por cada boton
        # y lo muliplico por el indice para evitar que se superpongan
        rect = pygame.Rect(x_inicial, y_inicial + i *(alto + espaciado), ancho, alto)
        botones.append((rect, opciones[i]))


    return botones

def dibujar_botones(ventana: pygame.Surface, botones: list, fuente, color_borde = NEGRO):
    '''
    ¿Que hace? -> Dibuja los botones en la ventana

    ¿Que parametros acepta?
        -ventana: pygame.Surface -> Superficie donde se van a dibujar los botones
        -botones: Lista de botones(tupla(rectangulo,texto))
        -fuente: pygame.font.Font -> fuente utilizada para los textos

    ¿Que retorna? -> Nada
    '''
    for rect, texto in botones:
        # rectangulo celeste
        pygame.draw.rect(ventana, AZUL_CLARO, rect)
        # borde
        pygame.draw.rect(ventana, color_borde, rect, 2)

        texto_boton = fuente.render(texto, True, NEGRO)
        
        # Centra el texto en el botón
        texto_x = rect.centerx - texto_boton.get_width() // 2
        texto_y = rect.centery - texto_boton.get_height() // 2
        
        ventana.blit(texto_boton, (texto_x, texto_y))

def manejar_click_botones(botones: list) -> str|None:
    '''
    ¿Que hace? -> maneja los clicks para checkear si se clickeo en alguna botón

    ¿Que parametros acepta?
        -botones: Lista de botones(tupla(rectangulo,texto))

    ¿Que retorna?:str|None -> Si te toco un boton el texto del mismo, sino None
    '''
    pos_mouse = pygame.mouse.get_pos()
    # verifica si hay colisin de la posición del mouse con los botones
    for rect, texto in botones:
        if rect.collidepoint(pos_mouse):
            return texto
    return None

def ajustar_texto(texto: str, fuente: pygame.font.Font, ancho_maximo: int) -> list:
    '''
    ¿Qué hace? -> Ajusta un texto para que se ajuste dentro de un ancho máximo especificado, dividiéndolo en líneas 
    que no excedan el ancho máximo en píxeles.

    ¿Qué parámetros acepta?
        -texto: str -> El texto completo que se desea ajustar a las líneas.
        -fuente: pygame.font.Font -> La fuente utilizada para calcular el tamaño del texto.
        -ancho_maximo: int ->  El ancho máximo permitido para cada línea de texto, en píxeles.

    ¿Qué retorna?: list -> Una lista de cadenas de texto, cada una representando una línea ajustada que cabe dentro 
    del ancho máximo especificado.
    '''
    palabras = texto.split()
    lineas = []
    linea_actual = ""

    for palabra in palabras:
        if fuente.size(linea_actual + palabra)[0] <= ancho_maximo:
            linea_actual += palabra + " "
        else:
            lineas.append(linea_actual.strip())
            linea_actual = palabra + " "

    if linea_actual:
        lineas.append(linea_actual.strip())

    return lineas

def obtener_puntaje_y_convertir_a_entero(diccionario: dict) -> int:
    '''
    ¿Que hace? -> Extrae el valor asociado a la clave 'puntaje' de un diccionario y
    lo convierte a un número entero.

    ¿Que parametros recibe?
        -diccionario: dict ->  Un diccionario que debe contener una clave 'puntaje' a convertir.     
    
    ¿Que retorna?: int -> El valor del 'puntaje' convertido a entero.
    '''
    puntaje_a_entero = int(diccionario['puntaje'])
    return puntaje_a_entero

def ordenar_lista_diccionarios(lista:list) -> list:
    '''
    ¿Que hace? -> Ordena una lista de diccionarios en orden descendente según el puntaje, 
    convirtiendo dicho valor a entero antes de ordenar.

    ¿Que parametros recibe?
        -lista: list -> Una lista de diccionarios a ordenar.

    ¿Que retorna?:list -> La lista de diccionarios ordenada en orden descendente por puntaje.
    '''
    lista_ordenada = sorted(lista, key=obtener_puntaje_y_convertir_a_entero, reverse=True)
    return lista_ordenada

def cambiar_configuracion(configuracion_a_cambiar: str, nuevo_valor: str):
    '''
    ¿Que hace? -> Cambia el valor de una configuración específica en un archivo CSV, actualizando el valor de 
    la configuración indicada y guardando los cambios.

    ¿Que parametros recibe?
        -configuracion_a_cambiar: str -> Configuracion a cambiar
        -nuevo_valor: str -> El nuevo valor que se asignará a la configuración especificada.
        
    ¿Que retorna? -> Nada
    '''
    configuraciones = convertir_csv_a_lista_diccionarios(
        RUTA_CONFIGURACIONES_CSV)
    for i in range(len(configuraciones)):
        if configuraciones[i]['configuracion'] == configuracion_a_cambiar:
            configuraciones[i]['valor_elegido'] = nuevo_valor

    convertir_lista_diccionarios_a_csv(configuraciones, RUTA_CONFIGURACIONES_CSV)

def cargar_fondo(ruta: str, dimensiones: tuple) -> pygame.Surface:
    '''
    ¿Que hace? -> Carga una imagen desde una ruta y la escala a las dimensiones proporcionadas.

    ¿Que parametros recibe?
        -ruta: str ->  La ruta del archivo de imagen a cargar.
        -dimensiones: tuple -> Las dimensiones (ancho, alto) a las que se debe redimensionar la imagen.

    ¿Que retorna?:pygame.Surface -> El objeto de superficie de Pygame que contiene la imagen cargada y redimensionada.
    '''
    fondo = pygame.image.load(ruta)
    return pygame.transform.scale(fondo, dimensiones)

def configurar_pantalla_base(ventana: pygame.Surface, fondo: pygame.Surface, 
                             titulo: str, fuente_titulo: pygame.font.Font) -> None:
    '''
    ¿Que hace? -> Configura la pantalla de la ventana con un fondo y un título centrado en la parte superior.

    ¿Que parametros acepta?
        -ventana: pygame.Surface -> Superficie donde se van a dibujar los botones
        -fuente: pygame.Surface -> La superficie que contiene la imagen de fondo a dibujar.
        -titulo: str -> El texto que se usará como título.
        -fuente_titulo: pygame.font.Font -> La fuente utilizada para renderizar el título.

    ¿Que retorna? -> Nada
    '''
    ventana.blit(fondo, (0, 0))
    texto_titulo = fuente_titulo.render(titulo, True, NEGRO)
    titulo_x = (DIMENSIONES_VENTANA[0] - texto_titulo.get_width()) // 2
    ventana.blit(texto_titulo, (titulo_x, 50))

def cargar_sonido(ruta:str) -> None:
    '''
    ¿Que hace? -> Carga y reproduce un archivo de sonido.

    ¿Que parametros recibe?
        -ruta: str -> Ruta del archivo de sonido que se desea cargar y reproducir.

    ¿Que retorna? -> Nada
    '''
    pygame.mixer.music.load(ruta)
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play()