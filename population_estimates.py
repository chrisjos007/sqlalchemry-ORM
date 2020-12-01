import csv
import json
from sqlalchemy import Integer, Column, String, Float, create_engine
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def dbloader(csv_data, session):
    """ creates a table based on the csv data """

    # traverse through the list and add rows to table
    for line in csv_data:
        population = User(
                          country=line[0],
                          code=int(line[1]),
                          year=int(line[2]),
                          population=float(line[3])
                        )
        session.add(population)

    # commit the added rows to the database
    session.commit()


def india_plot(session):
    """ Returns dictionary of indian population for each year """

    india_pop = defaultdict(float)

    # query rows matching nation as India
    for row in session.query(User).filter(User.country == 'India'):
        india_pop[row.year] += row.population

    return india_pop


def asean_plot(session, asean):
    """ queries table for countries in ASEAN nations

    Data considered for the year 2014 for each ASEAN nation """

    asean_dict = defaultdict(float)

    # query of ASEAN nations
    for row in session.query(User).\
            filter(User.year == 2014, User.country.in_(asean)):
        asean_dict[row.country] += row.population

    return asean_dict


def saarc_plot(session, saarc):
    """ queries filtering population of SAARC nations

    returns population dictionary based on the query"""

    saarc_dict = defaultdict(float)

    # query of rows belonging to SAARC nations
    for row in session.query(User).filter(User.country.in_(saarc)):
        saarc_dict[row.year] += row.population

    return saarc_dict


def group_plot_asean(session, asean):
    """ Returns a population dictionary for ASEAN countries

    keys: ASEAN countries
    values: population over the years as list

    Grouped into countries over the years 2004 to 2014"""

    population_asean = defaultdict(dict)
    population_list = defaultdict(list)
    years = [i for i in range(2004, 2015)]    # list of years

    # query for rows matching ASEAN nations for each year
    for row in session.query(User).\
        filter(User.country.in_(asean)).\
            filter(User.year.in_(years)):
        population_asean[row.country][row.year] = row.population

    for key, val in population_asean.items():
        population_list[key] = list(val.values())

    return population_list


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
    """ Creates a mapping and binds it to session
    Read in the csv file and create table from it.

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

    # catalog for the ORM model
    Base = declarative_base()

    # ORM table model
    class User(Base):
        __tablename__ = 'UN_population'
        id = Column(Integer, primary_key=True)
        country = Column(String)
        code = Column(Integer)
        year = Column(Integer)
        population = Column(Float)

        def __repr__(self):
            return f"<Population(id={self.id},\
                        country={self.country},\
                        country_code={self.code},\
                        year={self.year},\
                        population={self.population})>"

    # creates a new engine instance using postgres
    engine = create_engine(
        'postgres://chris:chris@localhost:5432/sqlp', echo=True)

    Base.metadata.create_all(engine)

    # creating session object and binding to engine
    Session = sessionmaker(bind=engine)
    session = Session()

    # loading our csv data into a relational database
    dbloader(csv_read, session)

    # function calls for each plot
    json_saver(india_plot(session), "india_plot")
    json_saver(asean_plot(session, asean), "asean_plot")
    json_saver(saarc_plot(session, saarc), "saarc_plot")
    json_saver(group_plot_asean(session, asean), "asean_group_plot")

    run()        # run localhost server
