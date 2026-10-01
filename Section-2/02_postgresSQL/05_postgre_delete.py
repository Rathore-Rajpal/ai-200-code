import psycopg

conn=psycopg.connect(
    host="ai-200-raj.postgres.database.azure.com",
    port=6432,
    dbname="appdb",
    user="sqladmin",
    password="Rathore@1811",
    sslmode="require"
)

product_id = "p6"
with conn.cursor() as cursor:
    cursor.execute("""
            DELETE FROM products
            WHERE id = %s;
        """, (
            product_id,
        ))
    conn.commit()

print("Product deleted")