from pymysql import OperationalError, connect


class Verifier:
    def __init__(self, ID, passwd, Type):
        self.id = ID.upper()
        self.passwd = passwd
        self.type = Type
        self.error = False

        try:
            self.conn = self.connection()
        except OperationalError:
            self.error = True

    def connection(self, host="localhost", user="root", password="password"):
        conn = connect(host, user, password, db="jee")
        return conn

    def verify(self):

        if self.error:
            raise OperationalError

        cursor = self.conn.cursor()
        if self.type == "student":
            cursor.execute("SELECT * FROM credential WHERE id='%s' AND password='%s'" % (self.id, self.passwd))
            result1 = cursor.fetchall()  # returns ( (id, name, passwd) )
            try:
                cursor.execute("SELECT * FROM student WHERE id=%s" % (self.id))
                result2 = cursor.fetchall()  # returns ( (data) )
            except Exception as e:
                print(e)
                return None
            # student credentials are wrong
            if not result1:
                return None
            else:
                return result2[0]  # student credentials

        elif self.type == "admin":
            cursor.execute("SELECT ID,password FROM credential WHERE id='admin' and password='%s'" % (self.passwd))
            result = cursor.fetchall()
            # admin password is wrong
            if not result:
                return False
            else:
                return True  # admin credentials
