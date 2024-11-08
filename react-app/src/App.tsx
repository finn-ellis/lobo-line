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

/** Styled Components */

/* HiddenSpan for measuring text width */
const HiddenSpan = styled.span`
  visibility: hidden;
  position: absolute;
  white-space: pre;
  font-size: 1rem;
  font-family: inherit;
  padding: 15px;
  border: 2px solid ${({ theme }) => theme.colors.black};
  box-sizing: border-box;
  /* Match other styles as needed */
`;

/* InputBox with dynamic width */
const InputBox = styled.textarea<{ dynamicWidth: number }>`
  width: ${(props) => props.dynamicWidth}px;
  min-width: 200px; /* Minimum width to ensure usability */
  max-width: 75vw; /* Ensure the textarea doesn't exceed 75% of the viewport width */
  padding: 15px;
  border-radius: 15px;
  border: 2px solid ${({ theme }) => theme.colors.black};
  font-size: 1rem;
  color: ${({ theme }) => theme.text};
  outline: none;
  background-color: ${({ theme }) => `${theme.colors.mesa}50`};
  white-space: pre-wrap; /* Allow text to wrap */
  word-wrap: break-word; /* Ensure long words break appropriately */
  resize: none; /* Disable manual resizing */
  overflow: hidden; /* Hide scrollbars */
  box-sizing: border-box; /* Include padding and border in width calculations */

  ::placeholder {
    color: ${({ theme }) => theme.colors.loboGray};
    font-style: italic;
  }
`;

/* Button Styles */
const ButtonContainer = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 3vw; /* Optional: Add space between buttons */
`;

const BaseButton = styled.button<React.ButtonHTMLAttributes<HTMLButtonElement>>`
  margin-top: 1vh;
  padding: 1vh 10vw;
  border-radius: 15px;
  border: none;
  color: white;
  font-size: 1rem;
  cursor: ${({ disabled }) => (disabled ? 'wait' : 'pointer')};
  transition: background-color 0.3s;
  height: 100%;
  box-sizing: border-box; /* Ensure padding is included within the button size */
`;

const PromptButton = styled(BaseButton)`
  background-color: ${({ theme, disabled }) =>
    disabled ? 'gray' : theme.colors.turquoise};

  &:hover {
    background-color: ${({ theme, disabled }) =>
      disabled ? 'gray' : `${theme.colors.turquoise}80`};
  }
  &:active {
    background-color: ${({ theme, disabled }) =>
      disabled ? 'gray' : theme.colors.deepDusk};
  }
`;

const FollowUpButton = styled(BaseButton)`
  background-color: ${({ theme, disabled }) =>
    disabled ? 'gray' : theme.colors.deepDusk};

  &:hover {
    background-color: ${({ theme, disabled }) =>
      disabled ? 'gray' : `${theme.colors.deepDusk}80`};
  }
  &:active {
    background-color: ${({ theme, disabled }) =>
      disabled ? 'gray' : theme.colors.deepDusk};
  }
`;

const ResponseBox = styled.div`
  width: 50%;
	min-width: 80vw;
  padding: 15px;
  border-radius: 15px;
  border: 2px solid ${({ theme }) => theme.colors.greenChile};
  font-size: 1rem;
  background-color: ${({ theme }) => `${theme.colors.greenChile}50`};
  margin-bottom: 5vh;
  box-sizing: border-box; /* Include padding and border in width calculations */
`;

/** React Component */

const App: React.FC = () => {
  const [inputValue, setInputValue] = useState('');
  const [response, setResponse] = useState<{ answer: string, session_id?: string } | null>(
    process.env.NODE_ENV === 'development'
      ? {
          answer: '<b>Development Mode Response:</b> This is a long string used as a response in development mode to simulate the behavior of the application when it is running in a development environment. This helps in testing and debugging the application without making actual API calls or relying on production data. For more information, visit <a href="https://appcontest.unm.edu/rules.html">UNM App Contest Rules</a>.',
        }
      : null
  );
  const [isLoading, setIsLoading] = useState(false);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const spanRef = useRef<HTMLSpanElement>(null);

  const placeholderText = "Question about New Mexico's Flagship University?";

  const [dynamicWidth, setDynamicWidth] = useState(200); // Initial width in pixels
  const [sessionId, setSessionId] = useState<string | null>(null); // Updated: sessionId starts as null

  // Add intent state
  const [intent, setIntent] = useState<'prompt' | 'followUp'>('prompt');

  /** Function to calculate width based on content */
  const calculateWidth = () => {
    if (spanRef.current) {
      const spanWidth = spanRef.current.scrollWidth;
      const computedWidth = Math.min(spanWidth, window.innerWidth * 0.75);
      setDynamicWidth(computedWidth + 15); // Add small buffer
    }
  };

  const handleInputChange = (
    event: React.ChangeEvent<HTMLTextAreaElement>
  ) => {
    setInputValue(event.target.value);
  };

  useEffect(() => {
    calculateWidth();
  }, [inputValue]);

  /** Handle window resize to adjust max-width */
  useEffect(() => {
    const handleResize = () => {
      calculateWidth();
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    // Removed FormData since we're using intent state

    const isFollowUp = intent === 'followUp';
    console.log(intent, isFollowUp, sessionId);

    setIsLoading(true);
    try {
      if (process.env.NODE_ENV === 'development') {
        await new Promise((resolve) => setTimeout(resolve, 1000));
        setIsLoading(false);
        return;
      }
      
      const payload: { prompt: string; session_id?: string } = { prompt: inputValue };
      if (isFollowUp && sessionId) {
        payload.session_id = sessionId;
      }
      const response = await fetch(`/prompt`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      setResponse(data);
      if (data.session_id) {
        setSessionId(data.session_id);
      }
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
            key={response.answer}
            options={{
              delay: 10,
            }}
            onInit={(typewriter) => {
              typewriter
                .typeString(response.answer)
                .callFunction(() => {
                  setIsLoading(false);
                })
                .start();
            }}
          />
        </ResponseBox>
      )}
      <StyledForm onSubmit={handleSubmit}>
        {/* HiddenSpan to measure text width */}
        <HiddenSpan ref={spanRef}>
          {inputValue || placeholderText}
        </HiddenSpan>
        <InputBox
          ref={inputRef}
          autoFocus
          placeholder={placeholderText}
          value={inputValue}
          onChange={handleInputChange}
          dynamicWidth={dynamicWidth}
          style={{ width: `${dynamicWidth}px` }}
        />
        <ButtonContainer>
          <PromptButton
            type="submit"
            // Remove name and value attributes
            disabled={isLoading}
            onClick={() => setIntent('prompt')} // Set intent on click
          >
            {isLoading ? <i>Thinking...</i> : <b>PROMPT</b>}
          </PromptButton>
          {!isLoading && response && (
            <FollowUpButton
              type="submit"
              // Remove name and value attributes
              disabled={isLoading}
              onClick={() => setIntent('followUp')} // Set intent on click
            >
              Follow Up
            </FollowUpButton>
          )}
        </ButtonContainer>
      </StyledForm>
    </Container>
  );
};

export default App;