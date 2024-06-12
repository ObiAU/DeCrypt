import * as React from "react";
import { useState } from "react";
import TokenStore, { TokenRowData } from './tokenVal-store';
import logo from '../im-dir_s/logo.svg';
// import oaclanlogoMod from '../im-dir_s/oaclanlogoMod.svg';
import DeltaPrice, { PriceRowData } from './deltaPrice-store';
import { ResponseData, ExtraData } from "../dependencies/Elements";
import Cover from '../format/Cover';
import { theme, Spacer, Box, Flex, useColorModeValue, Image, Spinner, Text, Button, Input, FormControl, FormLabel } from '@chakra-ui/react';
// import HandleSubmit from "./handleSubmit";
import { TypeAnimation } from "react-type-animation";
import userIcon3 from '../im-dir_s/userIcon3.png';
import Logo from "../format/logo";


const ClanHead: React.FC = () => {

const boxColor = useColorModeValue('black', 'white');
const txtColor = useColorModeValue('black', 'cyan');
const inputColor = useColorModeValue('black', 'white');

const [walletAddress, setWalletAddress] = useState<string>('');
const [userInput, setUserInput] = useState<string>('');
const [responses, setResponses] = useState<Array<string | ResponseData>>([]);
const [step, setStep] = useState<number>(0);
const [extraData, setExtraData] = useState<ExtraData>({});
const [needMoreInfo, setNeedMoreInfo] = useState<boolean>(false);
const [currentResponse, setCurrentResponse] = useState<string>('');
const [extraInfoStep, setExtraInfoStep] = useState<number>(0);
const [isLoading, setIsLoading] = useState<boolean>(false);
const [tokenBalances, setTokenBalances] = useState<Array<any>>([])

const [showTypeAnim, setshowTypeAnim] = useState(true);

const HandleSubmit = async (e: React.FormEvent<HTMLFormElement>): Promise<void> => {

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
        setNeedMoreInfo(false);
        setExtraInfoStep(0); 
      }
    } else {
      const data = {
        wallet_address: walletAddress,
        user_input: userInput,
        extra_data: extraData
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
          if (responseData.response.type === 'dataframe' || responseData.response.type === 'pricechange') {
            newResponses.push({ type: responseData.response.type, data: JSON.parse(responseData.response.data) });
          } else {
            newResponses.push(`DeCrypt: ${responseData.response}`);
          }
        } else if (responseData.need_more_info) {
          setNeedMoreInfo(true);
        } else {
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

  
  <Flex direction="column" justifyContent="flex-end" alignItems="center" minHeight="79vh" minWidth="max-content"  flex="1">
{/* <Box flex="1" overflowY="auto" alignSelf="center"> */}
<Flex position="absolute" justifyContent="center" alignItems="center" top={20} bottom={170} >
        <TypeAnimation
          sequence={[
            "How can I help you today?", 2500, 
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b',
          ]}
          wrapper="div"
          speed={50}
          cursor={false}
          style={{ fontSize: '24px', textAlign: 'center' }}
          repeat={0}
          
          // onComplete={() => setshowTypeAnim(false)}
        /></Flex>

        <Box width="75vh" textAlign="center" alignSelf="center" overflowY='auto' 
        // pos="absolute" bottom="20"
        >
          
          {responses.map((res, index) => {

            if (typeof res === 'string' && res.startsWith('You:')) {
              return (      
              <Flex key={index} alignItems="center" mb='4' borderBottom='1px solid' borderColor={boxColor} borderStyle="groove" pb='2' w="full">
              <Image src={userIcon3} w="24px" h="24px" mr={2} />
              <Text color={boxColor}>{res}</Text>
              </Flex>
          );
              } else if (typeof res === 'string'){
                return (
                  <Flex key={index} alignItems="center" mb='4' borderBottom='1px solid' borderColor={boxColor} borderStyle="groove" pb='2' w="full">
                  {/* <Image src={logo} className="App-logo" w="24px" h="24px" mr={2} /> */}
                  <Logo className="App-logo" w="24px" h="24px" mr={2}/>
                  <Text color={boxColor}>{res}</Text>
                  </Flex>
                );

            } else if (res.type === 'dataframe') {
              return (
              <Flex key={index} alignItems="center" mb='4' borderBottom='1px solid' borderColor={boxColor} borderStyle="groove" pb='2' w="full">
                {/* <Image src={Logo} className="App-logo" w="24px" h="24px" mr={2}/> */}
                <Logo className="App-logo" w="24px" h="24px" mr={2}/>
              <TokenStore key={index} data={res.data as TokenRowData[]} />
              </Flex>);
            } else if (res.type === 'pricechange'){
              return (
                <Flex key={index} alignItems="center" mb='4' borderBottom='1px solid' borderColor={boxColor} borderStyle="groove" pb='2' w="full">
              {/* <Image src={logo} className="App-logo" w="24px" h="24px" mr={2}/> */}
              <Logo className="App-logo" w="24px" h="24px" mr={2}/>
            <DeltaPrice key={index} data={res.data as PriceRowData[]} />
            </Flex>
            );
          }
          })}
          
          {isLoading && (
            <Spinner
            size='lg' color='teal' />
          )}
          {/* <Box width="60vh" alignSelf="center" pos="absolute" bottom="20"> */}
          <form onSubmit={HandleSubmit}>
            {step < 1 && (
              <FormControl>
              <Input
                id="walletAddress"
                type="text"
                color={inputColor}
                value={walletAddress}
                onChange={e => setWalletAddress(e.target.value)}
                placeholder="Please enter your Wallet Address"
                _placeholder={{ color: txtColor }}
                focusBorderColor={boxColor}
                className="query-input"
              />
              </FormControl>
            )}

            {step === 1 && !needMoreInfo && (
              <FormControl>
              <Input
                id="userInput"
                type="text"
                color={inputColor}
                value={userInput}
                onChange={e => setUserInput(e.target.value)}
                placeholder="How can I help you today?"
                _placeholder={{ color: txtColor }}
                focusBorderColor={boxColor}
                className="query-input"
              />
              </FormControl>
            )}

            {needMoreInfo && (
              <FormControl>
              <Input
                id="extraInfoInput"
                type="text"
                color={inputColor}
                value={userInput}
                onChange={e => setUserInput(e.target.value)}
                placeholder={
                  extraInfoStep === 0 ? "Please enter the ticker symbol (e.g., BTC, ETH)" :
                  extraInfoStep === 1 ? "Please enter the Start Date (dd-mm-yyyy)" :
                  "Please enter the End Date (dd-mm-yyyy)"
                }
                _placeholder={{ color: txtColor }}
                focusBorderColor={boxColor}
                className="query-input"
              />
              </FormControl>
            )}
          </form>
          {/* </Box> */}

          </Box>
      
      {/* </Box> */}
      </Flex>

  );
              
};

export default ClanHead;