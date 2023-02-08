from datetime import datetime

import pytest

from vacancies.models import Skill


@pytest.mark.django_db
def test_create_vacancy(client, hr_token):
    expected_response = {
        "id": 1,
        "created": datetime.now().strftime("%Y-%m-%d"),
        "skills": [],
        "slug": "123",
        "text": "123",
        "status": "draft",
        "min_experience": None,
        "likes": 0,
        "updated_at": None,
        "user": None
    }

    Skill.objects.create(name="test")
    data = {
        "slug": "123",
        "text": "123",
        "status": "draft"
    }
    response = client.post(
        "/vacancy/create/",
        data,
        content_type="application/json",
        HTTP_AUTHORIZATION="Token " + hr_token)

    assert response.status_code == 201
    assert response.data == expected_response


@pytest.mark.django_db
@pytest.mark.parametrize("status", ["closed"])
def test_vacancy_wrong_status(client, hr_token, status):
    data = {
        "slug": "test",
        "text": "test",
        "status": status,
    }

    response = client.post(
        "/vacancy/create/",
        data,
        content_type="application/json",
        HTTP_AUTHORIZATION="Token " + hr_token
    )

    assert response.status_code == 400
    assert response.json() == {'status': ['Incorrect status']}
