f"""---
layout: post
title: {title}
date: {datetime.date.today().strftime("%Y-%m-%d")}
categories: {", ".join(categories)}
---

### {authors}

Originally published on {date}.

Categories: {", ".join(categories)}  

Link: [{pdflink}]({pdflink})

### Abstract:
{abstract}

### Bibtex:
```
{bibtex}
```

---

### My reading



"""