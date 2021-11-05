import requests


class JiraLabelAdder:
    def __init__(self, login, password, jira_base_url, batch_size=50):
        self.login = login
        self.password = password
        self.jira_base_url = jira_base_url
        self.batch_size = batch_size

    def add_label(self, jql, label):
        with requests.Session() as session:
            session.auth = (self.login, self.password)
            return [self.__add_label(session, ticket, label) for ticket in self.__read_tickets(session, jql)]

    def __add_url_prefix(self, relative_path):
        return self.jira_base_url + relative_path

    @staticmethod
    def __check_if_there_are_more_tickets_for_updates(search_result):
        next_start_at = search_result['startAt'] + search_result['maxResults']
        return next_start_at < search_result['total'], next_start_at

    def __read_tickets(self, session, query):
        are_there_more_tickets_for_updates = True
        start_at = 0

        while are_there_more_tickets_for_updates:
            search_result = session.get(self.__add_url_prefix('/rest/api/latest/search'),
                                        params={'jql': query, "startAt": start_at, "maxResults": self.batch_size}).json()

            for ticket in search_result['issues']:
                yield ticket

            are_there_more_tickets_for_updates, start_at = self.__check_if_there_are_more_tickets_for_updates(search_result)

    @staticmethod
    def __create_add_label_result(ticket, label, is_success, message):
        return {
            'ticket': ticket['key'],
            'label': label,
            'success': is_success,
            'message': message
        }

    @staticmethod
    def __is_label_present(ticket, label):
        ticket_fields = ticket['fields']
        return 'labels' in ticket_fields and ticket_fields['labels'] is not None and label in ticket_fields['labels']

    def __add_label(self, session, ticket, label):
        if self.__is_label_present(ticket, label):
            return self.__create_add_label_result(ticket, label, False, "The label is already present")

        response = session.put(self.__add_url_prefix('/rest/api/latest/issue/' + ticket['key']),
                               json={"update": {"labels": [{"add": label}]}})

        if response.ok:
            return self.__create_add_label_result(ticket, label, True, "The label added successfully")
        else:
            return self.__create_add_label_result(ticket, label, False,
                                                  "Request to add the label failed with status" + str(response.status_code))
