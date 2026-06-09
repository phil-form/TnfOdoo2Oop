import psycopg2

entities = []
connection = psycopg2.connect("dbname=postgres user=app password=1234 host=localhost port=5435")

def get_cursor():
    global connection
    return connection.cursor()