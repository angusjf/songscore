# SongScore API
Learning Python/Flask by creating a website to rate songs. Currently hosted at [songscore.herokuapp.com](songscore.herokuapp.com)

# environment variables
```
export DATABASE_URL=postgres://<username>:<password>@<host>:<port>/<databasename>
export FLASK_APP=songscore_api
export FLASK_DEBUG=true
export SECRET_KEY='secret key here'
```

# import requirements
see `requirements.txt`

# REST endpoints
Most rest endpoints are plurals, e.g. users not user.

| Method | Endpoint | Meaning
| --- | --- | ---
| GET | /api/auth | get token
| GET | /api/feeds/:id | get that user's feed
| GET | /api/users/:id | get the user with that id
| GET | /api/users?username=:name | get user with that username
| POST | /api/users | add a new user
| GET | /api/users/:id/reviews | get that user's reviews
| GET | /api/reviews | get all the reviews
| GET | /api/reviews/:id | get a the review with that id
| DELETE | /api/reviews/:id | delete that review
| POST | /api/reviews/:id/comments | add a comment to that review
| POST | /api/reviews/:id/likes | like that review
| POST | /api/reviews/:id/dislikes | dislike that review
| GET | /api/users/:id/followers | all the people follow that user
| GET | /api/users/:id/following | all the people that user is following
| POST | /api/users/:id/following/:id | make id 1 follow id 2
| DELETE | /api/users/:id/following/:id | make id 1 unfollow id 2
