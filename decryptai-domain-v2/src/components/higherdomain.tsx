import React, { useState } from "react";
import { ColorModeSwitcher } from "./ColorModeSwitcher";
import { Link } from "react-router-dom";
import { Box, Flex, Heading, Button, Text, Spacer, ButtonGroup, Image } from "@chakra-ui/react";

const HDomain = () =>
{
    return (
        <Box px={2}>
          <Flex alignItems="center" justifyContent="space-between" minHeight="5vh">
            {/* Left Side - DeCrypt Text */}
            <Box flex={{ base: 1, md: 'auto' }} lineHeight="1.2">
              <Text fontWeight="bold" fontSize="2xl">
                DeCrypt
              </Text>
            </Box>
    
            {/* Center - Navigation Links */}
            <Flex flex={{ base: 1, md: 'auto' }} justify="center" alignItems="center">
             <ButtonGroup gap='10'>
             <Button as={Link} to="/" colorScheme="cyan" variant="outline" size="md">
                Home
              </Button>
              {/* <Button as={Link} to="/About" colorScheme="cyan" variant="outline" size="md">
                About
              </Button> */}
              <Button as={Link} to="/ChatBot" colorScheme="cyan" variant="outline" size="md">
                Analytics
              </Button>
             </ButtonGroup>
            </Flex>
    
            {/* Right Side - Color Mode Switcher */}
            <Flex flex={{ base: 1, md: 'auto' }} justify="flex-end">
              <ColorModeSwitcher />
            </Flex>
          </Flex>
        </Box>
      );
    }

export default HDomain;
