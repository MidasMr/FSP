def test_find_shortest_path_no_city(client):
    # Query param unknown city
    response = client.get('/cities/SoDo/findShortestPath?target_city=SomeCity')
    assert response.status_code == 404
    assert response.json() == {'detail': 'City not found'}

    # Path param unknown city
    response = client.get('/cities/SomeCity/findShortestPath?target_city=SoDo')
    assert response.status_code == 404
    assert response.json() == {'detail': 'City not found'}


def test_find_shortest_path(client):
    # Check that correct result returned
    response = client.get('/cities/Renton/findShortestPath?target_city=Eastlake')
    assert response.status_code == 200
    assert response.json() == {'city': 'Renton', 'result': {'distance': 15, 'targetCity': 'Eastlake'}}

    # Same for reversed
    response = client.get('/cities/Eastlake/findShortestPath?target_city=Renton')
    assert response.status_code == 200
    assert response.json() == {'city': 'Eastlake', 'result': {'distance': 15, 'targetCity': 'Renton'}}

    # Other paths
    response = client.get('/cities/Issaquah/findShortestPath?target_city=Northup')
    assert response.status_code == 200
    assert response.json() == {'city': 'Issaquah', 'result': {'distance': 13, 'targetCity': 'Northup'}}

    response = client.get('/cities/Redmond/findShortestPath?target_city=Eastlake')
    assert response.status_code == 200
    assert response.json() == {'city': 'Redmond', 'result': {'distance': 13, 'targetCity': 'Eastlake'}}

    response = client.get('/cities/Bellevue/findShortestPath?target_city=SoDo')
    assert response.status_code == 200
    assert response.json() == {'city': 'Bellevue', 'result': {'distance': 10, 'targetCity': 'SoDo'}}

    # Target city equals departure city
    response = client.get('/cities/Renton/findShortestPath?target_city=Renton')
    assert response.status_code == 200
    assert response.json() == {'city': 'Renton', 'result': {'distance': 0, 'targetCity': 'Renton'}}


def test_find_shortest_path_case_insensitive(client):
    response = client.get('/cities/Bellevue/findShortestPath?target_city=SoDo')
    assert response.status_code == 200
    assert response.json() == {'city': 'Bellevue', 'result': {'distance': 10, 'targetCity': 'SoDo'}}

    response = client.get('/cities/BeLlEvUe/findShortestPath?target_city=SODO')
    assert response.status_code == 200
    assert response.json() == {'city': 'Bellevue', 'result': {'distance': 10, 'targetCity': 'SoDo'}}
