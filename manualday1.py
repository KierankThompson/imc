
class Node():
    def __init__(self,name):
        self.name = name
        self.nodes = {}
    def addNode(self,node,multiplier):
        self.nodes[node] = multiplier
    def __str__(self):
        return f"{self.name}"
    def __repr__(self):
        return f"{self.name}"

seashells = Node("seashells")
snowballs = Node("snowballs")
nuggets = Node("nuggets")
pizzas = Node("pizzas")

sbList = [(pizzas,1.45),(nuggets,0.52),(seashells,0.72)]
for name,mult in sbList:
    snowballs.addNode(name,mult)
pzList = [(snowballs,0.7),(nuggets,0.31),(seashells,0.48)]
for name,mult in pzList:
    pizzas.addNode(name,mult)
ngList = [(snowballs,1.95),(pizzas,3.1),(seashells,0.48)]
for name,mult in ngList:
    nuggets.addNode(name,mult)
ssList = [(snowballs,1.34),(pizzas,1.98),(nuggets,0.64)]
for name,mult in ssList:
    seashells.addNode(name,mult)

paths = []
start = [([seashells],1)]
while start:
    path,curNum = start.pop(0)
    if len(path) > 5:
        continue
    curDic = path[-1].nodes
    for node in curDic:
        temp = path.copy()
        temp.append(node)
        tempNum = curNum
        tempNum *= curDic[node]
        start.append((temp,tempNum))
        if node.name == "seashells":
            paths.append((temp,tempNum))

paths.sort(key= lambda x: x[1])
print(paths[-1])
print(paths[-2])
print(paths[-3])





