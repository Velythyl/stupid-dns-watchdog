f"""
---
layout: post
title: A reading of {title}
date: {datetime.date.today().strftime("%Y-%m-%d")}
categories: {", ".join(categories)}
---

# {title}
###{authors}
##### {date}
##### {", ".join(categories)}  
##### {pdflink}
### Abstract:
{abstract}

### Bibtex:
```
{bibtex}
```

# My reading

"""