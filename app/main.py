from fastapi import FastAPI,Response,Request
from reefinterface import Keypair, ReefInterface
from reefinterface.base import *

mnemonics = []

def generate_account():
    try:
        network = "testnet"
        substrate = ReefInterface(url=network)
        reef = substrate
        mnemonic = Keypair.generate_mnemonic()
        keypair = Keypair.create_from_uri(mnemonic + '//hard/soft')
        account_info = reef.query(
        module='System',
        storage_function='Account',
        params=[keypair.ss58_address])

        return {'address':keypair.ss58_address,'balance':account_info.value['data']['free'],'mnemonic':mnemonic}
    except ConnectionRefusedError:
        print("Reef node could not be reached.")
        exit()

def get_account_address(mnemonic):
    network = "testnet"
    substrate = ReefInterface(url=network)
    reef = substrate
    keypair = Keypair.create_from_uri(mnemonic + '//hard/soft')
    return keypair.ss58_address

def fetch_balance(mnemonic):
    network = "testnet"
    substrate = ReefInterface(url=network)
    reef = substrate
    keypair = Keypair.create_from_uri(mnemonic + '//hard/soft')
    account_info = reef.query(
        module='System',
        storage_function='Account',
        params=[keypair.ss58_address])

    return {'address':keypair.ss58_address,'balance':account_info.value['data']['free']/1e18}


def transfer(dest,mnemonic):
    keypair = Keypair.create_from_mnemonic(mnemonic)
    substrate = ReefInterface(url="testnet")
    reef = substrate
    call = reef.compose_call(
        call_module='Balances',
        call_function='transfer',
        call_params={
            'dest': dest,
            'value': 10 * 10**18
        }
    )

    extrinsic = reef.create_signed_extrinsic(call=call, keypair=keypair)

    try:
        receipt = reef.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        print("Extrinsic '{}' sent and included in block '{}'".format(receipt.extrinsic_hash, receipt.block_hash))
    except Exception as e:
        print(e)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Message": "Claim free REEF account from /claim"}


@app.get("/claim")
def claim_root(response: Response):
    temp = generate_account()
    response.set_cookie(key="mnemonic", value=temp["mnemonic"])
    return {"Account Address": temp["address"],"Balance":temp["balance"],"Mnemonic":temp["mnemonic"]}

@app.get("/send/{addr}")
def read_item(addr: str,request: Request):
    transfer(addr,request.cookies.get("mnemonic"))
    return {
        "receiver": addr,
        "sender": get_account_address(request.cookies.get("mnemonic")),
        "operation":"Sending 10 tokens",
        "response":200,
        "status":"success"

    }


@app.get("/fetch")
def read_item(request: Request):
    return fetch_balance(request.cookies.get("mnemonic"))