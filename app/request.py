import urllib.request,json


base_url = 'http://quotes.stormconsultancy.co.uk/random.json'

def get_random_quote():
    
    with urllib.request.urlopen(base_url) as url:
        quote_data = url.read()
        quote_response = json.loads(quote_data)

    return quote_response
 