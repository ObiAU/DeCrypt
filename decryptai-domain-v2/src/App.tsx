import React, { useState, useEffect } from 'react';
import './format/App.css';
import { ChakraProvider } from '@chakra-ui/react';
import Layout from './layout';
import theme from './format/theme';

const App: React.FC = () => {
  return (
    <ChakraProvider theme={theme}>
      <Layout/>
    </ChakraProvider>
  );
}

export default App;
