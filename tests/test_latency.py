import urllib.parse
import requests, json
from time import time

url = "http://fake-news-lab7.eba-ficycrcw.us-east-2.elasticbeanstalk.com/"

def latency_test(calls: int = 100, news: str) -> float:
    """calls the api with input news.
    # Returns prediction
    # Average latency is taken over number of calls"""

    time = list()
    par_dict = {'news': news}
    prediction = list()
    i = 0
    while True:
        if i >= len(calls):
            break
        begin = time()
        result = requests.get(f'{url}predict?{urllib.parse.urlencode(par_dict)}')
        time += [(time() - begin)*1000] # converting to ms
        prediction += [result.json().get('prediction')]
        

    avg_func = lambda l: sum(l) / len(l)
    print(f'mean predictions over {calls} calls: {avg_func(prediction)}')
    print(f'mean latency over {calls} calls: {avg_func(time)} ms')

    return avg_func(prediction), avg_func(time)

latency_test(news="Emperor of Mars has declared war on Earth.") # fake
latency_test(news="Messi leads argentina for the round of super 16") # expect: 0 (real)
latency_test(news="eBron James is best ever to touch a basketball!") # expect: 1 (fake)
latency_test(news="Elon Musk bought Google with 1$") # expect: 1 (fake