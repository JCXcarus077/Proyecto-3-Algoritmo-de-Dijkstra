# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 12:02:30 2024

@author: Juan Carlos Perez Meneses
"""
import random
import math
import heapq


class Nodo:
    
    def __init__(self, id): #Self se usa para hacer referencia
    
        self.id = id #Inicializa un nuevo nodo con un identificador
        
class Arista:
    
    def __init__(self, nodo_origen, nodo_destino, peso = 1.0):
        #inicializar una nueva arista con un origen, destino y un identificador
        self.arista = [nodo_origen, nodo_destino]
        self.peso = peso
        
class Grafo:
    
    def __init__(self,dirigido = False):
        self.dirigido = dirigido
        self.nodos = []
        self.aristas = []
        self.pesos = {}
        
        
    
    def addNodo(self,nodo):
        if nodo not in self.nodos:
            nodo = Nodo(nodo)
            self.nodos.append(nodo.id)
            
    def addArista(self, n0, n1, peso = None):
        
        if n0 in self.nodos and n1 in self.nodos:
            if not self.dirigido and (n1, n0) in self.aristas: #checar esto
                return  # Avoid duplicate edges in undirected graphs
            self.aristas.append((n0, n1))
            if peso is None:
                peso = random.uniform(1, 10)
            self.pesos[(n0, n1)] = peso
            if not self.dirigido:
                self.aristas.append((n1, n0))
                self.pesos[(n1, n0)] = peso
        
    
    def gen_archivo(self, T_grafo):
        if T_grafo == 7:
            self._gen_graphml()
        else:
            self._gen_graphviz(T_grafo)
            
    def _gen_graphviz(self, T_grafo):
        grafo_files = {
        1: "Grafo de Malla.gv",
        2: "Grafo de Erdös y Rényi.gv",
        3: "Grafo de Gilbert.gv",
        4: "Grafo Geográfico Simple.gv",
        5: "Grafo Barabási-Albert.gv",
        6: "Grafo Dorogovtsev-Mendes.gv",
        7: "Arbol de Dijkstra.gv"
        # 8: "Arbol_DFS_R.gv",
        # 9: "Arbol_DFS_I.gv"
        }
        
        filename = grafo_files.get(T_grafo)
        if filename is None:
            print("Tipo de grafo no válido.")
            return
        with open(filename, "w") as f:
            f.write("graph sample {\n")
            
            for arista in self.aristas:
                n0, n1 = str(arista[0]), str(arista[1])
                # f.write(f"{n0} -- {n1};\n")
                f.write(f"{n0} -- {n1} [label={self.pesos[(int(n0), int(n1))]:.2f}];\n")
            
            for nodo in self.nodos:
                if not any(nodo in arista for arista in self.aristas):
                    f.write(f"{nodo};\n")
            
            f.write("}")
            
    def BFS(self, s):
        visitado = set() #Los set en Python son un tipo que permite almacenar varios elementos y acceder a ellos de una forma muy similar a las listas pero con ciertas diferencias: Los elementos de un set son único, lo que significa que no puede haber elementos duplicados.
        cola = [s]
        arbol_BFS = Grafo()
        visitado.add(s)

        while cola:
            nodo = cola.pop(0)
            arbol_BFS.addNodo(nodo)

            for vecino in self.obtenerVecinos(nodo):
                if vecino not in visitado:
                    visitado.add(vecino)
                    cola.append(vecino)
                    arbol_BFS.addNodo(vecino)
                    arbol_BFS.addArista(nodo, vecino)

        return arbol_BFS
    
    def _gen_graphml(self):
        filename = "Arbol_Dijkstra.graphml"
        with open(filename, "w") as f:
            f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            f.write("<graphml xmlns=\"http://graphml.graphdrawing.org/xmlns\"\n")
            f.write("         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n")
            f.write("         xsi:schemaLocation=\"http://graphml.graphdrawing.org/xmlns\n")
            f.write("         http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd\">\n")
            f.write("  <graph id=\"G\" edgedefault=\"undirected\">\n")
            
            for nodo in self.nodos:
                f.write(f"    <node id=\"{nodo}\"/>\n")
            
            for arista in self.aristas:
                n0, n1 = arista[0], arista[1]
                peso = self.pesos[(n0, n1)]
                f.write(f"    <edge source=\"{n0}\" target=\"{n1}\">\n")
                f.write(f"      <data key=\"weight\">{peso}</data>\n")
                f.write("    </edge>\n")
                
            f.write("  </graph>\n")
            f.write("</graphml>")
    
    def DFS_R(self, s):
        visitado = set()
        arbol_DFS = Grafo()
        
        def dfs_recursivo(nodo):
            visitado.add(nodo)
            arbol_DFS.addNodo(nodo)

            for vecino in self.obtenerVecinos(nodo):
                if vecino not in visitado:
                    arbol_DFS.addArista(nodo, vecino)
                    dfs_recursivo(vecino)
                elif not arbol_DFS.aristas or [nodo, vecino] not in arbol_DFS.aristas:
                    arbol_DFS.addArista(nodo, vecino)
                    
            # print(nodo, "-->" ,vecino) #Crea linea negra, ya que se repite en ambas veces

        dfs_recursivo(s)
        return arbol_DFS

    def DFS_I(self, s):                             #stack --> Pila
        visitado = set()
        pila = [(s, None)] #Cada iteración en la pila es una tupla
        arbol_DFS = Grafo()

        while pila:
            nodo, origen = pila.pop()
            if nodo not in visitado:
                visitado.add(nodo)
                arbol_DFS.addNodo(nodo)
                
                if origen is not None: #Agrega arista solo si el nodo actual tiene un origen
                    arbol_DFS.addArista(origen, nodo)
                    #print("Añadiendo arista:", origen, "->", nodo)
                for vecino in self.obtenerVecinos(nodo):
                    if vecino not in visitado:
                        pila.append((vecino, nodo))  # Push neighbor and its parent to the stack

              
        return arbol_DFS

    def obtenerVecinos(self, nodo):
        vecinos = []
        for arista in self.aristas:
            if nodo in arista:
                vecinos.append(arista[1] if arista[0] == nodo else arista[0])
        return vecinos
    
    def Dijkstra(self, s):
        distancias = {nodo:float('inf') for nodo in self.nodos}
        distancias[s] = 0
        pq = [(0,s)]
        padres = {nodo: None for nodo in self.nodos}
        
        while pq:
            dist_actual, nodo_actual = heapq.heappop(pq)
            
            if dist_actual > distancias[nodo_actual]:
                continue
            
            for vecino in self.obtenerVecinos(nodo_actual):
                peso = self.pesos[(nodo_actual, vecino)]
                dist = dist_actual + peso
                
                if dist < distancias[vecino]:
                    distancias[vecino] = dist
                    padres[vecino] = nodo_actual
                    heapq.heappush(pq, (dist, vecino))
        
        arbol_Dijkstra = Grafo()
        for nodo in self.nodos:
            arbol_Dijkstra.addNodo(f"{nodo} ({distancias[nodo]:.2f})")
        
        for nodo in self.nodos:
            if padres[nodo] is not None:
                padre_nodo = padres[nodo]
                # arbol_Dijkstra.addArista(padre_nodo, nodo,self.pesos[(padre_nodo, nodo)])
                arbol_Dijkstra.addArista(
                    f"{padre_nodo} ({distancias[padre_nodo]:.2f})",
                    f"{nodo} ({distancias[nodo]:.2f})",
                    self.pesos[(padre_nodo, nodo)])
        
        arbol_Dijkstra.gen_archivo(7)
        return arbol_Dijkstra
"""
    Genera grafo de malla
    :param m: número de columnas (> 1)
    :param n: número de filas (> 1)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
"""
def grafoMalla(m, n, dirigido = False):
    T_grafo = 1
    g = Grafo()
    
        # Crear nodos en la malla
    for i in range(m):
        for j in range(n):
            nodo_id = i * n + j  # Asignar un ID único para cada nodo
            g.addNodo(nodo_id)
    
    # Agregar aristas entre nodos adyacentes
    for i in range(m):
        for j in range(n):
            nodo_id = i * n + j
            if i < m - 1:
                g.addArista(nodo_id, nodo_id + n)  # Agregar arista hacia abajo
            if j < n - 1:
                g.addArista(nodo_id, nodo_id + 1)  # Agregar arista hacia la derecha
    
    g.gen_archivo(T_grafo)
    s= int(input("Dame un nodo: "))
    Dijkstra = g.Dijkstra(s)
    #Dijkstra.gen_archivo(7)
    return g 


"""
  Genera grafo aleatorio con el modelo Erdos-Renyi
  :param n: número de nodos (> 0)
  :param m: número de aristas (>= n-1)
  :param dirigido: el grafo es dirigido?
  :return: grafo generado
"""
def grafoErdosRenyi(n, m, dirigido=False):
    T_grafo = 2
    if m < n - 1:
        raise ValueError("El número de aristas debe ser al menos n - 1")
        
    g1 = Grafo()
    
    # Agregar nodos
    for nodo_id in range(1, n + 1):
        g1.addNodo(nodo_id)
    
    # Generar aristas aleatorias
    contador_aristas = 0
    while contador_aristas < m:
        nodo1 = random.randint(1, n)
        nodo2 = random.randint(1, n)
        
        # Verificar si la arista ya existe o si es un bucle
        #if nodo1 != nodo2 and not aristas(nodo1, nodo2):
        if nodo1 != nodo2 and (nodo1, nodo2) not in g1.aristas:
            g1.addArista(nodo1, nodo2)
            contador_aristas += 1
    
    g1.gen_archivo(T_grafo)
    s = int(input("Dame un nodo: "))
    Dijkstra = g1.Dijkstra(s)
   
    return g1


"""
  Genera grafo aleatorio con el modelo Gilbert
  :param n: número de nodos (> 0)
  :param p: probabilidad de crear una arista (0, 1)
  :param dirigido: el grafo es dirigido?
  :return: grafo generado
  """
def grafoGilbert(n, p, dirigido=False):
    T_grafo = 3
    
    g2 = Grafo()
    
    
    # Agregar nodos
    for nodo_id in range(1, n + 1):
        g2.addNodo(nodo_id)
    
    # Generar aristas aleatorias
    for nodo1 in g2.nodos: #Lista de nodos 
        for nodo2 in range(nodo1 + 1, n + 1):  # Iterate from nodo1 + 1 to n
            if random.random() < p:  # Comprobamos si se debe agregar una arista entre estos dos nodos
                g2.addArista(nodo1, nodo2)
                    
                    
    # print(g2.aristas) #Imprime los datos dentro de la lista aristas
    # print(g2.nodos)
    g2.gen_archivo(T_grafo)
    s= int(input("Dame un nodo: "))
    Dijkstra = g2.Dijkstra(s)
    
    return g2


"""
Genera grafo aleatorio con el modelo geográfico simple
:param n: número de nodos (> 0)
:param r: distancia máxima para crear un nodo (0, 1)
:param dirigido: el grafo es dirigido?
:return: grafo generado
"""

def grafoGeografico(n, r, dirigido=False):
    T_grafo = 4
    g = Grafo()
    coor = []
    # Agregar nodos
    for nodo_id in range(n):
        g.addNodo(nodo_id)    # añadir el nodo con sus coordenadas
        x = random.random()  # coordenada x aleatoria
        y = random.random()  # coordenada y aleatoria
        coor.append([x,y])
    for i in g.nodos:
        for j in g.nodos:
            distancia = math.sqrt((coor[j-1][0]-coor[i-1][0])**2 + (coor[j-1][1]-coor[i-1][1])**2)
            if distancia <= r and [i,j] not in g.aristas and [j,i] not in g.aristas and i!=j:
                g.addArista(i, j)
                g.aristas.append([i,j])
            
    
    g.gen_archivo(T_grafo)
    s= int(input("Dame un nodo: "))
    Dijkstra = g.Dijkstra(s)
    return g


"""
  Genera grafo aleatorio con el modelo Barabasi-Albert
  :param n: número de nodos (> 0)
  :param d: grado máximo esperado por cada nodo (> 1) --> número de vertices en c/nodo.
  :param dirigido: el grafo es dirigido?
  :return: grafo generado
  """


def grafoBarabasiAlbert(n, d, dirigido=False):
    T_grafo = 5
    g = Grafo()
    
    # Agregar los primeros d nodos
    for nodo_id in range(1, d + 1):
        g.addNodo(nodo_id)
    
    # Conectar los primeros d nodos entre sí
    for i in range(1, d + 1):
        for j in range(i + 1, d + 1):
            g.addArista(i, j)
    
    # Generar el resto de los nodos
    for nodo_id in range(d + 1, n + 1):
        nuevos_enlaces = []
        for _ in range(d):  # Conectar el nuevo nodo a d nodos existentes
            total_grados = sum(len(g.obtenerVecinos(nodo)) for nodo in g.nodos)
            probabilidad = [len(g.obtenerVecinos(nodo)) / total_grados for nodo in g.nodos]
            nodo_destino = random.choices(g.nodos, weights=probabilidad)[0]
            while nodo_destino in nuevos_enlaces:  # Evitar enlaces duplicados
                nodo_destino = random.choices(g.nodos, weights=probabilidad)[0]
            nuevos_enlaces.append(nodo_destino)
            g.addArista(nodo_id, nodo_destino)
            g.addArista(nodo_destino, nodo_id)  # Si no es dirigido, también agregar arista en la otra dirección
    
    g.gen_archivo(T_grafo)
    s = int(input("Dame un nodo: "))
    Dijkstra = g.Dijkstra(s)
    
    return g


"""
  Genera grafo aleatorio con el modelo
  :param n: número de nodos (≥ 3)
  :param dirigido: el grafo es dirigido?
  :return: grafo generado
  """

def grafoDorogovtsevMendes(n, dirigido=False):
    if n < 3:
        raise ValueError("El número de nodos debe ser al menos 3 para crear un triángulo inicial")
    T_grafo = 6
    g = Grafo(dirigido)
    
    # Agregar los primeros 3 nodos formando un triángulo
    for nodo_id in range(1, 4):
        g.addNodo(nodo_id)
    
    g.addArista(1, 2)
    g.addArista(2, 3)
    g.addArista(3, 1)
    
    # Generar el resto de los nodos
    for nodo_id in range(4, n + 1):
        arista_seleccionada = random.choice(g.aristas)
        nodo1, nodo2 = arista_seleccionada[0], arista_seleccionada[1]
        
        g.addNodo(nodo_id)
        g.addArista(nodo_id, nodo1)
        g.addArista(nodo_id, nodo2)
        
    g.gen_archivo(T_grafo)
    s = int(input("Dame un nodo: "))
    Dijkstra = g.Dijkstra(s)
    return g


if __name__ == "__main__":
   
    #grafoMalla(20,25) 
    #grafoErdosRenyi(500,500) 
    #grafoGilbert(30, 0.15) #0.15,0.04
    #grafoGeografico(30, 0.4) #0.09, 
    #grafoBarabasiAlbert(3,100)
    #grafoDorogovtsevMendes(30)
    pass