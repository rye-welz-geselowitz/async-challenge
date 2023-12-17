import requests
from bs4 import BeautifulSoup
from typing import Set, List, Optional
from dataclasses import dataclass 
from bs4.element import Tag

EXCLUDED_TERMS = {'Main_Page'}
MAX_LINKS = 50
MAX_DEPTH = 3 
MAX_CHILDREN = 2


@dataclass
class Tree:
    children: List['Tree']
    title: str
    url: str


def get_article_tree(search_term: str, visited: Optional[Set[str]] = None, depth: int=0) -> Tree:
    
    if visited is None:
        visited = set()

    url = f'https://en.wikipedia.org/wiki/{search_term}'

    tree = Tree(title=search_term, children=[], url=url)

    visited.add(search_term)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    links: List[Tag] = soup.find_all("a") 

    child_count = 0 
    for link in links:
        if len(visited) <= MAX_LINKS and child_count < MAX_CHILDREN: 
            href = link.get("href")
            if href:
                assert type(href) == str
                if href.startswith('/wiki/') and ':' not in href:
                    search_term = href.replace('/wiki/', '')
                    if (search_term not in visited) and (search_term not in EXCLUDED_TERMS) and depth < MAX_DEPTH:
                        child_tree = get_article_tree(search_term, visited, depth=depth+1)
                        tree.children.append(child_tree)
                        child_count +=1
    
    return tree
        

