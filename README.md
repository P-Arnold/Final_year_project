# Final_year_project

This repository contains most of the code that was written and used during the process of completing my final year project.
The code that was written for the project was mainly for gathering data, through HTML parsing. The data was then cleaned and stored
in a [Neo4j](https://neo4j.com/) database.
I used the project as an opportunity to become familiar with python, however I failed to make use of virtual environments and so 
libraries were installed globally on my machine and python files ran individually.

Files were updated and changed along the way in a sometimes haphazard fashion.

The directory [Hackage Parser 2](https://github.com/P-Arnold/Final_year_project/tree/master/Hackage%20Parser%202) contains two python scripts. [main.py](https://github.com/P-Arnold/Final_year_project/tree/master/Hackage%20Parser%202/main.py) and [cypherFuncs2.py](https://github.com/P-Arnold/Final_year_project/tree/master/Hackage%20Parser%202/cypherFuncs2.py).
The latter includes the functions used to interact with the Neo4j database and create the appropriate vertices and edges.

[main.py](https://github.com/P-Arnold/Final_year_project/tree/master/Hackage%20Parser%202/main.py) includes the code used for making http requests to [Hackage.org](Hackage.org), the resource from which data was gathered, and the code that parsed the returned HTML.

The other main component of code was related to the analysis of Github repositories' complexity over time.
It is included in the XXX directory.
For this I used a Haskell tool that was ran through a shell script from [script.py]


