from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
import openai
from config import OPENAI_API_KEY, SESSION_KEY
import json
from decrypt_transformer import check_for_command, get_completion, prompt_engineer

openai.api_key = OPENAI_API_KEY

app = Flask(__name__)
app.secret_key = SESSION_KEY
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_query', methods=['POST'])
def process_query():
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
            checker = prompt_engineer(user_input, openai)

            if 'yes' in checker.lower():
                command_response = check_for_command(user_input, wallet_address, is_web=False, extra_data=extra_data)
                messages.append({"role": "assistant", "content": str(command_response)})

            else:
                prompt = " ".join([msg['content'] for msg in messages])
                gpt_response = get_completion(prompt, openai)
                messages.append({"role": "assistant", "content": gpt_response})
        
        else:
            command_response = check_for_command(user_input, wallet_address, is_web=False, extra_data=extra_data)
            
            if isinstance(command_response, dict) and command_response.get("need_more_info"):
                return jsonify(command_response), 200
            
            elif command_response:

                messages.append({"role": "assistant", "content": str(command_response)})

            else:
                MAX_HISTORY = 5
        
                if len(messages) > MAX_HISTORY:
                    messages = messages[-MAX_HISTORY:]

                prompt = " ".join([msg['content'] for msg in messages])

                gpt_response = get_completion(prompt, openai)

                messages.append({"role": "assistant", "content": gpt_response})
        
        return jsonify({"response": command_response or gpt_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
    # app.run(debug = True)

# "0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8"
