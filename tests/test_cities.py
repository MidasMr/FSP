from app.crud.city import get_city_by_name


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
    assert response.json() == {'detail': 'City already registered'}

    # # Check cant create city with same name in other case
    # response = client.post(
    #     'cities',
    #     json={
    #         'name': 'VlAdIvOsToK'
    #     }
    # )
    # assert response.status_code == 400
    # assert response.json() == {'detail': 'City already registered'}
