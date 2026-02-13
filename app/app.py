from flask import Flask
import logging
import os
from routes import main_bp

def create_app():
    app = Flask(__name__)
    
    # 設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'shrimp-secret')
    
    # 註冊路由
    app.register_blueprint(main_bp)
    
    # 設定日誌
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler("logs/app.log"),
            logging.StreamHandler()
        ]
    )
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("公司蝦服務啟動在 http://localhost:18080")
    app.run(host='0.0.0.0', port=18080, debug=True)
