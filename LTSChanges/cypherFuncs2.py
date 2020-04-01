from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "ltslts"))


#Neo4J Cypher commands
#Create Node _WITH_ LTS

def add_package(tx, name, lts):
    tx.run("CREATE (p:Package {name: $name, lts: $lts}) ", name=name, lts=lts)

#Set number of reverse dependencies
def set_num_rev_deps(tx, name, lts, num_rev_deps):
    tx.run("MATCH (p:Package) WHERE p.name = $name AND p.lts = $lts SET p.num_rev_deps = $num_rev_deps", name=name, lts=lts, num_rev_deps=num_rev_deps)

#Set git link exists = true
# def set_git_true(tx,name):
#     tx.run("MATCH (p:Package) WHERE p.name = $name SET p.gitLinkExists = TRUE",name=name)

#Check if node exists
def check_package(tx, name, lts):
    for record in tx.run("MATCH (p:Package) WHERE p.name = $name AND p.lts = $lts RETURN p", name=name, lts=lts):
        return record

#Get ID
def get_package_id(tx, name, lts):
    for id in tx.run("MATCH (p:Package) WHERE p.name = $name AND p.lts = $lts RETURN ID(p)", name=name, lts=lts):
        return id

def get_package_name(tx, id, lts):
    for name in tx.run("MATCH (p:Package) WHERE ID(p) = $id AND p.lts = $lts RETURN p.name", id=id):
        return name

#Check if reverse dependency relationship exists between two nodes
def check_reverse_dependency(tx,nameA,nameB,lts):
    tx.run("RETURN EXISTS( (:Package {name:$nameA,lts:$lts})-[:reverse_dependency]-(:Package {name:$nameB,lts:$lts}))",nameA=nameA,nameB=nameB,lts=lts)

#Create reverse dependency relationship
def create_reverse_dependency(tx,nameA,nameB,lts):
    tx.run("MATCH (a:Package),(b:Package) WHERE a.name = $nameA AND b.name = $nameB AND a.lts = $lts AND b.lts = $lts CREATE (a)-[r:ReverseDepends]->(b)",nameA=nameA,nameB=nameB,lts=lts)


#Functions that will be called

def addPackage(packageName,lts):
    driver.session().write_transaction(add_package,packageName,lts)

def setNumRevDeps(packageName,lts,revDeps):
    driver.session().write_transaction(set_num_rev_deps,packageName,lts,revDeps)

# def setGitTrue(packageName):
#     driver.session().write_transaction(set_git_true,packageName)

def checkPackage(packageName,lts):
    return driver.session().read_transaction(check_package,packageName,lts)

def getPackageId(packageName,lts):
    return driver.session().read_transaction(get_package_id,packageName,lts)[0]

def getPackageName(packageId,lts):
    return driver.session().read_transaction(get_package_name,packageId,lts)[0]

def checkRevDep(packageNameA,packageNameB,lts):
    return driver.session().read_transaction(check_reverse_dependency,packageNameA,packageNameB,lts)

def createRevDep(packageNameA,packageNameB,lts):
    driver.session().write_transaction(create_reverse_dependency,packageNameA,packageNameB,lts)
