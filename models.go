package main

import (
    "time"
)

type ReviewModel struct {
	ID        int
	Text      string
	Stars     int
	UserId    int
	SubjectId int
    CreatedAt time.Time
    UpdatedAt time.Time
    DeletedAt *time.Time
}

func (s *server) ReviewToWeb(model ReviewModel) ReviewWeb {
    var user UserModel
    if s.db.Where("id = ?", model.UserId).Find(&user).Error != nil {
        panic("User is missing!")
    }
    var subject SubjectModel
    if s.db.Where("id = ?", model.SubjectId).Find(&subject).Error != nil {
        panic("Subject is missing!")
    }
    return ReviewWeb{
        ID: model.ID,
        Text: model.Text,
        Stars: model.Stars,
        User: s.UserToWeb(user),
        Subject: s.SubjectToWeb(subject),
        CreatedAt: model.CreatedAt,
    }
}

func (s *server) NewReviewToModel(web ReviewWeb) ReviewModel {
    model := ReviewModel{
        Text: web.Text,
        Stars: web.Stars,
        UserId: web.User.ID,
    }

    subject := s.NewSubjectToModel(web.Subject)
    err := s.db.Create(&subject).Error
    if err != nil {
        panic(err)
    }
    model.SubjectId = subject.ID

    return model
}

func (s *server) ReviewToModel(web ReviewWeb) ReviewModel {
    model := ReviewModel{
        Text: web.Text,
        Stars: web.Stars,
        UserId: web.User.ID,
    }

    model.ID = web.ID
    model.SubjectId = web.Subject.ID

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
    }
}

type UserModel struct {
	ID           int
	Username     string
	Image        string
    PasswordHash string
    CreatedAt    time.Time
    UpdatedAt    time.Time
    DeletedAt    *time.Time
}

func (s *server) UserToWeb(model UserModel) UserWeb {
    return UserWeb{
        ID: model.ID,
        Username: model.Username,
        Image: model.Image,
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
    }
}

type SubjectKind int

const (
	Song  = 0
	Album = 1
)
