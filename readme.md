# Simple utility to add label to jira tickets 

## Run python directly
1) install python 3.9
2) install dependencies: `pip3 install -r requirements.txt`
3) Run `python3 add_jira_label_cmd_adapter.py -jql "some jql query" -l "test_label" -u "user" -p "password" -url "https://jira-api.example.com"`
Note: please update parameters values in the command above!

## Run from docker
1) Install docker
2) Build image: `docker build -t add-jira-label .`
3) Run: `docker run --rm add-jira-label python add_jira_label_cmd_adapter.py -jql "some jql query" -l "test_label" -u "user" -p "password" -url "https://jira-api.example.com"`
