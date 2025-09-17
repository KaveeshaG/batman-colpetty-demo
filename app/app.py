from flask import Flask, jsonify, render_template_string
import os
import socket
import datetime

app = Flask(__name__)

CITY_NAME = os.getenv('CITY_NAME', 'Unknown City')
HERO_NAME = os.getenv('HERO_NAME', 'Unknown Hero')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'unknown')
VERSION = os.getenv('VERSION', '1.0.0')

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>{{hero}} Protects {{city}}</title>
    <style>
        body { 
            font-family: 'Courier New', monospace; 
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d30 100%);
            color: #f0f0f0;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            text-align: center;
            padding: 40px 20px;
        }
        .hero-badge {
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            color: #1a1a1a;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
        }
        .city-name {
            font-size: 2.5em;
            color: #00bcd4;
            text-shadow: 0 0 10px #00bcd4;
            margin: 20px 0;
        }
        .status {
            background: #2e7d32;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 5px solid #4caf50;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .info-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .bat-symbol {
            font-size: 4em;
            color: #ffd700;
            text-shadow: 0 0 20px #ffd700;
            margin: 20px 0;
        }
        .version-badge {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #673ab7;
            color: white;
            padding: 8px 12px;
            border-radius: 15px;
            font-size: 0.8em;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        .pulse { animation: pulse 2s infinite; }
    </style>
</head>
<body>
    <div class="version-badge">v{{version}} | {{environment}}</div>
    <div class="container">
        <div class="bat-symbol pulse">🦇</div>
        <div class="hero-badge">{{hero}} IS ON DUTY</div>
        <div class="city-name">{{city}}</div>
        <div class="status">
            <h2>🛡️ CITY STATUS: PROTECTED</h2>
            <p>The Dark Knight's GitOps deployment is active and monitoring all threats.</p>
        </div>
        
        <div class="info-grid">
            <div class="info-card">
                <h3>🏢 Location</h3>
                <p><strong>{{city}}</strong></p>
                <p>Pod: {{hostname}}</p>
            </div>
            <div class="info-card">
                <h3>⚙️ Environment</h3>
                <p><strong>{{environment|upper}}</strong></p>
                <p>Deployed via ArgoCD</p>
            </div>
            <div class="info-card">
                <h3>🚀 Version</h3>
                <p><strong>{{version}}</strong></p>
                <p>GitOps Powered</p>
            </div>
            <div class="info-card">
                <h3>⏰ Last Check</h3>
                <p><strong>{{timestamp}}</strong></p>
                <p>All systems operational</p>
            </div>
        </div>
        
        <div style="margin-top: 40px; padding: 20px; background: rgba(255, 193, 7, 0.1); border-radius: 10px;">
            <h3>🦇 GitOps Status</h3>
            <p>✅ Deployment automated via ArgoCD</p>
            <p>✅ Configuration managed by Kustomize</p>
            <p>✅ CI/CD powered by GitHub Actions</p>
            <p>✅ Running on Kubernetes (K3s)</p>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE,
                                hero=HERO_NAME,
                                city=CITY_NAME,
                                environment=ENVIRONMENT,
                                version=VERSION,
                                hostname=socket.gethostname(),
                                timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"))

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'hero': HERO_NAME,
        'city': CITY_NAME,
        'environment': ENVIRONMENT,
        'version': VERSION,
        'hostname': socket.gethostname(),
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/api/status')
def api_status():
    return jsonify({
        'hero': HERO_NAME,
        'city': CITY_NAME,
        'status': 'PROTECTED',
        'environment': ENVIRONMENT,
        'version': VERSION,
        'deployment': 'argocd-gitops',
        'container_orchestration': 'kubernetes',
        'configuration_management': 'kustomize',
        'ci_cd': 'github-actions'
    })

@app.route('/villain/<villain_name>')
def villain_alert(villain_name):
    villains = {
        'joker': {'threat': 'HIGH', 'message': 'Chaos detected! Auto-scaling activated.'},
        'penguin': {'threat': 'MEDIUM', 'message': 'Traffic spike detected! Load balancing engaged.'},
        'riddler': {'threat': 'LOW', 'message': 'Configuration puzzle solved by Kustomize!'},
        'twoface': {'threat': 'MEDIUM', 'message': 'A/B deployment ready for canary release.'}
    }
    
    villain_info = villains.get(villain_name.lower(), {
        'threat': 'UNKNOWN', 
        'message': 'New villain detected! Batman is investigating.'
    })
    
    return jsonify({
        'villain': villain_name.upper(),
        'threat_level': villain_info['threat'],
        'batman_response': villain_info['message'],
        'city': CITY_NAME,
        'auto_response': 'ArgoCD monitoring and ready to rollback if needed',
        'status': 'UNDER_PROTECTION'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
