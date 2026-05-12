async def test_create_task(client_with_token):
    response = await client_with_token.post("/task", json={
        "title":"Gym",
        "description":"Go to gym with the buddies"
    })
    assert response.status_code == 201
    
async def test_get_all_tasks(client_with_token):
    response = await client_with_token.get(url="/task")
    assert response.status_code == 200
    
async def test_get_unreal_task(client_with_token):
    response = await client_with_token.get(url="/task/999")
    assert response.status_code == 404