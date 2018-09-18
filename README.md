# SongScore API
Learning Python/Flask by creating a website to rate songs. Currently hosted at [songscore.herokuapp.com](songscore.herokuapp.com)

## REST endpoints
Most rest endpoints are plurals, e.g. users not user.
The endpoints have a prefix of `/api/v1`.

Example: `/api/v1/users/1/following/2`

| Method | Endpoint | Meaning | Request Body
| --- | --- | ---
| POST | `/auth` | Get a new token | `{username, password}`
| GET | `/feeds/:id` | Get that user's feed
| GET | `/users/:id` | Get the user with that id
| GET | `/users?username=:name` | Get user with that username
| POST | `/users` | Add a new user | User Model 
| GET | `/users/:id/reviews` | Get that user's reviews
| GET | `/reviews` | Get all the reviews
| GET | `/reviews/:id` | Get a the review with that id
| DELETE | `/reviews/:id` | Delete that review
| POST | `/reviews/:id/comments` | Add a comment to that review
| POST | `/reviews/:id/likes` | Like that review
| POST | `/reviews/:id/dislikes` | Dislike that review
| GET | `/users/:id/followers` | All the people follow that user
| GET | `/users/:id/following` | All the people that user is following
| POST | `/users/:id/following/:id` | Make id 1 follow id 2
| DELETE | `/users/:id/following/:id` | Make id 1 unfollow id 2

## Environment variables
```
export DATABASE_URL=postgres://<username>:<password>@<host>:<port>/<databasename>
export FLASK_APP=songscore_api
export FLASK_DEBUG=true
export SECRET_KEY='secret key here'
```

## Import requirements
see `requirements.txt`
