package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
    "os"
    "time"

	jwt "github.com/dgrijalva/jwt-go"
	"github.com/gorilla/mux"
	"github.com/rs/cors"
    "github.com/jinzhu/gorm"
    _ "github.com/jinzhu/gorm/dialects/postgres"
)

type Review struct {
	ID      uint            `json:"id"`
	Text    string          `json:"text"`
	Stars   int             `json:"stars"`
	User    User            `json:"user"`
	Subject Subject         `json:"subject"`
    CreatedAt time.Time     `json:"createdAt"`
    UpdatedAt time.Time     `json:"updatedAt"`
    DeletedAt *time.Time    `json:"deletedAt"`
}

type User struct {
	ID       int    `json:"id"`
	Username string `json:"username"`
	Image    string `json:"image"`
    CreatedAt time.Time     `json:"createdAt"`
    UpdatedAt time.Time     `json:"updatedAt"`
    DeletedAt *time.Time    `json:"deletedAt"`
}

type Subject struct {
	ID     int         `json:"id"`
	Title  string      `json:"title"`
	Artist string      `json:"artist"`
	Image  string      `json:"image"`
	Kind   SubjectKind `json:"kind"`
    CreatedAt time.Time     `json:"createdAt"`
    UpdatedAt time.Time     `json:"updatedAt"`
    DeletedAt *time.Time    `json:"deletedAt"`
}

type SubjectKind int

const (
	Song  = 0
	Album = 1
)

type Credentials struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

var jwtSecretKey = []byte("toroymoi")

var db *gorm.DB

func getReviews(w http.ResponseWriter, r *http.Request) {
    var reviews []Review
    db.Find(&reviews)
    fmt.Printf("%s", reviews)
	json.NewEncoder(w).Encode(reviews)
}

func getReview(w http.ResponseWriter, r *http.Request) {
    var review Review
    db.Where("ID = ?").Find(&review)
	json.NewEncoder(w).Encode(review)
}

func postReview(w http.ResponseWriter, r *http.Request) {
	var review Review
	err := json.NewDecoder(r.Body).Decode(&review)
	if err != nil {
		fmt.Fprintf(w, "couldn't decode review")
	} else {
        db.Create(&review)
	    json.NewEncoder(w).Encode(review)
    }
}

func postAuth(w http.ResponseWriter, r *http.Request) {
	var credentials Credentials
	err := json.NewDecoder(r.Body).Decode(&credentials)
	if err != nil {
		fmt.Fprintf(w, "couldn't decode")
		return
	}

	token := jwt.New(jwt.SigningMethodHS256)
	claims := token.Claims.(jwt.MapClaims)

	claims["username"] = credentials.Username

	tokenString, err := token.SignedString(jwtSecretKey)

	if err != nil {
		fmt.Fprintf(w, "couldn't sign token")
		return
	}

	fmt.Fprintf(w, tokenString)
}

func getMe(w http.ResponseWriter, r *http.Request) {
	json.NewEncoder(w).Encode(User{ ID: 0, Username: "angusjf", Image: "" })
}

func onlyIfAuthorized(endpoint func(w http.ResponseWriter, r *http.Request)) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Header["Authorization"] != nil {
			trimmedToken := r.Header.Get("Authorization")[len("Bearer "):]
			token, err := jwt.Parse(trimmedToken, func(token *jwt.Token) (interface{}, error) {
				if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
					return nil, fmt.Errorf("There was an error")
				} else {
					return jwtSecretKey, nil
				}
			})

			if err != nil {
				fmt.Fprintf(w, err.Error())
			}

			if token.Valid {
				endpoint(w, r)
			}
		} else {
			fmt.Fprintf(w, "Not Authorized: No Auth header")
		}
	})
}

func getFrontend(w http.ResponseWriter, r *http.Request) {
    http.ServeFile(w, r, "build/index.html")
}

func main() {
	port := os.Getenv("PORT")

	if port == "" {
        port = "8081"
	}

    databaseUrl := os.Getenv("DATABASE_URL")
    if databaseUrl == "" {
        fmt.Errorf("no DATABASE_URL")
        return
    }

    var err error
    db, err = gorm.Open("postgres", databaseUrl)
    if err != nil {
        fmt.Errorf("ERROR!")
        return
    }
    defer db.Close()

    db.AutoMigrate(&Review{})
    db.AutoMigrate(&User{})
    db.AutoMigrate(&Subject{})

	router := mux.NewRouter()

    api := router.PathPrefix("/api").Subrouter()
	api.Handle("/reviews", onlyIfAuthorized(getReviews)).Methods("GET")
	api.HandleFunc("/reviews/{id}", getReview).Methods("GET")
	api.HandleFunc("/reviews", postReview).Methods("POST")
	api.HandleFunc("/auth", postAuth).Methods("POST")
	api.HandleFunc("/me", getMe).Methods("GET")

    router.HandleFunc("/", getFrontend).Methods("GET")

	handler := cors.AllowAll().Handler(router)

	log.Fatal(http.ListenAndServe(":" + port, handler))
}
