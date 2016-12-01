import datetime
import logging


class Core(object):
    def __init__(self, session, api_key, service_key):
        """

        :param session: The Flask requests object used to connect to PD
        :param api_key: The PD read-only, V2 API key
        :param service_key: The PD service name which is interrogated
        """

        self._api_key = api_key
        self._service_key = service_key

        self.timezone = 'UTC'
        logging.basicConfig(level=logging.INFO)

        self._s = session
        self._headers = {
            'Accept': 'application/vnd.pagerduty+json;version=2',
            'Authorization': 'Token token=' + self._api_key
        }
        self._s.headers.update(self._headers)

    def _get_url(self, payload, endpoint):
        """
        Performs a GET request to the requested PD API endpoint with the payload.
        If a 200 response is received the response data is returned.

        :param payload: The GET payload to send to the PD API
        :param endpoint: The PagerDuty endpoint, appended to api.pagerduty.com
        :return: The response data from the PD endpoint
        """
        url = 'https://api.pagerduty.com/%s' % endpoint
        try:
            r_data = self._s.get(url, params=payload)
            if r_data.status_code != 200:
                logging.error('PagerDuty API returned a status code of %s' % r_data.status_code)
            return r_data.json()
        except Exception, e:
            logging.error(e)

    def incident(self, service_id):
        """
        Details the number of currently active alerts in triggered and acknowledged state
        Also details the number of resolved alerts over the past 24hrs
        The alert summary is also included to allow for easy inspection

        :param service_id:
        :return: The number of triggered, acknowledged and resolved alerts and the summary of each
        """
        payload = {
            'statuses[]': ['triggered', 'acknowledged', 'resolved'],
            'service_ids[]': service_id,
            'time_zone': self.timezone,
            'since': datetime.date.today() - datetime.timedelta(days=1),
            'limit': 100
        }
        r = self._get_url(payload, 'incidents')['incidents']

        triggered = [i['summary'] for i in r if i['status'] == 'triggered']
        acknowledged = [i['summary'] for i in r if i['status'] == 'acknowledged']
        resolved = [i['summary'] for i in r if i['status'] == 'resolved']

        out = dict()
        out['triggered'] = {'count': len(triggered), 'details': triggered}
        out['acknowledged'] = {'count': len(acknowledged), 'details': acknowledged}
        out['resolved'] = {'count': len(resolved), 'details': resolved}
        return out

    def oncall(self, schedule_id):
        """
        Takes the escalation target ID of a service and calls the PD API.
        This discovers information regarding the 1st line responder.

        :param schedule_id: The escalation_policy target of the PD service
        :return: The details of the current oncall member
        """
        payload = {
            'time_zone': self.timezone,
            'schedule_ids[]': schedule_id
        }
        r = self._get_url(payload, 'oncalls')
        return r['oncalls'][0]

    def service(self):
        """
        Takes the PD service name and calls the PD API for details of the service in question


        :return: The PD service details aligned to the PD service name
        """
        payload = {
            'time_zone': self.timezone,
            'query': self._service_key,
            'include[]': 'escalation_policies'
        }
        r = self._get_url(payload, 'services')
        return r['services'][0]
