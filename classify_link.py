
from random import choice
from requests import exceptions as req_exc
from bs4 import BeautifulSoup
from lxml.html.clean import clean_html, Cleaner

user_agent_list = ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36']

domain = 'http://www.example.com'

def random_user_agent():
    agent = choice(user_agent_list)
    return {'User-Agent':agent}

def make_request(url):
    try:
        r = requests.get(url,headers=random_user_agent())
        return r
    except req_exc.InvalidURL as invalid_url:
        with open('Classification.csv','a',encoding='utf-8') as class_file:
            class_file.write('"{}","{}"\n'.format(url,'Invalid URL'))
    except req_exc.ConnectionError as conn_error:
        with open('Classification.csv','a',encoding='utf-8') as class_file:
            class_file.write('"{}","{}"\n'.format(url, 'Connection Error'))
    except req_exc.TooManyRedirects as too_many_redirects:
        with open('Classification.csv','a',encoding='utf-8') as class_file:
            class_file.write('"{}","{}"\n'.format(url, 'Too Many Redirects'))
    except req_exc.MissingSchema as missing_schema:
        with open('Classification.csv','a',encoding='utf-8') as class_file:
            class_file.write('"{}","{}"'.format(url,'Missing Schema'))
    except:
        pass

def generate_link_list(response,clean_html):
    url = response.url
    empty_link_list = []
    paragraphs_with_links = []
    soup = BeautifulSoup(clean_html,'html5lib')
    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        does_paragraph_have_link = paragraph.find('a')
        if does_paragraph_have_link != None:
            if 'http://www.example.com' in str(does_paragraph_have_link):
                paragraphs_with_links.append(paragraph)
    for paragraphs_with_link in paragraphs_with_links:
        paragraph_link = paragraphs_with_link.find('a')
        paragraph_text = paragraphs_with_link.get_text()
        link_text = paragraph_link.get_text()
        if len(str(paragraph_text)) > len(str(link_text)):
            with open('Classification.csv','a',encoding='utf-8') as class_file:
                class_file.write('"{}","{}"\n'.format(url,'Content'))
        else:
            with open('Classification.csv','a',encoding='utf-8') as class_file:
                class_file.write('"{}","{}"\n'.format(url,'Navigational'))



def clean_html(html):
    try:
        cleaner = Cleaner(page_structure=False, scripts=True, style=True,
                          remove_tags=['span', 'div', 'li', 'ul'],kill_tags=['img'])
        new_html = cleaner.clean_html(html)
        return new_html
    except:
        pass

def main():
    url_list = [line.rstrip() for line in open(r'urls.txt')]
    for url in url_list:
        try:
            response = requests.get(url)
            cleaned_html = clean_html(response.text)
            generate_link_list(response,cleaned_html)
        except:
            pass

main()

