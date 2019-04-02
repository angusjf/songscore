{-# LANGUAGE OverloadedStrings #-}

module Songscore (main) where

import Web.Scotty (scotty, get, post, delete, notFound)
import Actions
import System.Environment
import Data.Maybe (fromMaybe)
import Control.Monad (join)
import Control.Applicative ((<$>))
import Text.Read (readMaybe)

main :: IO ()
main = do
  port <- fromMaybe 8080
          . join
          . fmap readMaybe <$> lookupEnv "PORT"
  scotty port app
    where
      app = do
        get "/auth" getAuthAction
        get "/feeds/:user_id" getFeedAction
        get "/users/:user_id" getUserAction
        get "/users" getUsersAction
        get "/users/:user_id/reviews" getUserReviewsAction
        get "/reviews" getReviewsAction
        get "/reviews/:id" getReviewAction
        get "/users/:id/followers" getUserFollowingAction
        get "/api/users/:id/following" getUserFollowersAction
        get "/users/:id_a/following/:id_b" getUserFollowerAction
        get "/reviews/:id/comments" getReviewCommentsAction
        get "/reviews/:id/likes" getReviewLikesAction
        get "/reviews/:id/dislikes" getReviewDislikesAction
        notFound notFoundAction
