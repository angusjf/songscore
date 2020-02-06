package main

import (
    "time"
)

type Review struct {
	ID      uint            `json:"id"`
	Text    string          `json:"text"`
	Stars   int             `json:"stars"`
	User    User            `json:"user"`
	Subject Subject         `json:"subject"`
    CreatedAt time.Time     `json:"createdAt"`
    UpdatedAt time.Time     `json:"-"`
    DeletedAt *time.Time    `json:"-"`
}

type User struct {
	ID           int        `json:"id"`
	Username     string     `json:"username"`
	Image        string     `json:"image"`
    CreatedAt    time.Time  `json:"-"`
    UpdatedAt    time.Time  `json:"-"`
    DeletedAt    *time.Time `json:"-"`
    PasswordHash string     `json:"-"`
}

type Subject struct {
	ID     int           `json:"id"`
	Title  string        `json:"title"`
	Artist string        `json:"artist"`
	Image  string        `json:"image"`
	Kind   SubjectKind   `json:"kind"`
    CreatedAt time.Time  `json:"-"`
    UpdatedAt time.Time  `json:"-"`
    DeletedAt *time.Time `json:"-"`
}

type SubjectKind int

const (
	Song  = 0
	Album = 1
)
