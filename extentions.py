import requests
import json
from token_keys import keys


class ConversionException(Exception):
    pass


class Converter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConversionException('Вы переводите одну и ту же валюту. Используйте рекомендуемый шаблон.\n<1ая валюта> <2ая валюта> <Количество>')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConversionException(f'Валюты "{quote}" нет в списке.\nСписок валют - /values')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionException(f'Валюты "{base}" нет в списке.\nСписок валют - /values')
        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException('Количество введено неверно. Используйте рекомендуемый шаблон.\n<1ая валюта> <2ая валюта> <Количество>')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base

