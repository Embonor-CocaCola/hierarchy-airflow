from collections import deque


class Graph:
    def __init__(self, graph_dict=None):
        self.graph = {}
        if graph_dict:
            for node in graph_dict:
                name = node.get('name', None)
                if not name:
                    raise ValueError(f'Name not found in node {node}')

                self.add_node(name, node)

            for node in graph_dict:
                edges = node.get('edges', None)
                name = node.get('name', None)
                print(edges)
                if edges is None:
                    raise ValueError(f'Edges not found in node {node}')

                for node_ref in edges:
                    self.add_edge(origin=name, dest=node_ref)

    def add_node(self, name, metadata):
        self.graph[name] = {'metadata': metadata, 'edges': []}

    def get_node(self, name):
        return self.graph[name]['metadata']

    def add_edge(self, origin: str, dest: str):
        if not self.graph[origin]:
            raise ValueError(f'Node name does not exist in current graph: {origin}')
        elif not self.graph[dest]:
            raise ValueError(f'Node name does not exist in current graph: {dest}')

        self.graph[origin]['edges'].append(dest)

    def get_topology_sort(self):
        visited_nodes = []
        stack = deque()

        for node_name in list(self.graph.keys()):
            if node_name not in visited_nodes:
                self.get_topology_sort_util(visited_nodes=visited_nodes, stack=stack, start_node=node_name)

        return stack

    def get_topology_sort_util(self, visited_nodes, stack, start_node):
        visited_nodes.append(start_node)

        current_node = self.graph[start_node]

        for node_name in current_node['edges']:
            if node_name not in visited_nodes:
                self.get_topology_sort_util(visited_nodes=visited_nodes, stack=stack, start_node=node_name)

        stack.append(start_node)
