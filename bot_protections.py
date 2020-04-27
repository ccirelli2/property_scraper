import random

'https://oxylabs.io/blog/5-key-http-headers-for-web-scraping'


def generate_ran_headers():
    
    # List of Referers
    Referer = ['http://www.google.com/', 'https://www.realtor.com/realestateandhomes-search/', 
            'https://www.trulia.com/', 'https://www.redfin.com/', 'https://www.homes.com/', 
            'https://www.atlantafinehomes.com/eng', 'https://www.movoto.com/', 
            'https://www.coldwellbankerhomes.com/']
    
    encoding = ['br', 'gzip', 'deflate'] 

    # Generate random number from 0-3
    ref_randint = random.randint(0, 4)
    enc_randint = random.randint(0, 2)

    # Randomly Select Referer
    Referer = Referer[ref_randint]
    
    # Randomly select encoding
    encoding = encoding[enc_randint]

    # Build Header
    h = {  'Referer'        : '{}'.format(Referer),
           'Accept'        : "test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
           'Accept-Encoding':'{}'.format(encoding), 
           'Accept-Language':'en-gb', 
            'authority'     : 'www.zillow.com',
            'method'        : 'GET',
            'path'          : '/homes/',
            'scheme'        : 'https',
            'user-agent'    :
            '''
            Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)
            AppleWebKit/537.36 (KHTML, like Gecko)
            Chrome/61.0.3163.100 Safari/537.36'''
            }

    # Return header
    return h


   
