import sqlite3
from flask import g
import os

def get_db():
    """Conecta ao banco de dados"""
    if 'db' not in g:
        database_path = os.path.join(os.path.dirname(__file__), 'database.db')
        g.db = sqlite3.connect(database_path)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """Fecha a conexão com o banco de dados"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    """Registra funções com o app Flask"""
    app.teardown_appcontext(close_db)

def get_ferramentas():
    """Busca todas as ferramentas do banco"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("""
        SELECT 
            f.id,
            f.nome as ferramenta_nome,
            f.comando_sintaxe,
            f.protocolo_padrao,
            f.tipo,
            f.contexto_uso,
            fn.nome as funcao_nome,
            fn.descricao as funcao_descricao,
            fr.nome as fornecedor_nome,
            fr.descricao as fornecedor_descricao
        FROM ferramenta f
        JOIN funcao fn ON f.funcao_id = fn.id
        JOIN fornecedor fr ON f.fornecedor_id = fr.id
        ORDER BY fn.nome, f.nome
    """)
    
    return cursor.fetchall()

def get_funcoes():
    """Busca todas as funções do banco"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, nome, descricao FROM funcao ORDER BY nome")
    return cursor.fetchall()

def get_fornecedores():
    """Busca todos os fornecedores do banco"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, nome, descricao FROM fornecedor ORDER BY nome")
    return cursor.fetchall()

def get_ferramentas_por_funcao(funcao_id):
    """Busca ferramentas por função específica"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("""
        SELECT 
            f.id,
            f.nome as ferramenta_nome,
            f.comando_sintaxe,
            f.protocolo_padrao,
            f.tipo,
            f.contexto_uso,
            fn.nome as funcao_nome,
            fr.nome as fornecedor_nome
        FROM ferramenta f
        JOIN funcao fn ON f.funcao_id = fn.id
        JOIN fornecedor fr ON f.fornecedor_id = fr.id
        WHERE f.funcao_id = ?
        ORDER BY f.nome
    """, (funcao_id,))
    
    return cursor.fetchall()

def get_ferramentas_por_fornecedor(fornecedor_id):
    """Busca ferramentas por fornecedor específico"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("""
        SELECT 
            f.id,
            f.nome as ferramenta_nome,
            f.comando_sintaxe,
            f.protocolo_padrao,
            f.tipo,
            f.contexto_uso,
            fn.nome as funcao_nome,
            fr.nome as fornecedor_nome
        FROM ferramenta f
        JOIN funcao fn ON f.funcao_id = fn.id
        JOIN fornecedor fr ON f.fornecedor_id = fr.id
        WHERE f.fornecedor_id = ?
        ORDER BY fn.nome, f.nome
    """, (fornecedor_id,))
    
    return cursor.fetchall()

def buscar_ferramentas(termo):
    """Busca ferramentas por termo em múltiplos campos incluindo comando_sintaxe"""
    db = get_db()
    cursor = db.cursor()
    
    termo_pattern = f'%{termo.lower()}%'
    
    cursor.execute("""
        SELECT 
            f.id,
            f.nome as ferramenta_nome,
            f.comando_sintaxe,
            f.protocolo_padrao,
            f.tipo,
            f.contexto_uso,
            fn.nome as funcao_nome,
            fr.nome as fornecedor_nome
        FROM ferramenta f
        JOIN funcao fn ON f.funcao_id = fn.id
        JOIN fornecedor fr ON f.fornecedor_id = fr.id
        WHERE LOWER(f.nome) LIKE ? OR 
              LOWER(fn.nome) LIKE ? OR 
              LOWER(fr.nome) LIKE ? OR 
              LOWER(f.comando_sintaxe) LIKE ? OR 
              LOWER(f.protocolo_padrao) LIKE ? OR 
              LOWER(f.tipo) LIKE ? OR 
              LOWER(f.contexto_uso) LIKE ?
        ORDER BY fn.nome, f.nome
    """, [termo_pattern] * 7)
    
    return cursor.fetchall()

def get_ferramenta_por_id(ferramenta_id):
    """Obtém uma ferramenta específica por ID"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("""
        SELECT 
            f.id,
            f.nome as ferramenta_nome,
            f.comando_sintaxe,
            f.protocolo_padrao,
            f.tipo,
            f.contexto_uso,
            fn.nome as funcao_nome,
            fn.descricao as funcao_descricao,
            fr.nome as fornecedor_nome,
            fr.descricao as fornecedor_descricao
        FROM ferramenta f
        JOIN funcao fn ON f.funcao_id = fn.id
        JOIN fornecedor fr ON f.fornecedor_id = fr.id
        WHERE f.id = ?
    """, (ferramenta_id,))
    
    return cursor.fetchone()

def get_todas_ferramentas_ids():
    """Obtém todos os IDs de ferramentas para o sitemap"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT id FROM ferramenta ORDER BY id")
    return [row[0] for row in cursor.fetchall()]

def adicionar_ferramenta(dados_ferramenta):
    """Adiciona uma nova ferramenta ao banco de dados"""
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO ferramenta 
            (funcao_id, fornecedor_id, nome, comando_sintaxe, protocolo_padrao, tipo, contexto_uso) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            dados_ferramenta['funcao_id'],
            dados_ferramenta['fornecedor_id'],
            dados_ferramenta['nome'],
            dados_ferramenta['comando_sintaxe'],
            dados_ferramenta['protocolo_padrao'],
            dados_ferramenta['tipo'],
            dados_ferramenta['contexto_uso']
        ))
        
        db.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        db.rollback()
        raise e

def adicionar_funcao(nome, descricao):
    """Adiciona uma nova função ao banco de dados"""
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO funcao (nome, descricao, ramo_id) 
            VALUES (?, ?, ?)
        """, (nome, descricao, 1))  # ramo_id 1 = Redes de Computadores
        
        db.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        db.rollback()
        raise e

def adicionar_fornecedor(nome, descricao):
    """Adiciona um novo fornecedor ao banco de dados"""
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO fornecedor (nome, descricao) 
            VALUES (?, ?)
        """, (nome, descricao))
        
        db.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        db.rollback()
        raise e

def get_estatisticas():
    """Obtém estatísticas do banco de dados"""
    db = get_db()
    cursor = db.cursor()
    
    estatisticas = {}
    
    # Total de ferramentas
    cursor.execute("SELECT COUNT(*) FROM ferramenta")
    estatisticas['total_ferramentas'] = cursor.fetchone()[0]
    
    # Total de funções
    cursor.execute("SELECT COUNT(*) FROM funcao")
    estatisticas['total_funcoes'] = cursor.fetchone()[0]
    
    # Total de fornecedores
    cursor.execute("SELECT COUNT(*) FROM fornecedor")
    estatisticas['total_fornecedores'] = cursor.fetchone()[0]
    
    # Ferramentas por tipo
    cursor.execute("SELECT tipo, COUNT(*) FROM ferramenta GROUP BY tipo")
    estatisticas['ferramentas_por_tipo'] = dict(cursor.fetchall())
    
    return estatisticas