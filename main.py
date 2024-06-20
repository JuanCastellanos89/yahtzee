import random
import matplotlib.pyplot as plt

# Función para lanzar dados y obtener valores aleatorios entre 1 y 6 para num_dados dados.
def lanzar_dados(num_dados=5):
    return [random.randint(1, 6) for _ in range(num_dados)]

# Funciones para verificar combinaciones específicas en los dados obtenidos.

# Función para verificar si todos los dados son iguales (Yahtzee).
def es_yahtzee(dados):
    return len(set(dados)) == 1

# Función para verificar si se obtiene un Full House (un trio y un par).
def es_fullHouse(dados):
    conteo = {valor: dados.count(valor) for valor in set(dados)}
    valores_conteo = list(conteo.values())
    return sorted(valores_conteo) == [2, 3]

# Función para verificar si se obtiene un Poker (cuatro dados iguales).
def es_poker(dados):
    conteo = {valor: dados.count(valor) for valor in set(dados)}
    valores_conteo = list(conteo.values())
    return 4 in valores_conteo

# Función para verificar si se obtiene una Escalera Mayor (cinco dados consecutivos).
def es_escalera_mayor(dados):
    return sorted(dados) in [list(range(1, 6)), list(range(2, 7))]

# Función para verificar si se obtiene una Escalera Menor (cuatro dados consecutivos).
def es_escalera_menor(dados):
    sorted_dados = sorted(dados)
    return sorted_dados in [list(range(1, 5)) + [sorted_dados[-1]], [sorted_dados[0]] + list(range(2, 6))]

# Función para simular el turno de un jugador, deteniéndose si se logra una combinación deseada en los primeros dos lanzamientos.
def turno_jugador(objetivos):
    dados = lanzar_dados()
    num_lanzamientos = 1

    while num_lanzamientos < 3:
        nuevos_dados = lanzar_dados(5)
        dados = nuevos_dados
        
        for objetivo in objetivos:
            if objetivo(dados):
                return dados
        
        num_lanzamientos += 1

    return dados

# Función para simular una partida completa entre dos jugadores.
def simular_partida(num_simulaciones, objetivos):
    resultados_jugador1 = []
    resultados_jugador2 = []

    exitos_jugador1 = {objetivo.__name__: 0 for objetivo in objetivos}
    exitos_jugador2 = {objetivo.__name__: 0 for objetivo in objetivos}

    for _ in range(num_simulaciones):
        dados_j1 = turno_jugador(objetivos)
        dados_j2 = turno_jugador(objetivos)

        resultados_jugador1.append(dados_j1)
        resultados_jugador2.append(dados_j2)

        for objetivo in objetivos:
            if objetivo(dados_j1):
                exitos_jugador1[objetivo.__name__] += 1
            if objetivo(dados_j2):
                exitos_jugador2[objetivo.__name__] += 1

    return (exitos_jugador1, resultados_jugador1), (exitos_jugador2, resultados_jugador2)

# Función para generar histogramas que visualizan la frecuencia de cada combinación obtenida por los jugadores.
def generar_histograma(resultados, titulo):
    conteos = [tuple(sorted(dados)) for dados in resultados]
    frecuencia = {k: conteos.count(k) for k in set(conteos)}
    
    keys = list(map(str, frecuencia.keys()))
    values = list(frecuencia.values())

    plt.figure(figsize=(10, 6))
    plt.bar(keys, values)
    plt.xlabel('Combinaciones de dados')
    plt.ylabel('Frecuencia')
    plt.title(titulo)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

# Función principal que ejecuta la simulación y muestra los resultados.
def main():
    num_simulaciones = 100000

    # Definir los objetivos a buscar en cada turno
    objetivos = [es_yahtzee, es_fullHouse, es_poker, es_escalera_mayor, es_escalera_menor]

    # Simulación de la partida
    (exitos_j1, resultados_j1), (exitos_j2, resultados_j2) = simular_partida(num_simulaciones, objetivos)

    # Imprimir resultados y generar histogramas
    for objetivo in objetivos:
        nombre_objetivo = objetivo.__name__
        total_exitos_j1 = exitos_j1[nombre_objetivo]
        total_exitos_j2 = exitos_j2[nombre_objetivo]
        
        # Resultados jugador 1
        print(f"Total {nombre_objetivo} Jugador 1: {total_exitos_j1}")
        print(f"Probabilidad de {nombre_objetivo} Jugador 1: {total_exitos_j1 / num_simulaciones:.6f}")
        generar_histograma([resultados for resultados in resultados_j1 if objetivo(resultados)], f"Histograma de {nombre_objetivo} - Jugador 1")

        # Resultados jugador 2
        print(f"Total {nombre_objetivo} Jugador 2: {total_exitos_j2}")
        print(f"Probabilidad de {nombre_objetivo} Jugador 2: {total_exitos_j2 / num_simulaciones:.6f}")
        generar_histograma([resultados for resultados in resultados_j2 if objetivo(resultados)], f"Histograma de {nombre_objetivo} - Jugador 2")
        print()

if __name__ == "__main__":
    main()
