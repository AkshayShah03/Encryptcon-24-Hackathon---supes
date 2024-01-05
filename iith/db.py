import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234"
)
mycursor = mydb.cursor()
mycursor.execute("USE mlops")

#one time
'''
mycursor.execute("CREATE DATABASE supes")

mycursor.execute("SHOW DATABASES")
res = mycursor.fetchall()
print(res)

mycursor.execute("USE supes")
mycursor.execute(
    """
    CREATE TABLE customer(
        goal VARCHAR(500),
        budget INT,
        coll INT,
        assets INT,
        location VARCHAR(255),
        income INT,
        selected_options VARCHAR(30),
        extra_answer1 VARCHAR(50),
        extra_answer2 INT
    )
    """
)
'''

def new_customer(goal, budget, coll, assets, location, income, selectOptions, extra_answer1, extra_answer2):
    mycursor.execute("USE supes")
    sql = """
        INSERT INTO customer
        (goal, budget, coll, assets, location, income, selectOptions, extraAnswer1, extraAnswer2)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (goal, budget, coll, assets, location, income, selectOptions, extra_answer1, extra_answer2)
    
    mycursor.execute(sql, values)
    mydb.commit()