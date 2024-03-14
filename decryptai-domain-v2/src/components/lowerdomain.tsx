import * as React from "react";
import { Box, Flex, IconButton, Spacer, Link, Text, Icon } from "@chakra-ui/react";
import { FaLinkedin, FaGithub } from "react-icons/fa";
import { FiMail } from "react-icons/fi";


export interface MediaLink {
    href: string;
    ariaLabel: string;
    icon: React.ElementType; 
}

export const MediaLinks: MediaLink[] = [
    
        {href: "https://www.linkedin.com/in/obi-anthony-uzoeto-4219b1183/", ariaLabel:"LinkedIn", icon: FaLinkedin },
        {href:"https://github.com/ObiAU", ariaLabel:"GitHub Account", icon: FaGithub },
        {href:"mailto:obszeto@gmail.com", ariaLabel: "Email", icon: FiMail }
    
];

const Ldomain: React.FC = () => {
    return (
            <Box px={4}>
                <Flex h='16' alignItems='center' gap='2' justifyContent={'space-between'}>
                    <Box>
                        <Text as='cite'>&copy; {new Date().getFullYear()} OA Clan. All rights reserved.</Text>
                    </Box>
                    <Spacer/>
                    <Box>
                        <Text as='cite'> Media Links </Text>
                    </Box>
                <Flex alignItems='center'>
                    <Spacer/>
                    <Box p="5">
                            {/* as="a" changes prop to act like an anchor element */}
                            {MediaLinks.map((link) => (
                                <IconButton as="a" href={link.href} aria-label={link.ariaLabel} icon={<link.icon/>} isRound={true}/>
                            ))}
                        </Box>

                    </Flex>

                </Flex>
            </Box>


    );
};

export default Ldomain;