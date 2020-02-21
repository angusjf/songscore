package main

import (
    "fmt"
    "time"
    "strings"
)

type ReviewModel struct {
	ID        int
	Text      string
	Stars     int
	UserID    int
	SubjectID int
    Likers    []*UserModel `gorm:"many2many:user_likes"`
    Dislikers []*UserModel `gorm:"many2many:user_dislikes"`
    Comments  []CommentModel `gorm:"foreignkey:ReviewID"`
    CreatedAt time.Time
    UpdatedAt time.Time
    DeletedAt *time.Time
}

type CommentModel struct {
    ID int
    Text string
    UserID int
    ReviewID int
}

func (s *server) CommentToWeb(model CommentModel) CommentWeb {
    var user UserModel
    if s.db.Where("ID = ?", model.UserID).Find(&user).Error != nil {
        panic("comment conversion can't find user")
    }
    return CommentWeb {
        ID: model.ID,
        Text: model.Text,
        ReviewID: model.ReviewID,
        User: s.UserToWeb(user),
    }
}

func (s *server) CommentToModel(web CommentWeb) CommentModel {
    return CommentModel {
        ID: web.ID,
        Text: web.Text,
        UserID: web.User.ID,
        ReviewID: web.ReviewID,
    }
}

func (s *server) ReviewToWeb(model ReviewModel) ReviewWeb {
    var user UserModel
    if s.db.Where("id = ?", model.UserID).Find(&user).Error != nil {
        fmt.Printf("no user with id %s", model.UserID)
        panic("User is missing!")
    }
    var subject SubjectModel
    if s.db.Where("id = ?", model.SubjectID).Find(&subject).Error != nil {
        panic("Subject is missing!")
    }

    likes := make([]UserWeb, len(model.Likers))
    for i, user := range model.Likers {
        likes[i] = s.UserToWeb(*user)
    }

    dislikes := make([]UserWeb, len(model.Dislikers))
    for i, user := range model.Dislikers {
        dislikes[i] = s.UserToWeb(*user)
    }

    comments := make([]CommentWeb, len(model.Comments))
    for i, comment := range model.Comments {
        comments[i] = s.CommentToWeb(comment)
    }

    return ReviewWeb{
        ID: model.ID,
        Text: model.Text,
        Stars: model.Stars,
        User: s.UserToWeb(user),
        Subject: s.SubjectToWeb(subject),
        CreatedAt: model.CreatedAt.Unix() * 1000,
        Likes: likes,
        Dislikes: dislikes,
        Comments: comments,
    }
}

func (s *server) NewReviewToModel(web ReviewWeb) ReviewModel {
    model := ReviewModel{
        Text: strings.Trim(web.Text, " "),
        Stars: web.Stars,
        UserID: web.User.ID,
    }

    subject := s.NewSubjectToModel(web.Subject)
    err := s.db.Create(&subject).Error
    if err != nil {
        panic(err)
    }
    model.SubjectID = subject.ID

    return model
}

func (s *server) ReviewToModel(web ReviewWeb) ReviewModel {
    model := ReviewModel{
        Text: web.Text,
        Stars: web.Stars,
        UserID: web.User.ID,
    }

    model.ID = web.ID
    model.SubjectID = web.Subject.ID

    return model
}

func (s *server) SubjectToModel(web SubjectWeb) SubjectModel {
    var kind SubjectKind
    if web.Kind == "Album" {
        kind = Album
    } else {
        kind = Song
    }
	return SubjectModel {
        ID: web.ID,
        Title: web.Title,
        Artist: web.Artist,
        Image: web.Image,
        Kind: kind,
        SpotifyID: web.SpotifyID,
    }
}

func (s *server) NewSubjectToModel(web SubjectWeb) SubjectModel {
    var kind SubjectKind
    if web.Kind == "Album" {
        kind = Album
    } else {
        kind = Song
    }
    internalImage, _ := imageUrlToBase64(web.Image)
	return SubjectModel {
        ID: web.ID,
        Title: web.Title,
        Artist: web.Artist,
        Image: internalImage,
        Kind: kind,
        SpotifyID: web.SpotifyID,
    }
}

type UserModel struct {
	ID              int
    Username        string `gorm:"unique;not null"`
	Image           string
    PasswordHash    string
    LikedReviews    []*ReviewModel `gorm:"many2many:user_likes"`
    DislikedReviews []*ReviewModel `gorm:"many2many:user_dislikes"`
    CreatedAt       time.Time
    UpdatedAt       time.Time
    DeletedAt       *time.Time
}

func (s *server) UserToWeb(model UserModel) UserWeb {
    return UserWeb{
        ID: model.ID,
        Username: model.Username,
        Image: model.Image,
    }
}

func (s *server) UserToModel(web UserWeb) UserModel {
    return UserModel{
        ID: web.ID,
        Username: web.Username,
        Image: web.Image,
    }
}

type SubjectModel struct {
	ID     int
	Title  string
	Artist string
	Image  string
	Kind   SubjectKind
    CreatedAt time.Time
    UpdatedAt time.Time
    DeletedAt *time.Time
    SpotifyID string
}

func (s *server) SubjectToWeb(model SubjectModel) SubjectWeb {
    var kind string
    if model.Kind == Album {
        kind = "Album"
    } else {
        kind = "Song"
    }
    return SubjectWeb{
        ID: model.ID,
        Title: model.Title,
        Artist: model.Artist,
        Image: model.Image,
        Kind: kind,
        SpotifyID: model.SpotifyID,
    }
}

type SubjectKind int

const (
	Song  = 0
	Album = 1
)
