import requests
import json
import warnings
from requests.auth import HTTPBasicAuth
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def get_data_rabbitmq():
    host = sys.argv[1]
    vhost = sys.argv[2]
    queue = sys.argv[3]
    status = 0
    request = requests.get(f'http://{host}:15672/api/queues/{vhost}/{queue}', auth=HTTPBasicAuth(sys.argv[4], sys.argv[5]), verify=False)
    result = json.loads(request.text)
    if int(result['messages']) > 1000 or int(result['messages_ready']) > 1000 or int(result['messages_unacknowledged']) > 1000: 
        print(f"RABBITMQ_OVERVIEW CRIT - messages({result['messages']}) messages_ready ({result['messages_ready']}) messages_unacknowledged ({result['messages_unacknowledged']}) consumers ({result['consumers']}) | messages={result['messages']} messages_ready={result['messages_ready']} messages_unacknowledged={result['messages_unacknowledged']} consumers={result['consumers']}")
        sys.exit(2)
    elif int(result['messages']) > 700 or int(result['messages']) > 700 or int(result['messages']) > 700:
        print(f"RABBITMQ_OVERVIEW WARN - messages({result['messages']}) messages_ready ({result['messages_ready']}) messages_unacknowledged ({result['messages_unacknowledged']}) consumers ({result['consumers']}) | messages={result['messages']} messages_ready={result['messages_ready']} messages_unacknowledged={result['messages_unacknowledged']} consumers={result['consumers']}")
        sys.exit(1)
    else:
        print(f"RABBITMQ_OVERVIEW OK - messages({result['messages']}) messages_ready ({result['messages_ready']}) messages_unacknowledged ({result['messages_unacknowledged']}) consumers ({result['consumers']}) | messages={result['messages']} messages_ready={result['messages_ready']} messages_unacknowledged={result['messages_unacknowledged']} consumers={result['consumers']}")
        sys.exit(0)
    
if __name__ == '__main__':
    warnings.filterwarnings("ignore", category=InsecureRequestWarning)
    get_data_rabbitmq()
    