import sqlite3

def adicionar_nova_ferramenta():
    # Conectar ao banco de dados
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    print("=== ADICIONAR NOVA FERRAMENTA ===")
    
    # Verificar se existem fornecedores
    cursor.execute("SELECT COUNT(*) FROM fornecedor")
    count_fornecedores = cursor.fetchone()[0]
    
    if count_fornecedores == 0:
        print("Nenhum fornecedor encontrado. Vamos criar um novo.")
        usar_existente = 'n'
    else:
        # Listar fornecedores existentes
        cursor.execute("SELECT id, nome, descricao FROM fornecedor ORDER BY nome")
        fornecedores = cursor.fetchall()
        
        print("\nFornecedores existentes:")
        for id, nome, descricao in fornecedores:
            print(f"{id}: {nome} - {descricao}")
        
        # Opção para usar fornecedor existente ou adicionar novo
        usar_existente = input("\nDeseja usar um fornecedor existente? (s/n): ").lower().strip()
    
    if usar_existente == 's':
        fornecedor_id = input("Digite o ID do fornecedor: ")
        # Validar se o ID existe
        cursor.execute("SELECT id FROM fornecedor WHERE id = ?", (fornecedor_id,))
        if not cursor.fetchone():
            print("ID de fornecedor inválido! Criando novo fornecedor...")
            usar_existente = 'n'
    
    if usar_existente != 's':
        # Adicionar novo fornecedor
        novo_fornecedor = input("Nome do novo fornecedor: ")
        descricao_fornecedor = input("Descrição do fornecedor: ")
        
        cursor.execute(
            "INSERT INTO fornecedor (nome, descricao) VALUES (?, ?)",
            (novo_fornecedor, descricao_fornecedor)
        )
        fornecedor_id = cursor.lastrowid
        print(f"Fornecedor '{novo_fornecedor}' adicionado com ID {fornecedor_id}")
        conn.commit()
    
    # Verificar se existem funções
    cursor.execute("SELECT COUNT(*) FROM funcao")
    count_funcoes = cursor.fetchone()[0]
    
    if count_funcoes == 0:
        print("Nenhuma função encontrada. Vamos criar uma nova.")
        funcao_id = adicionar_nova_funcao_durante_processo(cursor, conn)
    else:
        # Listar funções existentes
        cursor.execute("SELECT id, nome, descricao FROM funcao ORDER BY nome")
        funcoes = cursor.fetchall()
        
        print("\nFunções existentes:")
        for id, nome, descricao in funcoes:
            print(f"{id}: {nome} - {descricao}")
        
        funcao_id = input("\nDigite o ID da função para esta ferramenta: ")
        
        # Validar se o ID da função existe
        cursor.execute("SELECT id FROM funcao WHERE id = ?", (funcao_id,))
        if not cursor.fetchone():
            print("ID de função inválido! Criando nova função...")
            funcao_id = adicionar_nova_funcao_durante_processo(cursor, conn)
    
    # Coletar informações da nova ferramenta
    print("\nInforme os dados da nova ferramenta:")
    nome_ferramenta = input("Nome da ferramenta: ")
    comando_sintaxe = input("Sintaxe do comando (ou deixe em branco se não aplicável): ") or None
    protocolo_padrao = input("Protocolo padrão (ou deixe em branco): ") or None
    
    print("Tipos disponíveis: CLI, GUI, API, SCRIPT, HARDWARE")
    tipo_ferramenta = input("Tipo da ferramenta: ").upper()
    while tipo_ferramenta not in ['CLI', 'GUI', 'API', 'SCRIPT', 'HARDWARE']:
        print("Tipo inválido! Escolha entre: CLI, GUI, API, SCRIPT, HARDWARE")
        tipo_ferramenta = input("Tipo da ferramenta: ").upper()
    
    contexto_uso = input("Contexto de uso/descrição: ")
    
    # Inserir a nova ferramenta
    cursor.execute(
        """INSERT INTO ferramenta 
        (funcao_id, fornecedor_id, nome, comando_sintaxe, protocolo_padrao, tipo, contexto_uso) 
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (funcao_id, fornecedor_id, nome_ferramenta, comando_sintaxe, protocolo_padrao, tipo_ferramenta, contexto_uso)
    )
    
    # Commit e fechar conexão
    conn.commit()
    conn.close()
    
    print(f"\nFerramenta '{nome_ferramenta}' adicionada com sucesso!")

def adicionar_nova_funcao_durante_processo(cursor, conn):
    """Função auxiliar para adicionar nova função durante o processo"""
    print("\n=== CRIAR NOVA FUNÇÃO ===")
    
    nome_funcao = input("Nome da nova função: ")
    descricao_funcao = input("Descrição da função: ")
    
    # Verificar se já existe
    cursor.execute("SELECT id FROM funcao WHERE nome = ?", (nome_funcao,))
    existe = cursor.fetchone()
    
    if existe:
        print(f"Função '{nome_funcao}' já existe com ID {existe[0]}")
        return existe[0]
    else:
        # Inserir a nova função (sempre associada a Redes de Computadores)
        cursor.execute(
            "INSERT INTO funcao (nome, descricao, ramo_id) VALUES (?, ?, ?)",
            (nome_funcao, descricao_funcao, 1)  # ramo_id 1 = Redes de Computadores
        )
        conn.commit()
        funcao_id = cursor.lastrowid
        print(f"Função '{nome_funcao}' criada com ID {funcao_id}")
        return funcao_id

def adicionar_nova_funcao():
    # Conectar ao banco de dados
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    print("=== ADICIONAR NOVA FUNÇÃO ===")
    
    # Coletar informações da nova função
    nome_funcao = input("Nome da nova função: ")
    descricao_funcao = input("Descrição da função: ")
    
    # Inserir a nova função (sempre associada a Redes de Computadores)
    cursor.execute(
        "INSERT INTO funcao (nome, descricao, ramo_id) VALUES (?, ?, ?)",
        (nome_funcao, descricao_funcao, 1)  # ramo_id 1 = Redes de Computadores
    )
    
    # Commit e fechar conexão
    conn.commit()
    conn.close()
    
    print(f"Função '{nome_funcao}' adicionada com sucesso!")

def listar_ferramentas():
    # Conectar ao banco de dados
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    try:
        # Buscar todas as ferramentas com informações relacionadas
        cursor.execute("""
            SELECT 
                f.nome as ferramenta, 
                fn.nome as funcao, 
                fr.nome as fornecedor,
                f.comando_sintaxe,
                f.protocolo_padrao,
                f.tipo,
                f.contexto_uso
            FROM ferramenta f
            JOIN funcao fn ON f.funcao_id = fn.id
            JOIN fornecedor fr ON f.fornecedor_id = fr.id
            ORDER BY fn.nome, f.nome
        """)
        
        ferramentas = cursor.fetchall()
        
        print("\n=== LISTA DE FERRAMENTAS ===")
        if not ferramentas:
            print("Nenhuma ferramenta encontrada no banco de dados.")
        else:
            for ferramenta in ferramentas:
                print(f"\nFerramenta: {ferramenta[0]}")
                print(f"Função: {ferramenta[1]}")
                print(f"Fornecedor: {ferramenta[2]}")
                print(f"Comando: {ferramenta[3] or 'N/A'}")
                print(f"Protocolo: {ferramenta[4] or 'N/A'}")
                print(f"Tipo: {ferramenta[5]}")
                print(f"Contexto: {ferramenta[6]}")
                print("-" * 50)
    
    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        print("O banco pode estar vazio ou com estrutura incompleta.")
    
    finally:
        conn.close()

def menu_principal():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Adicionar nova ferramenta")
        print("2. Adicionar nova função")
        print("3. Listar todas as ferramentas")
        print("4. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            adicionar_nova_ferramenta()
        elif opcao == '2':
            adicionar_nova_funcao()
        elif opcao == '3':
            listar_ferramentas()
        elif opcao == '4':
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    # Para usar o menu interativo:
    menu_principal()