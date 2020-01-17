# Casting Agency

## Specifications
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

- Models:
   - Movies with attributes title and release date
   - Actors with attributes name, age and gender
- Endpoints:
   - GET /actors and /movies
   - DELETE /actors/ and /movies/
   - POST /actors and /movies and
   - PATCH /actors/ and /movies/
- Roles:
   - Casting Assistant
      - Can view actors and movies
   - Casting Director
      - All permissions a Casting Assistant has and…
      - Add or delete an actor from the database
      - Modify actors or movies
   - Executive Producer
      - All permissions a Casting Director has and…
      - Add or delete a movie from the database
- Tests:
   - One test for success behavior of each endpoint
   - One test for error behavior of each endpoint
   - At least two tests of RBAC for each role

## Development Process
### Flask App
- models.py
- api.py
- auth.py

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:actors`, `get:movies`
    - `post:actors`, `post:movies`
    - `patch:actors`, `patch:movies`
    - `delete:actors`, `delete:movies`
6. Create new roles for:
    - Assistant
        - can `get:actors`, `get:movies`
    - Director
        - can `get:actors`, `get:movies`, `post:actors`, `delete:actors`, `patch:actors`, `patch:movies`
        - cannot `post:movies`, `delete:movies`
    - Producer
        - can perform all actions

### Unittesting
 - Test your endpoints with [Postman](https://getpostman.com). 
    - Register 3 users for each roles.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `unittests.postman_collection.json`
    - Right-clicking the collection folder for each roles, navigate to the authorization tab, and including the JWT in the token field.
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!
