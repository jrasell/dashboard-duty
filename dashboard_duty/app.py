import os
import logging
import requests
import dashboard_duty
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():

    try:
        api_key = os.environ['DASHBOARD_DUTY_KEY']
        service_key = os.environ['DASHBOARD_DUTY_SERVICE']
    except KeyError:
        logging.error('Missing Environment Variable(s)')
        exit(1)

    session = requests.Session()
    d_session = dashboard_duty.Core(session, api_key, service_key)

    service = d_session.service()
    incidents = d_session.incident(service['id'])
    oncall = d_session.oncall(service['escalation_policy']['escalation_rules'][0]['targets'][0]['id'])
    return render_template('index.html', service=service, incidents=incidents, oncall=oncall)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
