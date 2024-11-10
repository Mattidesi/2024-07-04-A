from database.DB_connect import DBConnect
from model.edge import Edge
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllSighting(year,shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.*
                        from sighting s 
                        where year(`datetime`) = %s
                        and shape = %s"""
            cursor.execute(query,(year,shape))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    #

    @staticmethod
    def getYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year(`datetime`) as year
                        from sighting s 
                        order by year(`datetime`) desc """
            cursor.execute(query)
            for row in cursor:
                result.append(row['year'])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getShapes(year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct shape 
                        from sighting s 
                        where shape != ''
                        and year(s.`datetime`) = %s 
                        order by shape asc"""
            cursor.execute(query,(year,))
            for row in cursor:
                result.append(row['shape'])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllEdges(year,shape,idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select t1.id as s1,t1.datetime as data1,t2.id as s2,t2.datetime as data2
                        from 
                        (select *
                         from sighting s
                         where year(datetime) = %s
                         and shape = %s) t1,
                        (select *
                         from sighting s
                         where year(datetime) = %s
                         and shape = %s) t2
                         where t1.state = t2.state
                         and t1.datetime < t2.datetime"""
            cursor.execute(query,(year,shape,year,shape))
            for row in cursor:
                result.append(Edge(idMap[row["s1"]],row["data1"],idMap[row["s2"]],row["data2"]))
            cursor.close()
            cnx.close()
        return result