import * as React from "react";
import Cover from './format/Cover';
import { theme, Spacer, Box, Flex, useColorModeValue, Image, Spinner, Text, Button, Input } from '@chakra-ui/react';
import Ldomain from "./components/lowerdomain";
import HDomain from "./components/higherdomain";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import oaclanlogoMod from './im-dir_s/oaclanlogoMod.svg';
import ClanHead from "./components/ClanHead";
import Home from "./components/Home";





const Layout: React.FC = () => {

  return (
    <Router>
    <Flex direction="column" minHeight="100vh">
      {/* <Cover /> */}
      <Image position='absolute' src={oaclanlogoMod} opacity={0.05} pb={0} boxSize="1150px"
            left="50%"
            top="45%"
            transform="translate(-50%, -55%)" 
            ></Image>
      <HDomain/>
      <Box textAlign="center" pt={10} pb={10} flex="1"> 
                
                <Routes>
                  <Route path='/' element={<Home />}/>
                  {/* <Route path='About' element=/> */}
                  <Route path='ChatBot' element={<ClanHead />}/>
                
                </Routes>
                  
              </Box>
      <Ldomain/>
    </Flex>
    </Router>
  );
};


export default Layout;

