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
    assert response.json() == {
        'id': 15,
        'from_city_id': 1,
        'to_city_id': 5,
        'distance': 1
    }

    # Cant create connection to same city
    response = client.post(
        'connections',
        json={
            'from_city_id': 1,
            'to_city_id': 1,
            'distance': 1
        }
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'Connection cannot be created between one city'}

    # Cant create duplicate connection
    # response = client.post(
    #     'connections',
    #     json={
    #         'from_city_id': 1,
    #         'to_city_id': 5,
    #         'distance': 1
    #     }
    # )
    # assert response.status_code == 400

    # # Cant create connection with reverse citites order
    # response = client.post(
    #     'connections',
    #     json={
    #         'from_city_id': 5,
    #         'to_city_id': 1,
    #         'distance': 1
    #     }
    # )

    # assert response.status_code == 400


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

    # Add connections to intermediate citiy
    connection_1_3 = client.post(
        'connections',
        json={
            'from_city_id': response_1.json()["id"],
            'to_city_id': response_3.json()["id"],
            'distance': 300
        }
    )
    assert connection_1_3.status_code == 201

    connection_2_3 = client.post(
        'connections',
        json={
            'from_city_id': response_2.json()["id"],
            'to_city_id': response_3.json()["id"],
            'distance': 600
        }
    )
    assert connection_2_3.status_code == 201

    response = client.get(
        f'/cities/{response_1.json()["id"]}/findShortestPath?target_city={response_2.json()["id"]}'
    )
    assert response.status_code == 200
    assert response.json() == {'city': 'Vladivostok', 'result': {'distance': 900, 'targetCity': 'Khabarovsk'}}

    response = client.get(
        f'/cities/{response_2.json()["id"]}/findShortestPath?target_city={response_1.json()["id"]}'
    )
    assert response.status_code == 200
    assert response.json() == {'city': 'Khabarovsk', 'result': {'distance': 900, 'targetCity': 'Vladivostok'}}

    # Add straight connection to target city
    connection_1_2 = client.post(
        'connections',
        json={
            'from_city_id': response_1.json()["id"],
            'to_city_id': response_2.json()["id"],
            'distance': 800
        }
    )
    assert connection_1_2.status_code == 201

    response = client.get(
        f'/cities/{response_1.json()["id"]}/findShortestPath?target_city={response_2.json()["id"]}'
    )
    assert response.status_code == 200
    assert response.json() == {'city': 'Vladivostok', 'result': {'distance': 800, 'targetCity': 'Khabarovsk'}}

def test_create_connection_nested_to_city(client, db_session):
    response = client.post(
        f'cities/{get_city_by_name(db_session, "SoDo").id}/connections',
        json={
            'to_city_id': get_city_by_name(db_session, "Issaquah").id,
            'distance': 10 
        }
    )

    assert response.status_code == 201
    assert response.json() == {
        'id': 15,
        'from_city_id': 2,
        'to_city_id': 4,
        'distance': 10
    }


def test_get_connections_for_city(client, db_session):
    response = client.get(
        f'cities/{get_city_by_name(db_session, "Seattle").id}/connections'
    )

    json_response = response.json()
    assert response.status_code == 200
    assert len(json_response) == 2
    assert json_response == [
        {'from_city_id': 2, 'to_city_id': 5, 'distance': 1, 'id': 5},
        {'from_city_id': 5, 'to_city_id': 8, 'distance': 2, 'id': 10},
    ]


def test_get_all_connections(client):
    response = client.get(
        'connections'
    )
    json_response = response.json()
    assert response.status_code == 200
    assert len(json_response) == 14

    assert json_response[0] == {
        'id': 1,
        'from_city_id': 1,
        'to_city_id': 2,
        'distance': 12
    }

    assert json_response[-1] == {
        'id': 14,
        'from_city_id': 9,
        'to_city_id': 7,
        'distance': 5
    }


def test_connection_delete(client):
    response = client.delete(
        'connections/1'
    )
    assert response.status_code == 204

    response = client.get(
        'connections'
    )
    assert response.status_code == 200
    assert len(response.json()) == 13


def test_nested_city_connection_delete(client, db_session):
    connections_before = client.get(
        f'cities/{get_city_by_name(db_session, "Seattle").id}/connections'
    )

    assert len(connections_before.json()) == 2

    connections_before_json = connections_before.json()

    assert connections_before_json == [
        {'from_city_id': 2, 'to_city_id': 5, 'distance': 1, 'id': 5},
        {'from_city_id': 5, 'to_city_id': 8, 'distance': 2, 'id': 10},
    ]

    response = client.delete(
        'connections/5'
    )
    assert response.status_code == 204

    response = client.get(
        f'cities/{get_city_by_name(db_session, "Seattle").id}/connections'
    )
    assert response.status_code == 200
    assert len(response.json()) == 1

    assert response.json() == [
        {'from_city_id': 5, 'to_city_id': 8, 'distance': 2, 'id': 10},
    ]
