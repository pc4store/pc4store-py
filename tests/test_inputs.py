import random
from uuid import uuid4

import pytest

from tests.utils.fixtures import rand_str
from pc4store.data import CreateOrderInput
from tests.data import min_dict_input, full_dict_input


@pytest.mark.usefixtures(min_dict_input.__name__)
def test_min_required_input(min_dict_input):
    input_obj = CreateOrderInput.from_dict(min_dict_input)
    assert isinstance(input_obj, CreateOrderInput)


@pytest.mark.usefixtures(full_dict_input.__name__)
def test_full_dict_input(full_dict_input):
    input_obj = CreateOrderInput.from_dict(full_dict_input)
    assert isinstance(input_obj, CreateOrderInput)


@pytest.mark.usefixtures(min_dict_input.__name__)
def test_missing_required_field(min_dict_input):
    del min_dict_input[random.choice(list(min_dict_input))]
    with pytest.raises(AssertionError) as e:
        CreateOrderInput.from_dict(min_dict_input)
    assert 'Missing required field' in str(e.value)


@pytest.mark.usefixtures(full_dict_input.__name__)
def test_unexpected_field(full_dict_input):
    full_dict_input[str(uuid4())] = rand_str()
    with pytest.raises(AssertionError) as e:
        CreateOrderInput.from_dict(full_dict_input)
    assert 'Got unexpected params:' in str(e.value)
