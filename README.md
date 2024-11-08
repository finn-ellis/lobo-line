# LOBOLINE

Subject "App Contest Submission – LoboLine" to appcontest@unm.edu
https://appcontest.unm.edu/rules.html

LoboLine is an AI-powered application utilizing OpenAI's latest API to interact with natural language queries & results on ~4GB of data collected from University of New Mexico web pages (data not included in repo).

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


## PROPOSED TECHNICAL ASPECTS
### APIs
- OpenAI Text Embedding Ada 002 & GPT 4o mini
- LangChain Prompt Hub

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
Due to the high personal cost of making OpenAI API requests, please limit your requests.


# FUTURE IMPROVEMENTS
- Re-embed data with smaller chunk sizes & overlaps with "text-embedding-3-small" instead?
-- I wonder if smaller data chunks & a higher k-value on the retriever will improve results... quantity > quality when initial quality is low?


# Licensing

This project is licensed under the GNU General Public License - see the [LICENSE](LICENSE) file for details.