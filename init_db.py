import sqlite3

conn = sqlite3.connect('pedidos.db')
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    whatsapp TEXT NOT NULL,
    retirada TEXT NOT NULL,
    dia_retirada TEXT,
    nome_voluntario TEXT,
    total_pizzas INTEGER NOT NULL,
    total_preco REAL NOT NULL,
    data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pizzas_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER,
    sabor TEXT,
    quantidade INTEGER,
    FOREIGN KEY (pedido_id) REFERENCES pedidos (id)
);
""")

conn.commit()
conn.close()

print("Banco de dados e tabelas criados com sucesso.")