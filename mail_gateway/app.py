from flask import Flask
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime, timezone
import smtplib

from config import smtp_server, smtp_port, from_email
from config import debug, log

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='SMTP API Gateway',
          description='A simple API gateway to send email messages over SMTP service in Gmail',)

ns = api.namespace('mail', description='mail operations')

message = api.model('Message', {
    'id': fields.Integer(readonly=True, description='Message unique identifier'),
    'to': fields.String(required=True, description='Recipient email address'),
    'subject': fields.String(required=True, description='Email subject'),
    'body': fields.String(required=False, description='Email body (optional)'),
    'timestamp': fields.DateTime(readonly=True)
})


class MessageDAO(object):
    def __init__(self):
        self.counter = 1
        self.messages = []

    def get(self, id):
        for message in self.messages:
            if message['id'] == id:
                return message
        api.abort(404, f'Message with id: {id} does not exist')

    def create(self, data):
        message = data
        message['id'] = self.counter = self.counter + 1
        message['timestamp'] = datetime.isoformat(datetime.now(tz=timezone.utc))
        self.messages.append(message)
        return message


DAO = MessageDAO()


@ns.route('/')
class Mail(Resource):
    @ns.doc('list_messages')
    def get(self):
        """List all messages sent"""
        return DAO.messages

    @ns.doc('send_message')
    @ns.expect(message)
    def post(self):
        """Send new SMTP message"""
        data = api.payload
        message = f'Subject: {data["subject"]}\n\n{data["body"]}'
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.sendmail(from_email, data['to'], message)
        except Exception as e:
            log.error(f'mail send failed with error: {e}')
            api.abort(500, f'mail send failed with error: {e}')
        finally:
            server.quit()

        DAO.create(data)
        return {'status': 'ok'}


if __name__ == '__main__':
    app.run(debug=debug, host='0.0.0.0')
