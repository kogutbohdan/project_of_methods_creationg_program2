from url_normalize import url_normalize
from urllib.parse import urlparse,urlunparse

def get_sentences_html(url,tree,tree_wrapper,chuncks):
    elements=["h1","h2","h3","p","a"]
    count=0
    i=0
    groups_by_chunks={
        chuncks[i]:{
            "texts":[],
            "urls":[],
            "names":[]
        }
    }
    for elem in elements:
        for tag in tree.xpath(f"//{elem}"):
            text="".join(tag.itertext()).strip()
            count_words=len(text.split())
            if text:
                count+=count_words
                groups_by_chunks[chuncks[i]]["texts"].append(text)
                groups_by_chunks[chuncks[i]]["names"].append(text)
                xpath=tree_wrapper.getpath(tag)
                groups_by_chunks[chuncks[i]]["urls"].append(f"{url}?xpath={xpath}")
            if count>=300:
                i+=1
                count=0
                groups_by_chunks[chuncks[i]]={
                    "texts":[],
                    "urls":[],
                    "names":[]
                }
    return groups_by_chunks

def get_chuncks_html(tree):
    text=tree.text_content().strip()
    words=text.split()
    len_w=len(words)
    chuncks=[]
    for i in range(0,len_w,300):
        k=i+300
        if k>len_w:k=i+(len_w-i)
        chuncks.append(" ".join(words[i:k]))
    return chuncks

def urlnormilize(url):
    url=url_normalize(url)
    parse=urlparse(url)
    parse=parse._replace(scheme="https",netloc=parse.netloc.replace("www.",""))
    return urlunparse(parse)
