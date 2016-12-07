**NOTE:** This project is currently primarily a vehicle for my efforts to learn analytics in Python. But, these efforts need to have a framework, and *Custodial* is that framework. 


## Custodial
Software design today emphasized discoverability at the expense of legibility. Powerful search  features, in-situ alerting, and personalized recommendations have enhanced usability, but at the cost of losing a sense of the overall lay of the land. 

Custodial is a tool to enhance the legibility of browsing. It will watch your browsing history, recommend pages to bookmark, suggest categories for these bookmarks, and recommend changes to the categorization of current bookmarks. Mac and Chrome only to start. 


#### Project Phases
1. Create a naive Bookmarker: a process that will recommend urls to bookmark based on visit counts and timing, concurrence and length of time. 
2. Create a naive Organizer, a bookmark classifier based on overall text website similarity. This classifier will:
    - Cache website text
    - Compare a newly bookmarked site to an existing set of categories,
    - Recommend categories to add the site to, or prompt for a new category.
    - Display the categories
3. Use website text/similarity to improve bookmarker recommendations
4. Use url visit graph in bookmarker and organizer
5. Track adoption of recommendations and use it to improve recommendations  
