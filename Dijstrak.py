from flask import Flask, render_template, jsonify, request
import sys

app = Flask(__name__)

def dijkstra(grafo, nodo_inicial, nodo_final=None):
    etiquetas = {}
    visitados = []
    pendientes = [nodo_inicial]
    nodo_actual = nodo_inicial
    etiquetas[nodo_actual] = [0, '']
    
    while len(pendientes) > 0:
        nodo_actual = nodo_menor_peso(etiquetas, visitados)
        visitados.append(nodo_actual)
        
        # Si llegamos al nodo final, podemos terminar
        if nodo_final and nodo_actual == nodo_final:
            break
            
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
        
        if nodo_actual in pendientes:
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

def obtener_ruta(etiquetas, nodo_inicial, nodo_final):
    if nodo_final not in etiquetas:
        return [], 0
    
    ruta = [nodo_final]
    nodo_actual = nodo_final
    peso_total = etiquetas[nodo_final][0]
    
    while nodo_actual != nodo_inicial:
        nodo_actual = etiquetas[nodo_actual][1]
        ruta.append(nodo_actual)
    
    ruta.reverse()
    return ruta, peso_total

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dijkstra', methods=['POST'])
def calcular_dijkstra():
    data = request.get_json()
    grafo = data.get('grafo', {})
    nodo_inicial = data.get('nodo_inicial')
    nodo_final = data.get('nodo_final')
    
    if not grafo or not nodo_inicial or not nodo_final:
        return jsonify({'error': 'Se requiere grafo, nodo inicial y nodo final'}), 400
    
    try:
        etiquetas = dijkstra(grafo, nodo_inicial, nodo_final)
        ruta, peso_total = obtener_ruta(etiquetas, nodo_inicial, nodo_final)
        
        # Recolectar información sobre todos los nodos para la visualización
        nodos = list(grafo.keys())
        enlaces = []
        for origen in grafo:
            for destino, peso in grafo[origen].items():
                enlaces.append({'origen': origen, 'destino': destino, 'peso': peso})
        
        return jsonify({
            'etiquetas': etiquetas,
            'ruta_mas_corta': ruta,
            'peso_total': peso_total,
            'grafo': {
                'nodos': nodos,
                'enlaces': enlaces
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)