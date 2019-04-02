{-# LANGUAGE DeriveGeneric #-}

module Models where

import GHC.Generics
import Data.Aeson (ToJSON, FromJSON)
--import Data.Dates

data Review = Review
  { reviewId            :: Int
  , reviewUser          :: User
  , reviewSubject       :: Subject
  , reviewReviewText    :: String
  , reviewStars         :: Int
  , reviewDatetime      :: String --DateTime
  , reviewComments      :: [Comment]
  , reviewLikes         :: [User]
  , reviewDislikes      :: [User]
  } deriving Generic
instance ToJSON Review
instance FromJSON Review

data User = User
  { userId                  :: Int
  , userName                :: String
  , userUsername            :: String
  , userEmail               :: String
  , userPassword            :: String
  , userPicture             :: String
  , userRegisterDatetime    :: String
  , userToken               :: String
  , userTokenExpiryDatetime :: String
  , userReviews             :: [Review]
  , userComments            :: [Comment]
  , userLikes               :: [Review]
  , userDislikes            :: [Review]
  , userFollowers           :: [User]
  , userFollowing           :: [User]
  } deriving Generic
instance ToJSON User
instance FromJSON User

data Subject = Subject
  { subjectId           :: Int
  , subjectType         :: String
  , subjectName         :: String
  , subjectArtistName   :: String
  , subjectArt          :: String
  , subjectReviews      :: [Review]
  } deriving Generic
instance ToJSON Subject
instance FromJSON Subject

data Comment = Comment
  { commentId :: Int
  , commentText :: String
  , commentDatetime :: String
  , commentUser :: User
  , commentReview :: Review
  } deriving Generic
instance ToJSON Comment
instance FromJSON Comment
