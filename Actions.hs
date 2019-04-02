{-# LANGUAGE OverloadedStrings #-}

module Controllers
    ( authAction, feedAction, userAction, usersAction, userReviewsAction, reviewsAction, reviewAction
    , userFollowingAction, userFollowersAction, userFollowerAction, reviewCommentsAction
    , reviewLikesAction, reviewDislikesAction
    ) where

import Web.Scotty (ScottyM, json, status, text, param)
import Network.HTTP.Types (status204, notFound404)
import Dao
import Models

type Action = ScottyM ()

getAuthAction :: Action
getAuthAction = (text "TOKEN")

getFeedAction :: Action
getFeedAction = param "user_id" >>= (json . userFeed . userById)

getUserAction :: Action
getUserAction = param "user_id" >>= (json . userById)

--userRoutePost :: Action
--userRoutePost = jsonData >>= addUser

getUsersAction :: Action
getUsersAction = json allUsers

getUserReviewsAction :: Action
getUserReviewsAction = param "user_id" >>= (json . userReviews . userById)

getReviewsAction :: Action
getReviewsAction = json allReviews

getReviewAction :: Action
getReviewAction = param "id" >>= (json . reviewById)

getUserFollowingAction :: Action
getUserFollowingAction = param "id" >>= (json . userFollowers . userById)

getUserFollowersAction :: Action
getUserFollowersAction = param "id" >>= (json . userFollowing . userById)

getUserFollowerAction :: Action
getUserFollowerAction = (status status204)

getReviewCommentsAction :: Action
getReviewCommentsAction = param "id" >>= (json . reviewComments . reviewById)

getReviewLikesAction :: Action
getReviewLikesAction = param "id" >>= (json . reviewLikes . reviewById)

getReviewDislikesAction :: Action
getReviewDislikesAction = param "id" >>= (json . reviewDislikes . reviewById)

notFoundAction :: Action
notFoundAction = (status notFound404) >>= json Null
