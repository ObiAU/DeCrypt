from decrypt_transformer import check_for_command 
from decrypt_transformer import get_completion, get_token_balances, parse_dates_from_input
from decrypt_transformer import calculate_profit_and_loss, calculate_sharpe_ratio
from decrypt_transformer import calculate_volatility, extract_ticker, filter_by_token_name
from decrypt_transformer import top_n_by_value
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def main():
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
        command_response = check_for_command(user_input, wallet_address)

        if command_response:
            print(command_response)
            messages.append({"role": "assistant", "content": str(command_response)})
        else:
            MAX_HISTORY = 4
            if len(messages) > MAX_HISTORY:
                messages = messages[-MAX_HISTORY:]


            prompt = " ".join([msg['content'] for msg in messages])
            # print("Final prompt being sent:", prompt)  
            gpt_response = get_completion(prompt, client)
            print(gpt_response)
            messages.append({"role": "assistant", "content": gpt_response})

      except Exception as e:
        print(f"An error occurred: {e}. Please try again.")

    print("Goodbye!")

# "0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8"
# i want the sharpe ratio for BTC for the dates 05-12-2022 and 05-12-2023  
main()
