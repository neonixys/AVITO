import pytest
from tests.factories import AdFactory
from tests.fixtures import user_token


@pytest.mark.django_db
def test_selection_create(client, user_token, user):
    ad_list = AdFactory.create_batch(3)
    data = {
        "name": "Тестовая подборка",
        "author": user.pk,
        "items": [ad.pk for ad in ad_list]
    }

    expected_data = {
        "id": 1,
        "name": "Тестовая подборка",
        "author": user.pk,
        "items": [ad.pk for ad in ad_list]
    }

    response = client.post('/selection/', data, HTTP_AUTHORIZATION=f'Bearer {user_token}')
    assert response.status_code == 201
    assert response.data == expected_data
