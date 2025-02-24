from app.crud.city import get_city_by_name
from app.crud.connection import get_all_connections


def test_find_shortest_path_no_city(client, db_session):
    # Query param unknown city
    response = client.get(
        f'/cities/{get_city_by_name(db_session, "SoDo").id}/findShortestPath?target_city=12345'
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'Target city not found'}

    # Path param unknown city
    response = client.get(
        f'/cities/12345/findShortestPath?target_city={get_city_by_name(db_session, "Renton").id}'
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'City not found'}


def test_find_shortest_path(client, db_session):
    # Check that correct result returned
    renton = get_city_by_name(db_session, "Renton").id
    eastlake = get_city_by_name(db_session, "Eastlake").id
    issaquah = get_city_by_name(db_session, "Issaquah").id
    northup = get_city_by_name(db_session, "Northup").id
    redmond = get_city_by_name(db_session, "Redmond").id
    bellevue = get_city_by_name(db_session, "Bellevue").id
    sodo = get_city_by_name(db_session, "SoDo").id

    response = client.get(f'/cities/{renton}/findShortestPath?target_city={eastlake}')
    assert response.status_code == 200
    assert response.json() == {'city': 'Renton', 'result': {'distance': 15, 'targetCity': 'Eastlake'}}

    # Same for reversed
    response = client.get(f'/cities/{eastlake}/findShortestPath?target_city={renton}')
    assert response.status_code == 200
    assert response.json() == {'city': 'Eastlake', 'result': {'distance': 15, 'targetCity': 'Renton'}}

    # Other paths
    response = client.get(f'/cities/{issaquah}/findShortestPath?target_city={northup}')
    assert response.status_code == 200
    assert response.json() == {'city': 'Issaquah', 'result': {'distance': 13, 'targetCity': 'Northup'}}

    response = client.get(f'/cities/{redmond}/findShortestPath?target_city={eastlake}')
    assert response.status_code == 200
    assert response.json() == {'city': 'Redmond', 'result': {'distance': 13, 'targetCity': 'Eastlake'}}

    response = client.get(f'/cities/{bellevue}/findShortestPath?target_city={sodo}')
    assert response.status_code == 200
    assert response.json() == {'city': 'Bellevue', 'result': {'distance': 10, 'targetCity': 'SoDo'}}

    # Target city equals departure city
    response = client.get(f'/cities/{renton}/findShortestPath?target_city={renton}')
    assert response.status_code == 200
    assert response.json() == {'city': 'Renton', 'result': {'distance': 0, 'targetCity': 'Renton'}}


def test_city_creation(client):
    response = client.post(
        'cities',
        json={
            'name': 'Vladivostok'
        }
    )
    assert response.status_code == 201
    assert response.json() == {'id': 10, 'name': 'Vladivostok'}

    # Check cant create city with same name
    response = client.post(
        'cities',
        json={
            'name': 'Vladivostok'
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'City already exists or incorrect data provided'}


def test_cities_list(client):
    response = client.get('cities')
    assert response.status_code == 200
    print(response.json())
    assert response.json() == [
        {'name': 'Renton', 'id': 1},
        {'name': 'SoDo', 'id': 2},
        {'name': 'Factoria', 'id': 3},
        {'name': 'Issaquah', 'id': 4},
        {'name': 'Seattle', 'id': 5},
        {'name': 'Bellevue', 'id': 6},
        {'name': 'Redmond', 'id': 7},
        {'name': 'Eastlake', 'id': 8},
        {'name': 'Northup', 'id': 9}
    ]


def test_city_delete(client, db_session):
    connections_count_before = len(get_all_connections(db_session))

    response = client.get('cities/5/connections')
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = client.delete('cities/5')
    assert response.status_code == 204

    response = client.delete('cities/5')
    assert response.status_code == 404
    assert response.json() == {'detail': 'City not found'}

    print(len(get_all_connections(db_session)))
    assert len(get_all_connections(db_session)) == connections_count_before - 2

    response = client.get('cities/5')
    assert response.status_code == 404
    assert response.json() == {'detail': 'City not found'}


def test_city_detail(client):
    response = client.get('cities/5')
    assert response.status_code == 200
    assert response.json() == {'name': 'Seattle', 'id': 5}


def test_city_update(client):
    response = client.patch(
        'cities/5',
        json={
            'name': 'Vladivostok'
        }
    )
    assert response.status_code == 200
    assert response.json() == {'id': 5, 'name': 'Vladivostok'}

    response = client.patch(
        'cities/123321',
        json={
            'name': 'Vladivostok'
        }
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'City not found'}

    response = client.patch(
        'cities/5',
        json={
            'name': 'Vladivostok'
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Prodvided city name matches current name'}
