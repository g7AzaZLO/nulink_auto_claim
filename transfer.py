from web3 import Web3
from eth_account import Account
from config import bsc_testnet_url, chain_id, contract_address, token_address
from account_generation import del0x


def send_bnb(private_key: str, to_address: str, amount_bnb=0.01) -> None:
    # Настройка подключения к сети BSC
    web3 = Web3(Web3.HTTPProvider(bsc_testnet_url))
    # Получение аккаунта отправителя из приватного ключа
    from_account = Account.from_key(private_key)
    # Настройка транзакции
    nonce = web3.eth.get_transaction_count(from_account.address)
    value = web3.to_wei(amount_bnb, 'ether')  # Конвертация суммы в wei
    gasPrice = web3.eth.gas_price
    gasLimit = 21000  # Стандартный лимит газа для транзакции перевода
    # Подготовка транзакции
    tx = {
        'nonce': nonce,
        'to': to_address,
        'value': value,
        'gas': gasLimit,
        'gasPrice': gasPrice,
        'chainId': chain_id
    }
    # Подписание транзакции
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    # Отправка транзакции
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"BNB sent! Hash: {tx_hash.hex()}")


def recive_token(private_key: str, public_key: str) -> None:
    # Настройка подключения к тестовой сети BSC
    web3 = Web3(Web3.HTTPProvider(bsc_testnet_url))
    account = Account.from_key(private_key)
    # Адрес контракта и данные для вызова метода
    contract_method_data = '0xee42b5c7000000000000000000000000' + del0x(
        public_key) + '000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000001300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000013000000000000000000000000000000000000000000000000000000000000000'
    # Формирование и отправка транзакции
    nonce = web3.eth.get_transaction_count(account.address)
    transaction = {
        'to': contract_address,
        'value': 0,  # Количество отправляемых токенов - 0 для вызова метода
        'gas': 2000000,  # Установите достаточно высокий лимит газа
        'gasPrice': web3.to_wei('5', 'gwei'),
        'nonce': nonce,
        'data': contract_method_data,
        'chainId': chain_id
    }
    # Подписание и отправка транзакции
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # Вывод хэша транзакции
    print(f"Token recieve hash: {tx_hash.hex()}")


def transfer_token(from_private_key, to_address, gas_price="20") -> None:
    web3 = Web3(Web3.HTTPProvider(bsc_testnet_url))
    # Создание объекта контракта токена
    token_abi = [
        {
            "constant": False,
            "inputs": [
                {
                    "name": "_to",
                    "type": "address"
                },
                {
                    "name": "_value",
                    "type": "uint256"
                }
            ],
            "name": "transfer",
            "outputs": [
                {
                    "name": "",
                    "type": "bool"
                }
            ],
            "type": "function"
        }
    ]
    token_contract = web3.eth.contract(address=token_address, abi=token_abi)

    # Получение аккаунта отправителя
    account = Account.from_key(from_private_key)

    # Подготовка данных транзакции
    nonce = web3.eth.get_transaction_count(account.address)
    tx = token_contract.functions.transfer(to_address, web3.to_wei(10, 'ether')).build_transaction({
        'chainId': web3.eth.chain_id,
        'gas': 70000,
        'gasPrice': web3.to_wei(gas_price, 'gwei'),
        'nonce': nonce,
    })
    # Подписание транзакции
    signed_tx = web3.eth.account.sign_transaction(tx, from_private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"Token transfer to home: {tx_hash.hex()}")
