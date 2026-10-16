# PyMySQL as MySQLdb drop-in (no C compiler / mysqlclient needed, works on Windows)
try:
    import pymysql
    pymysql.version_info = (2, 2, 1, "final", 0)
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
