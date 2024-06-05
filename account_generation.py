from eth_account import Account
import secrets


def generate_account():
    # Генерация нового приватного ключа
    private_key = secrets.token_hex(32)
    private_key_with_prefix = "0x" + private_key

    # Создание аккаунта с использованием сгенерированного приватного ключа
    account = Account.from_key(private_key_with_prefix)

    print("Generating new account...")
    print(f"Приватный ключ: {private_key_with_prefix}")
    print(f"Адрес кошелька: {account.address}")
    return private_key_with_prefix, account.address


def del0x(hex_string: str) -> str:
    modified_string_1 = hex_string.replace("0x", "")
    return modified_string_1
