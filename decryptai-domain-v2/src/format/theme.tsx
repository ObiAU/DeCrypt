import { extendTheme, type ThemeConfig } from "@chakra-ui/react";

const config: ThemeConfig = {
    initialColorMode: 'dark',
    useSystemColorMode: false,
}

const customTheme = {
    colors: {
        eletricBlue: '#7DF9BFF'
    },
    config,
}

const theme = extendTheme(customTheme);

export default theme;