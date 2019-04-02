{-# LANGUAGE OverloadedStrings #-}

import Web.Scotty (scotty)
import Actions

main :: IO ()
main = scotty port app
  where
    port = 8080
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
