# a cursor is the object we use to interact with the database
import pymysql.cursors
#this class will give us an instance of a connection to our database
class MySQLConnection:
    def __init__(self, db):
        #change the user/pw as needed
        connection = pymysql.connect(host = 'localhost',
                                    user = 'root',
                                    password = 'password',
                                    db = db,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = True)
        #establish the connection to the database
        self.connection = connection
    #the method to query the database
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)

                cursor.execute(query)
                if query.lower().find("insert") >= 0:
                    #INSERT queries will return the ID NUMBER of the row inserted
                    self.connecton.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    #SELECT queries will return the data of the database as a LIST OF DICTIONARIES -> some_list[0]['first_name]
                    result = cursor.fetchall()
                    return result
                else:
                    #UPDATE and DELETE queries will return nothing
                    self.connection.commit()
            except Exception as e:
                # if the query fails the method will return FALSE
                print("Something went wrong", e)
            finally:
                #close the connection
                self.connection.close()
# connectToMySQL receives the database we're using and uses it to create an instance of MySQLConneciton
def connectToMySQL(db):
    return MySQLConnection(db)