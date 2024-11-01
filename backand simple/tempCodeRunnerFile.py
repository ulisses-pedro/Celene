import secrets
from datetime import datetime, timedelta
import hashlib
import hmac
import base64
import flask
from flask_cors import CORS
from email_sender import send_email

app = flask.Flask(__name__)
CORS(app)

# Gerando uma chave secreta para assinar URLs
SECRET_KEY = secrets.token_bytes(32)
EXPIRATION_TIME_MINUTES = 10

def generate_signed_url(path):
    expiration = datetime.utcnow() + timedelta(minutes=EXPIRATION_TIME_MINUTES)
    expiration_timestamp = int(expiration.timestamp())
    signature = hmac.new(
        SECRET_KEY,
        f"{path}{expiration_timestamp}".encode('utf-8'),
        hashlib.sha256
    ).digest()
    signature_base64 = base64.urlsafe_b64encode(signature).decode('utf-8')
    return f"{path}?expires={expiration_timestamp}&signature={signature_base64}"

def validate_signed_url(path, expires, signature):
    try:
        expiration_timestamp = int(expires)
        if datetime.utcnow().timestamp() > expiration_timestamp:
            return False
        expected_signature = hmac.new(
            SECRET_KEY,
            f"{path}{expiration_timestamp}".encode('utf-8'),
            hashlib.sha256
        ).digest()
        expected_signature_base64 = base64.urlsafe_b64encode(expected_signature).decode('utf-8')
        return hmac.compare_digest(expected_signature_base64, signature)
    except Exception as e:
        print("Erro ao validar URL assinada:", e)
        return False

@app.route('/generate-url')
def generate_url():
    path = flask.request.args.get('path', '/secure-content')
    signed_url = generate_signed_url(path)
    return {"signed_url": signed_url}

@app.route('/secure-content')
def secure_content():
    expires = flask.request.args.get('expires')
    signature = flask.request.args.get('signature')
    if not validate_signed_url('/secure-content', expires, signature):
        flask.abort(403)
    return {"message": "Acesso autorizado ao conteúdo seguro!"}

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    
    
    