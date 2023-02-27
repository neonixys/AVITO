import pytest

from ads.serializers import AdListSerializer
from tests.factories import AdFactory
from tests.fixtures import user_token


@pytest.mark.django_db
def test_list_ad(client, user_token):
    ads = AdFactory.create_batch(3)

    response = client.get("/ad/", HTTP_AUTHORIZATION="Bearer " + user_token)
    assert response.status_code == 200
    assert response.data["results"] == AdListSerializer(ads, many=True).data
