f"""---
layout: post
title: A reading of {title}
date: {datetime.date.today().strftime("%Y-%m-%d")}
categories: {", ".join(categories)}
---

## {title}

###{authors}

Originally published on {date}

Categories: {", ".join(categories)}  

Link: [{pdflink}]({pdflink})

### Abstract:
{abstract}

### Bibtex:
```
{bibtex}
```

---

# My reading



"""