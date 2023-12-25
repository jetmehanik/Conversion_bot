import requests
import json
from config import keys, api_conversion

class ConversionException(Exception):
    pass

class CryptoConversion:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
 #       quote_ticker = keys[quote]
 #       base_ticker = keys[base]
        if quote == base:
            raise ConversionException('Валюты совпадают')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionException(f'Не удалось обработать валюту {base}')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConversionException(f'Не удалось обработать валюту {quote}')
        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f'Не удалось обработать количество монет {amount}')
        r = requests.get(f'https://api.freecurrencyapi.com/v1/latest?apikey={api_conversion}&base_currency={base}&currencies={quote}')
        total_base = json.loads(r.content)
        total_base = total_base.get('data')
        total_base = total_base.get(f'{quote}')
        return total_base