from backend.jsonrpc import ServiceProxy

MAIN_ACCOUNT = 'main'
rpc = ServiceProxy('http://un:pw@127.0.0.1:8332')

def create_account(username):
    """
    Creates a new account for the given username, returns the new address.
    """
    
    if rpc.listaccounts().get('username'):
        return False
    
    return rpc.getnewaddress(username)


def get_address(account_name):
    return rpc.getaccountaddress(account_name)

def get_balance(account_name):
    return rpc.getbalance(account_name)

def credit(amount, account_name):
    return rpc.move(MAIN_ACCOUNT, account_name, amount)

def debit(amount, account_name):
    return rpc.move(account_name, MAIN_ACCOUNT, amount)

def send(account_name, to_address, amount):
    return rpc.sendfrom(account_name, to_address, amount)
