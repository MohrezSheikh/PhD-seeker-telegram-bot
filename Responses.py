from datetime import datetime
import requests
from bs4 import BeautifulSoup as bs
import urllib3

def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ('hello', 'hi', 'sup'):
        return "Hey, How's it going? Give me a field of study!"

    if user_message in ('who are you', 'who are you?'):
        return "I am Ph.D. Seekr bot!"

    if user_message in ('time', 'time?'):
        now = datetime.now()
        date_time = now.strftime("%d/%m/%y, %H/%M/%S")

        return str(date_time)


    return "I don't understand you."


def scrape(input_field):
    msg = str(input_field).lower()

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    keywords = [f'{msg}']

    title_list = []
    country_list = []
    link_list = []

    fields = '+'.join([f"\"{item.replace(' ', '+')}\"" for item in keywords])
    config = {'scholarshipdb': {
        'url': 'https://scholarshipdb.net/scholarships/Program-PhD?page={page}&q={fields}',
        'title': 'h4 a', "country": '.list-unstyled a.text-success', 'link': ".list-unstyled h4 a",
        'dl': "https://scholarshipdb.net",
    },
        'findaphd': {
            'url': 'https://www.findaphd.com/phds/non-eu-students/?01w0&Keywords={fields}&PG={page}',
            'title': "h4 text-dark mx-0 mb-3",
            'country': "country-flag img-responsive phd-result__dept-inst--country-icon",
            'link': "h4 text-dark mx-0 mb-3",
            'dl': "https://www.findaphd.com"
        },
    }

    for i in ['scholarshipdb', 'findaphd']:  #
        for page in range(1, 2):
            url = config[i]['url'].format(fields=fields, page=page)
            response = requests.get(url, headers={'User-agent': 'your bot 0.1'}, verify=False)
            soup = bs(response.text, "html.parser")
            titles, countries, links = [soup.select(item) if i == 'scholarshipdb' else soup.find_all(class_=item)
                                        for item in (config[i]['title'], config[i]['country'], config[i]['link'])]
            for title, country, link in zip(titles, countries, links):
                title_list.append((title.text).strip().replace('"', ''))
                country_list.append(country.text if i == 'scholarshipdb' else country['title'])
                link_list.append(config[i]['dl'] + link['href'])



    # for i in range(0, len(link_list)):
    return link_list
