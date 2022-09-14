KEY="xxx"
CHAINID="evmos_9001-2"
MONIKER="pokt-1"
KEYRING="test"
KEYALGO="eth_secp256k1"
LOGLEVEL="info"
# to trace evm
#TRACE="--trace"
TRACE=""

evmosd config keyring-backend $KEYRING
evmosd config chain-id $CHAINID

# Start the node (remove the --pruning=nothing flag if historical queries are not needed)
evmosd start --pruning=nothing $TRACE --log_level $LOGLEVEL --minimum-gas-prices=0.0001aphoton --json-rpc.api eth,txpool,personal,net,debug,web3
