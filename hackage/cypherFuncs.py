from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neofour"))


#Neo4J Cypher commands
#Create Node

def add_package(tx, name):
    tx.run("CREATE (p:Package {name: $name}) ", name=name)

#Set number of reverse dependencies
def set_num_rev_deps(tx, name, num_rev_deps):
    tx.run("MATCH (p:Package) WHERE p.name = $name SET p.num_rev_deps = $num_rev_deps", name=name, num_rev_deps=num_rev_deps)

#Set git link exists = true
def set_git_true(tx,name):
    tx.run("MATCH (p:Package) WHERE p.name = $name SET p.gitLinkExists = TRUE",name=name)

#Check if node exists
def check_package(tx, name):
    for record in tx.run("MATCH (p:Package) WHERE p.name = $name RETURN p", name=name):
        return record

#Get ID
def get_package_id(tx, name):
    for id in tx.run("MATCH (p:Package) WHERE p.name = $name RETURN ID(p)", name=name):
        return id

def get_package_name(tx, id):
    for name in tx.run("MATCH (p:Package) WHERE ID(p) = $id RETURN p.name", id=id):
        return name

#Check if reverse dependency relationship exists between two nodes
def check_reverse_dependency(tx,nameA,nameB):
    tx.run("RETURN EXISTS( (:Package {name:$nameA})-[:reverse_dependency]-(:Package {name:$nameB}))",nameA=nameA,nameB=nameB)

#Create reverse dependency relationship
def create_reverse_dependency(tx,nameA,nameB):
    tx.run("MATCH (a:Package),(b:Package) WHERE a.name = $nameA AND b.name = $nameB CREATE (a)-[r:ReverseDepends]->(b)",nameA=nameA,nameB=nameB)


#Functions that will be called

def addPackage(packageName):
    driver.session().write_transaction(add_package,packageName)

def setNumRevDeps(packageName,revDeps):
    driver.session().write_transaction(set_num_rev_deps,packageName,revDeps)

def setGitTrue(packageName):
    driver.session().write_transaction(set_git_true,packageName)

def checkPackage(packageName):
    return driver.session().read_transaction(check_package,packageName)

def getPackageId(packageName):
    return driver.session().read_transaction(get_package_id,packageName)[0]

def getPackageName(packageId):
    return driver.session().read_transaction(get_package_name,packageId)[0]

def checkRevDep(packageNameA,packageNameB):
    return driver.session().read_transaction(check_reverse_dependency,packageNameA,packageNameB)

def createRevDep(packageNameA,packageNameB):
    driver.session().write_transaction(create_reverse_dependency,packageNameA,packageNameB)
