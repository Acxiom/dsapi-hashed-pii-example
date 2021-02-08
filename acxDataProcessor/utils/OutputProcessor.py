import sqlite3
import csv
from sqlite3 import Error
from flatten_json import flatten

class OutputProcessor:
    def __init__(self):
        self.databaseName = 'acxDataProcessSet'
        self.databaseLocation = './acxDataProcessor/db/'
        self.databaseConnString = self.databaseLocation + self.databaseName + '.db'
        self.conn = None
        self.createDatabaseConn()
        self.preferredOutputOrder = ['firstName', 'middleName', 'lastName', 'generationalSuffix', 'primaryNumber', 'preDirectional', 'street', 'streetSuffix', 'postDirectional', 'unitDesignator', 'secondaryNumber', 'city', 'state', 'zipCode', 'zipExtension', 'phone', 'email', 'latitude', 'longitude', 'ip']
        print("Created the work database " + self.databaseConnString)

    def getFlattenedOutputStructure(self, personInformation: dict, bundleInformation: dict):
        return ({**flatten(personInformation), **flatten(bundleInformation)})

    def createDatabaseConn(self):
        try:
            print("Starting db creation process")
            self.conn = sqlite3.connect(self.databaseConnString)
            print("Should have opened the db")
            print(sqlite3.version)
        
            initialDropSql = """DROP TABLE IF EXISTS IB_OUTPUT_DATA"""
            initialCreateSql = """CREATE TABLE IF NOT EXISTS IB_OUTPUT_DATA (id INTEGER PRIMARY KEY AUTOINCREMENT) """

            self.conn.execute(initialDropSql)
            self.conn.execute(initialCreateSql)
            self.conn.commit()

        except Error as e:
            print("There was an error...")
            print(e)
        
    def compareDatabaseToOutputCols(self, dataRow):
        getColumnNamesSql = """SELECT * FROM IB_OUTPUT_DATA where 1=0"""
        cursor = self.conn.execute(getColumnNamesSql)
        columnNames = list(map(lambda x: x[0], cursor.description))
        
        return list(set(dataRow) - set(columnNames))

    def getNonPreferredDbColumns(self, preferredColumns):
        getColumnNamesSql = """SELECT * FROM IB_OUTPUT_DATA where 1=0"""
        cursor = self.conn.execute(getColumnNamesSql)
        columnNames = list(map(lambda x: x[0], cursor.description))
        
        return list(set(columnNames) - set(preferredColumns))

    def addColumnsToDbForProcessing(self, dataRow):
        diffColumns = self.compareDatabaseToOutputCols(dataRow.keys())

        if diffColumns:
            for col in diffColumns:
                addColumnsSql = """ALTER TABLE IB_OUTPUT_DATA ADD COLUMN {} text""".format(col)
                print("Executing statement " + addColumnsSql)
                self.conn.execute(addColumnsSql)
        else:
            print("There were no new columns to add to processing DB...")

    def addRowToDatabaseTable(self, dataRow):
        self.addColumnsToDbForProcessing(dataRow)

        columns = ', '.join(dataRow.keys())
        placeholders = ':' + ', :'.join(dataRow.keys())
        insertRowSql="""INSERT INTO IB_OUTPUT_DATA ({}) VALUES ({})""".format(columns, placeholders)
        self.conn.execute(insertRowSql, dataRow)
        self.conn.commit()

    def processOutputIntoDb(self, outputStructure: dict):
        for dataRow in outputStructure:
            flattenedRow = self.getFlattenedOutputStructure(dataRow['origData']['origDataRow'], dataRow['response'])
            self.addRowToDatabaseTable(flattenedRow)

    def outputAllDbRowsToFile(self, outputFileLocation: str):
        selectAllSql = """SELECT {}, {} FROM IB_OUTPUT_DATA""".format(', '.join(self.preferredOutputOrder), ', '.join(self.getNonPreferredDbColumns(self.preferredOutputOrder)))

        with open(outputFileLocation, "w", newline='') as outputFile:
            csv_out = csv.writer(outputFile)
            cursor = self.conn.cursor().execute(selectAllSql)
            csv_out.writerow(d[0] for d in cursor.description)
            for row in cursor:
                csv_out.writerow(row)
            