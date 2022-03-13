from flask import Flask
from flask import request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)


# -- DO NOT EDIT
# sample end point for HTTP Get
@app.route("/")
def default():
    """
    default endpoint for this server, just for demo.

    :return: str
    """
    return "FIRST PROJECT - we have " + str(len(get_client_rates())) + " clients in total."


# sample data load function
# This is a temporary data file - when we get to know more about database and cloud storage
# we would not be using this kind of data storage.
def get_client_rates():
    """
    return all the client - rate pairs we have.

    :return: dict {id: {'rate':float}}
    """
    import pandas as pd
    df = pd.read_json("client_rate.json")
    return df.to_dict()


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_write_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


# load some existing data in data.sql
def load_data(database):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    sql_file = open("data.sql")
    sql_as_string = sql_file.read()
    cursor.executescript(sql_as_string)


# -- DO NOT EDIT END


# When query http://hostname/rate/client1 it would return the rate number for client1 - 0.2
@app.route("/rate/<client_id>")
def get_client_rate(client_id):
    """
    End point for getting rate for a client_id.

    :param client_id: str
    :return: http response
    """
    # SELECT rate FROM client_rates WHERE client_id = '{client_id}'
    conn = create_connection("test.db")
    res = execute_read_query(conn, f"SELECT rate FROM client_rates WHERE client_id = '{client_id}'")
    if res is None or len(res) == 0:
        return "0.0"
    return str(res[0][0])


@app.route("/rate", methods=['POST'])
def upsert_client_rate():
    """
    End point for updating or inserting client rate values in the post param.

    :return: http response.
    """
    data = request.get_json()
    update_client_rates(data["client_id"], data["rate"])
    return "SUCCESSFULLY UPDATED!"


def update_client_rates(client_id, rate):
    """
    update or insert a client_id - rate pair.

    :param client_id: string, e.g. 'client1'
    :param rate: float, e.g. 0.1
    :return:
    """
    conn = create_connection("test.db")
    res = execute_read_query(conn, f"SELECT rate FROM client_rates WHERE client_id = '{client_id}'")
    if res is None or len(res) == 0:
        # insert
        execute_write_query(conn, f"INSERT INTO client_rates (client_id, rate) VALUES('{client_id}', {rate})")
    else:
        # update
        execute_write_query(conn, f"UPDATE client_rates SET rate = {rate} WHERE id = '{client_id}'")


if __name__ == "__main__":
    # Comment load_data after the first run.
    # load_data("test.db")
    app.run()
