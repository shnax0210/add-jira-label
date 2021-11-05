import argparse

from add_jira_label import JiraLabelAdder

ap = argparse.ArgumentParser()

ap.add_argument("-u", "--user", required=True, help="jira user login")
ap.add_argument("-p", "--password", required=True, help="jira user password")
ap.add_argument("-url", "--url", required=True, help="jira base url")
ap.add_argument("-jql", "--jql", required=True, help="jql query to get tickets for label adding")
ap.add_argument("-l", "--label", required=True, help="label to add")
args = vars(ap.parse_args())

jira_label_adder = JiraLabelAdder(args['user'], args['password'], args['url'])

print('----------Start----------')
print(jira_label_adder.add_label(args['jql'], args['label']))
print('----------Finish----------')
