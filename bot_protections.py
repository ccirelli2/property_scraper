import random

'https://oxylabs.io/blog/5-key-http-headers-for-web-scraping'


def generate_ran_headers():
    
    # List of Referers
    Referer = ['http://www.google.com/', 'https://www.realtor.com/realestateandhomes-search/', 
            'https://www.trulia.com/', 'https://www.redfin.com/', 'https://www.homes.com/', 
            'https://www.atlantafinehomes.com/eng', 'https://www.movoto.com/', 
            'https://www.coldwellbankerhomes.com/']
    
    encoding = ['br', 'gzip', 'deflate', 'sdch'] 

    # Generate random number from 0-3
    ref_randint = random.randint(0, 4)
    enc_randint = random.randint(0, 2)

    # Randomly Select Referer
    Referer = Referer[ref_randint]
    
    # Randomly select encoding
    encoding = encoding[enc_randint]

    # Build Header
    h = {  'Referer'        : '{}'.format(Referer),
           'Accept'         : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", 
           'Accept-Encoding':'{}'.format(encoding), 
           'Accept-Language':'en-GB, en;q=0.8, en-US;q=0.6,ml;q=0.4',
           'cache-control'  : 'max-age=0', 
           'upgrade-insecure-requests':'1', 
            'authority'     : 'www.zillow.com',
            'method'        : 'GET',
            'path'          : 'www.zillow.com/homes/',
            'scheme'        : 'https',
            'user-agent'    :
            '''
            Mozilla/5.0 (X11; Linux x86_64)
            AppleWebKit/537.36 (KHTML, like Gecko)
            Chrome/74.0.3729.131 Safari/537.36
            '''}

    # Return header
    return h


   
