from game_modules.game import GameManager

# Importante: Utilizar una version reciente de python, superior a 3.5
# Importante: Para no saturar el archivo principal:
# La administracion del juego debe realizarse en el archivo /game_modules/game.py
# El juego se inicia llamando la funcion start_game del modulo game_modules.game que representa el archivo /game_modules/game.py 
# Los niveles deben crearse como archivos .py en la carpeta /levels
# En el archivo del nivel debe existir una funcion llamada create_level() que retornara el LevelWorsSpace del nivel 
# Ademas los modulos deben estar en la carpeta /game_modules para mantener en orden los archivos del juego
# Aún falta terminar textos o menus contextuales
# La hitbox falla cuando tocas el limite izquierdo y cuando el nivel cambia de posicion, utiliza las transiciones con cuidado

game = GameManager(FPS=60)

game.start_game()
