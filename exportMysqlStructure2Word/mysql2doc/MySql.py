__author__ = 'yanglikun'
from sqlalchemy import create_engine
import jsonpickle
from mysql2doc.TableData import *
import sys, traceback
from mysql2doc.config import dbConfigMap
from mysql2doc.Document import Word
from mysql2doc.Document import Document

class Schema:
    def __init__(self):
        super().__init__()
        dburl = "mysql+pymysql://{userName}:{password}@{host}:{port}/{databaseName}?charset={charset}".format(
            **dbConfigMap
        )
        self.engine = create_engine(dburl)

    def showSchemas(self):
        return [ele[0] for ele in self.engine.execute('select schema_name from information_schema.schemata where schema_name not in ("information_schema", "mysql","performance_schema")')]

    def showTables(self, schema):
        value = self.engine.execute('select table_name,table_comment from information_schema.TABLES where table_schema = \'' + schema + '\'')
        return value

    def tableDetail(self, schema, tableName, tableComment):
        fields = []
        for fieldRow in self.engine.execute('show full columns from ' + schema + '.' + tableName):
            field = Field()
            field.name = fieldRow['Field']
            field.type = str(fieldRow['Type']).lower()
            field.nullable = fieldRow['Null']
            field.isPK = fieldRow['Key'] == 'PRI'
            field.comment = fieldRow['Comment']
            field.default = fieldRow['Default']
            field.extra = fieldRow['Extra']
            fields.append(field)
        tableComment = tableComment
        indices = []
        for idx in self.engine.execute('show index from ' + schema + '.' +tableName):
            index = Index()
            index.isUnique = (idx['Non_unique'] == 0)
            index.name = str(idx['Key_name'])
            fieldName = idx['Column_name']
            index.fieldName = str(fieldName).lower()
            index.comment = idx['Comment']
            index.seqNO = str(idx['Seq_in_index'])
            index.type = idx['Index_type']
            indices.append(index)

        table = Table(tableName)
        table.fields = fields
        table.indices = indices
        table.comment = tableComment
        return table

    def generateTableData(self, schema):
        tableNames = self.showTables(schema)
        return [self.tableDetail(schema, tableName, tableComment) for (tableName, tableComment) in tableNames]

    def close(mysql):
        if mysql is None:
            return
        try:
            mysql.engine.dispose()
        except:
            traceback.print_exc(file=sys.stdout)


    def createFile(fileName='database'):
        mysql=None
        try:
            mysql = Schema()

            schemas = mysql.showSchemas()
            for schema in schemas:
                document = Document()
                document.add_heading('数据库表结构', 0)
                document.add_paragraph('数据库表结构')
            
                word = Word(document)

                for idx, table in enumerate(mysql.generateTableData(schema)):
                    word.addTable(table, idx)

                document.add_page_break()
                document.save(schema + '.docx')
        finally:
            Schema.close(mysql)