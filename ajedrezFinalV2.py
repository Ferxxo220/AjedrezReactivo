import copy
import random

class Ajedrez:
    def __init__(self):
        self.tablero = [
            ["🏤", "🐴", "🎩", "👩", "👑", "🎩", "🐴", "🏤"],  
            ["⚫", "⚫", "⚫", "⚫", "⚫", "⚫", "⚫", "⚫"],                                          
            ["⬜","⬛","⬜","⬛","⬜","⬛","⬜","⬛"],           
            ["⬛","⬜","⬛","⬜","⬛","⬜","⬛","⬜"],
            ["⬜","⬛","⬜","⬛","⬜","⬛","⬜","⬛"],
            ["⬛","⬜","⬛","⬜","⬛","⬜","⬛","⬜"],
            ["⚪", "⚪", "⚪", "⚪", "⚪", "⚪", "⚪", "⚪"],  
            ["🏰", "🎠", "⛪", "👸", "🤴", "⛪", "🎠", "🏰"]   
        ]
        
        self.blancas = ["🏰","🎠","⛪","👸","🤴","⚪"]
        self.negras = ["🏤","🐴","🎩","👩","👑","⚫"]
        self.columnas = ["a","b","c","d","e","f","g","h"]
        self.turno_negras = False
        self.game = True


    def ImprimirTablero(self, tablero=None):
        if tablero is None:
            tablero = self.tablero
        for i in range(8):
            print(8-i, end=" ")  
            for j in range(8):
                print(tablero[i][j], end=" ")
            print()
        print("  " + "  ".join(self.columnas))
        print()


    def ajedrez_a_matriz(self, pos):
        if len(pos) < 2:
            raise ValueError("Coordenada incompleta")
        columna = pos[0].lower()
        try:
            fila = int(pos[1])
        except ValueError:
            raise ValueError("La fila debe ser un número")
        if columna < 'a' or columna > 'h' or fila < 1 or fila > 8:
            raise ValueError("Coordenada fuera del rango del tablero")
        fila_matriz = 8 - fila
        columna_matriz = ord(columna) - ord('a')
        return fila_matriz, columna_matriz


    def sinPiezas(self, x1, y1, x2, y2, tablero=None):
        if tablero is None:
            tablero = self.tablero
        dx = (x2 - x1) // max(1, abs(x2 - x1)) if x2 != x1 else 0
        dy = (y2 - y1) // max(1, abs(y2 - y1)) if y2 != y1 else 0
        x, y = x1 + dx, y1 + dy
        while (x, y) != (x2, y2):
            if tablero[x][y] not in ["⬜","⬛"]:
                return False
            x += dx
            y += dy
        return True


    def es_movimiento_valido(self, pieza, x1, y1, x2, y2, tablero=None):
        if tablero is None:
            tablero = self.tablero
        dx = x2 - x1
        dy = y2 - y1
        destino = tablero[x2][y2]

        if dx == 0 and dy == 0:
            return False

        if pieza in self.blancas and destino in self.blancas:
            return False
        if pieza in self.negras and destino in self.negras:
            return False

        if pieza == "⚪":
            if x1 == 6 and dx == -2 and dy == 0 and tablero[x2][y2] in ["⬜","⬛"]:
                return True
            if dx == -1 and dy == 0 and tablero[x2][y2] in ["⬜","⬛"]:
                return True
            if dx == -1 and abs(dy) == 1 and tablero[x2][y2] in self.negras:
                return True
            return False

        if pieza == "⚫":
            if x1 == 1 and dx == 2 and dy == 0 and tablero[x2][y2] in ["⬜","⬛"]:
                return True
            if dx == 1 and dy == 0 and tablero[x2][y2] in ["⬜","⬛"]:
                return True
            if dx == 1 and abs(dy) == 1 and tablero[x2][y2] in self.blancas:
                return True
            return False

        if pieza in ["🏰","🏤"]:
            if dx == 0 or dy == 0:
                return self.sinPiezas(x1, y1, x2, y2, tablero)
            return False

        if pieza in ["🎠","🐴"]:
            return (abs(dx), abs(dy)) in [(2,1), (1,2)]

        if pieza in ["⛪","🎩"]:
            if abs(dx) == abs(dy):
                return self.sinPiezas(x1, y1, x2, y2, tablero)
            return False

        if pieza in ["👸","👩"]:
            if dx == 0 or dy == 0 or abs(dx) == abs(dy):
                return self.sinPiezas(x1, y1, x2, y2, tablero)
            return False

        if pieza in ["🤴","👑"]:
            return abs(dx) <= 1 and abs(dy) <= 1

        return False


    def tirar(self, origen, destino, color):
        try:
            x1, y1 = self.ajedrez_a_matriz(origen)
            x2, y2 = self.ajedrez_a_matriz(destino)
        except ValueError as e:
            print(f"❌ {e}")
            return False

        pieza = self.tablero[x1][y1]

        if pieza in ["⬜", "⬛"]:
            print("No hay pieza en la casilla de origen")
            return False

        if color == "blancas" and pieza not in self.blancas:
            print("Esa no es tu pieza")
            return False
        if color == "negras" and pieza not in self.negras:
            print("Esa no es tu pieza")
            return False

        if not self.es_movimiento_valido(pieza, x1, y1, x2, y2):
            print("Movimiento invalido para esa pieza")
            return False

        if self.tablero[x2][y2] in ["🤴","👑"]:
            print("🏁 ¡¡JAQUE!!")
            self.game = False

        if color == "negras":
            if pieza in ["🏰","🎠","⛪","👸","🤴","⚪"]:
                return False

        self.tablero[x2][y2] = pieza
        self.tablero[x1][y1] = "⬜" if (x1 + y1) % 2 == 0 else "⬛"
        return True


    def agente_blanco(self):
        movimientos_captura = []
        movimientos_normales = []

        for x in range(8):
            for y in range(8):
                pieza = self.tablero[x][y]
                if pieza in self.blancas:
                    for i in range(8):
                        for j in range(8):
                            if self.es_movimiento_valido(pieza, x, y, i, j):
                                origen = f"{self.columnas[y]}{8-x}"
                                destino = f"{self.columnas[j]}{8-i}"
                                if self.tablero[i][j] in self.negras:
                                    movimientos_captura.append((origen, destino))
                                else:
                                    movimientos_normales.append((origen, destino))

        if movimientos_captura:
            movimiento = random.choice(movimientos_captura)
            print(f"El agente blanco come con {movimiento[0]} -> {movimiento[1]}")
        elif movimientos_normales:
            movimiento = random.choice(movimientos_normales)
            print(f"El agente blanco mueve aleatoriamente {movimiento[0]} -> {movimiento[1]}")
        else:
            print("No hay movimientos posibles para las blancas.")
            return False

        return self.tirar(movimiento[0], movimiento[1], "blancas")


    def jugar(self):
        while self.game:
            color = "negras" if self.turno_negras else "blancas"
            print(f"----- Turno de {color.upper()} -----")
            self.ImprimirTablero()

            if color == "blancas":  
                exito = self.agente_blanco()
            else:
                exito = False
                while not exito:
                    origen = input("Ingresa la casilla de origen (ej: e7): ").strip()
                    destino = input("Ingresa la casilla de destino (ej: e5): ").strip()
                    exito = self.tirar(origen, destino, color)
                    if not exito:
                        print("Intenta de nuevo.\n")

            if exito:
                self.turno_negras = not self.turno_negras



juego = Ajedrez()
juego.jugar()
