FROM python:3.9.7-alpine3.14

ADD add_jira_label.py /jira/
ADD add_jira_label_cmd_adapter.py /jira/
ADD requirements.txt /jira/
WORKDIR /jira
RUN pip install -r requirements.txt
