# scout

https://github.com/shiv248/Streamlit-x-LangGraph-Cookbooks


## Loading spinners

https://changelog.com/news/a-collection-of-free-svg-loading-spinners-AX0y


## Risk assessment

Consult the general activities guidance https://www.scouts.org.uk/volunteers/running-your-section/programme-guidance/information-for-volunteers/general-activity-guidance/

- scrape the guidance page
- grab all links
- ask llm which are relevant, treat links as documents (title, link), alternative to embedding, near real time
- scrap relevant pages using links
- summarise

- Consult activities POR https://www.scouts.org.uk/por/9-activities/

- scrape the page
- use this as a consideration

Feed both of these into a risk assessment.

- UI should have a box with CONSIDERATIONS, with attributed links to docs, POR etc


# Search

- Force to use RAG docs, not weights
- Potential to re-write search term using llm knowledge of scouts, or info gained from RAG e.g. relevant related items mentioned (using separate llm call)
- Search using DuckDuckGo + relevant RAG strategy
- Need to be able to parse websites, possibly also scraping links in the page (specify depth)
- Attribute the search via markdown links - users should be able to click!