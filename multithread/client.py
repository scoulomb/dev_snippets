import json
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict

from chrono.chrono import with_chrono
from mywikipedia import wikipedia
# if call rename parallel_map to multithread we have a conflict issue and import error!
from parallel_map.parallel_map import parallel_map


@dataclass
class ArticleSummary:
    article_name: str
    article_content: str
    retrieve_date: str

    def as_json_string(self): # ArticleSummary -> str
        # https://docs.python.org/fr/3/library/json.html
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    def as_json_dict(self): # ArticleSummary -> str -> dict
        # https://docs.python.org/fr/3/library/json.html
        return json.loads(self.as_json_string())


# Loop version
@with_chrono
def get_all_summaries_for_a_search_loop(search_query: str) -> List[ArticleSummary]:
    article_list: List[str] = wikipedia.search(search_query)

    def _fetch_article(article_name: str) -> ArticleSummary:
        return ArticleSummary(article_name, wikipedia.summary(article_name),
                              datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

    pool_objects: List[ArticleSummary] = []
    for item in article_list:
        pool_objects.append(_fetch_article(item))

    return pool_objects


def reminder():
    def my_function(a):
        print(a)

    my_function("test")
    # https://www.w3schools.com/python/ref_func_map.asp
    x = map(my_function, ['apple', 'banana', 'cherry'])
    list(x)  # to iterate


# Map version
@with_chrono
def get_all_summaries_for_a_search_map(search_query: str) -> List[ArticleSummary]:
    article_list: List[str] = wikipedia.search(search_query)

    def _fetch_article(article_name: str) -> ArticleSummary:
        return ArticleSummary(article_name, wikipedia.summary(article_name),
                              datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

    pool_objects = list(map(_fetch_article, article_list))
    return pool_objects


# MT Map version
@with_chrono
def get_all_summaries_for_a_search_parallel_map(search_query: str) -> List[ArticleSummary]:
    article_list: List[str] = wikipedia.search(search_query)

    def _fetch_article(article_name: str) -> ArticleSummary:
        return ArticleSummary(article_name, wikipedia.summary(article_name),
                              datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

    pool_objects = list(parallel_map(_fetch_article, article_list))
    return pool_objects


def article_summaries_to_dict(article_summaries: List[ArticleSummary]) -> Dict[str, str]:
    print(len(article_summaries))
    return list([article.as_json_dict() for article in article_summaries])


if __name__ == "__main__":

    print("=============== Version Parallel Map ===================")
    print(article_summaries_to_dict(get_all_summaries_for_a_search_parallel_map("covid19")))

    print("=============== Version loop ====================")
    print(article_summaries_to_dict(get_all_summaries_for_a_search_loop("covid19")))

    print("=============== Version Map ======================")
    print(article_summaries_to_dict(get_all_summaries_for_a_search_map("covid19")))

    # Note: Some diff but article of equal size

