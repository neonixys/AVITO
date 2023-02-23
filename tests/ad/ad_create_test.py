import pytest


@pytest.mark.django_db
def test_create_ad(client, user, category, user_token):
    print(user.id)
    data = {
        "name": "New advertising",
        "price": 10,
        "description": "test advertising description",
        "is_published": False,
        "author": user.id,
        "category": category.id,
    }

    response = client.post(
        "/ad/create/", data=data, HTTP_AUTHORIZATION="Bearer " + user_token
    )

    assert response.status_code == 201
    # assert response.data["author"] == user.id
    # assert response.data["category"] == category.id
    # data = {
    #     "author": user.pk,
    #     "category": category.pk,
    #     "name": "Super car(used)",
    #     "price": 1000000,
    #     "address": "Vidone city"
    # }
    #
    # expected_data = {
    #         "id": 1,
    #         "is_published": False,
    #         "name": "Super car(used)",
    #         "price": 1000000,
    #
    #         "address": "Vidone city",
    #
    #         "author": user.pk,
    #         "category": category.pk
    #     }
    # response = client.post("/ad/", data, HTTP_AUTHORIZATION="Bearer " + user_token)
    #
    # assert response.status_code == 201
    # assert response.data == expected_data
    # # assert response.data["category"] == category.id
