import * as React from "react";
import { theme, Spacer, Box, Flex, useColorModeValue, Image, Text, VStack, Center, IconButton, Button } from '@chakra-ui/react';
import { TypeAnimation } from "react-type-animation";
import { Link } from "react-router-dom";

const Home: React.FC = () => {

    return (
        
< Center position='relative' flex="1" pl={4} pr={0.5} pt={20} pb={2}>
    <Box></Box>
    <Spacer/>
<Flex direction={{ base: 'column', md: 'row' }} alignItems="center" justifyContent="center" 
>


<VStack align='center' spacing={5} pl={[0, 0, 20]} pr={[0, 0, 20]}>

<Text fontSize={["4xl"]} fontWeight="bold" mt="6" textAlign="center" color="blue.600">
  <TypeAnimation
sequence={["Hello and welcome to DeCrypt",
1000,
]}
speed={50}
cursor={false}
  />
  </Text>
  <Text fontSize="2xl" textAlign="center">
  <TypeAnimation
sequence={["",
2000,
"I am the DeCrypt bot - your AI helper for"
]}
speed={50}
cursor={false}
  />
    <Text as="span" color="purple.500">
    <TypeAnimation
sequence={["",
4000,
" Live Financial Analytics"
]}
speed={50}
cursor={false}
  />
    </Text>
    <TypeAnimation
sequence={["",
4500,
" and"
]}
speed={50}
cursor={false}
  />
<Text as="span" color="green.500">
<TypeAnimation
sequence={["",
5000,
" Decision Support"
]}
speed={50}
cursor={false}
  />
  </Text>
  <TypeAnimation
sequence={["",
5100,
"."
]}
speed={50}
cursor={false}
  />
  </Text>
  <Text fontSize="xl" textAlign="center" maxWidth="container.md">
  <TypeAnimation
    sequence={["",
    6300,
    "All I need is your wallet address to begin!",]}
    cursor={false}/>
  </Text>

  <Text fontSize="2xl" textAlign="center" maxWidth="container.md">
  <TypeAnimation
    sequence={["",
    7900,
    "I offer",]}
    speed={50}
    cursor={false}/>
 <Text as="span" color="orange.400">
 <TypeAnimation
    sequence={["",
    8600,
    " Token Filtering",]}
    speed={50}
    cursor={false}/>
    </Text>
    <TypeAnimation
    sequence={["",
    9000,
    ",",]}
    speed={50}
    cursor={false}/> 
    <Text as="span" color="cyan.500">
    <TypeAnimation
    sequence={["",
    9500,
    " Profit & Loss calculations",]}
    speed={50}
    cursor={false}/> 
    </Text>
    <TypeAnimation
    sequence={["",
    9600,
    ",",]}
    speed={50}
    cursor={false}/> <Text as="span" color="teal.400">
    <TypeAnimation
    sequence={["",
    10800,
    " consultancy-type analytics",]}
    speed={50}
    cursor={false}/> 
    </Text>
    <TypeAnimation
    sequence={["",
    11800,
    ", and more.",]}
    speed={50}
    cursor={false}/> 
  </Text>
  <Text fontSize="xl" textAlign="center" maxWidth="container.md">
  <TypeAnimation
    sequence={["",
    13100,
    "Feel free to ask me anything!",]}
    speed={50}
    cursor={false}/>
  </Text>
  <Spacer/>
  <Text fontSize="xl">
    <TypeAnimation
    sequence={["",
    14500,
    "Click below to get started, or navigate to the Analytics Tab.",]}
    speed={50}
    cursor={false}/>
  </Text>
  <Button as={Link} to="/ChatBot" colorScheme="cyan" variant="outline" size="md">
    <TypeAnimation sequence={["", 16000, "Begin"]} cursor={false}/>
    {/* Analytics Page */}
  </Button>
</VStack>


        </Flex>
        <Spacer/>
        <Box>
        </Box>

        </Center>

      
    );
};


export default Home;