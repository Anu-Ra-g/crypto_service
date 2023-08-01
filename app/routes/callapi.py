from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from .. import utils, models, database
import time

session = Session()

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start': '1',
    'limit': '500',
    'convert': 'USD'
    }
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '379636da-1e76-4bb3-8931-abc483b887c6',
    }

def retrieve_cryptDetails(db):
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)

        gdata = json.loads(response.text)  # converting response into dict
      
        gen_list = utils.extract_crypto_details(gdata) # returns list of dictionaries containing the details of crypto

        for elem in gen_list:
            new_crypto = models.Crypto(**elem)
            db.add(new_crypto)
            db.commit()
            db.refresh(new_crypto)  
        
        print("Added Crypto details into database")
        
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def update_cryptDetails():

    from sqlalchemy.orm import Session

    db_session = Session(bind=database.engine)

    try:
        while True:
            retrieve_cryptDetails(db_session)

            time.sleep(60*10)   # crypto details updated every 15 minutes

            db_session.query(models.Crypto).delete()
            db_session.commit()

    except KeyboardInterrupt:
        pass

    finally:
        db_session.close()



