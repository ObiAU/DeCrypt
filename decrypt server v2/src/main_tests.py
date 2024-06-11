from tokenomics import Tokenomics
from command import Commander
from models import Model

class Maintenance(Commander, Model, Tokenomics):
    def __init__(self) -> None:
        super().__init__()

    def main(self):
        wallet_address = input("Enter your wallet address: ").replace('"', '').strip()
        # supported_chains = ["ethereum", "bitcoin"]

        # chain_name = input("Which blockchain/currency are you interested in (e.g., ethereum, bitcoin)? ").lower().strip()

        # if chain_name not in supported_chains:
        #     print("Currency not recognized. Please provide a valid blockchain/currency.")
        #     return

        messages = [
            {"role": "system", "content": "You are a helpful assistant guiding the user through querying their cryptocurrency wallet."}
        ]

        while True:
            try:
                user_input = input("\nEnter your query (or 'exit' to quit): ")

                if user_input.lower() == 'exit':
                    break

                # ticker, start_date, end_date, = None, None, None

                messages.append({"role": "user", "content": user_input})
                command_response = self.check_for_command(user_input, wallet_address)

                if command_response:
                    print(command_response)
                    messages.append({"role": "assistant", "content": str(command_response)})
                else:
                    MAX_HISTORY = 4
                    if len(messages) > MAX_HISTORY:
                        messages = messages[-MAX_HISTORY:]


                    prompt = " ".join([msg['content'] for msg in messages])
                    # print("Final prompt being sent:", prompt)  
                    gpt_response = self.get_completion(prompt, self.client)
                    print(gpt_response)
                    messages.append({"role": "assistant", "content": gpt_response})

            except Exception as e:
                print(f"An error occurred: {e}. Please try again.")

            print("Goodbye!")

if __name__ == '__main__':
    # "0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8"
    # i want the sharpe ratio for BTC for the dates 05-12-2022 and 05-12-2023  
    Maintenance()