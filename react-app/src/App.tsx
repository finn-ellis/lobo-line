import React, { useState, useRef, useEffect } from 'react';
import styled from 'styled-components';
import Typewriter from 'typewriter-effect';

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 90vh;
  background-color: ${({ theme }) => theme.background};
`;

const Title = styled.h1`
  font-size: 4rem;
  color: ${({ theme }) => theme.colors.cherry}; /* UNM crimson */
  margin-bottom: 5vh;
  font-weight: bold;
`;

const StyledForm = styled.form`
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  & > * {
    margin-bottom: 1vh; /* Add padding between children */
  }
`;

const InputBox = styled.input`
  width: 50%;
  max-width: 75vw; /* Ensure the input box doesn't exceed 75% of the viewport width */
  padding: 15px;
  border-radius: 15px;
  border: 2px solid ${({ theme }) => theme.colors.black};
  font-size: 1rem;
  color: ${({ theme }) => theme.text};
  outline: none;
  background-color: ${({ theme }) => `${theme.colors.mesa}50`};
  white-space: normal; /* Allow text to wrap */

  ::placeholder {
    color: ${({ theme }) => theme.colors.loboGray};
    font-style: italic;
  }
`;

const StyledButton = styled.button`
  margin-top: 10px;
  padding: 10px 20px;
  border-radius: 15px;
  border: none;
  background-color: ${({ theme }) => theme.colors.turquoise};
  color: white;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;

  &:hover {
    background-color: ${({ theme }) => theme.colors.highNoon};
  }
  &:active {
    background-color: ${({ theme }) => theme.colors.deepDusk};
  }
`;

const ResponseBox = styled.div`
  width: 50%;
  padding: 15px;
  border-radius: 15px;
  border: 2px solid ${({ theme }) => theme.colors.greenChile};
  font-size: 1rem;
  background-color: ${({ theme }) => `${theme.colors.greenChile}50`};
	margin-bottom: 5vh;
`;

const HiddenSpan = styled.span`
  visibility: hidden;
  position: absolute;
  max-width: 75vw; /* Ensure the hidden span doesn't exceed 75% of the viewport width */
`;

const App: React.FC = () => {
  const [inputValue, setInputValue] = useState('');
  const [response, setResponse] = useState<{ result: string } | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const spanRef = useRef<HTMLSpanElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

	const placeholderText = " Question about New Mexico's Flagship University? "

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
  };

  useEffect(() => {
    if (spanRef.current && inputRef.current) {
      inputRef.current.style.width = `${spanRef.current.offsetWidth+1}px`;
      inputRef.current.style.height = `${spanRef.current.offsetHeight}px`; // Match height
    }
  }, [inputValue]);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsLoading(true);
    try {
      const response = await fetch(`/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: inputValue }),
      });
      const data = await response.json();
      setResponse(data);
    } catch (error) {
      console.error('Error:', error);
      setIsLoading(false);
    }
  };

  return (
    <Container>
      <Title>LOBOLINE</Title>
      {response && (
        <ResponseBox>
          <Typewriter
						key={response.result}
            options={{
              delay: 10,
            }}
            onInit={(typewriter) => {
							typewriter
									.typeString(response.result)
									.callFunction(() => {
										setIsLoading(false);
									})
									.start();
            }}
          />
        </ResponseBox>
      )}
      {isLoading ? (
        <p>Thinking...</p>
      ) : (
        <StyledForm onSubmit={handleSubmit}>
          <HiddenSpan ref={spanRef}>{inputValue || placeholderText}</HiddenSpan>
          <InputBox
            ref={inputRef}
            type="text"
            autoFocus
            placeholder={placeholderText}
            value={inputValue}
            onChange={handleInputChange}
          />
          <StyledButton type="submit">Submit</StyledButton>
        </StyledForm>
      )}
    </Container>
  );
};

export default App;