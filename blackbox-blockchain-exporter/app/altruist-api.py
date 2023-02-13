import json
import time
import logging
import os
from flask import Flask, request, abort
import requests
from http import HTTPStatus
import base64

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

#Timeout     (Connect, Read)
REQ_TIMEOUT = (5,15)

# ####################
app = Flask(__name__)

VM_ADDRESS = os.environ.get('VM_ADDRESS')
VM_QUERY   = os.environ.get('VM_QUERY', '/api/v1/query?query=')

altruists = []

@app.route('/fastest')
def get_fastest():

    chainid = request.args.get('chainid', type = str)
    if chainid == None:
        return json.dumps({
                'success': False,
                'error': f"chainid argument not given"
                }), HTTPStatus.SERVICE_UNAVAILABLE, {'ContentType':'application/json'}

    interval = request.args.get('interval', default = '30m', type = str)

    query = ('sort('
        f'sum_over_time(last_block_duration_ns{{job="{chainid}"}}[{interval}])'
        f'+sum_over_time(node_syncing_duration_ns{{job="{chainid}"}}[{interval}])'
        f'+sum_over_time(node_peers_duration_ns{{job="{chainid}"}}[{interval}])'
        f'+sum_over_time(node_net_version_duration_ns{{job="{chainid}"}}[{interval}])'
        f' and node_syncing{{job="{chainid}"}}==0' # Node is synced
        f' and node_peers{{job="{chainid}"}}>10'   # Node is connected to >10 peers
        ')')

        # f' and node_net_version{{job="{chainid}"}}==1'
    global altruists
    if len(altruists) == 0 :

        query_url = VM_ADDRESS + VM_QUERY + requests.utils.quote(query)
        try:
            resp = requests.get(query_url, timeout=REQ_TIMEOUT)

            if resp.status_code == HTTPStatus.OK :
                altruists = resp.json()["data"]["result"][:5]
            else:
                raise Exception(f"Reply status_code: {resp.status_code} != 200")
        except Exception as e:
            logging.warning(f"Failed to request: {e}")
            return json.dumps({
                'success': False,
                'error': f"Couldn't get response from {query_url} response code: {resp.status_code}"
                }), HTTPStatus.SERVICE_UNAVAILABLE, {'ContentType':'application/json'}

    current_alt = altruists.pop()
    return json.dumps({
                       'success': True,
                       'instance': current_alt["metric"]["instance"],
                       'job': current_alt["metric"]["job"]
                       }), 200, {'ContentType':'application/json'}

@app.route('/node_metric')
def node_metric():

    instance = request.args.get('instance', type = str)
    if instance == None:
        return json.dumps({
                'success': False,
                'error': f"instance argument not given"
                }), HTTPStatus.SERVICE_UNAVAILABLE, {'ContentType':'application/json'}
    instance = str(base64.b64decode(instance))

    query = f'probe_success{{instance="{instance}"}}[5m]'
    print(query)
    query_url = VM_ADDRESS + VM_QUERY + requests.utils.quote(query)
    try:
        resp = requests.get(query_url, timeout=REQ_TIMEOUT)
        print(resp.json())
        if resp.status_code == HTTPStatus.OK :
            return json.dumps({
                            'success': True,
                            'data': resp.json()
                            }), 200, {'ContentType':'application/json'}

        raise Exception(f"Reply status_code: {resp.status_code} != 200")
    except Exception as e:
        logging.warning(f"Failed to request: {e}")
        return json.dumps({
            'success': False,
            'error': f"Couldn't get response from {query_url} response code: {resp.status_code}"
            }), HTTPStatus.SERVICE_UNAVAILABLE, {'ContentType':'application/json'}

@app.route('/health')
def health():
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000, debug=True)
    # app.run()
