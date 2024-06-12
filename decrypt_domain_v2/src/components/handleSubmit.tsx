// import * as React from "react";
import React from "react";
// import { useState } from "react";
// import { ExtraData, ResponseData } from "../dependencies/Elements";
// import { useNavigate } from "react-router-dom";

// const HandleSubmit = async (e: React.FormEvent<HTMLFormElement>): Promise<void> => {

//     e.preventDefault();

//     setIsLoading(true);

//     let newResponses = [...responses];
    
//     if (step === 0) {
//       newResponses.push(`DeCrypt Bot: Your Wallet Address is ${walletAddress}`);
//       setStep(1);
//     } else if (needMoreInfo) {
//       if (extraInfoStep === 0) {
//         setExtraData({ ...extraData, ticker: userInput });
//         setUserInput('');
//         setExtraInfoStep(1);
//       } else if (extraInfoStep === 1) {
//         setExtraData({ ...extraData, start_date: userInput });
//         setUserInput('');
//         setExtraInfoStep(2);
//       } else if (extraInfoStep === 2) {
//         setExtraData({ ...extraData, end_date: userInput });
//         setUserInput('');
//         setNeedMoreInfo(false);
//         setExtraInfoStep(0); 
//       }
//     } else {
//       const data = {
//         wallet_address: walletAddress,
//         user_input: userInput,
//         extra_data: extraData
//       };
//       const response = await fetch('http://127.0.0.1:5001/process_query', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(data),
//       });

//       const responseData = await response.json();
//       if (response.ok) {
//         newResponses.push(`You: ${userInput}`);

//         if (responseData.response) {
//           if (responseData.response.type === 'dataframe' || responseData.response.type === 'pricechange') {
//             newResponses.push({ type: responseData.response.type, data: JSON.parse(responseData.response.data) });
//           } else {
//             newResponses.push(`DeCrypt Bot: ${responseData.response}`);
//           }
//         } else if (responseData.need_more_info) {
//           setNeedMoreInfo(true);
//         } else {
//           newResponses.push("No additional information provided.");
//         }
//       } else {
//         newResponses.push(`Error: ${responseData.error}`);
//       }
           
//       setUserInput('');
//     } 

    // navigate('/Chatbot');
  
//     setResponses(newResponses);
//     setIsLoading(false);
//   };

// export default HandleSubmit;





