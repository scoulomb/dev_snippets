import random
import string

N = 10

CF_NUM = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))# seems to be unique, if not use uuid
YEAR_LIST = [2012, 2013, 2014]
FIRST_NAME_LIST = ['SYLVAIN', 'PIERRE', 'PAUL', 'JACQUES', 'MATHIEU', 'JEAN', 'NICOLAS', 'FRANCOIS', 'MANUEL']
COMMENTS_LIST = ["non smoking", "sea view", "VIP customer"]
CITY_CODE_LIST = ["PEK", "SHA", "PAR", "LPI", "LCY", "REO", "BOS", "NCE"]
MAIL_PROVIDER_LIST = ["gmail.com", "aol.com", "hotmail.com", "hp.com", "laposte.net", "yahoo.xom", "lycos.fr"]
CURRENCY_LIST = ["Euro", "US Dollard"] 

class ValueGen(object):

    
    def makeValue(self):   
    
       
        YEAR = YEAR_LIST[random.randint(0,len(YEAR_LIST)-1)]
        FIRST_NAME = FIRST_NAME_LIST[random.randint(0,len(FIRST_NAME_LIST)-1)]
        COMMENT = COMMENTS_LIST[random.randint(0,len(COMMENTS_LIST)-1)]
        CITY = CITY_CODE_LIST[random.randint(0,len(CITY_CODE_LIST)-1)]
        MAIL_PROVIDER = MAIL_PROVIDER_LIST[random.randint(0,len(MAIL_PROVIDER_LIST)-1)]
        CURRENCY = CURRENCY_LIST[random.randint(0,len(CURRENCY_LIST)-1)]
        
        booking = {
                
                    "CF_NUM": CF_NUM,
                    "YEAR": YEAR,
                    "FIRST_NAME": FIRST_NAME,
                    "COMMENT": COMMENT,
                    "CITY": CITY,
                    "MAIL_PROVIDER": MAIL_PROVIDER,
                    "Currency":CURRENCY
                    
                }
        
        return booking;


