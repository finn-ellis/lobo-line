# University Query-Answering Application

## Overview

This application answers user queries by:

1. **Discovering all subdomains and subsites** of the University of New Mexico (`unm.edu`) website and compiling their URLs into a text file.
2. **Selecting the most relevant URLs** based on the user's query.
3. **Scraping content** from these URLs in real-time.
4. **Generating an answer** using an OpenAI Large Language Model (LLM) based on the scraped content.

## Development Steps

### 1. Subdomain and Subsite Discovery

- **Script:** `discover_subdomains.py`
- **Description:** Finds all subdomains of `unm.edu` using Amass and saves them to `subdomains.txt`.

### 2. Crawl URLs

- **Script:** `crawl_urls.py`
- **Description:** Crawls each discovered subdomain to extract all accessible URLs and saves them to `urls.txt`.

### 3. Generate Embeddings

- **Script:** `generate_embeddings.py`
- **Description:** Generates embeddings for each URL's title or meta description using OpenAI's Embedding API and saves them to `embeddings.pkl`.

### 4. Select Relevant URLs

- **Script:** `select_relevant_urls.py`
- **Description:** Selects the top N relevant URLs based on the user's query and saves them to `selected_urls.txt`.

### 5. Scrape Content

- **Script:** `scrape_content.py`
- **Description:** Scrapes and cleans content from the selected URLs and saves it to `scraped_content.txt`.

### 6. Query LLM

- **Script:** `query_llm.py`
- **Description:** Constructs a prompt with the user's query and scraped content, sends it to OpenAI's GPT-4o-mini model, and retrieves the answer.

### 7. Main Application

- **Script:** `main.py`
- **Description:** Serves as the entry point to coordinate the entire workflow from query input to answer output.

## Setup and Usage

### 1. Installation

- **Clone the Repository:**

  ```bash
  git clone https://github.com/yourusername/university-query-app.git
  cd university-query-app
  ```

- **Install Dependencies:**

  ```bash
  pip install -r requirements.txt
  ```

### 2. Configuration

- **Configure API Keys:**
  
  - Create a `.env` file in the project root directory and add your OpenAI API key:

    ```env
    OPENAI_API_KEY=your_openai_api_key_here
    ```

  - Alternatively, you can set the environment variable in your terminal:

    ```bash
    export OPENAI_API_KEY="your_openai_api_key_here"
    ```

### 3. Initial Setup

- **Discover Subdomains:**

  ```bash
  python discover_subdomains.py
  ```

- **Crawl URLs:**

  ```bash
  python crawl_urls.py
  ```

- **Generate Embeddings:**

  ```bash
  python generate_embeddings.py
  ```

### 4. Running the Application

- **Start the App:**

  ```bash
  python main.py
  ```

- **Enter User Query:**
  
  - Follow the on-screen prompt to input your query.
  
  - Example:

    ```
    Enter your query: What are the admission requirements for the computer science master's program?
    ```

- **Sample Answer:**

    ```
    Answer: The admission requirements for the Master's program in Computer Science include a bachelor's degree in a related field, a minimum GPA of 3.0, GRE scores, letters of recommendation, and a statement of purpose. For detailed information, please visit the university's admissions page at [URL].
    ```

## Additional Considerations

### Error Handling

- Implement retries and timeouts for network requests to handle transient failures.
- Handle API rate limits by implementing exponential backoff strategies.
- Validate and sanitize user input to prevent injection attacks. *(TODO)*

### Performance Optimization

- **Caching:** Implement caching mechanisms for embeddings and scraped content to reduce redundant processing.
- **Asynchronous Operations:** Utilize asynchronous programming to handle multiple I/O-bound tasks concurrently.

### Compliance and Ethics

- **Respect `robots.txt`:** Ensure compliance with the website's crawling policies.
- **Terms of Service:** Verify that scraping activities adhere to the university's terms of service.
- **Data Privacy:** Avoid scraping sensitive or personal information.

### Scalability

- **Modular Design:** The application is divided into separate modules for easy maintenance and scalability.
- **Logging:** Implement logging to monitor application performance and troubleshoot issues.

### Testing

- **Unit Tests:** Write unit tests for individual functions in each module.
- **Integration Tests:** Test the complete workflow from query input to answer output.

## Licensing

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.