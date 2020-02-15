package main

import (
	"fmt"
	"net/http"
    "os"
    "time"

	"github.com/gorilla/mux"
	"github.com/rs/cors"
    "github.com/jinzhu/gorm"
    _ "github.com/jinzhu/gorm/dialects/postgres"
    heroku "github.com/jonahgeorge/force-ssl-heroku"
)

type server struct {
    db            *gorm.DB
    router        *mux.Router
    jwtSecretKey  []byte
    spotifyToken  []byte
    spotifyId     string
    spotifySecret string
    spotifyExp    time.Time
}

func main() {
    if err := run(); err != nil {
        fmt.Printf("%s", err)
        os.Exit(1)
    }
}

func run() error {
    s := &server{}

	port := os.Getenv("PORT")
	if port == "" {
        port = "8081"
	}

    s.jwtSecretKey = []byte(os.Getenv("JWT_SECRET_KEY"))
    if string(s.jwtSecretKey) == "" {
        s.jwtSecretKey = []byte("toroymoi")
    }

    databaseUrl := os.Getenv("DATABASE_URL")
    if databaseUrl == "" {
        return fmt.Errorf("no database url!")
    }

    s.spotifyId = os.Getenv("SPOTIFY_CLIENT_ID")
    if s.spotifyId == "" {
        return fmt.Errorf("set SPOTIFY_CLIENT_ID")
    }

    s.spotifySecret = os.Getenv("SPOTIFY_CLIENT_SECRET")
    if s.spotifySecret == "" {
        return fmt.Errorf("set SPOTIFY_CLIENT_SECRET")
    }

    var spotifyErr error
    s.spotifyToken, s.spotifyExp, spotifyErr = getSpotifyToken(s.spotifyId, s.spotifySecret)
    if spotifyErr != nil {
        return spotifyErr
    }
    fmt.Printf("%s\n", s.spotifyToken)

    var err error
    s.db, err = gorm.Open("postgres", databaseUrl)
    if err != nil {
        return err
    }
    defer s.db.Close()

    s.db.AutoMigrate(&ReviewModel{})
    s.db.AutoMigrate(&UserModel{})
    s.db.AutoMigrate(&SubjectModel{})
    s.db.AutoMigrate(&CommentModel{})

	s.router = mux.NewRouter()
    s.routes()

	handler := cors.AllowAll().Handler(s.router)

	return http.ListenAndServe(":" + port, heroku.ForceSsl(handler))
}
