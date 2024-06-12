# DeCrypt Functionality

DeCrypt is a cryptocurrency analysis and consultancy tool developed using Python, TypeScript and Reactjs. It uses OpenAI, Covalent, CryptoCompare and Moralis APIs primarily for analytics, and Chakra UI for interface design.

Designed for cryptocurrency enthusiasts, DeCrypt offers real-time financial analytics and decision support.

Functionality:

Live Financial Analytics: Compute live Sharpe ratio and risk/volatility metrics for specified periods.

Token Filtering: Filter cryptocurrencies by value, type, and other criteria.

Profit and Loss Calculations:
Quote P&L: Track market value changes of assets over specific periods.
Balance P&L: Monitor changes in current balances.
Real-time currency conversion (data as of 06.02.24).

Advanced Analysis: In-depth analysis and consultation of all outputs, with a memory of 5 messages and a 500-token response capability.

Price Change Analysis: Examine price fluctuations for individual and overall tokens.

Holdings Analysis: Review current holdings and compare with 24-hour historical data.

Technologies Used:

Programming Languages: Python, TypeScript (React.js), HTML, CSS

APIs: Covalent, OpenAI, Moralis, Deribit, Cryptocompare

AI Model: Integrated GPT-3.5 Turbo for enhanced interactivity

More features to come!

# Project Structure

- '/decrypt_domain_v2' - Contains all frontend components - UI components, routers and static assets.
- '/decrypt_server_v2' - Contains all backend modules, project setup configs, and the flask app.
- `/docker` - Contains all Docker-related files including Dockerfile, docker-compose for local setup, and Docker-specific instructions.
