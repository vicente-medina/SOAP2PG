# Program to consume data from SOAP WS and upload to PostgreSQL

import sys
import configparser
from zeep import Client
from lxml import etree
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from fechasGui import Ui_Dialog
from PyQt5 import QtSql
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt


class ui_Dialog(QWidget):
    def __init__(self):

        # Init dialog
        super().__init__()

        # Read config
        self.readConfig()

        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.show()

    def readConfig(self):

        # Read the config file
        config = configparser.ConfigParser()
        config.read("Server.txt")
        # config.read("Server_demo.txt")

        # Set the variables
        self.WSDL_URL = config.get("serverConfig", "WSDL_URL")
        self.LOGIN = config.get("serverConfig", "login")
        self.PASSWORD = config.get("serverConfig", "password")

    def readPGConfig(self):

        # Read the config file
        config = configparser.ConfigParser()
        config.read("Server.txt")
        # config.read("Server_demo.txt")

        # Set the variables
        self.dbName = config.get("postgresConfig", "db")
        self.dbUsername = config.get("postgresConfig", "username")
        self.dbPassword = config.get("postgresConfig", "password")
        self.dbHostName = config.get("postgresConfig", "hostname")

    # Perform the task
    def accept(self):
        print("Call to Ok.")

        # Get the datetime from Gui
        self.desdeText = self.ui.fechaDesde.text()
        self.hastaText = self.ui.fechaHasta.text()

        # Set cursor
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

        # Run
        client = Client(wsdl=self.WSDL_URL)
        self.xmlResponse = client.service.GetServiciosPorVehiculo(login=self.LOGIN, password=self.PASSWORD, fechaDesde=self.desdeText, fechaHasta=self.hastaText)
        print(self.xmlResponse)

        # to database
        self.uploadToPosgreSQL()

        # Get the vehicles id
        self.xmlResponse = client.service.GetVehiculos(login=self.LOGIN, password=self.PASSWORD)
        print(self.xmlResponse)

        # to database
        self.uploadVehiclesToPosgreSQL()

        # Get the vehicles id
        self.xmlResponse = client.service.GetPosicionesGPS(login=self.LOGIN, password=self.PASSWORD, fechadesde=self.desdeText, fechahasta=self.hastaText)
        print(self.xmlResponse)

        # to database
        self.uploadGPSToPosgreSQL()

        # Default cursor
        QApplication.restoreOverrideCursor()


    def uploadToPosgreSQL(self):

        # Read PG configuration
        self.readPGConfig()

        # Set database
        self.db = QtSql.QSqlDatabase.addDatabase('QPSQL')
        self.db.setDatabaseName(self.dbName)

        # Set user data
        self.db.setUserName(self.dbUsername)
        self.db.setPassword(self.dbPassword)
        self.db.setHostName(self.dbHostName)

        if not self.db.open():
            QMessageBox.critical(None, "Cannot open database",
                                       "Unable to establish a database connection.\n",
                                       QMessageBox.Cancel)

            return False


        # Query
        self.query = QtSql.QSqlQuery()

        self.query.exec_("DROP TABLE IF EXISTS llicamunt.servicios_por_vehiculo")
        self.query.exec_("CREATE TABLE llicamunt.servicios_por_vehiculo("
                    "id_vehiculo text NOT NULL,"
                    "matricula text NOT NULL,"
                    "tipoVehiculo text,"
                    "fechaHora text,"
                    "tipoServicio text,"
                    "the_geom geometry(Point,4326),"
                    "CONSTRAINT servicios_por_vehiculo_pkey PRIMARY KEY(id_vehiculo, fechaHora))")

        # Parse xml response
        registros = etree.fromstring(self.xmlResponse)

        # Datos leidos
        print("Datos de vehiculos leidos:\n\n")
        print(" idVehiculo matricula tipoVehiculo fechaHora  coordenadaX  coordenadaY tipoServicio tag marcaContenedor tipoContenedor tipoResiduo volumen peso idUbicacion tipoUbicacion distrito")
        print("=========================================================")
        for registro in registros:
            print("%10s %10s %14s %20s %10s %10s %14s %20s %10s %10s %14s %20s %10s %10s %14s %20s" % (registro[0].text, registro[1].text, registro[2].text, registro[3].text, registro[4].text, registro[5].text, registro[6].text, registro[7].text, registro[8].text, registro[9].text, registro[10].text, registro[11].text, registro[12].text, registro[13].text, registro[14].text, registro[15].text))

            self.query.exec_("INSERT INTO llicamunt.servicios_por_vehiculo values('" +
                        registro[0].text + "','" +
                        registro[1].text + "','" +
                        registro[2].text + "','" +
                        registro[3].text + "','" +
                        registro[6].text + "'," +
                        "ST_SetSRID(ST_MakePoint(" + registro[5].text + "," + registro[4].text + "),4326))"
                        )

        return True



    def uploadVehiclesToPosgreSQL(self):

        self.query.exec_("DROP TABLE IF EXISTS llicamunt.vehiculos")
        self.query.exec_("CREATE TABLE llicamunt.vehiculos("
                    "matricula text NOT NULL,"
                    "calca text,"
                    "descripcion text,"
                    "tipoVehiculo text,"
                    "CONSTRAINT vehiculos_pkey PRIMARY KEY(matricula))")

        # Parse xml response
        registros = etree.fromstring(self.xmlResponse)

        # Datos leidos
        print("Datos de vehiculos leidos:\n\n")
        print(" matricula    calca      descripcion     tipoVehiculo")
        print("=========================================================")
        for registro in registros:
            print("%10s %10s %14s %20s" % (registro[0].text, registro[1].text, registro[2].text, registro[3].text))

            if not self.query.exec_("INSERT INTO llicamunt.vehiculos values('" +
                        registro[0].text + "','" +
                        xstr(registro[1].text) + "','" +
                        xstr(registro[2].text) + "','" +
                        xstr(registro[3].text) + "')"
                        ):
                print(self.query.lastError())

        return True


    def uploadGPSToPosgreSQL(self):

        self.query.exec_("DROP TABLE IF EXISTS llicamunt.posiciones_gps")
        self.query.exec_("CREATE TABLE llicamunt.posiciones_gps("
                         "id_vehiculo text NOT NULL,"
                         "matricula text NOT NULL,"
                         "fechaHora text,"
                         "sensor1 text,"
                         "sensor2 text,"
                         "sensor3 text,"
                         "evento text,"
                         "the_geom geometry(Point,4326),"
                         "CONSTRAINT posiciones_gps_pkey PRIMARY KEY(id_vehiculo, fechaHora))")

        # Create view
        self.query.exec_("CREATE OR REPLACE VIEW llicamunt.v_posiciones_gps AS "
                         "SELECT min(gps.matricula) AS "
                         "matricula, st_makeline(array_agg(gps.the_geom)) AS newgeom FROM "
                         "(SELECT posiciones_gps.matricula, posiciones_gps.fechahora, "
                         "posiciones_gps.sensor1, posiciones_gps.the_geom, posiciones_gps.evento "
                         "FROM llicamunt.posiciones_gps ORDER BY posiciones_gps.fechahora) gps "
                         "GROUP BY gps.matricula")

        # Parse xml response
        registros = etree.fromstring(self.xmlResponse)

        # Datos leidos
        print("Datos de GPS leidos:\n\n")
        print(" idVehiculo        matricula           fechaHora     coordenadaX     coordenadaY   velocidad     sensor1     sensor2     sensor3     evento")
        print("=========================================================")
        for registro in registros:
            print("%20s %10s %30s %20s %20s %10s %20s %20s %20s %10s" % (registro[0].text, registro[1].text, registro[2].text, registro[3].text, registro[4].text, registro[5].text, registro[6].text, registro[7].text, registro[8].text, registro[9].text))

            if not self.query.exec_("INSERT INTO llicamunt.posiciones_gps values('" +
                         registro[0].text + "','" +
                         registro[1].text + "','" +
                         registro[2].text + "','" +
                         xstr(registro[6].text) + "','" +
                         xstr(registro[7].text) + "','" +
                         xstr(registro[8].text) + "','" +
                         xstr(registro[9].text) + "'," +
                         "ST_SetSRID(ST_MakePoint(" + registro[4].text + "," + registro[3].text + "),4326))"
                        ):
                print(self.query.lastError().text())


        return True


# Filter NULL db responses
def xstr(s):
    if s is None:
        return ''
    return s


if __name__ == '__main__':

    # Create Gui
    app = QApplication(sys.argv)
    myapp = ui_Dialog()

    # Show Gui
    sys.exit(app.exec_())



#
# # Parse xml response
# registros = etree.fromstring(xmlResponse)
#
# # Datos leidos
# print("Datos de vehiculos leidos:\n\n")
# print(" Matricula      Calca    Descripcion     Tipo de vehiculo")
# print("=========================================================")
# for registro in registros:
#     print("%10s %10s %14s %20s" % (registro[0].text, registro[1].text, registro[2].text, registro[3].text))
#
#
#
#
# # Matriculas
# print("Matriculas leidas:")
# for matricula in registros.iter("matricula"):
#     print(matricula.text)