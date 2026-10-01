import psycopg

conn=psycopg.connect(
    host="ai-200-raj.postgres.database.azure.com",
    port=6432,
    dbname="appdb",
    user="sqladmin",
    password="Rathore@1811",
    sslmode="require"
)

cursor=conn.cursor()
cursor.execute("SELECT version();")

print(cursor.fetchone())
cursor.close()
conn.close()
