from flask import Blueprint, render_template, request, jsonify
from models import get_ferramentas, get_funcoes, get_fornecedores, get_ferramentas_por_funcao, get_ferramentas_por_fornecedor, buscar_ferramentas, get_ferramenta_por_id, get_todas_ferramentas_ids

# Cria o Blueprint
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Página principal com todas as ferramentas"""
    ferramentas = get_ferramentas()
    funcoes = get_funcoes()
    fornecedores = get_fornecedores()
    
    return render_template('index.html', 
                         ferramentas=ferramentas,
                         funcoes=funcoes,
                         fornecedores=fornecedores,
                         pagina='inicio')

@main.route('/funcao/<int:funcao_id>')
def ferramentas_por_funcao(funcao_id):
    """Ferramentas filtradas por função"""
    ferramentas = get_ferramentas_por_funcao(funcao_id)
    funcoes = get_funcoes()
    fornecedores = get_fornecedores()
    
    # Obter nome da função atual
    funcao_atual = next((f for f in funcoes if f['id'] == funcao_id), None)
    
    return render_template('index.html', 
                         ferramentas=ferramentas,
                         funcoes=funcoes,
                         fornecedores=fornecedores,
                         funcao_atual=funcao_atual,
                         pagina='funcao')

@main.route('/fornecedor/<int:fornecedor_id>')
def ferramentas_por_fornecedor(fornecedor_id):
    """Ferramentas filtradas por fornecedor"""
    ferramentas = get_ferramentas_por_fornecedor(fornecedor_id)
    funcoes = get_funcoes()
    fornecedores = get_fornecedores()
    
    # Obter nome do fornecedor atual
    fornecedor_atual = next((f for f in fornecedores if f['id'] == fornecedor_id), None)
    
    return render_template('index.html', 
                         ferramentas=ferramentas,
                         funcoes=funcoes,
                         fornecedores=fornecedores,
                         fornecedor_atual=fornecedor_atual,
                         pagina='fornecedor')

@main.route('/buscar')
def buscar():
    """Busca de ferramentas com busca avançada incluindo comando_sintaxe"""
    termo = request.args.get('q', '').strip()
    funcoes = get_funcoes()
    fornecedores = get_fornecedores()
    
    if termo:
        # Busca avançada que inclui comando_sintaxe e outros campos
        ferramentas = buscar_ferramentas(termo)
    else:
        # Se não há termo de busca, mostra todas as ferramentas
        ferramentas = get_ferramentas()
    
    return render_template('index.html', 
                         ferramentas=ferramentas,
                         funcoes=funcoes,
                         fornecedores=fornecedores,
                         termo_busca=termo,
                         pagina='busca')

@main.route('/ferramenta/<int:ferramenta_id>')
def detalhes_ferramenta(ferramenta_id):
    """Página de detalhes de uma ferramenta específica - ideal para SEO"""
    ferramenta = get_ferramenta_por_id(ferramenta_id)
    if not ferramenta:
        return render_template('404.html'), 404
    
    funcoes = get_funcoes()
    fornecedores = get_fornecedores()
    
    return render_template('detalhes_ferramenta.html', 
                         ferramenta=ferramenta,
                         funcoes=funcoes,
                         fornecedores=fornecedores)

@main.route('/api/ferramentas')
def api_ferramentas():
    """API endpoint para ferramentas - útil para projetos no GitHub"""
    ferramentas = get_ferramentas()
    
    # Converter para formato JSON amigável
    ferramentas_json = []
    for f in ferramentas:
        ferramentas_json.append({
            'id': f['id'],
            'nome': f['ferramenta_nome'],
            'funcao': f['funcao_nome'],
            'fornecedor': f['fornecedor_nome'],
            'comando': f['comando_sintaxe'],
            'protocolo': f['protocolo_padrao'],
            'tipo': f['tipo'],
            'contexto': f['contexto_uso']
        })
    
    return jsonify(ferramentas_json)

@main.route('/sitemap.xml')
def sitemap():
    """Sitemap para melhor indexação por motores de busca"""
    from flask import make_response
    
    ferramentas_ids = get_todas_ferramentas_ids()
    sitemap_xml = render_template('sitemap.xml', ferramentas_ids=ferramentas_ids)
    response = make_response(sitemap_xml)
    response.headers['Content-Type'] = 'application/xml'
    return response

@main.route('/teste-erro-500')
def teste_erro_500():
    """Rota de teste para gerar erro 500 - REMOVER EM PRODUÇÃO"""
    # Isso causará um erro 500 proposital
    raise Exception("🚨 Este é um erro de teste para a página 500. "
                   "Isso é esperado e serve para testar a página de erro interno.")

# Exporta o blueprint para ser importado em server.py
blueprint = main