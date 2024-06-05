import time
import random
from config import YOUR_ADDRESS, min_time, max_time
from account_generation import generate_account
from transfer import send_bnb, recive_token, transfer_token


def main():
    count = input("Count: ")
    faucet_private_key, faucet_public_key = generate_account()
    stop = input("Send tBNB to " + faucet_public_key + " and after that press ENTER")
    for i in range(int(count)):
        print(i)
        start_time = time.time()
        private_key, public_key = generate_account()
        time.sleep(random.randint(min_time, max_time))
        send_bnb(faucet_private_key, public_key)
        time.sleep(random.randint(min_time, max_time))
        recive_token(private_key, public_key)
        time.sleep(random.randint(min_time, max_time))
        transfer_token(private_key, YOUR_ADDRESS)
        time.sleep(random.randint(min_time, max_time))
        end_time = time.time()
        print(f"Fake time: {end_time - start_time}")
    print("Done")


main()
