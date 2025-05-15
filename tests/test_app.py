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
#Fuctional Test 6: User can delete their posted secret
def test_delete_secret(client):
    # Post a secret first
    client.post("/profile/1/create", data={"title": "ToDelete", "content": "This will be deleted"}, follow_redirects=True)
    
    # Attempt to delete the secret
    res = client.post("/secret/1/delete", follow_redirects=True)

    # Ensure secret is removed from profile page
    assert res.status_code == 200
    assert b"This will be deleted" not in res.data
#Fuctional Test 7: User can edit a secret
def test_edit_secret(client):
    # Post a secret to edit
    client.post("/profile/1/create", data={"title": "EditMe", "content": "Old content"}, follow_redirects=True)

    # Edit the secret
    res = client.post("/secret/1/edit", data={"title": "Edited", "content": "New content"}, follow_redirects=True)

    # Confirm changes are reflected
    assert res.status_code == 200
    assert b"New content" in res.data
    assert b"Old content" not in res.data
# Functional Test 8: Timer-based expiry 
def test_expiry_timer(client):
    # Post a secret with a 1-minute expiry
    client.post("/profile/1/create", data={
        "title": "Expiring",
        "content": "This will expire",
        "hour": "0",
        "minutes": "1"
    }, follow_redirects=True)

    # Check if secret appears initially
    res = client.get("/secrets")
    assert res.status_code == 200
    assert b"This will expire" in res.data
#Functional Test 9: Login is required to access protected pages
def test_login_required_redirects(client):
    # Simulate logout by clearing session
    with client.session_transaction() as sess:
        sess.clear()

    # Try to access /secrets which requires login
    res = client.get("/secrets")
    
    # Should be redirected to login
    assert res.status_code == 302
# Functional Test 10: def test_sort_options(client):
def test_sort_options(client):
    # Post multiple secrets
    client.post("/profile/1/create", data={"title": "Secret1", "content": "Secret A"}, follow_redirects=True)
    client.post("/profile/1/create", data={"title": "Secret2", "content": "Secret B"}, follow_redirects=True)

    # Try different sort options
    for sort in ["spicy", "created-date", "expiry-date"]:
        res = client.get(f"/secrets?sort={sort}")
        assert res.status_code == 200
        assert b"Secret" in res.data
