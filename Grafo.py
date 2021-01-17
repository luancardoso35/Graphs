import sys

class Vertice(object):
    def __init__(self, nome: int):
        self.num = sys.maxsize
        self.dist = sys.maxsize
        self.nome = nome
        self.cor = None
        self.pai = None

    def __hash__(self):
        return self.nome.__hash__()

    def __eq__(self, other):
        return self.nome == other.nome

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self.num) + "-" + str(self.dist)

    def mudaDist(self, dist2):
        self.dist = dist2

class GrafoNaoOrientado(object):
    def __init__(self, vertices):
        self.listaAdj = {}
        self.nvertices = vertices

    def add_aresta(self, vert1 : Vertice, vert2 : Vertice):
        if vert1 not in self.listaAdj:
            self.listaAdj[vert1] = []
        if vert2 not in self.listaAdj:
            self.listaAdj[vert2] = []
        self.listaAdj[vert1].append(vert2)
        self.listaAdj[vert2].append(vert1)

    def get_vertices(self):
        return(list(self.listaAdj.keys()))

    def get_adjacentes(self, vertice : Vertice):
        return(list(self.listaAdj[vertice]))

    def mostraLista(self):
        for x in self.listaAdj.items():
            print(x)



class GrafoOrientado(object):
    def __init__(self, vertices):
        self.vertices = {}
        self.nv = vertices

    def add_aresta(self, chave_de : Vertice, chave_para : Vertice, peso):
        if chave_de not in self.vertices:
            self.vertices[chave_de] = {}
        if chave_para not in self.vertices:
            self.vertices[chave_para] = {}
        self.vertices[chave_de][chave_para] = peso

    def mostraGrafo(self):
        for x in self.vertices.items():
            print(x)

    def get_vertices(self):
        return(list(self.vertices.keys()))

    def get_adjacentes(self, chave : Vertice):
        return(list(self.vertices[chave].keys()))

    def get_pesosAdjacentes(self, chave : Vertice):
        return(list(self.vertices[chave].values()))

class GrafoNaoOrientadoComPeso(object):
    def __init__(self, vertices):
        self.vertices = {}
        self.nv = vertices

    def add_aresta(self, chave_de: Vertice, chave_para: Vertice, peso):
        if chave_de not in self.vertices:
            self.vertices[chave_de] = {}
        if chave_para not in self.vertices:
            self.vertices[chave_para] = {}
        self.vertices[chave_de][chave_para] = peso
        self.vertices[chave_para][chave_de] = peso

    def mostraGrafo(self):
        for x in self.vertices.items():
            print(x)

    def get_vertices(self):
        return (list(self.vertices.keys()))

    def get_adjacentes(self, chave: Vertice):
        return (list(self.vertices[chave].keys()))

    def get_pesosAdjacentes(self, chave: Vertice):
        return (list(self.vertices[chave].values()))


contadorDistancia = 1
arestas = []
def percursoProfundidade(grafo):

    for x in grafo.get_vertices():
        x.num = 0

    for x in grafo.get_vertices():
        if x.num == 0:
            dfs(grafo, x)

    return arestas

def dfs(grafo, vertice : Vertice):
    global contadorDistancia

    vertice.num = contadorDistancia
    contadorDistancia = contadorDistancia + 1

    for x in grafo.get_adjacentes(vertice):
        if (x.num == 0) :
            arestas.append(str(vertice.nome) + " para " + str(x.nome))
            dfs(grafo, x)


def percursoLargura(grafo, vertice):
    percorridos = []
    percorridos.append("comecei em " + str(vertice.nome))
    for x in grafo.get_vertices():
        if (x.__ne__(vertice)):
            x.cor = "branco"
            x.dist = None
            x.pai = None

    vertice.cor = "cinza"
    vertice.dist = 0
    vertice.pai = None
    q = []

    q.append(vertice)

    while(q.__len__() != 0):
        u = q.pop(0)
        for x in grafo.get_adjacentes(u):
            if (x.cor.__eq__("branco")):
                x.cor = "cinza"
                x.dist = vertice.dist + 1
                x.pai = vertice
                q.append(x)
                percorridos.append("fui para " + str(x.nome))
        vertice.cor = "preto"

    return percorridos

def arvoreGeradoraPrim(grafo, verticeInicial):
    for x in grafo.get_vertices():
        x.dist = sys.maxsize
        x.pai = None

    verticeInicial.dist = 0
    verticeInicial.pai = verticeInicial
    lista_distancias = []

    for x in grafo.get_vertices():
        lista_distancias.append(x)

    lista_agm = []
    while lista_distancias:
        u = acharMinimo(lista_distancias)
        if (verticeInicial.__ne__(u)):
            lista_agm.append("de " + str(u.pai.nome) + " para " + str(u.nome))
        else:
            lista_agm.append("Iniciando no " + str(verticeInicial.nome))
        lista_distancias.remove(u)
        for x in grafo.get_adjacentes(u):
            if x in lista_distancias and grafo.vertices[u][x] < x.dist :
                x.pai = u
                x.dist = grafo.vertices[u][x]

    return lista_agm

def acharMinimo(lista):
    minimo = lista[0]
    for x in range(len(lista)):
        if lista[x].dist < minimo.dist:
            minimo = lista[x]
    return minimo

def bellmanFord(grafo, verticeInicial):
    for x in grafo.vertices:
        x.dist = sys.maxsize
        x.pai = None

    verticeInicial.dist = 0

    for i in range(1, len(grafo.get_vertices())):
        for u in grafo.get_vertices():
            for v in grafo.get_adjacentes(u):
                if v.dist > u.dist + grafo.vertices[u][v]:
                    v.dist = u.dist + grafo.vertices[u][v]
                    v.pai = u

        for x in grafo.get_vertices():
            for y in grafo.get_adjacentes(x):
                if y.dist > x.dist + grafo.vertices[x][y]:
                    return False


    caminho = []
    for i in grafo.get_vertices():
        v = i
        while v:
            caminho.append(v.nome)
            v = v.pai
        print(list(reversed(caminho)), "Custo: ", i.dist)
        caminho.clear()

    return True


def main():

    g = GrafoNaoOrientado(7)

    v0 = Vertice(0)
    v1 = Vertice(1)
    v2 = Vertice(2)
    v3 = Vertice(3)
    v4 = Vertice(4)
    v5 = Vertice(5)
    v6 = Vertice(6)
    v7 = Vertice(7)
    v8 = Vertice(8)
    v9= Vertice(9)

    g.add_aresta(v1, v2)
    g.add_aresta(v1, v3)
    g.add_aresta(v1, v4)
    g.add_aresta(v2, v5)
    g.add_aresta(v3, v6)
    g.add_aresta(v3, v7)
    g.add_aresta(v4, v8)
    g.add_aresta(v5, v9)


    # arestas = percursoProfundidade(g)
    arestas2 = percursoLargura(g, v1)
    print(arestas)

    g1 = GrafoNaoOrientadoComPeso(7)
    g1.add_aresta(v0,v1,4)
    g1.add_aresta(v0,v7,8)
    g1.add_aresta(v1,v7,11)
    g1.add_aresta(v7,v8,7)
    g1.add_aresta(v7,v6, 1)
    g1.add_aresta(v8,v6, 6)
    g1.add_aresta(v1,v2, 8)
    g1.add_aresta(v2,v8, 2)
    g1.add_aresta(v6,v5, 2)
    g1.add_aresta(v2,v3,7)
    g1.add_aresta(v2,v5,4)
    g1.add_aresta(v3,v5,14)
    g1.add_aresta(v3,v4,9)
    g1.add_aresta(v4,v5,10)

    # agm = arvoreGeradoraPrim(g1, v0)
    # print(agm)
    bellmanFord(g1, v0)

if __name__ == "__main__":
    main()