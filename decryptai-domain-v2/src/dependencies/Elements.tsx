import { useState } from "react";
import { TokenRowData } from "../components/tokenVal-store";
import { PriceRowData } from "../components/deltaPrice-store";

export interface ResponseData {
    type: 'dataframe' | 'pricechange' | 'string';
    data: TokenRowData[] | PriceRowData[] | string;
}

export interface ExtraData {
    ticker?: string;
    start_date?: string;
    end_date?: string;
}



const [walletAddress, setWalletAddress] = useState<string>('');
const [userInput, setUserInput] = useState<string>('');
const [responses, setResponses] = useState<Array<string | ResponseData>>([]);
const [step, setStep] = useState<number>(0);
const [extraData, setExtraData] = useState<ExtraData>({});
const [needMoreInfo, setNeedMoreInfo] = useState<boolean>(false);
const [typingIndex, setTypingIndex] = useState<number>(0);
const [currentResponse, setCurrentResponse] = useState<string>('');
const [extraInfoStep, setExtraInfoStep] = useState<number>(0);
const [isLoading, setIsLoading] = useState<boolean>(false);
const [tokenBalances, setTokenBalances] = useState<Array<any>>([]);
