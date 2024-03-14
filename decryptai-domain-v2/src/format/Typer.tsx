import React, { useState, useEffect } from 'react';
import { Text, TextProps } from '@chakra-ui/react';

interface TypingEffectProps extends TextProps {
  text: string;
  speed?: number; // Optional with default value
}

const TypingEffect: React.FC<TypingEffectProps> = ({ text, speed = 200, ...textProps }) => {
  const [displayedText, setDisplayedText] = useState('');

  useEffect(() => {
    let index = 0;
    const timer = setInterval(() => {
      setDisplayedText((prev) => prev + text[index]);
      index += 1;
      if (index === text.length) {
        clearInterval(timer);
      }
    }, speed);

    return () => clearInterval(timer);
  }, [text, speed]);

  return <Text {...textProps}>{displayedText}</Text>;
};


export default TypingEffect;