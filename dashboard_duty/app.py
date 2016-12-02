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

    if service['escalation_policy']['escalation_rules'][0]['targets'][0]['type'] == 'schedule_reference':
        service_id = service['escalation_policy']['escalation_rules'][0]['targets'][0]['id']
        oncall = d_session.oncall_schedule_policy(service_id)

    elif service['escalation_policy']['escalation_rules'][0]['targets'][0]['type'] == 'user_reference':
        username = service['escalation_policy']['escalation_rules'][0]['targets'][0]['summary']
        oncall = d_session.oncall_user_policy(username)
    else:
        logging.error('Unable to handle oncall policy for %s' % service_key)
        exit(1)

    return render_template('index.html', service=service, incidents=incidents, oncall=oncall)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
