from jsonrpc import ServiceProxy
MAIN_ACCOUNT = 'main'
rpc = ServiceProxy('http://un:pw@127.0.0.1:8332')

def create_account(username):
    """
    Creates a new account for the given username, returns the new address.
    """
    
    if rpc.listaccounts().get('username'):
        return False
    
    return rpc.getnewaddress(username)


def get_address(username):
    return rpc.getaccountaddress(username)

def get_balance(username):
    return rpc.getbalance(username)

def credit(amount, address):
    return rpc.move(MAIN_ACCOUNT, address, amount)

def debit(amount, address):
    return rpc.move(address, MAIN_ACCOUNT, amount)

    