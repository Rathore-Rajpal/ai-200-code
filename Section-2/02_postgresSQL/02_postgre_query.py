import psycopg

conn=psycopg.connect(
    host="ai-200-raj.postgres.database.azure.com",
    port=6432,
    dbname="appdb",
    user="sqladmin",
    password="Rathore@1811",
    sslmode="require"
)

with conn.cursor() as cursor:
    cursor.execute("""
        SELECT id, name, category, price, stock_quantity
        FROM products
        ORDER BY name;
    """)
    products = cursor.fetchall()
for product in products:

    print(
        f"ID: {product[0]} | "
        f"Name: {product[1]} | "
        f"Category: {product[2]} | "
        f"Price: {product[3]} | "
        f"Stock: {product[4]}"
    )


conn.close()