__author__ = 'yanglikun'
# 首先在config.properties配置数据库信息
from mysql2doc.MySql import Schema

Schema.createFile()

