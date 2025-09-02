import sqlite3

# Conecta ao banco
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Lista todas as tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cursor.fetchall()

print("Tabelas existentes e seus registros:")
for tabela in tabelas:
    tabela_nome = tabela[0]
    print(f"\nTabela: {tabela_nome}")

    # Mostra colunas da tabela
    cursor.execute(f"PRAGMA table_info({tabela_nome});")
    colunas = cursor.fetchall()
    col_names = [coluna[1] for coluna in colunas]
    print("Colunas:", ", ".join(col_names))

    # Mostra registros da tabela
    cursor.execute(f"SELECT * FROM {tabela_nome};")
    registros = cursor.fetchall()
    if registros:
        for registro in registros:
            print("Registro:", registro)
    else:
        print("Nenhum registro encontrado.")

conn.close()
