from flask import request, jsonify
from command import Commander
from models import Model, Prompters

class Processor(Model, Prompters, Commander):
    def __init__(self) -> None:
        super().__init__()

    def process_query(self):
        try:
            commands_balance = ['token balance', 'token balances', 'token', 'tokens']
            commands_pnl = ['profit and loss', 'p&l']
            commands_sharpe = ['sharpe ratio', 'sharpe']
            commands_volatility = ['volatility', 'risk']

            messages = []

            data = request.get_json()
            wallet_address = data['wallet_address'].replace('"', '').strip()
            user_input = data['user_input']
            extra_data = data.get("extra_data")
            
            messages.append({"role": "user", "content": user_input})

            command_response = None
            
            command_keyword = next((command for command in commands_balance + commands_pnl + commands_sharpe + commands_volatility if command in user_input.lower()), None)

            if command_keyword:
                checker = self.CoT_prompt_engineer(user_input, self.client)

                if 'yes' in checker.lower():
                    command_response = self.check_for_command(user_input, wallet_address, is_web=False, extra_data=extra_data)
                    messages.append({"role": "assistant", "content": str(command_response)})

                else:
                    prompt = " ".join([msg['content'] for msg in messages])
                    gpt_response = self.get_completion(prompt, self.client)
                    messages.append({"role": "assistant", "content": gpt_response})
            
            else:
                command_response = self.check_for_command(user_input, wallet_address, is_web=False, extra_data=extra_data)
                
                if isinstance(command_response, dict) and command_response.get("need_more_info"):
                    return jsonify(command_response), 200
                
                elif command_response:

                    messages.append({"role": "assistant", "content": str(command_response)})

                else:
                    MAX_HISTORY = 5
            
                    if len(messages) > MAX_HISTORY:
                        messages = messages[-MAX_HISTORY:]

                    prompt = " ".join([msg['content'] for msg in messages])

                    gpt_response = self.get_completion(prompt, self.client)

                    messages.append({"role": "assistant", "content": gpt_response})
            
            return jsonify({"response": command_response or gpt_response})

        except Exception as e:
            return jsonify({"error": str(e)}), 500