import pygame
from package.constantes import *
from package.funciones_generales import *
from package.funciones_especificas import *
from package.pantallas import *
from pygame import *


pygame.init()
pygame.mixer.init()

ventana = pygame.display.set_mode(DIMENSIONES_VENTANA)
pygame.display.set_caption("Preguntados")

cargar_sonido(RUTA_SONIDO_MENU)
fondo = cargar_fondo(RUTA_FONDO_MENU,DIMENSIONES_VENTANA)
fuente = pygame.font.Font(None, 48)

botones_menu_principal = crear_botones(OPCIONES_MENU, ALTO_BOTON_MENU,
                                        ANCHO_BOTON_MENU, ESPACIADO_BOTON_MENU)

iniciado = True
mostrar_ranking = False
mostrar_configuraciones = False
mostrar_partida = False
mostrar_cambiar_dificultad = False
mostrar_cambiar_puntaje = False
mostrar_cambiar_tiempo = False
mostrar_cambiar_vidas = False
mostrar_estadisticas = False

while iniciado:
    for evento in pygame.event.get():
        if evento.type == QUIT:
            iniciado = False

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if mostrar_ranking:
                rect_boton_volver = dibujar_ranking(ventana, fuente)
                if rect_boton_volver.collidepoint(evento.pos):
                    mostrar_ranking = False

            elif mostrar_configuraciones:
                rect_boton_volver, botones = dibujar_configuraciones(
                    ventana, fuente)
                if rect_boton_volver.collidepoint(evento.pos):
                    mostrar_configuraciones = False
                boton_clickeado = manejar_click_botones(botones)
                if boton_clickeado:
                    match boton_clickeado:
                        case "Cambiar dificultad":
                            dibujar_cambiar_dificultad(ventana, fuente)
                            mostrar_configuraciones = False
                            mostrar_cambiar_dificultad = True
                        case "Cambiar puntaje":
                            dibujar_cambiar_puntaje(ventana, fuente)
                            mostrar_configuraciones = False
                            mostrar_cambiar_puntaje = True
                        case "Cambiar tiempo":
                            dibujar_cambiar_tiempo(ventana, fuente)
                            mostrar_configuraciones = False
                            mostrar_cambiar_tiempo = True
                        case"Cambiar vidas":
                            dibujar_cambiar_vidas(ventana, fuente)
                            mostrar_configuraciones = False
                            mostrar_cambiar_vidas = True

            elif mostrar_cambiar_dificultad:
                botones = dibujar_cambiar_dificultad(ventana, fuente)
                boton_clickeado = manejar_click_botones(botones)
                if boton_clickeado:
                    cambiar_configuracion(
                        'dificultad_elegida', boton_clickeado)
                    mostrar_cambiar_dificultad = False
                    mostrar_configuraciones = True

            elif mostrar_cambiar_puntaje:
                botones = dibujar_cambiar_puntaje(ventana, fuente)
                boton_clickeado = manejar_click_botones(botones)
                if boton_clickeado:
                    boton_clickeado = boton_clickeado.split(
                        ":")[1].strip().split()[0]
                    cambiar_configuracion(
                        'puntaje_por_respuesta_correcta', boton_clickeado)
                    mostrar_cambiar_puntaje = False
                    mostrar_configuraciones = True

            elif mostrar_cambiar_tiempo:
                botones = dibujar_cambiar_tiempo(ventana, fuente)
                boton_clickeado = manejar_click_botones(botones)
                if boton_clickeado:
                    cambiar_configuracion(
                        'tiempo_para_responder', boton_clickeado)
                    mostrar_cambiar_tiempo = False
                    mostrar_configuraciones = True

            elif mostrar_cambiar_vidas:
                botones = dibujar_cambiar_vidas(ventana, fuente)
                boton_clickeado = manejar_click_botones(botones)
                if boton_clickeado:
                    cambiar_configuracion(
                        'vidas', boton_clickeado)
                    mostrar_cambiar_vidas = False
                    mostrar_configuraciones = True

            elif mostrar_estadisticas:
                rect_boton_volver = dibujar_estadisticas(ventana, fuente)
                if rect_boton_volver.collidepoint(evento.pos):
                    mostrar_estadisticas = False

            else:
                boton_clickeado = manejar_click_botones(botones_menu_principal)
                if boton_clickeado:
                    match boton_clickeado:
                        case "Jugar Partida":
                            dibujar_partida(ventana, fuente)
                            mostrar_partida = False
                        case "Ranking":
                            mostrar_ranking = True
                        case "Configuración":
                            mostrar_configuraciones = True
                        case "Estadísticas":
                            mostrar_estadisticas = True
                        case "Salir":
                            iniciado = False

    ventana.blit(fondo, (0, 0))

    if mostrar_ranking:
        dibujar_ranking(ventana, fuente)
    elif mostrar_configuraciones:
        dibujar_configuraciones(ventana, fuente)
    elif mostrar_cambiar_dificultad:
        dibujar_cambiar_dificultad(ventana, fuente)
    elif mostrar_cambiar_puntaje:
        dibujar_cambiar_puntaje(ventana, fuente)
    elif mostrar_cambiar_tiempo:
        dibujar_cambiar_tiempo(ventana, fuente)
    elif mostrar_cambiar_vidas:
        dibujar_cambiar_vidas(ventana, fuente)
    elif mostrar_estadisticas:
        dibujar_estadisticas(ventana, fuente)
    else:
        dibujar_botones(ventana, botones_menu_principal, fuente)

    pygame.display.flip()

pygame.quit()

