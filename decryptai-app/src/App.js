import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import TokenBalanceDataGrid from './TokenBalanceDataGrid';
import PriceChangeDataGrid from './PriceChangeDataGrid';
// import Particles from 'react-tsparticles'
import Cover from './Cover';

function App() {
  const [walletAddress, setWalletAddress] = useState('');
  const [userInput, setUserInput] = useState('');
  const [responses, setResponses] = useState([]);
  const [step, setStep] = useState(0);
  const [extraData, setExtraData] = useState({});
  const [needMoreInfo, setNeedMoreInfo] = useState(false);
  const [typingIndex, setTypingIndex] = useState(0);
  const [currentResponse, setCurrentResponse] = useState('');
  const [extraInfoStep, setExtraInfoStep] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [tokenBalances, setTokenBalances] = useState([]);

  useEffect(() => {
    if (currentResponse && typingIndex < currentResponse.length) {
      setTimeout(() => {
        setTypingIndex(typingIndex + 1);
      }, 50); 
    }
  }, [typingIndex, currentResponse]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    let newResponses = [...responses];
    
    if (step === 0) {
      newResponses.push(`DeCrypt Bot: Your Wallet Address is ${walletAddress}`);
      setStep(1);
    } else if (needMoreInfo) {
      if (extraInfoStep === 0) {
        setExtraData({ ...extraData, ticker: userInput });
        setUserInput('');
        setExtraInfoStep(1);
      } else if (extraInfoStep === 1) {
        setExtraData({ ...extraData, start_date: userInput });
        setUserInput('');
        setExtraInfoStep(2);
      } else if (extraInfoStep === 2) {
        setExtraData({ ...extraData, end_date: userInput });
        setUserInput('');
        // setNeedMoreInfo(false);
        // setExtraInfoStep(0);

      const data = {
        wallet_address: walletAddress,
        user_input: userInput,
        extra_data: extraData
      };

    }
    setNeedMoreInfo(false);
    setExtraInfoStep(0); 

    } else {
      const data = {
        wallet_address: walletAddress,
        user_input: userInput,
        extra_data: {}
      };
      const response = await fetch('http://127.0.0.1:5001/process_query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      const responseData = await response.json();
      if (response.ok) {
        newResponses.push(`You: ${userInput}`);

        if (responseData.response) {
          if (responseData.response.type === 'dataframe'){
            newResponses.push({ type: 'dataframe', data: JSON.parse(responseData.response.data) });

          } else if (responseData.response.type === 'pricechange') {
            newResponses.push({ type: 'pricechange', data: JSON.parse(responseData.response.data) });
          } else {
          newResponses.push(`DeCrypt Bot: ${responseData.response}`);

          }
  
        } else if (responseData.need_more_info) {
          setNeedMoreInfo(true);
        } else {
          // newResponses.push("Response: No additional information provided.");
          newResponses.push("No additional information provided.");
        }
      } else {
        newResponses.push(`Error: ${responseData.error}`);
      }
           
      setUserInput('');
    } 
  
    setResponses(newResponses);
    setIsLoading(false);
  };

  return (
    <div className="App">
      <Cover />
      <div className="App-content" style={{ position: 'relative', zIndex: 1 }}>
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h2>DeCrypt-AI</h2>

        {responses.map((res, index) => {
            if (typeof res === 'string') {
              return <p key={index} className='response-text'>{res}</p>;
            } else if (res.type === 'dataframe') {
              return <TokenBalanceDataGrid key={index} data={res.data} />;
            } else if (res.type === 'pricechange'){
              return <PriceChangeDataGrid key={index} data={res.data} />;
            }
          })}

        {/* {tokenBalances.length > 0 && <TokenBalanceDataGrid data={tokenBalances} />} */}

        <p>{currentResponse.substring(0, typingIndex)}</p>
        {isLoading && (
        <div className="loading-spinner"></div>
)}
        <form onSubmit={handleSubmit}>
          {step < 1 && (
            <input
              type="text"
              value={walletAddress}
              onChange={e => setWalletAddress(e.target.value)}
              placeholder={"Please enter your Wallet Address"}
              className="query-input"
            />
          )}

          {step === 1 && !needMoreInfo && (
            <input
              type="text"
              value={userInput}
              onChange={e => setUserInput(e.target.value)}
              placeholder="How can I help you today?"
              className="query-input"
            />
          )}

          {needMoreInfo && (
            <input
              type="text"
              value={userInput}
              onChange={e => setUserInput(e.target.value)}
              placeholder={
                extraInfoStep === 0 ? "Please enter the ticker symbol (e.g., BTC, ETH)" :
                extraInfoStep === 1 ? "Please enter the Start Date (dd-mm-yyyy)" :
                "Please enter the End Date (dd-mm-yyyy)"
              }
              className="query-input"
            />
          )}
        </form>

        {/* {responses.map((res, index) => (
          <p key={index}>{res}</p>
        ))} */}
      </header>
     </div>
    </div>
  );
}

export default App;

// "0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8"