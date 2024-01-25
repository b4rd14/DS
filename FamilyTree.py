import networkx as nx
import matplotlib.pyplot as plt
from SHA2 import *


class Person :
    def __init__(self, name, parent, level):
        self.name = name
        self.parent = parent
        self.level = level
        self.children = []
    
    def addChild(self, person):
        self.children.append(person)

    


class FamilyTree :
    def __init__(self, name):
        self.root = Person(name, None, 0)
        self.family_tree = [self.root]
        self.family_hash ={name : SHA256(name.encode('utf-8'))}

    def addPerson(self, name, parent):
        person = Person(name, parent , parent.level + 1)
        parent.addChild(person)
        self.family_tree.append(person)
        self.family_hash[name] = SHA256(name.encode('utf-8'))

    def visualizeFamilyTree(self):
        G = nx.DiGraph()
        self._buildGraph(G, self.root)
        pos = self._layoutTrie(G, self.root)
        nx.draw(G, pos, with_labels=True, arrows=True , font_size = 5)
        plt.show()

    def _buildGraph(self, G, person):
        for child in person.children:
            G.add_edge(self.family_hash[person.name], self.family_hash[child.name])
            self._buildGraph(G, child)

    def _layoutTrie(self, G, person):
        pos = {}
        pos[self.family_hash[person.name]] = (0, 0)
        self._assignPositions(G, person, pos, 0, 0)
        return pos

    def _assignPositions(self, G, person, pos, level, idx):
        num_children = len(person.children)
        if num_children == 0:
            return

        dx = 1.0 / num_children
        x = pos[self.family_hash[person.name]][0] - 0.5 + dx / 2.0
        y = pos[self.family_hash[person.name]][1] - 1

        for child in person.children:
            pos[self.family_hash[child.name]] = (x, y)
            G.add_edge(self.family_hash[person.name], self.family_hash[child.name])
            self._assignPositions(G, child, pos, level + 1, idx)
            x += dx
            idx += 1

    def findHash(self, name):
        return self.family_hash[name]

    def Size(self):
        return len(self.family_tree)
    
    def deletePerson(self, name):
        person = self.getPerson(name)
        if person == None:
            return None
        else:
            parent = person.parent
            parent.children.remove(person)
            self.family_tree.remove(person)
            del self.family_hash[name]
            return person


    def getRoot(self):
        return self.root

    def getChildren(self, person):
        return person.children

    def getParent(self, person):
        return person.parent

    def getPerson(self, name):
        return self.findPerson(name, self.root)
    
    def findPerson(self, name, person):
        if person.name == name:
            return person
        else:
            for child in person.children:
                p = self.findPerson(name, child)
                if p:
                    return p
            return None

    
    def areSiblings(self, person1, person2):
        return person1.parent == person2.parent
    
    def areParentAndChild(self, parent, child):
        return child.parent == parent
    
    
    def findCommonAncestor(self, person1, person2):
        if person1.level == person2.level:
            if person1 == person2:
                return None
            
            elif person1.parent == person2.parent:
                return self.family_hash[person1.parent]
            elif person1.parent == None or person2.parent == None:
                return None
            else:
                return self.findCommonAncestor(person1.parent, person2.parent)
        elif person1.level > person2.level:
            return self.findCommonAncestor(person1.parent, person2)
        else:
            return self.findCommonAncestor(person1, person2.parent)
        
    def areRelated (self, person1, person2):
        if person1 == person2:
            return False
        else:
            ancestor = self.findCommonAncestor(person1, person2)
            if ancestor:
                return True
            else:
                return False
        
    def findFarthestDescendant(self , person):
        if not person.children :
            return 0
        else:
            maxDepth = max(self.findFarthestDescendant(child) for child in person.children)
            return maxDepth + 1
        
    def getLeaves(self):
        leaves = []
        for person in self.family_tree:
            if person.children == []:
                leaves.append(person)

        return leaves

    def BFS (self, person):
        visited = [person]
        p = person
        maxDistance = 0
        queue = []
        queue.append([person, 0])
        while queue:
            s = queue.pop(0)
            if s[1] > maxDistance:
                maxDistance = s[1]
                p = s[0]
            for child in s[0].children + [s[0].parent]:
                if child not in visited and child != None:
                    visited.append(child)
                    queue.append([child, s[1] + 1])
        return [p, maxDistance]
    
    def findLongestPath(self):
        longestPath = 0
        p = self.root
        leaf = None
        for l in self.getLeaves():
            path = self.BFS(l)
            if path[1] > longestPath:
                longestPath = path[1]
                p = path[0]
                leaf = l

        return [self.family_hash[p.name], self.family_hash[leaf.name], longestPath]
    



def main():
    ft = FamilyTree("Adam")
    ft.addPerson("Eve", ft.getRoot())
    ft.addPerson("Cain", ft.getPerson("Adam"))
    ft.addPerson("Abel", ft.getPerson("Adam"))
    ft.addPerson("Seth", ft.getPerson("Adam"))
    ft.addPerson("Enoch", ft.getPerson("Seth"))
    ft.addPerson("Irad", ft.getPerson("Enoch"))
    ft.addPerson("Mehujael", ft.getPerson("Irad"))
    ft.addPerson("Methushael", ft.getPerson("Mehujael"))
    ft.addPerson("Lamech", ft.getPerson("Methushael"))
    ft.addPerson("Jabal", ft.getPerson("Lamech"))
    ft.addPerson("Jubal", ft.getPerson("Lamech"))
    ft.addPerson("Tubal-Cain", ft.getPerson("Lamech"))
    ft.addPerson("Naamah", ft.getPerson("Lamech"))
    ft.addPerson("Enos", ft.getPerson("Seth"))
    ft.addPerson("Noam", ft.getPerson("Enos"))
    ft.addPerson("Kenan", ft.getPerson("Enos"))
    ft.addPerson("Mahalalel", ft.getPerson("Kenan"))


    

    ft.visualizeFamilyTree()

    print(ft.findLongestPath())

    


if __name__ == "__main__":
    main()

            
            
        
        
        
    
    

    
    
        
 



    

    
    
        
        
