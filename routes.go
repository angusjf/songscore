package main

import (
	"encoding/json"
	"fmt"
	"net/http"

	jwt "github.com/dgrijalva/jwt-go"
    _ "github.com/jinzhu/gorm/dialects/postgres"
)

func (s *server) routes() {
    api := s.router.PathPrefix("/api").Subrouter()
	api.Handle("/reviews", s.onlyIfAuthorized(s.handleReviewsGet())).Methods("GET")
	api.HandleFunc("/reviews/{id}", s.handleReviewsGet()).Methods("GET")
	api.HandleFunc("/reviews", s.handleReviewPost()).Methods("POST")
	api.HandleFunc("/auth", s.handleAuthLogin()).Methods("POST")
	api.HandleFunc("/me", s.handleUserGet()).Methods("GET")
    s.router.HandleFunc("/", s.handlerFrontendGet()).Methods("GET")
}

func (s *server) handleReviewsGet() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
        var reviews []Review
        s.db.Find(&reviews)
        json.NewEncoder(w).Encode(reviews)
    }
}

func (s *server) handleReviewGet() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
        var review Review
        s.db.Where("ID = ?").Find(&review)
        json.NewEncoder(w).Encode(review)
    }
}

func (s *server) handleReviewPost() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
        var review Review
        err := json.NewDecoder(r.Body).Decode(&review)
        if err != nil {
            fmt.Fprintf(w, "couldn't decode review")
        } else {
            s.db.Create(&review)
            json.NewEncoder(w).Encode(review)
        }
    }
}

func (s *server) handleAuthLogin() http.HandlerFunc {
    type Credentials struct {
        Username string `json:"username"`
        Password string `json:"password"`
    }

    return func (w http.ResponseWriter, r *http.Request) {
        var credentials Credentials
        err := json.NewDecoder(r.Body).Decode(&credentials)
        if err != nil {
            fmt.Fprintf(w, "couldn't decode")
            return
        }

        token := jwt.New(jwt.SigningMethodHS256)
        claims := token.Claims.(jwt.MapClaims)

        claims["username"] = credentials.Username

        tokenString, err := token.SignedString(s.jwtSecretKey)

        if err != nil {
            fmt.Fprintf(w, "couldn't sign token")
            return
        }

        fmt.Fprintf(w, tokenString)
    }
}

func (s *server) handleUserGet() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
	    json.NewEncoder(w).Encode(User{ ID: 0, Username: "angusjf", Image: "" })
    }
}

func (s *server) onlyIfAuthorized(h http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		if r.Header["Authorization"] != nil {
			trimmedToken := r.Header.Get("Authorization")[len("Bearer "):]
			token, err := jwt.Parse(trimmedToken, func(token *jwt.Token) (interface{}, error) {
				if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
					return nil, fmt.Errorf("There was an error")
				} else {
					return s.jwtSecretKey, nil
				}
			})

			if err != nil {
				fmt.Fprintf(w, err.Error())
			}

			if token.Valid {
				h(w, r)
			}
		} else {
			fmt.Fprintf(w, "Not Authorized: No Auth header")
		}
	}
}

func (s *server) handlerFrontendGet() http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        http.ServeFile(w, r, "build/index.html")
    }
}

func (s *server) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    s.router.ServeHTTP(w, r)
}
