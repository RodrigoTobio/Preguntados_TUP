import pygame
from package.constantes import *
from pygame import *
from package.funciones_generales import *
from package.funciones_especificas import *


#Pantalla partida
def dibujar_partida(ventana: pygame.Surface, fuente: pygame.font.Font) -> pygame.rect.Rect:
    '''
    ¿Que hace? -> Dibuja la pantalla de la partida en curso, mostrando las preguntas, opciones, el temporizador,
    las vidas y manejando la interacción del usuario con las opciones. La función también se encarga de verificar
    el tiempo restante y actualizar el puntaje y las estadísticas del jugador.
    La partida continúa hasta que el jugador responde todas las preguntas o se queda sin vidas.
    Si el jugador se queda sin vidas, se muestra una pantalla de "Game Over"
    y luego se guarda el puntaje en el ranking.

    ¿Que parametros recibe?
        -ventana:pygame.Surface -> Superficie en la que se dibuja el botón.
        -fuente:pygame.font.Font -> La fuente que se utiliza para renderizar el texto en el botón.

    ¿Que retorna?: pygame.rect.Rect -> Un rectángulo que representa el botón de volver.
    '''
    partida = inicializar_partida()
    partida["datos_ranking"] = {"dificultad": partida["dificultad"]}
    pygame.mixer.init()

    fondo = cargar_fondo(RUTA_FONDO_CELESTE, DIMENSIONES_VENTANA)

    imagen_game_over = pygame.image.load(RUTA_IMAGEN_GAME_OVER)
    imagen_game_over = pygame.transform.scale(imagen_game_over, DIMENSIONES_VENTANA)

    while partida["indice_pregunta"] < len(partida["preguntas"]) and partida["vidas"] > 0:
        pregunta_actual = partida["preguntas"][partida["indice_pregunta"]]

        ventana.blit(fondo, (0, 0))

        y_actual = mostrar_pregunta(ventana, fuente, pregunta_actual['pregunta'])

        opciones = pregunta_actual['opciones'].split(';')
        botones_opciones = crear_botones(
            opciones, ALTO_BOTON_MENU, ANCHO_BOTON_MENU, ESPACIADO_BOTON_MENU, opcional=60)
        dibujar_botones(ventana, botones_opciones, fuente, color_borde=NEGRO)

        texto_vidas = fuente.render(f"Vidas: {partida['vidas']}", True, NEGRO)
        ventana.blit(texto_vidas, (10, 10))

        pygame.display.flip()

        respuesta_usuario = None
        tiempo_inicio = pygame.time.get_ticks()

        while respuesta_usuario is None and partida["vidas"] > 0:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    respuesta_usuario = manejar_click_botones(botones_opciones)

            tiempo_actual = pygame.time.get_ticks()
            tiempo_restante = max(
                0, partida["tiempo_por_pregunta"] - (tiempo_actual - tiempo_inicio) // 1000)

            if tiempo_restante == 0:
                manejar_respuesta(partida, None, pregunta_actual['respuesta_correcta'])
                partida["indice_pregunta"] += 1
                break

            ventana.blit(fondo, (0, 0))
            mostrar_pregunta(ventana, fuente, pregunta_actual['pregunta'])
            dibujar_botones(ventana, botones_opciones, fuente, color_borde=NEGRO)
            ventana.blit(texto_vidas, (10, 10))

            rect_tiempo = pygame.Rect(ANCHO - 150, 10, 140, 30)
            ventana.blit(fondo, rect_tiempo, rect_tiempo)

            texto_tiempo = fuente.render(f"{tiempo_restante}", True, NEGRO)
            ventana.blit(texto_tiempo, (ANCHO - texto_tiempo.get_width() - 20, 10))
            pygame.display.flip()

        if tiempo_restante > 0:
            partida["tiempo_utilizado"] += (pygame.time.get_ticks() - tiempo_inicio) // 1000
            manejar_respuesta(partida, respuesta_usuario, pregunta_actual['respuesta_correcta'])
            partida["indice_pregunta"] += 1

    if partida["vidas"] <= 0:
        ventana.blit(imagen_game_over, (0, 0))
        pygame.display.flip()
        pygame.time.delay(1500)

    nombre_usuario = pedir_nombre_usuario(
        ventana, fuente, partida["correctas"], len(partida["preguntas"]))
    puntaje_jugador = partida["correctas"] * partida["puntaje_por_acierto"]
    datos_jugador = {"usuario": nombre_usuario, "puntaje": str(puntaje_jugador),
                     "tiempo": str(partida["tiempo_utilizado"])}

    modificar_ranking(datos_jugador)
    modificar_estadisticas(partida["datos_ranking"])
    boton_volver = crear_boton_menu(ventana, fuente)

    pygame.display.flip()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            if evento.type == pygame.MOUSEBUTTONDOWN and boton_volver.collidepoint(evento.pos):
                return boton_volver

# Pantalla de ranking
def dibujar_ranking(ventana: pygame.Surface, fuente: pygame.font.Font) -> pygame.rect.Rect:
    '''
    ¿Que hace? -> Dibuja la pantalla del ranking de los jugadores, mostrando una lista 
    de los mejores puntajes junto con los tiempos.
    
    ¿Que parametros recibe?
        -ventana:pygame.Surface -> Superficie en la que se dibuja el botón.
        -fuente:pygame.font.Font -> La fuente que se utiliza para renderizar el texto en el botón.

    ¿Que retorna?: pygame.rect.Rect -> Un rectángulo que representa el botón de volver.
    '''
    lista_ranking = cargar_ranking()

    fondo = cargar_fondo(RUTA_FONDO_CELESTE, DIMENSIONES_VENTANA)
    ventana.blit(fondo, (0, 0))

    y_inicial = 60
    y_inicial = dibujar_encabezados_ranking(ventana, fuente, y_inicial)

    dibujar_filas_ranking(ventana, fuente, lista_ranking, y_inicial)

    dibujar_divisiones_ranking(ventana, 60, len(lista_ranking))

    boton_volver = crear_boton_menu(ventana, fuente)

    return boton_volver

#Pantalla estadisticas
def dibujar_estadisticas(ventana: pygame.Surface, fuente: pygame.font.Font) -> pygame.rect.Rect:
    '''
    ¿Que hace? -> Dibuja la pantalla de estadísticas del juego, traidas desde un archivo CSV.

    ¿Que parametros recibe?
        -ventana:pygame.Surface -> Superficie en la que se dibuja el botón.
        -fuente:pygame.font.Font -> La fuente que se utiliza para renderizar el texto en el botón.

    ¿Que retorna?: pygame.rect.Rect -> Un rectángulo que representa el botón de volver.
    '''
    pygame.init()
    fuente_encabezado = pygame.font.SysFont('Verdana', 18, bold=True)
    fuente_datos = pygame.font.SysFont('Verdana', 16, bold=True)

    lista_estadisticas = convertir_csv_a_lista_diccionarios('csv/estadisticas.csv')

    margen_superior = 50
    celda_ancho = ANCHO // 10
    celda_alto = 35

    fondo = cargar_fondo(RUTA_FONDO_CELESTE, DIMENSIONES_VENTANA)
    ventana.blit(fondo, (0, 0))

    y_actual = dibujar_encabezados_estadisticas(ventana, fuente_encabezado, fuente_datos,
                                                 margen_superior, celda_ancho, celda_alto)

    dibujar_filas_estadisticas(ventana, lista_estadisticas, fuente_datos,celda_ancho,
                                celda_alto, y_actual)

    for fila in range(len(lista_estadisticas) + 3):
        pygame.draw.line(ventana, NEGRO, (0, margen_superior + fila * celda_alto),
                         (ANCHO, margen_superior + fila * celda_alto))

    altura_tabla = margen_superior + ((len(lista_estadisticas) + 2) * celda_alto)
    
    for columna in range(11):
        pygame.draw.line(ventana, NEGRO,
                         (columna * celda_ancho, margen_superior),
                         (columna * celda_ancho, altura_tabla))

    boton_volver = crear_boton_menu(ventana, fuente)

    return boton_volver

# Pantalla de configuraciones
def dibujar_configuraciones(ventana: pygame.Surface, fuente: pygame.font.Font) -> tuple[pygame.rect.Rect, list[pygame.rect.Rect]]:
    '''
    ¿Que hace? -> Dibuja la pantalla de configuraciones del juego, pantalla con botones que permiten al 
    jugador modificar diferentes configuraciones del juego.

    ¿Que parametros recibe?
        -ventana:pygame.Surface -> Superficie en la que se dibuja el botón.
        -fuente:pygame.font.Font -> La fuente que se utiliza para renderizar el texto en el botón.

    ¿Que retorna?: tuple[pygame.rect.Rect, list[pygame.rect.Rect]] -> Una tupla con el botón volver y
    una lista de los botones de configuración
    '''
    fondo = cargar_fondo(RUTA_FONDO_CONFIGURACION, DIMENSIONES_VENTANA)
    configurar_pantalla_base(
        ventana, fondo, "Configuraciones", pygame.font.Font(None, 60))

    opciones = ["Cambiar dificultad", "Cambiar puntaje", "Cambiar tiempo", "Cambiar vidas"]
    botones_opciones = crear_botones(opciones, 50, 320, 20)
    dibujar_botones(ventana, botones_opciones, fuente)

    boton_volver = crear_boton_menu(ventana, fuente)
    return boton_volver, botones_opciones

# Pantalla de cambiar dificultad
def dibujar_cambiar_dificultad(ventana: pygame.Surface, fuente: pygame.font.Font) -> list[pygame.rect.Rect]:
    '''
    ¿Que hace? -> Dibuja la pantalla de configuración para cambiar la dificultad,
    se carga el fondo, se configura la pantalla base, y se crean y dibujan botones.

    ¿Que parametros recibe?
        -ventana:pygame.Surface -> Superficie en la que se dibuja el botón.
        -fuente:pygame.font.Font -> La fuente que se utiliza para renderizar el texto en el botón.

    ¿Que retorna?: list[pygame.rect.Rect] -> Una lista de rectángulos (botones) que representan
    las opciones de dificultad.
    '''
    fondo = cargar_fondo(RUTA_FONDO_CONFIGURACION, DIMENSIONES_VENTANA)
    configurar_pantalla_base(ventana, fondo, "Configuraciones", fuente)

    opciones = ["facil", "normal", "dificil"]
    botones_opciones = crear_botones(opciones, 50, 200, 20)
    dibujar_botones(ventana, botones_opciones, fuente)

    return botones_opciones

# Pantalla de cambiar puntaje
def dibujar_cambiar_puntaje(ventana: pygame.Surface, fuente: pygame.font.Font) -> list[pygame.rect.Rect]:
    '''
    ¿Que hace? -> Dibuja la pantalla de configuración para cambiar puntaje escalado por dificultad,
    se carga el fondo, se configura la pantalla base, y se crean y dibujan botones.

    ¿Que parametros recibe?
        -ventana:pygame.Surface -> Superficie en la que se dibuja el botón.
        -fuente:pygame.font.Font -> La fuente que se utiliza para renderizar el texto en el botón.

    ¿Que retorna?: list[pygame.rect.Rect] -> Una lista de rectángulos (botones) que representan
    las opciones de puntaje.
    '''
    fondo = cargar_fondo(RUTA_FONDO_CONFIGURACION, DIMENSIONES_VENTANA)
    configurar_pantalla_base(
        ventana, fondo, "Puntaje por respuesta correcta", fuente)

    opciones = [
        "Facil: 1   Normal: 2   Dificil: 3", "Facil: 2   Normal: 3   Dificil: 4",
        "Facil: 3   Normal: 4   Dificil: 5", "Facil: 4   Normal: 5   Dificil: 6",
        "Facil: 5   Normal: 6   Dificil: 7"
    ]
    botones_opciones = crear_botones(opciones, 45, 500, 20)
    dibujar_botones(ventana, botones_opciones, fuente)

    return botones_opciones

# Pantalla de cambiar tiempo
def dibujar_cambiar_tiempo(ventana: pygame.Surface, fuente: pygame.font.Font) -> list[pygame.rect.Rect]:
    '''
    ¿Que hace? -> Dibuja la pantalla de configuración para cambiar el tiempo de respuesta,
    se carga el fondo, se configura la pantalla base, y se crean y dibujan botones.

    ¿Que parametros recibe?
        -ventana:pygame.Surface -> Superficie en la que se dibuja el botón.
        -fuente:pygame.font.Font -> La fuente que se utiliza para renderizar el texto en el botón.

    ¿Que retorna?: list[pygame.rect.Rect] -> Una lista de rectángulos (botones) que representan
    las opciones de tiempo de respuesta.
    '''
    fondo = cargar_fondo(RUTA_FONDO_CONFIGURACION, DIMENSIONES_VENTANA)
    configurar_pantalla_base(
        ventana, fondo, "Tiempo para responder en Segundos", fuente)

    opciones = ["5", "10", "15", "20", "25", "30"]
    botones_opciones = crear_botones(opciones, 45, 90, 5)
    dibujar_botones(ventana, botones_opciones, fuente)

    return botones_opciones

# Pantalla de cambiar cantidad de vidas
def dibujar_cambiar_vidas(ventana: pygame.Surface, fuente: pygame.font.Font) -> list[pygame.rect.Rect]:
    '''
    ¿Que hace? -> Dibuja la pantalla de configuración para cambiar la cantidad de vidas,
    se carga el fondo, se configura la pantalla base, y se crean y dibujan botones.

    ¿Que parametros recibe?
        -ventana:pygame.Surface -> Superficie en la que se dibuja el botón.
        -fuente:pygame.font.Font -> La fuente que se utiliza para renderizar el texto en el botón.

    ¿Que retorna?: list[pygame.rect.Rect] -> Una lista de rectángulos (botones) que representan
    las opciones de cantidad de vidas.
    '''
    fondo = cargar_fondo(RUTA_FONDO_CONFIGURACION, DIMENSIONES_VENTANA)
    configurar_pantalla_base(
        ventana, fondo, "Cantidad de vidas", fuente)

    opciones = ["1", "2", "3", "4", "5"]
    botones_opciones = crear_botones(opciones, 45, 90, 5)
    dibujar_botones(ventana, botones_opciones, fuente)

    return botones_opciones
