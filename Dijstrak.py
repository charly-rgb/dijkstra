from flask import Flask, render_template, jsonify
import sys

app = Flask(__name__)

def dijkstra(grafo, nodo_inicial):
    etiquetas = {}
    visitados = []
    pendientes = [nodo_inicial]
    nodo_actual = nodo_inicial
    etiquetas[nodo_actual] = [0, '']

    while len(pendientes) > 0:
        nodo_actual = nodo_menor_peso(etiquetas, visitados)
        visitados.append(nodo_actual)
        for adyacente, peso in grafo[nodo_actual].items():
            if adyacente not in pendientes and adyacente not in visitados:
                pendientes.append(adyacente)
            nuevo_peso = etiquetas[nodo_actual][0] + grafo[nodo_actual][adyacente]
            if adyacente not in visitados:
                if adyacente not in etiquetas:
                    etiquetas[adyacente] = [nuevo_peso, nodo_actual]
                else:
                    if etiquetas[adyacente][0] > nuevo_peso:
                        etiquetas[adyacente] = [nuevo_peso, nodo_actual]
        del pendientes[pendientes.index(nodo_actual)]
    return etiquetas

def nodo_menor_peso(etiquetas, visitados):
    menor = sys.maxsize
    nodo_menor = None
    for nodo, etiqueta in etiquetas.items():
        if etiqueta[0] < menor and nodo not in visitados:
            menor = etiqueta[0]
            nodo_menor = nodo
    return nodo_menor

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dijkstra')
def calcular_dijkstra():
    grafo = {
        '1': {'3': 6, '2': 3},
        '2': {'4': 1, '1': 3, '3': 2},
        '3': {'1': 6, '2': 2, '4': 4, '5': 2},
        '4': {'2': 1, '3': 4, '5': 6},
        '5': {'3': 2, '4': 6, '6': 2, '7': 2},
        '6': {'5': 2, '7': 3},
        '7': {'5': 2, '6': 3}
    }
    etiquetas = dijkstra(grafo, '1')
    return jsonify(etiquetas)

if __name__ == "__main__":
    app.run(debug=True)
