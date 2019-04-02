# SongScore API
Learning Haskell by creating the api for a website to rate songs. Currently hosted at [songscore.herokuapp.com](songscore.herokuapp.com)

# REST endpoints
Most rest endpoints are plurals, e.g. users not user.

The endpoints have a prefix of `/api/v1`.

Example: `GET /api/v1/users/1/reviews`.

## Get a new token
`POST /auth`
#### Parameters
| Name | Type | Description
| --- | --- | ---
| `username` | `string` | Username
| `password` | `string` | Password (unencypted)

## Get that user's feed
`GET /feeds/:id`

## Get the user with that id
`GET /users/:id`

## Get user with that username
`GET /users?username=:name`

## Add a new user
`POST /users`
#### Parameters
| Name | Type | Description
| --- | --- | ---
| `username` | `string` | Username
| `password` | `string` | Password (unencypted)
| `name` | `string` | Name
| `email` | `string` | Email

## Get that user's reviews
`GET /users/:id/reviews`

## Get all the reviews
`GET /reviews`

## Add a new review
`POST /reviews`
#### Parameters
`Review` model

## Get a the review with that id
`GET /reviews/:id`

## Delete that review
`DELETE /reviews/:id`

## All the people follow that user
`GET /users/:id/followers`

## All the people that user is following
`GET /users/:id/following`

## Make id 1 follow id 2
`POST /users/:id/following/:id`

## Make id 1 unfollow id 2
`DELETE /users/:id/following/:id`

## Make id add a comment to that review
`POST /users/:id/comments`
#### Parameters
`ReviewComment` Model

## Make id like that review
`POST /users/:id/likes`
#### Parameters
`review_id`

## Make id dislike that review
`POST /users/:id/dislikes`
#### Parameters
`review_id`

# Environment variables
```
export DATABASE_URL=postgres://<username>:<password>@<host>:<port>/<databasename>
```
