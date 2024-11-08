import React, { createContext, useState, useContext, useEffect } from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { ThemeProvider, createGlobalStyle } from 'styled-components';

const tintColorLight = '#0a7ea4';
const tintColorDark = '#fff';

// https://brand.unm.edu/brand-style/color-palette/index.html

const colorDictionary = {
  cherry: "#ba0c2f",
  turquoise: "#007a86",
  silver: "#a7a8aa",
  loboGray: "#63666a",
  highNoon: "#ffc600",
  sandiaSunset: "#ed8b00",
  terra: "#c05131",
  mesa: "#d6a461",
  greenChile: "#a8aa19",
  deepDusk: "#8a387c",
  black: "#000000",
  white: "#ffffff",
};

// Define light and dark theme colors
const lightTheme = {
  text: "#000000",
  background: "#ffffff",
  colors: colorDictionary
};

const darkTheme = {
  text: "#ffffff",
  background: "#191919",
  colors: colorDictionary
};

// Create a GlobalStyle component
const GlobalStyle = createGlobalStyle`
  body {
    background-color: ${(props) => props.theme.background};
    color: ${(props) => props.theme.text};
  }
`;

// Create a ThemeContext to manage the current theme
const ThemeContext = createContext({
  theme: lightTheme,
  toggleTheme: () => {}
});

const ThemeProviderComponent = ({ children }: { children: React.ReactNode }) => {
  const [theme, setTheme] = useState(lightTheme);

	useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

    const handleChange = (matches: boolean) => {
      setTheme(matches ? darkTheme : lightTheme);
    };

    handleChange(mediaQuery.matches); // Set initial theme
    mediaQuery.addEventListener('change', (e) => handleChange(e.matches));

    return () => mediaQuery.removeEventListener('change', (e) => handleChange(e.matches));
  }, [])

  const toggleTheme = () => {
    setTheme((prevTheme) => (prevTheme === lightTheme ? darkTheme : lightTheme));
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      <ThemeProvider theme={theme}>
        <GlobalStyle />
        {children}
      </ThemeProvider>
    </ThemeContext.Provider>
  );
};

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <ThemeProviderComponent>
      <App />
    </ThemeProviderComponent>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
