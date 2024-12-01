import pygame
from package.constantes import *
from pygame import *
from package.funciones_generales import *

def crear_boton_menu(ventana: pygame.Surface, fuente: pygame.font.Font):
    '''
    ¿Que hace? -> Crea un botón usado para volver al menú con un rectángulo y texto centrado.

    ¿Que parametros recibe?
        -ventana:pygame.Surface -> Superficie en la que se dibuja el botón.
        -fuente:pygame.font.Font -> La fuente que se utiliza para renderizar el texto en el botón.
        
    ¿Que retorna?:pygame.Rect -> El rectángulo del botón, que puede usarse para detectar clics.
    '''
    rect_boton = pygame.Rect(BOTON_X, BOTON_Y, BOTON_ANCHO, BOTON_ALTO)
    pygame.draw.rect(ventana, AZUL_CLARO, rect_boton)
    pygame.draw.rect(ventana, NEGRO, rect_boton, 2)

    texto_renderizado = fuente.render(BOTON_TEXTO, True, NEGRO)
    texto_x = rect_boton.centerx - texto_renderizado.get_width() // 2
    texto_y = rect_boton.centery - texto_renderizado.get_height() // 2
    ventana.blit(texto_renderizado, (texto_x, texto_y))

    return rect_boton

def obtener_dificultad():
    '''
    ¿Que hace? -> Obtiene la dificultad elegida desde un archivo CSV de configuraciones

    ¿Que parametros recibe? -> Ninguno

    ¿Que retorna?:str -> La dificultad seleccionada, como una cadena de texto.
    '''
    configuraciones = convertir_csv_a_lista_diccionarios(
        RUTA_CONFIGURACIONES_CSV)
    dificultad = ''
    for i in configuraciones:
        if i['configuracion'] == 'dificultad_elegida':
            dificultad = i['valor_elegido']
    return dificultad

def buscar_menor_puntaje_ranking(lista: list) -> int:
    '''
    ¿Que hace?: -> Busca el índice del jugador con el menor puntaje en el ranking.

    ¿Que parametros recibe?:
        -lista:list -> Una lista de diccionarios, donde cada diccionario contiene información de un jugador, incluyendo su puntaje.

    ¿Que retorna?:int -> El índice del jugador con el menor puntaje en la lista. Si hay empates, devuelve el índice del jugador con el menor puntaje más arriba.
    '''
    min_valor = int(lista[0]['puntaje'])
    indice_menor_valor = 0

    for i in range(1, len(lista)):
        if int(lista[i]['puntaje']) < min_valor:
            min_valor = int(lista[i]['puntaje'])
            indice_menor_valor = i
        elif int(lista[i]['puntaje']) == min_valor:
            if indice_menor_valor > i:
                min_valor = int(lista[i]['puntaje'])
                indice_menor_valor = i

    return indice_menor_valor

def filtrar_preguntas_por_dificultad(dificultad: str):
    '''
    ¿Que hace? -> Filtra las preguntas de un archivo CSV según la dificultad dada.

    ¿Que parametros recibe?
        -dificultad: str -> La dificultad por la cual se desea filtrar las preguntas.

    ¿Que retorna?:list -> Una lista de diccionarios que contiene solo las preguntas 
                                que coinciden con la dificultad dada.
    '''
    preguntas = convertir_csv_a_lista_diccionarios(RUTA_PREGUNTAS_CSV)
    preguntas_filtradas = []
    for pregunta in preguntas[1:]:
        if pregunta['dificultad'] == dificultad:
            preguntas_filtradas.append(pregunta)

    return preguntas_filtradas

# Ranking
def cargar_ranking() -> list:
    '''
    ¿Que hace? -> Carga los datos del ranking desde un archivo CSV.

    ¿Que parametros recibe? -> Ninguno

    ¿Que retorna?:list -> Una lista de diccionarios con los datos del ranking.
    '''
    return convertir_csv_a_lista_diccionarios(RUTA_RANKING_CSV)

def dibujar_encabezados_ranking(ventana: pygame.Surface, fuente: pygame.font.Font, y_inicial: int) -> int:
    '''
    ¿Que hace? -> Dibuja los encabezados para las columnas "Usuario", "Puntuación" y "Tiempo"
    en la parte superior de la tabla del ranking, centrando el texto en cada columna.

    ¿Que parametros recibe?
        -ventana:pygame.Surface -> Superficie en la que se dibuja el botón.
        -fuente:pygame.font.Font -> La fuente que se utiliza para renderizar el texto en el botón.
        -y_inicial: int ->  La posición Y desde donde se comenzarán a dibujar los encabezados.

    ¿Que retorna?:int -> La nueva posición Y después de dibujar los encabezados, que es utilizada para dibujar las filas de datos.
    '''

    textos = ["Usuario", "Puntuación", "Tiempo"]
    posiciones = [ANCHO // 6, ANCHO // 2, 5 * ANCHO // 6]

    for texto, x in zip(textos, posiciones):
        render = fuente.render(texto, True, NEGRO)
        ventana.blit(render, (x - render.get_width() // 2, y_inicial))

    pygame.draw.line(ventana, NEGRO, (50, y_inicial + 30),
                     (ANCHO - 50, y_inicial + 30), 2)
    return y_inicial + 40

def dibujar_filas_ranking(ventana: pygame.Surface, fuente: pygame.font.Font, lista_ranking: list, y_inicial: int) -> None:
    '''
    ¿Que hace? -> Recorre la lista de entradas del ranking y dibuja una fila para cada entrada,
    mostrando el nombre de usuario, el puntaje y el tiempo en columnas centradas en posición.

    ¿Que parametros recibe?
        -ventana:pygame.Surface -> Superficie en la que se dibuja el botón.
        -fuente:pygame.font.Font -> La fuente que se utiliza para renderizar el texto en el botón.
        -lista_ranking: list -> Una lista de diccionarios que contiene las entradas del ranking.
        -y_inicial: int -> La posición Y desde donde comenzarán a dibujarse las filas en la ventana.

    ¿Que retorna? -> Nada
    '''
    posiciones = [ANCHO // 6, ANCHO // 2, 5 * ANCHO // 6]

    for i in range(len(lista_ranking)):
        textos = [lista_ranking[i]['usuario'], str(lista_ranking[i]['puntaje']), str(lista_ranking[i]['tiempo'])]
        y_fila = y_inicial + i * 40
        for texto, x in zip(textos, posiciones):
            render = fuente.render(texto, True, NEGRO)
            ventana.blit(render, (x - render.get_width() // 2, y_fila))

def dibujar_divisiones_ranking(ventana: pygame.Surface, y_inicial: int, num_filas: int) -> None:
    '''
    ¿Que hace? -> Dibuja las divisiones verticales de la tabla de ranking en la ventana del juego.

    ¿Que parametros recibe?
        -ventana:pygame.Surface -> Superficie en la que se dibuja el botón.
        -y_inicial: int -> La posición Y inicial desde donde se dibujarán las divisiones.
        -num_filas: int -> El número de filas de la tabla.

    ¿Que retorna? -> Nada
    '''
    altura_tabla = y_inicial + num_filas * 40 + 30
    posiciones = [ANCHO // 3, 2 * ANCHO // 3]

    for x in posiciones:
        pygame.draw.line(ventana, NEGRO,
                         (x, 60), (x, altura_tabla), 1)

# Estadisticas
def dibujar_encabezados_estadisticas(ventana: pygame.Surface, fuente: pygame.font.Font, fuente_datos: pygame.font.Font,
                                      margen_superior: int, celda_ancho: int, celda_alto: int) -> int:
    '''
    ¿Que hace? -> Dibuja los encabezados y subencabezados de las estadísticas en la ventana del juego.

    ¿Que parametros recibe?
        -ventana:pygame.Surface -> Superficie en la que se dibuja el botón.
        -fuente:pygame.font.Font -> La fuente que se utiliza para renderizar el texto en el botón.
        -fuente_datos: pygame.font.Font -> La fuente utilizada para renderizar los subencabezados.
        -margen_superior: int -> El margen superior que se debe dejar antes de dibujar los encabezados.
        -celda_ancho: int -> El ancho de cada celda.
        -celda_alto: int -> La altura de cada celda.

    ¿Que retorna?:int -> La posición Y donde deben comenzar a dibujarse las filas de datos después de los encabezados y subencabezados.
    '''
    # Encabezados principales
    encabezados = ["Preg N°", "", "Fácil", "",
                   "", "Normal", "", "", "Difícil", ""]
    colores_encabezados = [NEGRO, NEGRO, VERDE_OSCURO, NEGRO,
                           NEGRO, AMARILLO, NEGRO, NEGRO, ROJO, NEGRO]

    y_actual = margen_superior + 16
    for i, texto in enumerate(encabezados):
        x = i * celda_ancho
        render = fuente.render(texto, True, colores_encabezados[i])
        ventana.blit(render, render.get_rect(
            center=(x + celda_ancho // 2, y_actual)))

    # Subencabezados
    y_actual += celda_alto
    sub_encabezados = ["", "Total", "Aciertos", "Fallos", "Total",
                       "Aciertos", "Fallos", "Total", "Aciertos", "Fallos"]
    colores_sub_encabezados = [NEGRO, VERDE_OSCURO, VERDE_OSCURO, VERDE_OSCURO,
                               AMARILLO, AMARILLO, AMARILLO, ROJO, ROJO, ROJO]

    for i, texto in enumerate(sub_encabezados):
        x = i * celda_ancho
        render = fuente_datos.render(texto, True, colores_sub_encabezados[i])
        ventana.blit(render, render.get_rect(
            center=(x + celda_ancho // 2, y_actual)))

    return y_actual + celda_alto

def dibujar_filas_estadisticas(ventana: pygame.Surface, lista_estadisticas: list, fuente_datos: pygame.font.Font,
                                celda_ancho: int, celda_alto: int, y_inicial: int) -> None:
    '''
    ¿Que hace? -> Dibuja las filas de estadísticas en la ventana del juego.

    ¿Que parametros recibe?
        -ventana:pygame.Surface -> Superficie en la que se dibuja el botón.
        -lista_estadisticas: list -> Una lista de diccionarios que contienen las estadísticas de cada pregunta.
        -fuente_datos: pygame.font.Font -> La fuente utilizada para renderizar el texto de las estadísticas.
        -margen_superior: int -> El margen superior que se debe dejar antes de dibujar las estadísticas.
        -celda_ancho: int -> El ancho de cada celda.
        -celda_alto: int -> La altura de cada celda.
        -y_inicial: int -> La coordenada Y inicial donde comenzarán a dibujarse las filas de estadísticas.

    ¿Que retorna? -> Nada
    '''
    for estadistica in lista_estadisticas:
        fila = [
            estadistica['numero_pregunta'],
            estadistica['cantidad_preguntada_facil'], estadistica['cantidad_aciertos_facil'], estadistica['cantidad_fallos_facil'],
            estadistica['cantidad_preguntada_normal'], estadistica['cantidad_aciertos_normal'], estadistica['cantidad_fallos_normal'],
            estadistica['cantidad_preguntada_dificil'], estadistica['cantidad_aciertos_dificil'], estadistica['cantidad_fallos_dificil']
        ]
        for i, texto in enumerate(fila):
            x = i * celda_ancho
            render = fuente_datos.render(texto, True, NEGRO)
            ventana.blit(render, render.get_rect(
                center=(x + celda_ancho // 2, y_inicial)))
        y_inicial += celda_alto

# Partida
def inicializar_partida() -> dict:
    '''
    ¿Que hace? -> Inicializa una nueva partida con los valores de configuración traidos de un archivo CSV.

    ¿Que parametros recibe? -> Ninguno

    ¿Que retorna?:dict ->  Un diccionario con la configuración de la partida.
    '''
    configuraciones = convertir_csv_a_lista_diccionarios(RUTA_CONFIGURACIONES_CSV)
    dificultad = configuraciones[0]['valor_elegido'].strip("'")
    puntaje_por_acierto = int(configuraciones[1]['valor_elegido'])
    tiempo_por_pregunta = int(configuraciones[2]['valor_elegido'])
    vidas = int(configuraciones[3]['valor_elegido'])

    return {
        "dificultad": dificultad,
        "puntaje_por_acierto": puntaje_por_acierto,
        "tiempo_por_pregunta": tiempo_por_pregunta,
        "preguntas": filtrar_preguntas_por_dificultad(dificultad),
        "correctas": 0,
        "incorrectas": 0,
        "indice_pregunta": 0,
        "tiempo_utilizado": 0,
        "vidas": vidas
    }

def mostrar_pregunta(ventana: pygame.Surface, fuente: pygame.font.Font, pregunta: str) -> int:
    """
    ¿Que hace? -> Muestra una pregunta en la ventana de juego. Ajustada previamente si demasiado
    larga.

    ¿Que parametros recibe?
        -ventana:pygame.Surface -> Superficie en la que se dibuja el botón.
        -fuente:pygame.font.Font -> La fuente que se utiliza para renderizar el texto en el botón.
        -pregunta: str -> La pregunta a mostrar en pantalla.

    ¿Que retorna? -> La coordenada y donde se dibujó la última línea de la pregunta.
    """
    lineas_pregunta = ajustar_texto(pregunta, fuente, ANCHO - 100)
    y_actual = 120
    for linea in lineas_pregunta:
        texto_pregunta = fuente.render(linea, True, NEGRO)
        ventana.blit(texto_pregunta, (ANCHO // 2 -
                     texto_pregunta.get_width() // 2, y_actual))
        y_actual += texto_pregunta.get_height() + 10
    return y_actual

def manejar_respuesta(partida: dict, respuesta_usuario: str, respuesta_correcta: str) -> None:
    """
    ¿Que hace? -> Procesa la respuesta del usuario, actualizando la partida según si es correcta o incorrecta.

    ¿Que parametros recibe?
        -partida: dict -> Diccionario que contiene los datos de la partida, incluyendo estadísticas 
        como vidas, respuestas correctas e incorrectas.

        -respuesta_usuario: str -> La opción seleccionada por el usuario. Contemplando la posibilidad
        de que se le acabe el tiempo.

        -respuesta_correcta: str -> La respuesta correcta de la pregunta actual.

    ¿Que retorna? -> Nada
    """
    if respuesta_usuario == respuesta_correcta:
        partida["correctas"] += 1
        partida["datos_ranking"][str(partida["indice_pregunta"] + 1)] = 1
        pygame.mixer.Sound(RUTA_ACIERTO).play()
    else:
        partida["vidas"] -= 1
        partida["incorrectas"] += 1
        partida["datos_ranking"][str(partida["indice_pregunta"] + 1)] = 0
        pygame.mixer.Sound(RUTA_FALLO).play()

def modificar_ranking(datos_jugador: dict):
    '''
    ¿Que hace? -> Modifica el ranking de jugadores almacenado en un archivo CSV, reemplazando los datos del jugador con el menor puntaje
                    si el jugador actual tiene un puntaje mayor o, en caso de empate, un tiempo menor.

    ¿Que parametros recibe?
        -datos_jugador: dict -> Un diccionario que contiene la información del jugador a comparar y agregar el ranking si es el caso.

    ¿Que retorna? -> Nada
    '''
    lista = convertir_csv_a_lista_diccionarios(RUTA_RANKING_CSV)
    indice = buscar_menor_puntaje_ranking(lista)
    datos = lista[indice]

    if int(datos_jugador['puntaje']) > int(datos['puntaje']):
        lista[indice] = datos_jugador
    elif (int(datos_jugador['puntaje']) == int(datos['puntaje']) and
          int(datos_jugador['tiempo']) < int(datos['tiempo'])):
        lista[indice] = datos_jugador

    lista = ordenar_lista_diccionarios(lista)
    convertir_lista_diccionarios_a_csv(lista, RUTA_RANKING_CSV)

def modificar_estadisticas(diccionario: dict):
    '''
    ¿Que hace? -> Modifica las estadísticas de las preguntas en función de las respuestas de un jugador,
                actualizando los conteos de aciertos y fallos por dificultad en el archivo CSV de estadísticas.

    ¿Que parametros recibe?
        -diccionario: dict -> Un diccionario que contiene la respuesta del jugador a las preguntas,
                                así como la dificultad de cada pregunta.

    ¿Que retorna? -> Nada
    '''
    lista_estadisticas = convertir_csv_a_lista_diccionarios(
        'csv/estadisticas.csv')

    for pregunta in lista_estadisticas:
        numero_pregunta = pregunta['numero_pregunta']
        dificultad = diccionario['dificultad']

        if numero_pregunta in diccionario:
            respuesta = diccionario[numero_pregunta]

            if dificultad == 'facil':
                if respuesta == 1:
                    pregunta['cantidad_preguntada_facil'] = str(
                        int(pregunta['cantidad_preguntada_facil']) + 1)
                    pregunta['cantidad_aciertos_facil'] = str(
                        int(pregunta['cantidad_aciertos_facil']) + 1)
                elif respuesta == 0:
                    pregunta['cantidad_preguntada_facil'] = str(
                        int(pregunta['cantidad_preguntada_facil']) + 1)
                    pregunta['cantidad_fallos_facil'] = str(
                        int(pregunta['cantidad_fallos_facil']) + 1)

            elif dificultad == 'normal':
                if respuesta == 1:
                    pregunta['cantidad_preguntada_normal'] = str(
                        int(pregunta['cantidad_preguntada_normal']) + 1)
                    pregunta['cantidad_aciertos_normal'] = str(
                        int(pregunta['cantidad_aciertos_normal']) + 1)
                elif respuesta == 0:
                    pregunta['cantidad_preguntada_normal'] = str(
                        int(pregunta['cantidad_preguntada_normal']) + 1)
                    pregunta['cantidad_fallos_normal'] = str(
                        int(pregunta['cantidad_fallos_normal']) + 1)

            elif dificultad == 'dificil':
                if respuesta == 1:
                    pregunta['cantidad_preguntada_dificil'] = str(
                        int(pregunta['cantidad_preguntada_dificil']) + 1)
                    pregunta['cantidad_aciertos_dificil'] = str(
                        int(pregunta['cantidad_aciertos_dificil']) + 1)
                elif respuesta == 0:
                    pregunta['cantidad_preguntada_dificil'] = str(
                        int(pregunta['cantidad_preguntada_dificil']) + 1)
                    pregunta['cantidad_fallos_dificil'] = str(
                        int(pregunta['cantidad_fallos_dificil']) + 1)

    convertir_lista_diccionarios_a_csv(
        lista_estadisticas, 'csv/estadisticas.csv')

def pedir_nombre_usuario(ventana: pygame.Surface, fuente: pygame.font.Font, cantidad_respuestas_correctas: int, total: int):
    '''
    ¿Que hace? -> Muestra una pantalla en la que se solicita al usuario ingresar su nombre y muestra su puntaje final.

    ¿Que parametros recibe?
        -ventana:pygame.Surface -> Superficie en la que se dibuja el botón.
        -fuente:pygame.font.Font -> La fuente que se utiliza para renderizar el texto en el botón.
        -cantidad_respuestas_correctas:int -> El número de respuestas correctas del usuario.
        -total:int -> El número total de preguntas o respuestas.

    ¿Que retorna?:str -> El nombre ingresado por el usuario como una cadena de texto.
    '''
    nombre_ingresado = ""
    bandera_pedir_nombre = True

    while bandera_pedir_nombre:

        ventana.fill(NEGRO)
        # Mostrar puntaje final
        resultado_texto = fuente.render(
            f"Puntaje final: {cantidad_respuestas_correctas}/{total}", True, BLANCO)
        ventana.blit(resultado_texto, (DIMENSIONES_VENTANA[0] // 2 - resultado_texto.get_width(
        ) // 2, (DIMENSIONES_VENTANA[1] // 3 - 50)))

        mensaje = fuente.render("Ingrese su nombre:", True, BLANCO)
        ventana.blit(
            mensaje, (DIMENSIONES_VENTANA[0] // 2 - mensaje.get_width() // 2, DIMENSIONES_VENTANA[1] // 3))

        nombre_texto = fuente.render(nombre_ingresado, True, ROJO)
        ventana.blit(
            nombre_texto, (DIMENSIONES_VENTANA[0] // 2 - nombre_texto.get_width() // 2, DIMENSIONES_VENTANA[1] // 2))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    bandera_pedir_nombre = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre_ingresado = nombre_ingresado[:-1]
                else:
                    nombre_ingresado += evento.unicode

    return nombre_ingresado
