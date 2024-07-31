
def test_find_shortest_path_no_route(client):
    response = client.get("/cities/SoDo/findShortestPath?target_city=Renton")
    assert response.status_code == 404
    assert response.json() == {"detail": "City not found"}
