from web3 import Web3

def get_transactions_from_alchemy(number_of_blocks):

    alchemy_api_key = "6KLe5prh13byVO2IOuppruX8k7jDdZPZ"
    alchemy_url = f'https://eth-mainnet.g.alchemy.com/v2/{alchemy_api_key}'
    w3 = Web3(Web3.HTTPProvider(alchemy_url))

    block_number = 16171541
    for i in range(number_of_blocks):
        block_number = block_number - i
        block = w3.eth.get_block(block_number)
        for transac in block.transactions:
            transac_details = w3.eth.get_transaction(transac)
            #print(Web3.toJSON(transac_details))
            print('from : ')
            w3.eth.get_code(transac_details["to"])
            #print(f'to : {w3.eth.get_code(transac_details["to"])}')
            print()

