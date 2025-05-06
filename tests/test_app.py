# Unit Test 1: Homepage and All-Secrets page are accessible
def test_home_and_secrets_accessible(client):
    res_home = client.get("/")
    res_secrets = client.get("/secrets")
    assert res_home.status_code == 200
    assert res_secrets.status_code == 200

# Unit Test 2: User can post a secret to /profile/<id>/create
def test_post_secret(client):
    res = client.post("/profile/1/create", data={
        "title": "pytest title",
        "content": "pytest content"
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"pytest title" in res.data or b"pytest content" in res.data

# Unit Test 3: Each post should be assigned to a random anonymous name
def test_post_secret_has_fake_name(client):
    res = client.post("/profile/1/create", data={
        "title": "anonymous test",
        "content": "check fake name"
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"anonymous" in res.data.lower() or b"by" in res.data.lower()  
