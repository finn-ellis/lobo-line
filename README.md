# LOBOLINE
LoboLine is an AI-powered application utilizing OpenAI's latest API to interact with natural language queries about UNM and return results on ~4GB of data collected from University of New Mexico web pages (data not included in repo).

## Team
 ### Finn Ellis (<finnellis@unm.edu>)
> I am a passionately inquisitve junior-level undergraduate student studying and teaching computer science. I was born and raised here in New Mexico. I've been interested in interactive simulation and game design for years. International Baccalaureate alumni.

## Examples
![Example 1](/example_images/LoboLineSC1.jpg "Prompt: What is the UNM CNM App Contest?")
![Example 2](/example_images/LoboLineSC4.jpg "Prompt: What is organic chemistry, and which organic chemistry classes does UNM offer?")
![Example 3](/example_images/LoboLineSC2.jpg "Prompt: Who is the President of UNM?")
![Example 4](/example_images/LoboLineSC3.jpg "Prompt: How can I schedule a SHAC appointment?")

# SCORING

## PURPOSE, AUDIENCE, FUNCTIONS, PATHWAY TO SATISFACTION
### Purpose
Provide new students with an easy, accessible tool to answer questions or grab information - a lot like a personal guide to adjusting to college life.

### Audience
LoboLine in its current form primarily benefits new students and people unfamiliar with the University of New Mexico. While it has a large database to draw from,
information is still limited and to knowledgeable researchers, a thorough search may produce more relevant results. Artificial intelligence is largely meant to aid people,
improve accessibility, and speed up existing tasks. LoboLine aims to do this.

### Functions
LoboLine's main function is to increase accessibility of information. People interact with information in various ways, and LoboLine collects this information
and centralizes it so it can be interacted with via natural language. It aims to reduce time spent sorting through information and give easy questions easy answers.

### Pathway to Satisfaction
LoboLine's ease of access is demonstrated by the simple text box and reply box design. This could be further simplified with a text message API.
The LLM model is prompted to return concise results based on data and formatted to make the answer easily readable.

## PROPOSED TECHNICAL ASPECTS
### APIs
- OpenAI Text Embedding Ada 002 & GPT 4o mini
- LangChain Prompt Hub
- Google Cloud for hosting demo

### Libraries
- React, *ReactDOM, styled-components, typewriter-effect*
- LangChain, *community*, *Chroma*, *OpenAI*
- BeautifulSoup4
- *asyncio, tqdm*

Include a prototype of the important screens within the application (i.e. using rapid-prototyping software such as Figma).
Also include an architecture diagram using an application such Visio, Lucidchart, Excalidraw, etc.

## SECURITY
Security is inherent. Prompts are anonymous and no user data is stored. All data used is publically available.

## PROTOTYPE
Due to the high personal cost of making OpenAI API requests, please limit your requests:

https://lobo-line-463950868880.us-west3.run.app/


# FUTURE IMPROVEMENTS
- Re-embed data with smaller chunk sizes & overlaps with "text-embedding-3-small" instead?
	- I wonder if smaller data chunks & a higher k-value on the retriever will improve results... quantity > quality when initial quality is low?
- Use SMS API to allow users to text the service

# Licensing

This project is licensed under the GNU General Public License - see the [LICENSE](LICENSE) file for details.