from .constants import MONTH_MAP, WEEK_MAP, QUERY_URL
from datetime import datetime, date, timedelta
import calendar, requests, json



def get_food_list(query):

    foods = []
    if query != "":
        url = QUERY_URL.format(query)
        r = requests.get(url)
        response = json.loads(r.content)
        try:
            for f in response["hits"]:
                for k in f['fields'].keys():
                    if f['fields'][k] is None:
                        f['fields'][k] = 0
                    elif type(f['fields'][k]) is float:
                        f['fields'][k] = int(f['fields'][k])
                f['fields']['urlsafe_name'] = f['fields']['item_name'].replace("/", "%2F")
                f['fields']['urlsafe_brand'] = f['fields']['brand_name'].replace("/", "%2F")

                foods.append(f['fields'])
            error = 0
        except KeyError:
            error = response
    else:
        error = 0

    return foods, error
