import re
from django.shortcuts import redirect,render
from news.models import Headline

def scrape(request):
    session=request.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    url = "https://www.timesofindia.indiatimes.com/"
    content=session .get(url,verify=False).content
    News = re.find_all('div', {"class":" Headline"})
    for article in News:
        main = article.find_all('a')[0]
        link = main['href']
        image_src = str(main.find('img')['srcset']).split(" ")[-4]
        title = main['title']
        new_headline = Headline()
        new_headline.title= title
        new_headline.url = link
        new_headline.image = image_src
        new_headline.save()
    return redirect("../")

def news_list(request):
    headlines = Headline.objects.all()[::-1]
    context = {
        'object_list': headlines,
    }
    return render(request, 'home.html', {'context':context})

