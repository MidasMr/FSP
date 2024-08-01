from app.crud.city import get_city_by_name


def test_create_connections(client):
    response = client.post(
        'connections',
        json={
            'from_city_id': 1,
            'to_city_id': 5,
            'distance': 1
        }
    )

    assert response.status_code == 201
    assert response.json() == [
        {
            'id': 29,
            'from_city_id': 1,
            'to_city_id': 5,
            'distance': 1
        },
        {
            'id': 30,
            'from_city_id': 5,
            'to_city_id': 1,
            'distance': 1
        },
    ]


def test_connections_created_path_search(client):
    response_1 = client.post(
        'cities',
        json={
            'name': 'Vladivostok'
        }
    )
    assert response_1.status_code == 201

    response_2 = client.post(
        'cities',
        json={
            'name': 'Khabarovsk'
        }
    )
    assert response_2.status_code == 201

    response_3 = client.post(
        'cities',
        json={
            'name': 'Ussuriisk'
        }
    )
    assert response_3.status_code == 201

    response = client.get(
        f'/cities/{response_1.json()["id"]}/findShortestPath?target_city={response_2.json()["id"]}'
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'Path not found'}

    connection_1_2 = client(

    )

