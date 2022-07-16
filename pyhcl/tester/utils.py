from collections import OrderedDict, defaultdict
from copy import deepcopy
from pyhcl.tester.exception import TesterException
class DAG:
    """ Directed acyclic graph implementation."""

    def __init__(self):
        self.graph = OrderedDict()
    
    def add_node(self, name: str, graph = None):
        if graph is None:
            graph = self.graph
        if name in graph:
            ...
        else:
            graph[name] = set()
    
    def add_node_if_not_exists(self, name: str, graph = None):
        try:
            self.add_node(name, graph = graph)
        except TesterException as e:
            raise e
    
    def delete_node(self, name: str, graph = None):
        if graph is None:
            graph = self.graph
        if name not in graph:
            raise TesterException(f'node {name} is not exists.')
        graph.pop(name)
        for _, edges in graph.items():
            if name in edges:
                edges.remove(name)
    
    def delete_node_if_exists(self, name: str, graph = None):
        try:
            self.delete_node(name, graph = graph)
        except TesterException as e:
            raise e
    
    def add_edge(self, ind_node, dep_node, graph = None):
        if graph is None:
            graph = self.graph
        if ind_node not in graph or dep_node not in graph:
            raise TesterException(f'nodes do not exist in graph.')
        test_graph = deepcopy(graph)
        test_graph[ind_node].add(dep_node)
        is_valid, msg = self.validate(test_graph)
        if is_valid:
            graph[ind_node].add(dep_node)
        else:
            raise TesterException(f'Loop do exist in graph: {msg}')
    
    def delete_edge(self, ind_node, dep_node, graph = None):
        if graph is None:
            graph = self.graph
        if dep_node not in graph.get(ind_node, []):
            raise TesterException(f'This edge does not exist in graph')
        graph[ind_node].remove(dep_node)
    
    def ind_nodes(self, graph = None):
        if graph == None:
            graph = self.graph
        dep_nodes = set(
            node for deps in graph.values() for node in deps
        )

        return [node for node in graph.keys() if node not in dep_nodes]
    
    def topological_sort(self, graph = None):
        if graph is None:
            graph = self.graph
        result = []
        in_degree = defaultdict(lambda: 0)

        for u in graph:
            for v in graph[u]:
                in_degree[v] += 1
        
        ready = [node for node in graph if not in_degree[node]]

        while ready:
            u = ready.pop()
            result.append(u)
            for v in graph[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    ready.append(v)
        if len(result) == len(graph):
            return result
        else:
            raise TesterException(f'graph is not acyclic.')

    
    def validate(self, graph = None):
        if graph is None:
            graph = self.graph
        if len(self.ind_nodes(graph)) == 0:
            return False, 'no independent nodes detected.'
        try:
            self.topological_sort(graph)
        except TesterException:
            return False, 'graph is not acyclic.'
        return True, 'valid'
    
    def visit_graph(self, graph = None):
        visited = []
        if graph is None:
            graph = self.graph
        for v in graph:
            for u in graph[v]:
                visited.append(f'{v} -> {u}')
        return visited
    
    def travel_graph(self, init: list, graph = None):
        if graph is None:
            graph = self.graph
        visits = []
        history = set()
        while len(init) > 0:
            visited = init.pop(0)
            if len(graph[visited]) > 0:
                for u in graph[visited]:
                    if u not in init and u not in history:
                        init.append(u)
            history.add(visited)
            visits.append(visited)
        return visits
    
    
    def size(self):
        return len(self.graph)