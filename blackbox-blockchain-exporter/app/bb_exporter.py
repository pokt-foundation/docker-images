import json
import time
import logging
from flask import Flask, request, abort
from prometheus_client import Gauge, Counter, generate_latest, CollectorRegistry
import requests
# from datetime import timezone
# from web3 import Web3
# from web3.middleware import geth_poa_middleware
# import asyncio
# from terra_sdk.client.lcd import LCDClient
# import iso8601

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

#Timeout     (Connect, Read)
REQ_TIMEOUT = (5,15)
#Requests data
ETH_syncing   = '{"jsonrpc":"2.0","method":"eth_syncing","params":[],"id":1}'
ETH_getBlockByNumber = '{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["latest",false],"id":1}'
NET_peerCount = '{"jsonrpc":"2.0","method":"net_peerCount","params":[],"id":1}'
NET_version   = '{"jsonrpc":"2.0","method":"net_version","params":[],"id":67}'
####################
app = Flask(__name__)

reg = CollectorRegistry()
lastBlockNumber     = Gauge('last_block_number', "Number of the node's latest block", [], registry=reg)
lastBlockAge        = Gauge('last_block_age', "How many seconds old is the node's latest block", [], registry=reg)
lastBlockDuration   = Gauge('last_block_duration_ns', 'How many nanoseconds took to get the block', [], registry=reg)
nodeSyncing         = Gauge('node_syncing', "Is the node syncing", [], registry=reg)
nodeSyncingDuration = Gauge('node_syncing_duration_ns', 'How many nanoseconds took to get syncing status', [], registry=reg)
nodePeers           = Gauge('node_peers', "How many connected peers the node has", [], registry=reg)
nodePeersDuration   = Gauge('node_peers_duration_ns', 'How many nanoseconds took to get the number of connceeted peers', [], registry=reg)
nodeNetVersion          = Gauge('node_net_version', "ChainID returned by the node", [], registry=reg)
nodeNetVersionDuration  = Gauge('node_net_version_duration_ns', 'How many nanoseconds took to get the chainid', [], registry=reg)
probeSuccess       = Gauge('probe_success', 'Displays whether or not the probe was a success', [], registry=reg)

def rpcRequest(target: str, data: str):
    try:
        resp = requests.post(f"{target}",
                                json=json.loads(data),
                                timeout=REQ_TIMEOUT)

        if resp.status_code == 200 :
            return resp.json()

        raise Exception(f"Reply status_code: {resp.status_code} != 200")
    except Exception as e:
        logging.warning(f"Failed to request: {e}")

@app.route('/probe')
def get_metrics():
    try:
        target  = request.args.get('target')
        chainid = request.args.get('chainid')

        if chainid in ["0021", "0022", "0050", "0051"]:

            t0 = time.perf_counter_ns()
            block = rpcRequest(target, ETH_getBlockByNumber)["result"]
            lastBlockDuration.set(time.perf_counter_ns() - t0)
            # print(block)
            lastBlockAge.set(int(time.time()) - int(block["timestamp"], base=16))

            lastBlockNumber.set(int(block["number"], base=16))

            t0 = time.perf_counter_ns()
            syncing = rpcRequest(target, ETH_syncing)["result"]
            # print(syncing)
            nodeSyncing = 0 if syncing == False else 1
            nodeSyncingDuration.set(time.perf_counter_ns() - t0)

            t0 = time.perf_counter_ns()
            peers = rpcRequest(target, NET_peerCount)["result"]
            # print(peers)
            nodePeers.set(int(peers, base=16))
            nodePeersDuration.set(time.perf_counter_ns() - t0)

            t0 = time.perf_counter_ns()
            netversion = rpcRequest(target, NET_version)["result"]
            # print(netversion)
            nodeNetVersion.set(int(netversion, base=16))
            nodeNetVersionDuration.set(time.perf_counter_ns() - t0)

        else:
            raise Exception(f"Given chainid {chainid} is not supported")

        probeSuccess.set(1)

    except Exception as e:
        probeSuccess.set(0)
        logging.error(f"Caught exception: {e}")

    return generate_latest(registry=reg)

@app.route('/health')
def health():
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=9000, debug=True)
    app.run()
