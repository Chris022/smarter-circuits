import sys
sys.path.append('../')

from lib.components.componentCollection import PATTERNS

def getComponents(graph):
    matches = []
    for comp in PATTERNS.values():
        matchingInCopy = comp.match(graph)

        for i in matchingInCopy:
            a = []
            for j in i:
                a.append(graph.getVertex(j.id))
            matches.append(a)

    return list(matches)