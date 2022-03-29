import math
from collections import OrderedDict, defaultdict
from copy import copy, deepcopy

def indent(string: str, space: int = 1) -> str:
    return string.replace('\n', '\n' + '  ' * space)


def backspace(string: str) -> str:
    return string.replace('\n  ', '\n')


def backspace1(string: str) -> str:
    return string if string[-3:-1] != '\n  ' else string[:-2]


def deleblankline(string: str) -> str:
    list = string.split("\n")
    lines = [line for line in list if line.strip()]
    return "\n".join(lines)


def auto_connect(ma, mb):
    from pyhcl import IO
    assert hasattr(ma, "value") and hasattr(mb, "value")
    assert type(ma.value) == IO and type(mb.value) == IO

    for (key_left, value_left) in ma.value._ios.items():
        for (key_right, value_right) in mb.value._ios.items():
            from pyhcl import Input, Output
            assert type(value_left) == Input or type(value_left) == Output
            assert type(value_right) == Input or type(value_right) == Output

            if key_left == key_right and type(value_left) != type(value_right):
                io_left = getattr(ma, key_left)
                io_right = getattr(mb, key_right)
                if type(value_left) == Input:
                    io_left <<= io_right
                else:
                    io_right <<= io_left

def get_binary_width(target):
    width = 1
    while target / 2 >= 1:
        width += 1
        target = math.floor(target / 2)
    return width

class TransformException(Exception):
    def __init__(self, message: str):
        self.message = message
    
    def __str__(self):
        return self.message

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
        except TransformException as e:
            raise e
    
    def delete_node(self, name: str, graph = None):
        if graph is None:
            graph = self.graph
        if name not in graph:
            raise TransformException(f'node {name} is not exists.')
        graph.pop(name)
        for _, edges in graph.items():
            if name in edges:
                edges.remove(name)
    
    def delete_node_if_exists(self, name: str, graph = None):
        try:
            self.delete_node(name, graph = graph)
        except TransformException as e:
            raise e
    
    def add_edge(self, ind_node, dep_node, graph = None):
        if graph is None:
            graph = self.graph
        if ind_node not in graph or dep_node not in graph:
            raise TransformException(f'nodes do not exist in graph.')
        test_graph = deepcopy(graph)
        test_graph[ind_node].add(dep_node)
        is_valid, msg = self.validate(test_graph)
        if is_valid:
            graph[ind_node].add(dep_node)
        else:
            raise TransformException(f'Loop do exist in graph: {msg}')
    
    def delete_edge(self, ind_node, dep_node, graph = None):
        if graph is None:
            graph = self.graph
        if dep_node not in graph.get(ind_node, []):
            raise TransformException(f'This edge does not exist in graph')
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
            raise TransformException(f'graph is not acyclic.')

    
    def validate(self, graph = None):
        if graph is None:
            graph = self.graph
        if len(self.ind_nodes(graph)) == 0:
            return False, 'no independent nodes detected.'
        try:
            self.topological_sort(graph)
        except TransformException:
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
    
    def size(self):
        return len(self.graph)
