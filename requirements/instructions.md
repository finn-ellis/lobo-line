# Development Plan for a Query-Answering Application Based on a University Website

## Overview

The goal is to develop an application that answers user queries by:

1. **Discovering all subdomains and subsites** of a university website and compiling their URLs into a text file.
2. **Selecting the most relevant URLs** based on the user's query.
3. **Scraping content** from these URLs in real-time.
4. **Generating an answer** using an OpenAI Large Language Model (LLM) based on the scraped content.

---

## Development Steps

### **1. Subdomain and Subsite Discovery**

- **Objective:** Find all subdomains and subsites of the university website.
- **Approach:** Use subdomain enumeration tools and web crawling techniques.
- **Output:** `urls.txt` — A text file containing a list of all discovered URLs.

### **2. Relevant Link Selection upon User Query**

- **Objective:** Choose the most relevant URLs based on the user's query.
- **Approach:** Use embeddings to match the user's query with the URLs.
- **Output:** A list of the top N relevant URLs.

### **3. Content Scraping**

- **Objective:** Scrape content from the selected URLs.
- **Approach:** Fetch and parse the HTML content to extract text.
- **Output:** Cleaned and consolidated text from the selected URLs.

### **4. Query OpenAI LLM**

- **Objective:** Generate an answer using the scraped content.
- **Approach:** Formulate a prompt incorporating the user's query and the scraped content, then query the OpenAI API.
- **Output:** The answer to the user's query.

---

## File Overview

Below is an overview of each file required for the application and its purpose.

### **1. `main.py`**

- **Purpose:** The entry point of the application.
- **Responsibilities:**
  - Accept user queries.
  - Coordinate the selection of relevant URLs.
  - Scrape content and query the OpenAI LLM.
  - Display the final answer to the user.

### **2. `discover_subdomains.py`**

- **Purpose:** Discover all subdomains and subsites of the university website.
- **Responsibilities:**
  - Use DNS enumeration and web scraping techniques to find subdomains.
  - Save the list of subdomains to `subdomains.txt`.

### **3. `crawl_urls.py`**

- **Purpose:** Crawl each subdomain to extract all accessible URLs.
- **Responsibilities:**
  - Read subdomains from `subdomains.txt`.
  - Use a web crawler to find all URLs within each subdomain.
  - Save the list of URLs to `urls.txt`.

### **4. `generate_embeddings.py`**

- **Purpose:** Generate embeddings for the URLs to facilitate similarity searches.
- **Responsibilities:**
  - Read URLs from `urls.txt`.
  - Fetch page titles or meta descriptions.
  - Generate embeddings using OpenAI's Embedding API.
  - Save embeddings and corresponding URLs to `embeddings.pkl`.

### **5. `select_relevant_urls.py`**

- **Purpose:** Select the most relevant URLs based on the user's query.
- **Responsibilities:**
  - Generate an embedding for the user's query.
  - Compare the query embedding with URL embeddings.
  - Return the top N most relevant URLs.

### **6. `scrape_content.py`**

- **Purpose:** Scrape and clean content from the selected URLs.
- **Responsibilities:**
  - Fetch HTML content from each URL.
  - Parse and extract meaningful text.
  - Clean and preprocess the text for input to the LLM.

### **7. `query_llm.py`**

- **Purpose:** Interact with the OpenAI LLM to get the answer.
- **Responsibilities:**
  - Construct a prompt including the user's query and scraped content.
  - Send the prompt to the OpenAI API.
  - Handle the response and any potential errors.

### **8. `config.py`**

- **Purpose:** Store configuration settings and API keys.
- **Responsibilities:**
  - Define constants such as the university domain and API keys.
  - Manage parameters like the number of URLs to select.

### **9. `requirements.txt`**

- **Purpose:** Specify all Python dependencies.
- **Responsibilities:**
  - List libraries such as `requests`, `beautifulsoup4`, `openai`, etc.

### **10. `utils.py`**

- **Purpose:** Provide utility functions used across multiple modules.
- **Responsibilities:**
  - Functions for text cleaning, embedding calculations, and error handling.

### **11. `README.md`**

- **Purpose:** Documentation for setting up and running the application.
- **Responsibilities:**
  - Installation instructions.
  - Usage guidelines.
  - Troubleshooting tips.

### **12. `LICENSE`**

- **Purpose:** Define the legal terms for using and distributing the application.
- **Responsibilities:**
  - Specify the software license (e.g., MIT, GPL).

---

## Detailed Implementation

### **1. Subdomain and Subsite Discovery**

#### **File:** `discover_subdomains.py`

- **Functionality:**
  - Use tools like `Sublist3r` or `Amass` to enumerate subdomains.
  - Implement DNS brute-forcing for comprehensive discovery.
- **Output:**
  - `subdomains.txt` containing all discovered subdomains.

### **2. Crawl URLs**

#### **File:** `crawl_urls.py`

- **Functionality:**
  - Read subdomains from `subdomains.txt`.
  - Use a crawler (e.g., `Scrapy`) to navigate each subdomain.
  - Extract all unique URLs.
- **Output:**
  - `urls.txt` containing all discovered URLs.

### **3. Generate Embeddings**

#### **File:** `generate_embeddings.py`

- **Functionality:**
  - Fetch titles or summaries of each URL for embedding.
  - Use OpenAI's Embedding API to generate embeddings.
  - Store embeddings and URLs in `embeddings.pkl` using `pickle`.
- **Output:**
  - `embeddings.pkl` for efficient retrieval during similarity search.

### **4. Select Relevant URLs**

#### **File:** `select_relevant_urls.py`

- **Functionality:**
  - Generate an embedding for the user's query.
  - Compute cosine similarity between the query and URL embeddings.
  - Select the top N URLs with the highest similarity scores.
- **Dependencies:**
  - `numpy` for numerical operations.
  - `sklearn.metrics.pairwise` for similarity calculations.

### **5. Scrape Content**

#### **File:** `scrape_content.py`

- **Functionality:**
  - Fetch HTML content using `requests` or `aiohttp`.
  - Parse HTML with `BeautifulSoup` to extract text.
  - Remove boilerplate content (navigation menus, footers).
  - Clean and preprocess text (remove extra whitespace, special characters).
- **Output:**
  - Consolidated text ready for inclusion in the LLM prompt.

### **6. Query LLM**

#### **File:** `query_llm.py`

- **Functionality:**
  - Construct a prompt that includes the user's query and scraped content.
  - Ensure the prompt stays within token limits (e.g., 4096 tokens for GPT-4).
  - Send the prompt to the OpenAI API using the `openai` library.
  - Handle API responses, including retries and error handling.
- **Output:**
  - The LLM's answer to the user's query.

### **7. Main Application**

#### **File:** `main.py`

- **Workflow:**
  1. **Input:** Prompt the user for their query.
  2. **URL Selection:** Call `select_relevant_urls.py` to find relevant URLs.
  3. **Content Scraping:** Use `scrape_content.py` to get the content.
  4. **Answer Generation:** Invoke `query_llm.py` to get the answer.
  5. **Output:** Display the answer to the user.

### **8. Configuration**

#### **File:** `config.py`

- **Settings:**
  - `API_KEY`: Your OpenAI API key.
  - `UNIVERSITY_DOMAIN`: The base domain of the university.
  - `NUM_URLS_TO_SELECT`: Number of top URLs to consider.
  - `MAX_TOKENS`: Token limit for the LLM prompt.

---

## Dependencies

**Include in `requirements.txt`:**

- `requests` (HTTP requests)
- `aiohttp` (Asynchronous HTTP requests)
- `beautifulsoup4` (HTML parsing)
- `openai` (OpenAI API interaction)
- `numpy` (Numerical computations)
- `scikit-learn` (Similarity calculations)
- `tqdm` (Progress bars)
- `pickle` (Object serialization)
- `python-dotenv` (Environment variables)
- `scrapy` (Web crawling)
- `dnspython` (DNS queries)

---

## Setup and Usage

### **1. Installation**

- **Clone the Repository:**

  ```bash
  git clone https://github.com/yourusername/university-query-app.git
  cd university-query-app
  ```

- **Install Dependencies:**

  ```bash
  pip install -r requirements.txt
  ```

- **Configure API Keys:**

  - Update `config.py` with your OpenAI API key or set it as an environment variable.

### **2. Initial Setup**

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

### **3. Running the Application**

- **Start the App:**

  ```bash
  python main.py
  ```

- **Enter User Query:**

  - Follow the on-screen prompt to input your query.

### **4. Application Flow**

1. **User Query Input:**
   - The application prompts the user for a query.
2. **Relevant URL Selection:**
   - `select_relevant_urls.py` processes the query to find relevant URLs.
3. **Content Scraping:**
   - `scrape_content.py` fetches and cleans content from the selected URLs.
4. **Answer Generation:**
   - `query_llm.py` sends the prompt to the OpenAI LLM and retrieves the answer.
5. **Display Answer:**
   - The application displays the LLM's response to the user.

---

## Additional Considerations

### **Error Handling**

- **Network Issues:**
  - Implement retries and timeouts for network requests.
- **API Rate Limits:**
  - Handle `429 Too Many Requests` errors by implementing exponential backoff.
- **Data Validation:**
  - Validate and sanitize user input to prevent injection attacks.

### **Performance Optimization**

- **Caching:**
  - Cache embeddings and scraped content to improve response times.
- **Asynchronous Operations:**
  - Use `asyncio` to perform network I/O concurrently.

### **Compliance and Ethics**

- **Respect `robots.txt`:**
  - Before crawling, check the site's `robots.txt` file for permissions.
- **Terms of Service:**
  - Ensure that scraping and data usage comply with the university's policies.
- **Data Privacy:**
  - Avoid scraping personal or sensitive information.

### **Scalability**

- **Modular Design:**
  - The application is divided into modules for ease of maintenance and scalability.
- **Logging:**
  - Implement logging to monitor application performance and errors.

### **Testing**

- **Unit Tests:**
  - Write tests for individual functions in each module.
- **Integration Tests:**
  - Test the entire application flow from query input to answer output.

---

## Example Usage

**User Query:**

```
"What are the admission requirements for the computer science master's program?"
```

**Application Steps:**

1. **Select Relevant URLs:**
   - Finds URLs related to admissions and computer science programs.
2. **Scrape Content:**
   - Extracts information from admissions pages.
3. **Generate Answer:**
   - The LLM composes an answer based on the latest scraped information.

**Sample Answer:**

```
"The admission requirements for the Master's program in Computer Science include a bachelor's degree in a related field, a minimum GPA of 3.0, GRE scores, letters of recommendation, and a statement of purpose. For detailed information, please visit the university's admissions page at [URL]."
```

---

## Conclusion

By following this plan and utilizing the outlined files, you can develop an efficient and scalable application that answers user queries using real-time data from a university website. The modular structure facilitates easy updates and maintenance, ensuring that users receive accurate and up-to-date information.

---

**Next Steps:**

- **Development:**
  - Begin coding each module as per the specifications.
- **Testing:**
  - Test each component individually before integrating.
- **Deployment:**
  - Deploy the application on a server or cloud platform for accessibility.

---

**Note:** Always ensure compliance with legal and ethical guidelines when scraping and using web content.