# dataproject-sqlalchemy

SQL version of dataproject.

## Objective
1) Design table schema, based on your csv.
2) To write Json files using database and problem statements
3) To write HTML/CSS/JS code to plot the data on the browser

## Data and References

csv file has been provided in the repo.

[ASEAN countries wiki](https://en.wikipedia.org/wiki/ASEAN)

[SAARC countries wiki](https://en.wikipedia.org/wiki/South_Asian_Association_for_Regional_Cooperation)

## Dependencies

1) The Dependencies required for running the program has been provided in the **requirements.txt** file
2) Good network connectivity
3) web browser

## Code contents

1) population_estimates.py -> python file that writes the json files required for plotting.
2) popest.csv -> csv file containing UN population estimates
3) creator.sql -> to create the role and database
4) remover.sql -> to remove the database and role
5) index.html -> file containing HTML data
6) myplot.js -> javascript file for Highchart plotting
7) style.css -> style sheet


## Running the program

1) Clone the repository
2) run the creator.sql file in postgres
3) run the python file - population_estimates.py
4) open a browser and go to [http://localhost:8000/](http://localhost:8000/)
5) Plot specifications can be obtained in the dataproject-python README
6) run the remover.sql file in postgres