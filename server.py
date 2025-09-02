from flask import Flask, render_template
from routes import blueprint
from models import init_app
import os
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'sua_chave_secreta_aqui_altere_em_producao'
    app.config['DATABASE'] = os.environ.get('DATABASE') or 'database.db'
    
    # Configurações para GitHub e produção
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Desativa cache para desenvolvimento
    
    # Inicializar a aplicação com o banco de dados
    init_app(app)
    
    # Registrar blueprint principal
    app.register_blueprint(blueprint)
    
    # Error handlers para melhor experiência do usuário
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html', now=datetime.now()), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html', now=datetime.now()), 500
    
    # Rota de saúde para monitoramento (útil para GitHub e produção)
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'IT Essentials API is running'}
    
    return app

def configure_app_for_production(app):
    """Configurações específicas para ambiente de produção"""
    # Desativa debug mode em produção
    app.debug = False
    
    # Configurações de segurança
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['REMEMBER_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['REMEMBER_COOKIE_HTTPONLY'] = True
    
    # Configurações de performance
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = False

if __name__ == '__main__':
    app = create_app()
    
    # Verifica se está em ambiente de produção
    is_production = os.environ.get('FLASK_ENV') == 'production'
    
    if is_production:
        configure_app_for_production(app)
        print("🚀 Servidor iniciado em modo produção")
        print("📊 Acesse: http://localhost:5000")
        print("❤️  Health check: http://localhost:5000/health")
    else:
        print("🔧 Servidor iniciado em modo desenvolvimento")
        print("🌐 Acesse: http://localhost:5000")
        print("🔍 Health check: http://localhost:5000/health")
        print("⚡ Debug mode: ON")
    
    # Inicia o servidor
    app.run(
        debug=not is_production,
        host='0.0.0.0', 
        port=int(os.environ.get('PORT', 5000))
    )