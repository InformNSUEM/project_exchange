import pyodbc
from django.conf import settings


class StudentData:
    server = settings.TANDEM_HOST
    database = settings.TANDEM_DB
    username = settings.TANDEM_USERNAME
    password = settings.TANDEM_PASSWORD

    def connect(self):

        self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+self.password)


    def get(self, booknumber):
        
        self.connect()

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(f"""select distinct
            VPO.LASTNAME lastname
            ,VPO.FIRSTNAME firstname
            ,VPO.MIDDLENAME partonymic
            ,VPO.EMAIL email
            ,VPO.PHONEMOBILE mobile
            ,ISNULL(VPO.PHONEDEFAULT, '') dopmobile
            ,VPO.BIRTHDATE datebirth
            ,VPO.GROUPTITLE as 'group'
            from vpo2_view  VPO
            join PERSON_T P on P.ID = VPO.PERSON_ID
            join PERSONCONTACTDATA_T CD on P.CONTACTDATA_ID = CD.ID

            WHERE VPO.STATUSTITLE = 'активный' 
            and VPO.BOOKNUMBER = '{booknumber}'
            """)
            row = cursor.fetchone()
            
            if row:
                return row
            

