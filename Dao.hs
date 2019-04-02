module Dao where

import Models

userById :: Int -> User
userById identifier = exampleUser

reviewById :: Int -> Review
reviewById _ = exampleReview

userFeed :: User -> [Review]
userFeed user = [exampleReview, exampleReview]

allUsers = [exampleUser]

allReviews = [exampleReview]

-------------

exampleReview :: Review
exampleReview = Review
  { reviewId            = 1
  , reviewUser          = exampleUser
  , reviewSubject       = exampleSubject
  , reviewReviewText    = "Test"
  , reviewStars         = 1
  , reviewDatetime      = "Test" --DateTime
  , reviewComments      = [exampleComment]
  , reviewLikes         = [exampleUser]
  , reviewDislikes      = [exampleUser]
  }

exampleComment :: Comment
exampleComment = Comment
  { commentId = 1
  , commentText = "HELLO"
  , commentDatetime = "DSA"
  , commentUser = exampleUser
  , commentReview = exampleReview
  }
 

exampleUser :: User
exampleUser = User
  { userId                  = 1
  , userName                = "Test"
  , userUsername            = "Test"
  , userEmail               = "Test"
  , userPassword            = "Test"
  , userPicture             = "Test"
  , userRegisterDatetime    = "Test"
  , userToken               = "Test"
  , userTokenExpiryDatetime = "Test"
  , userReviews             = [exampleReview]
  , userComments            = [exampleComment]
  , userLikes               = [exampleReview]
  , userDislikes            = [exampleReview]
  , userFollowers           = [exampleUser]
  , userFollowing           = [exampleUser]
  }

exampleSubject :: Subject
exampleSubject = Subject
  { subjectId           = 1
  , subjectType         = "Test"
  , subjectName         = "Test"
  , subjectArtistName   = "Test"
  , subjectArt          = "Test"
  , subjectReviews      = [exampleReview]
  }
