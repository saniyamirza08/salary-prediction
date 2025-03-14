import mysql.connector as mc

conn = mc.connect(user='root', password='SaniyaMirza@23', host='localhost', database='datascience')

if conn.is_connected():
    print("You are connected.")
else:
    print('Unable to connect.')

mycursor = conn.cursor()

query = """CREATE TABLE Salaries_data(
    job_title VARCHAR(100),
    job_type VARCHAR(50),
    experience_level VARCHAR(50),
    predicted int
)
"""

mycursor.execute(query)
print('Your table is created.')

mycursor.close()
conn.close()
