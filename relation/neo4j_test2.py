from neo4j import GraphDatabase
from py2neo import Graph, Node, Relationship
'''
password = "withdrawal magenta Face to face 2"
uid = [5935597009,1660544250]

#graph = Graph("bolt://localhost:7687",username="neo4j",password=password)
testnode1 = Node('user',name=str(uid[0]))
testnode2 = Node('user',name=str(uid[1]))
ab = Relationship(testnode2, "favorite", testnode1)

a = Node("Person", name="Alice")
b = Node("Person", name="Bob")
ab = Relationship(a, "KNOWS", b)
print(ab)
test_graph = Graph(
    "http://localhost:7474",
    username="neo4j",
    password="withdrawal magenta Face to face 2"
)

'''



test_graph = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "withdrawal magenta Face to face 2"))
uid = [5935597009,1660544250]
test_node_1 = Node('user',name=str(uid[0]))
test_node_2 = Node('user',name=str(uid[1]))
test_graph.create(test_node_1)
test_graph.create(test_node_2)

node_1_call_node_2 = Relationship(test_node_1,'CALL',test_node_2)
node_1_call_node_2['count'] = 1
node_2_call_node_1 = Relationship(test_node_2,'CALL',test_node_1)
node_2_call_node_1['count'] = 2
test_graph.create(node_1_call_node_2)
test_graph.create(node_2_call_node_1)
node_1_call_node_2['count']+=1
test_graph.push(node_1_call_node_2)