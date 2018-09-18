# SongScore API
Learning Python/Flask by creating a website to rate songs. Currently hosted at [songscore.herokuapp.com](songscore.herokuapp.com)

## REST endpoints
Most rest endpoints are plurals, e.g. users not user.
The endpoints have a prefix of `/api/v1`.
Example: `/api/v1/users/1/following/2`

| Method | Endpoint | Meaning
| --- | --- | ---
| GET | /auth | get token
| GET | /feeds/:id | get that user's feed
| GET | /users/:id | get the user with that id
| GET | /users?username=:name | get user with that username
| POST | /users | add a new user
| GET | /users/:id/reviews | get that user's reviews
| GET | /reviews | get all the reviews
| GET | /reviews/:id | get a the review with that id
| DELETE | /reviews/:id | delete that review
| POST | /reviews/:id/comments | add a comment to that review
| POST | /reviews/:id/likes | like that review
| POST | /reviews/:id/dislikes | dislike that review
| GET | /users/:id/followers | all the people follow that user
| GET | /users/:id/following | all the people that user is following
| POST | /users/:id/following/:id | make id 1 follow id 2
| DELETE | /users/:id/following/:id | make id 1 unfollow id 2

## Environment variables
```
export DATABASE_URL=postgres://<username>:<password>@<host>:<port>/<databasename>
export FLASK_APP=songscore_api
export FLASK_DEBUG=true
export SECRET_KEY='secret key here'
```

## Import requirements
see `requirements.txt`
