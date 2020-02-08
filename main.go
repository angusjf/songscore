package main

import (
	"fmt"
	"net/http"
    "os"

	"github.com/gorilla/mux"
	"github.com/rs/cors"
    "github.com/jinzhu/gorm"
    _ "github.com/jinzhu/gorm/dialects/postgres"
)

type server struct {
    db              *gorm.DB
    router          *mux.Router
    jwtSecretKey    []byte
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

    var err error
    s.db, err = gorm.Open("postgres", databaseUrl)
    if err != nil {
        return err
    }
    defer s.db.Close()

    s.db.AutoMigrate(&ReviewModel{})
    s.db.AutoMigrate(&UserModel{})
    s.db.AutoMigrate(&SubjectModel{})

	s.router = mux.NewRouter()
    s.routes()

	handler := cors.AllowAll().Handler(s.router)

	return http.ListenAndServe(":" + port, handler)
}
