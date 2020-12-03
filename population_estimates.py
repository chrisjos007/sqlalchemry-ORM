import csv
import json
from sqlalchemy import func
from table import session, Population
from http.server import HTTPServer, SimpleHTTPRequestHandler


def dbloader(csv_data, session, asean, saarc):
    """ creates a table based on the csv data """

    # traverse through the list and add rows to table
    for line in csv_data:
        g = "None"
        if line[0] in asean:
            g = "asean"
        elif line[0] in saarc:
            g = "saarc"
        rows = Population(
                          country=line[0],
                          code=int(line[1]),
                          year=int(line[2]),
                          population=float(line[3]),
                          group=g
                        )
        session.add(rows)

    # commit the added rows to the database
    session.commit()


def india_plot(session):
    """ queries table for countries matching India

    Returns dictionary of indian population for each year """

    # query rows matching nation as India
    india_population = session.\
        query(Population.year, func.sum(Population.population)).\
        filter(Population.country == 'India').\
        group_by(Population.year).all()
    return dict(india_population)


def asean_plot(session):
    """ queries table for countries which are ASEAN

    Data considered for the year 2014 for each ASEAN nation """

    # query of ASEAN nations
    asean_population = session.\
        query(Population.country, func.sum(Population.population)).\
        filter(Population.group == 'asean', Population.year == 2014).\
        group_by(Population.country).all()

    return dict(asean_population)


def saarc_plot(session):
    """ function that queries for  population of SAARC nations

    returns population for each year """

    # query of rows belonging to SAARC nations
    saarc_population = session.\
        query(Population.year, func.sum(Population.population)).\
        filter(Population.group == 'saarc').\
        group_by(Population.year).all()

    return dict(saarc_population)


def group_plot_asean(session):
    """ Returns a population dictionary for ASEAN countries

    keys: ASEAN countries
    values: population over the years as list

    Grouped into countries over the years 2004 to 2014"""

    # query for asean nations for ordered by year
    asean_grouped = session.\
        query(Population.country, func.array_agg(Population.population)).\
        filter(Population.year >= 2004, Population.year <= 2014).\
        filter(Population.group == 'asean').\
        group_by(Population.country)

    return dict(asean_grouped)


def json_saver(dict, filename):
    """ writes a json file from the filename and dictionary passed """

    f = open(filename+".json", 'w')
    f.write(json.dumps(dict))
    f.close()


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    """ Driver code for running and keeping server running """

    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    """ Read in the csv file and maps it with the schema

    Using the table query, make function calls

    Each call returns the json file for the required plots
    and to run a local server"""

    # list of SAARC nations
    saarc = [
        "Afghanistan",
        "Bangladesh",
        "Bhutan",
        "India",
        "Maldives",
        "Nepal",
        "Pakistan",
        "Sri Lanka"
        ]

    # list of ASEAN nations
    asean = [
        "Singapore",
        "Brunei",
        "Malaysia",
        "Thailand",
        "Cambodia",
        "Indonesia",
        "Laos",
        "Myanmar",
        "Philippines",
        "Viet Nam"
        ]

    # opening the csv file and writing to a list
    with open('popest.csv', 'r') as newfile:
        csv_read = list(csv.reader(newfile, delimiter=','))

    # rename 2 nations to their shorter names
    for line in csv_read:
        if(line[0] == "Lao People's Democratic Republic"):
            line[0] = "Laos"
        if(line[0] == "Brunei Darussalam"):
            line[0] = "Brunei"

    # loading our csv data into a relational database
    dbloader(csv_read, session, asean, saarc)

    # function calls for each plot
    json_saver(india_plot(session), "india_plot")
    json_saver(asean_plot(session), "asean_plot")
    json_saver(saarc_plot(session), "saarc_plot")
    json_saver(group_plot_asean(session), "asean_group_plot")

    run()        # run localhost server
