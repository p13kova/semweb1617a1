from urllib.request import urlopen,Request
from urllib.parse import urlencode
import json

endpoint = "http://data.linkedmdb.org/sparql?"
print ("paraxwriste mou onoma ithopoiou: ")

start =input()

getActorsByName = """
PREFIX movie: <http://data.linkedmdb.org/resource/movie/>
PREFIX lmdba: <http://data.linkedmdb.org/resource/actor/>
PREFIX lmdbf: <http://data.linkedmdb.org/resource/film/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?actor ?aname WHERE {
?actor a movie:actor .
?actor movie:actor_name ?aname.
FILTER (regex(?aname,"^""" + start + """","i"))
}
"""

params = { 'query': getActorsByName }
paramstr = urlencode(params)

req = Request(endpoint+paramstr)
req.add_header('Accept','application/sparql-results+json')
page = urlopen(req)
text = page.read().decode('utf-8')
page.close()

archJson = json.loads(text)

actorsDict = {}


for binding in archJson['results']['bindings']:
        actorsDict[binding['aname']['value']] = binding['actor']['value']



print("diathesimoi ithopoioi: ")

for eisagwgi in actorsDict:
        print(eisagwgi)

print("dialekse ithopoio ")
specificActor = input()

if (specificActor in actorsDict):
	selectedURI = actorsDict[specificActor]

else:
	print("den uparxei ithopoios me ayto to onoma")


getCoActors = """
PREFIX movie: <http://data.linkedmdb.org/resource/movie/>
PREFIX lmdba: <http://data.linkedmdb.org/resource/actor/>
PREFIX lmdbf: <http://data.linkedmdb.org/resource/film/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT(?filmName) ?actorName WHERE {
	?film movie:actor <""" + selectedURI+"""> .
	?film movie:actor ?oneDeg .
	?film rdfs:label ?filmName .
	?oneDeg movie:actor_name ?actorName .
	FILTER(?oneDeg != <""" + selectedURI+""">)
}
"""

params = { 'query': getCoActors }
paramstr = urlencode(params)


req = Request(endpoint+paramstr)
req.add_header('Accept','application/sparql-results+json')
page = urlopen(req)
text = page.read().decode('utf-8')
page.close()

archJsonCoActors = json.loads(text)

print("oriste h lista me tis tainies tou/tis " + specificActor + " me symprotagwnisti: ")

for binding in archJsonCoActors['results']['bindings']:

       print(binding['actorName']['value'],"sthn tainia", binding['.0']['value'])



