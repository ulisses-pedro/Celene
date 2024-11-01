import flask
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)

SENDGRID_API_KEY = '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'

@app.route('/send-email', methods=['POST'])
def send_email():
    data = flask.request.get_json()
    email = data.get('email')
    
    if not email:
        return flask.jsonify({"error": "E-mail não fornecido"}), 400

    message = Mail(
        from_email='nufileboxreverse@gmail.com',
        to_emails=email,
        subject='Novo curso',
        plain_text_content='Olá, você agora terá acesso à plataforma NufileBox Reverse durante xx:xx tempo',
        html_content='<strong>Olá, você agora terá acesso à plataforma NufileBox Reverse</strong> durante <b>xx:xx</b> tempo'
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return flask.jsonify({"message": "Email enviado com sucesso!"}), 200
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
