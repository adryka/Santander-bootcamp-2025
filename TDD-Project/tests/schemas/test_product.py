from pydantic import ValidationError
import pytest
from tests.factories import product_data
from tests.schemas.product import ProductIn


def test_schemas_return_success():
    data = product_data()
    product = ProductIn.model_validate(data)

    assert product.name == "Iphone 14 pro Max"

def test_schemas_return_raise():
    data = {"name": "Iphone 14 Pro Max", "quantity": 10, "price": 8.500}

    with pytest.raises(ValidationError) as err:
        ProductIn.model_validate(data)

    assert err.value.errors() [0] == {
        "type": "missing",
        "loc": ("status",),
        "msg": "Field required",
        "input": {"name": "Iphone 14 Pro Ma", "quantity": 10, "price": 8.5},
        "url": "https://errors.pydantic.dev/2.5/v/missing",
    
    }