from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMap = {}

    def getYears(self):
        return DAO.getYears()

    def getShapes(self,year):
        return DAO.getShapes(year)

    def buildGraph(self,year,shape):
        self._grafo.clear()

        nodes = DAO.getAllSighting(year,shape)
        self._grafo.add_nodes_from(nodes)

        for node in nodes:
            self._idMap[node.id] = node

        edges = DAO.getAllEdges(year,shape,self._idMap)

        for edge in edges:
            if self._grafo.has_edge(edge.s1,edge.s2):
                return
            else:
                self._grafo.add_edge(edge.s1,edge.s2)

    def getGraphDetails(self):
        return len(self._grafo.nodes),len(self._grafo.edges)




    def getTotConnesse(self):
        comp_conn =  list(nx.weakly_connected_components(self._grafo))
        return len(comp_conn)

    def largestConnessa(self):
        conn = list(nx.weakly_connected_components(self._grafo))
        conn.sort(key = lambda x:len(x),reverse=True)
        return conn[0]

