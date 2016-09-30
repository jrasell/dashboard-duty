import datetime
import logging


class Core(object):
    def __init__(self, session, api_key, service_key):
        """

        :return:
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

        :param payload:
        :param endpoint:
        :return:
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

        :param service_id:
        :return:
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

        :param schedule_id:
        :return:
        """
        payload = {
            'time_zone': self.timezone,
            'schedule_ids[]': schedule_id
        }
        r = self._get_url(payload, 'oncalls')
        return r['oncalls'][0]

    def service(self):
        """

        :return:
        """
        payload = {
            'time_zone': self.timezone,
            'query': self._service_key,
            'include[]': 'escalation_policies'
        }
        r = self._get_url(payload, 'services')
        return r['services'][0]
