import requests
from bs4 import BeautifulSoup as bs
import re

from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import RequestedURL, URLResults


class IndexView(generic.ListView):
    template_name = 'test_task_app/index.html'
    context_object_name = 'latest_url_list'

    def get_queryset(self):
        urls = RequestedURL.objects.all()
        results = URLResults.objects.all()
        for url in urls:
            if url.is_ready():
                result = URLResults()
                result.requested_url = url
                result.info = parse_url(url.url_name)
                result.pub_date = timezone.now()
                result.save()
            else:
                results.filter(requested_url=url).delete()  # Не создавать запись при увеличении задержки
        
        results = URLResults.objects.all()
        return results
    
def parse_url(url):
    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                             '(KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
    info = ''
    session = requests.Session()
    try:
        request = session.get(url, headers=headers)
        if request.status_code == 200:
            soup = bs(request.content, 'html.parser')
            title = soup.find('title').text
            headers1 = soup.find_all('h1')
            encod = soup.meta.get('charset')
            if title:
                info += ('title: ' + title + '\n')
            else:
                info += 'Невозможно получить title\n'
            if len(headers1) > 0:
                for h in headers1:
                    info += ('header1: ' + h.text + '\n')
            else:
                info += 'Невозможно получить h1\n'
            if encod is None:
                encod = soup.meta.get('content-type')
                if encod is None:
                    content = soup.meta.get('content')
                    match = re.search('charset=(.*)', content)
                    if match:
                        encod = match.group(1)
                    else:
                        encod = 'Невозможно получить кодировку'
            info += ('encod: ' + encod)
        else:
            info += 'Сервер не отвечает'
    except:
        return info

    return info
