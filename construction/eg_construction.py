# -*- coding:utf-8 -*-
import json

from py2neo import Graph, Node


def create_nodes(graph, label, node_dict, rel_dict, if_only=False):
    if if_only:
        try:
            graph.run(f"CREATE CONSTRAINT ON (n:{label}) ASSERT n.name IS UNIQUE")
        except:
            pass
    for node_name in node_dict.keys():
        node = Node(label, name=node_name)
        graph.create(node)
        if node_dict[node_name]:
            attribute_dict = node_dict[node_name]
            for node_attribute in attribute_dict.keys():
                if node_attribute not in rel_dict.keys():
                    graph.run(
                        f"match(a:{label}) where a.name = '{node_name}' set a.{node_attribute} = '{attribute_dict[node_attribute]}'"
                    )


def create_rel(graph, label, node_dict, rel_dict):
    for node_name in node_dict.keys():
        attribute_dict = node_dict[node_name]
        for node_attribute in attribute_dict.keys():
            if node_attribute in rel_dict.keys():
                o_label = rel_dict[node_attribute]
                o_names = attribute_dict[node_attribute]
                if type(o_names) == list:
                    for o_name in o_names:
                        try:
                            graph.run(
                                f"CREATE CONSTRAINT ON (n:{o_label}) ASSERT n.name IS UNIQUE"
                            )
                        except:
                            pass
                        node = Node(o_label, name=o_name)
                        try:
                            graph.create(node)
                        except:
                            pass
                        graph.run(
                            f"match(a:{label}), (b:{o_label}) where a.name = '{node_name}' and b.name = '{o_name}' create (a)-[r:{node_attribute}]->(b)"
                        )
                else:
                    try:
                        graph.run(
                            f"CREATE CONSTRAINT ON (n:{o_label}) ASSERT n.name IS UNIQUE"
                        )
                    except:
                        pass
                    node = Node(o_label, name=o_names)
                    try:
                        graph.create(node)
                    except:
                        pass
                    graph.run(
                        f"match(a:{label}), (b:{o_label})\
                                where a.name = '{node_name}' and b.name = '{o_names}'\
                                create (a)-[r:{node_attribute}]->(b)"
                    )
                    graph.run(
                        f"match(a:{label})-[r]->(b:{o_label}) set r.rel_name='{node_attribute}'"
                    )


def delete_all_nodes_rels(graph):
    graph.run("match(n)-[r]->(m) delete r")
    graph.run("match(n) delete n")


if __name__ == "__main__":
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "Zs19980425"))
    delete_all_nodes_rels(graph)
    rel_dict = {
        "time":"Time",
        "location_province":"Province",
        "casualty_number":"Casualty_Number",
        "accident_cause":"Accident_Cause",
        "solution_method":"Method"
    }
    fp = open("./province.json", "r", encoding="utf-8")
    province_dict = json.load(fp)
    create_nodes(
        graph,
        label="Province",
        node_dict=province_dict,
        rel_dict=rel_dict,
        if_only=True,
    )
    fp = open("./accident.json", "r", encoding="utf-8")
    accident_dict = json.load(fp)
    create_nodes(
        graph,
        label="Accident",
        node_dict=accident_dict,
        rel_dict=rel_dict,
        if_only=True,
    )
    create_rel(graph, label="Accident", node_dict=accident_dict, rel_dict=rel_dict)
