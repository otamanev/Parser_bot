from pydantic import BaseModel, model_validator


class Item(BaseModel):
    id: int
    brand: str
    name: str
    salePriceU: float
    priceU: float
    pics: int
    image_links: str = None


@model_validator(mode='before')
def convert_sale_prise(cls, values):
    sale_price = values.get('salePriceU')
    if sale_price is not None:
        values['salePriceU'] = sale_price / 100
    return values


class Items(BaseModel):
    products: list[Item]
