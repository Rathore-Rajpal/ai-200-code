CREATE TABLE products(
    id VARCHAR(20) PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    embedding VECTOR(1536)
)