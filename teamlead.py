import sqlite3

con = sqlite3.connect('team.db')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS teamlead (
    userid INT PRIMARY KEY,
    fname TEXT,
    work TEXT);
''')
cur.execute('''INSERT INTO teamlead(userid, fname, work) VALUES(00001,'Андрей','Programmer');''')
cur.execute('''INSERT INTO teamlead(userid, fname, work) VALUES(00002,'Антон','QA');''')
cur.execute('''INSERT INTO teamlead(userid, fname, work) VALUES(00003,'Bograch','Сценарист');''')
cur.execute('''INSERT INTO teamlead(userid, fname, work) VALUES(00004,'Иван','Дизайнер');''')

cur.execute("SELECT * FROM teamlead;")
result = cur.fetchall()
print(result)

con.commit()


