from url_normalize import url_normalize
from urllib.parse import urlparse,urlunparse
import re


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

def creat_chucnks(text,number_split=300):
    words=text.split()
    len_w=len(words)
    chuncks=[]
    for i in range(0,len_w,number_split):
        k=i+number_split
        if k>len_w:k=i+(len_w-i)
        chuncks.append(" ".join(words[i:k]))
    return chuncks

def get_chuncks_html(tree):
    text=tree.text_content().strip()
    return creat_chucnks(text)
 

def get_chuncks_pdf(pagas):
    page_text=""
    numbers_page=[]
    i=0
    for page in pagas:
        page_text+=page.extract_text()
        sentences=creat_chucnks(page.extract_text(),10)
        for sentence in sentences:
            numbers_page.append([sentence,page.page_number])
        if i>=20:
            break
        i+=1
    return creat_chucnks(page_text),numbers_page

def get_sentences_pdf(pages,url,chuncks):
    index=0
    count=0
    group_by_chunks={
        chuncks[0][index]:{
            "texts":[],
            "urls":[],
            "names":[]
        }
    }
    
    for sentence in chuncks[1]:
        group_by_chunks[chuncks[0][index]]["texts"].append(sentence[0])
        group_by_chunks[chuncks[0][index]]["names"].append(f"{sentence[0]}...")
        group_by_chunks[chuncks[0][index]]["urls"].append(f"{url}#page={sentence[1]}")
        count+=len(sentence)
        if count>=300:
            index+=1
            count=0
            print(index)
            if index>=len(chuncks[0]):break
            group_by_chunks[chuncks[0][index]]={
                "texts":[],
                "urls":[],
                "names":[]
            }

    
    
    return group_by_chunks

def urlnormilize(url):
    url=url_normalize(url)
    parse=urlparse(url)
    parse=parse._replace(scheme="https",netloc=parse.netloc.replace("www.",""))
    return urlunparse(parse)
