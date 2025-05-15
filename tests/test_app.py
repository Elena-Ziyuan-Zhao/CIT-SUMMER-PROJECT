# Functional Test 1: Homepage and All-Secrets page are accessible

def test_home_and_secrets_accessible(client):
    res_home = client.get("/")
    res_secrets = client.get("/secrets")
    assert res_home.status_code == 200
    assert res_secrets.status_code == 200

# Fucntional Test 2: User can post a secret to /profile/<id>/create
def test_post_secret(client):
    res = client.post("/profile/1/create", data={
        "title": "pytest title",
        "content": "pytest content"
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"pytest title" in res.data or b"pytest content" in res.data

# Functional Test 3: Each post should be assigned to a random anonymous name
def test_post_secret_has_fake_name(client):
    # Post a secret
    res = client.post("/profile/1/create", data={
        "title": "anonymous test",
        "content": "check fake name"
    }, follow_redirects=True)

    # Go to the secrets page and check if the secret is posted with an anonymous name
    res = client.get("/secrets")
    assert res.status_code == 200
    assert b"anonymous" in res.data.lower()
    assert b"testuser" not in res.data.lower()

# Functional Test 4: Submit a comment for a secret and check if it appears in the response
def test_add_comment(client):
    # Add a secret to comment
    client.post("/profile/1/create", data={"title": "WithComment", "content": "Let's test comments"}, follow_redirects=True)

    # Submit a comment
    res = client.post("/secrets/1", data={"comment": "This is great!"}, follow_redirects=True)
    assert res.status_code == 200
    assert b"this is great" in res.data.lower()

# Fuctional Test 5: Submit a rating and verify it is accepted and displayed
def test_add_rating(client):
    # Add a secret to rate
    client.post("/profile/1/create", data={"title": "RatingTest", "content": "Should be rated"}, follow_redirects=True)

    # Submit a rating
    res = client.post("/secrets/1", data={"rating": "4"}, follow_redirects=True)
    assert res.status_code == 200
    assert b"4" in res.data or b"rating" in res.data.lower()

# Functional Test 6: Submitting an invalid (non-integer) rating should not crash the app
def test_invalid_rating(client):
    # Add a secret to rate
    client.post("/profile/1/create", data={"title": "BadRating", "content": "Testing invalid rating"}, follow_redirects=True)

    # Submit a rating with string input
    res = client.post("/secrets/1", data={"rating": "bad_input"}, follow_redirects=True)
    assert res.status_code == 200
    assert b"error" not in res.data.lower() 

# Functional Test 7: Submitting a rating out of accepted range (not between 1 and 5) should be ignored
def test_out_of_range_rating(client):
    # Step 1: Create a new secret to rate
    client.post("/profile/1/create", data={"title": "OutOfRange", "content": "testing rating limits"}, follow_redirects=True)

    # Step 2: Submit a rating that is too high, like 6
    res_high = client.post("/secrets/1", data={"rating": "6"}, follow_redirects=True)
    assert res_high.status_code == 200
    assert b"6" not in res_high.data 

    # Step 3: Submit a rating that is too low, like -1
    res_low = client.post("/secrets/1", data={"rating": "-1"}, follow_redirects=True)
    assert res_low.status_code == 200
    assert b"-1" not in res_low.data 
