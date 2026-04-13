from data.models import Bike, User


# Bikes endpoint returns 200 on an empty DB
async def test_get_bikes(client):
    response = await client.get("/bikes/")
    assert response.status_code == 200


# GET /bikes/ returns the correct number of bikes from the DB
async def test_get_bikes_returns_one_bike(client, test_db_session):
    bike = Bike(model="TestBike", battery=80, status="available")
    test_db_session.add(bike)
    await test_db_session.commit()

    response = await client.get("/bikes/")
    assert response.status_code == 200
    assert len(response.json()) == 1


# POST /bikes/ creates a bike and returns 201 with the generated id
async def test_create_bike(client):
    payload = {"model": "Speedo", "battery": 90, "status": "available"}
    response = await client.post("/bikes/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["model"] == "Speedo"
    assert "id" in data


# DELETE /bikes/{id} returns 404 when the bike doesn't exist
async def test_delete_bike_not_found(client):
    response = await client.delete("/bikes/9999")
    assert response.status_code == 404


# GET /bikes/?status= only returns bikes matching that status
async def test_filter_bikes_by_status(client, test_db_session):
    test_db_session.add(Bike(model="A", battery=80, status="available"))
    test_db_session.add(Bike(model="B", battery=50, status="rented"))
    await test_db_session.commit()

    response = await client.get("/bikes/?status=available")
    assert response.status_code == 200
    bikes = response.json()
    assert len(bikes) == 1
    assert bikes[0]["status"] == "available"


# POST /rentals/ creates a rental and marks the bike as "rented" in the DB
async def test_create_rental_success(client, test_db_session):
    bike = Bike(model="Fast", battery=80, status="available")
    user = User(username="bob", hashed_password="hashed", role="rider", is_active=True)
    test_db_session.add(bike)
    test_db_session.add(user)
    await test_db_session.commit()
    await test_db_session.refresh(bike)
    await test_db_session.refresh(user)

    payload = {"bike_battery": 80, "user_id": user.id, "bike_id": bike.id}
    response = await client.post("/rentals/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == user.id
    assert data["bike_id"] == bike.id

    # Verify the side effect: bike status must be updated in the DB
    await test_db_session.refresh(bike)
    assert bike.status == "rented"
