import sqlite3

DB_NAME = "database.db"

def init_db():
    """Cria a tabela produto se não existir"""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produto (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                valor REAL
            )
        """)
        conn.commit()

def add_produto(nome, valor):
    """Insere um produto no banco"""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO produto (nome, valor) VALUES (?, ?)", (nome, valor))
        conn.commit()

def get_produtos():
    """Retorna todos os produtos"""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produto")
        return cursor.fetchall()
