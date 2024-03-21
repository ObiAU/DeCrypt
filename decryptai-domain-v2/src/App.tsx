import React, { StrictMode } from 'react';
import './format/App.css';
import { ChakraProvider } from '@chakra-ui/react';
import Layout from './layout';
import theme from './format/theme';

const App: React.FC = () => {
  return (
    <StrictMode>
    <ChakraProvider theme={theme}>
      <Layout/>
    </ChakraProvider>
    </StrictMode>
  );
}

export default App;
