"""
@author: Hima Bindu Krovvidi hk4233

Lab2 AI CSCI 630
"""

import sys
import re
from itertools import combinations

resolvelist = []

class Base:
    def __init__(self):

        self.preds = []
        self.vars = []
        self.consts = []
        self.funcs = []
        self.clauses = []
        

    def __hash__(self) -> int:
        return hash(self)

    def userinput(self):
        if len(sys.argv) < 1:
            print("Usage: python3 filename location_of_testcase")
            sys.exit(1)
        else:
            filetocheck = sys.argv[1]
            with open(filetocheck, "r") as fp:
                self.preds = fp.readline().split()[1:]
                self.vars = fp.readline().split()[1:]
                self.consts = fp.readline().split()[1:]
                self.funcs = fp.readline().split()[1:]
                while(fp.readline):
                    line = fp.readline()
                    if line == "": break
                    self.clauses.append(line.strip())

    def checkkb(self):
        """
        This function checks if the KB is consistent or not
        """
        curr = set()
        f = True
        while f:
            """
            This loop runs until the set of clauses is not empty
            """
            combs = combinations(self.clauses, 2)
            for (i, j) in combs:
                """
                This loop runs for all the combinations of clauses
                """
                checkers = self.check(i, j)
                if [] in checkers:
                    return f
                for k in checkers:
                    """
                    This loop runs for all the clauses that are returned by the check function
                    """
                    if k not in curr: curr.add(k)
            if curr.issubset(self.clauses):
                """
                If the set of clauses is a subset of the current set of clauses, then the KB is consistent
                """
                return not f
            for every in curr:
                """
                This loop runs for all the clauses in the current set of clauses
                """
                if every not in self.clauses:
                    """
                    If the clause is not in the set of clauses, then it is added to the set of clauses
                    """
                    self.clauses.append(every)
                    


    def check(self, c1, c2): 
        """
        This function checks if the clauses are consistent or not
        """
        curr = []
        for i in c1.split(" "):
            """
            This loop runs for all the predicates in the first clause
            """
            for j in c2.split(" "):
                """
                This loop runs for all the predicates in the second clause
                """
                rule1, rule2 = self.rules(i, j)
                if rule1 == ("!" + rule2) or rule2 == ("!" + rule1):
                    """
                    If the clauses are consistent, then the clauses are returned
                    """
                    splitc1 = c1.split(" ")
                    splitc2 = c2.split(" ")
                    splitc1.remove(i)
                    splitc2.remove(j)
                    curr = self.resolvecls(splitc1, splitc2)
        return curr


    def resolvecls(self, c1, c2):
        """
        This function resolves the clauses
        """
        c1_temp = ' '.join(c1)
        c2_temp = ' '.join(c2)
        if c1_temp == "" and c2_temp == "":
            """
            If the clauses are empty, then the clauses are returned
            """
            resolvelist.append([])
        elif c1_temp == "" or c2_temp == "":
            resolvelist.append(c1_temp + c2_temp)
        for i in range(len(c1)):
            """
            This loop runs for all the clauses in the first clause
            """
            for j in range(len(c2)):
                """
                This loop runs for all the clauses in the second clause
                """
                if c1[i] == "~" + c2[j] or c2[j] == "~" + c1[i]:
                    """
                    If the clauses are consistent, then the clauses are resolved
                    """
                    c1_temp = c1.copy()
                    c2_temp = c2.copy()
                    c1_temp.remove(c1[i])
                    c2_temp.remove(c2[j])
                    c1_temp.extend(c2_temp)
                    c1_temp = list(set(c1_temp))
                    c1_temp.sort()
                    resolvelist.append(c1_temp)
        return resolvelist


    def totalparse(self, cons1, cons2):
        """
        This function parses the clauses
        """
        c1 = cons1.count("(") + cons1.count(")")
        c2 = cons2.count("(") + cons2.count(")")
        m, n, var1, var2 = self.varsprocess(cons1, cons2)
        if c1 == 4:
            """
            If the first clause has 4 predicates, then the variables are replaced with constants
            """
            if c2 != 4:
                """
                If the second clause has less than 4 predicates, then the variables are replaced with constants
                """
                for i in range(len(var2)):
                    if var2[i] in self.vars:
                        re.sub(var2[i], var1[i], cons2)
            elif c2 == 4:
                """
                If the second clause has 4 predicates, then the variables are replaced with constants
                """
                for i in range(len(var1)):
                    """
                    This loop runs for all the variables in the first clause
                    """
                    if var1[i].find("(") != -1:
                        cons1, cons2 = self.varandcons(var1[i], var2[i], cons1, cons2)
        else:
            """
            If the first clause has less than 4 predicates, then the variables are replaced with constants
            """
            if c2 == 4:
                for i in range(len(var1)):
                    if var1[i] in self.vars:
                        re.sub(var1[i], var2[i], cons1)
        return cons1, cons2


    def varandcons(self, varc1, varc2, c1, c2):
        """
        This function replaces the variables with constants
        """
        c1count = c1.count("(")
        c1count += c1.count(")")
        c2count = c2.count("(")
        c2count += c2.count(")")
        if c1count==4:
            """
            If the clause has 4 variables, then the variables are replaced with constants
            """
            if c2count==4:
                """
                If both the clauses have 4 predicates, then the variables are replaced with constants
                """
                v = varc1[0].split("(")
                if v in self.funcs:
                    """
                    If the first variable is a function, then the variables are replaced with constants
                    """
                    k1 = varc1.find('(')
                    l1 = varc1.rfind(')')
                    k2 = varc2.find('(')
                    l2 = varc2.rfind(')')
                    varc1 = varc1[k1 + 1 : l1]
                    varc2 = varc2[k2 + 1 : l2]
                    if varc2 in self.vars:
                        """
                        If the first variable is a variable, then the variables are replaced with constants
                        """
                        re.sub(varc2, varc1, c2)
                    elif varc1 in self.vars:
                        """
                        If the second variable is a variable, then the variables are replaced with constants
                        """
                        re.sub(varc1, varc2, c1)
                else:
                    """
                    If the first variable is not a function, then the variables are replaced with constants
                    """
                    re.sub(varc1, varc2, c1)
                return c1, c2
            else:
                """
                If the second clause has less than 4 predicates, then the variables are replaced with constants
                """
                if varc1.split("(")[0] in self.funcs:
                    k1 = c2.find('(')
                    l1 = c2.rfind(')')
                    varc2 = c2[k1 + 1 : l1]
                    if varc2 in self.vars:
                        re.sub(varc2, varc1, c2)
                return c1, c2
        else:
            if(c2count==2):
                """
                If the second clause has 2 predicates, then the variables are replaced with constants
                """
                if varc1.split("(")[0] in self.funcs:
                    """
                    If the first variable is a function, then the variables are replaced with constants
                    """
                    k1 = c2.find('(')
                    l1 = c2.rfind(')')
                    varc2 = c2[k1 + 1 : l1]
                    if varc2 in self.vars:
                        """
                        If the second variable is a variable, then the variables are replaced with constants
                        """
                        re.sub(varc2, varc1, c2)
                return c1, c2
            else:
                l = varc2.split("(")[0]
                if l in self.funcs:
                    k1 = c1.find('(')
                    l1 = c1.rfind(')')
                    varc1 = c1[k1 + 1 : l1]
                    if varc1 in self.vars:
                        re.sub(varc1, varc2, c1)
                return c1, c2


    def rules(self, cons1, cons2):
        """
        This function checks if the clauses are consistent or not
        """
        m1 = cons1.find('(')
        n1 = cons1.rfind(')')
        m2 = cons2.find('(')
        n2 = cons2.rfind(')')
        var1 = cons1[m1 + 1: n1]
        var2 = cons2[m2 + 1 : n2]
        cons1count = cons1.count("(") + cons1.count(")")
        cons2count = cons2.count("(") + cons2.count(")")
        if cons1.find(",") != -1 and cons2.find(",") != -1:
            """
            If the clauses have 2 variables, then the clauses are checked for consistency
            """
            if cons1count == 4 or cons2count == 4:
                cons1, cons2 = self.totalparse(cons1, cons2)
            var1, var2, varc1, varc2 = self.varsprocess(cons1, cons2)
            curr = []
            for i in range(len(varc1)):
                """
                This loop runs for all the variables in the first clause
                """
                if varc1[i] in self.vars:
                    """
                    If varc1[i] is a variable, then the clauses are checked for consistency
                    """
                    cons1 = cons1.replace(varc1[i], varc2[i])
                    curr.append(varc2[i])
            for i in curr:
                """
                This loop runs for all the variables in the second clause
                """
                if i in var2:
                    """
                    If the variables are consistent, then the clauses are returned
                    """
                    re.sub(i, "", cons2)
                re.sub(i, var1, cons2)
            for i in range(len(varc2)):
                if varc2[i] in self.vars:
                    cons2 = cons2.replace(varc2[i], varc1[i])
            return cons1, cons2
        else:
            """
            If the clauses have 1 variable, then the clauses are checked for consistency
            """
            if var1 in self.vars:
                cons1 = cons1.replace(var1, var2)
            elif var2 in self.vars:
                cons2 = cons2.replace(var2, var1)
            return cons1, cons2


    def varsprocess(self, c1, c2):
        """
        This function processes the variables in the clauses
        """
        m1 = c1.find('(')
        n1 = c1.rfind(')')
        m2 = c2.find('(')
        n2 = c2.rfind(')')
        varc1 = c1[m1 + 1 : n1]
        varc2 = c2[m2 + 1 : n2]
        return varc1, varc2, varc1.split(","), varc2.split(",")

def main():
    base = Base()
    base.userinput()
    if(base.checkkb()):
        print("no")
    else:
        print("yes")


if __name__ == "__main__":
    main()
