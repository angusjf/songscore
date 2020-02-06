package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"path/filepath"
    "strings"
    "context"

	jwt "github.com/dgrijalva/jwt-go"
    bcrypt "golang.org/x/crypto/bcrypt"
)

type spaHandler struct {
    staticPath string
    indexPath  string
}

func (s *server) routes() {
    api := s.router.PathPrefix("/api").Subrouter()
    api.Use(s.withAuth)
	api.HandleFunc("/reviews/{id}", s.handleReviewGet()).Methods("GET")
	api.HandleFunc("/reviews", s.handleReviewsGet()).Methods("GET")
	api.HandleFunc("/reviews", s.handleReviewPost()).Methods("POST")
	api.HandleFunc("/auth", s.handleAuthLogin()).Methods("POST")
	api.HandleFunc("/users", s.handleUsersPost()).Methods("POST")
	api.HandleFunc("/me", s.handleUserGet()).Methods("GET")

    s.router.PathPrefix("/").Handler(s.handlerSPA("build", "index.html"))
}

func (s *server) handleReviewsGet() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
        var reviews []Review
        s.db.Find(&reviews)
        s.respond(w, r, reviews, http.StatusOK)
    }
}

func (s *server) handleReviewGet() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
        var review Review
        if s.db.Where("ID = ?", "9999").Find(&review).Error != nil {
            s.respond(w, r, "No review with that ID found", http.StatusNotFound)
        } else {
            s.respond(w, r, review, http.StatusOK)
        }
    }
}

func (s *server) handleReviewPost() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
        var review Review
        err := s.decode(w, r, &review)
        if err != nil {
            s.respond(w, r, "Couldn't decode review", http.StatusBadRequest)
        } else {
            if review.User.Username == r.Context().Value("username") {
                s.db.Create(&review)
                s.respond(w, r, review, http.StatusCreated)
            } else {
                s.respond(w, r, "That user is not you", http.StatusForbidden)
            }
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
        decodeErr := s.decode(w, r, &credentials)
        if decodeErr != nil {
            s.respond(w, r, "Couldn't decode", http.StatusBadRequest)
            return
        }

        var user User
        if s.db.Where("USERNAME = ?", credentials.Username).Find(&user).Error != nil {
            s.respond(w, r, "Couldn't find user", http.StatusNotFound)
            return
        }

        compareErr := bcrypt.CompareHashAndPassword(
            []byte(user.PasswordHash),
            []byte(credentials.Password))

        if compareErr != nil {
            s.respond(w, r, "Wrong password", http.StatusForbidden)
        } else {
            token := jwt.New(jwt.SigningMethodHS256)
            claims := token.Claims.(jwt.MapClaims)

            claims["username"] = credentials.Username

            tokenString, err := token.SignedString(s.jwtSecretKey)

            if err != nil {
                s.respond(w, r, "Couldn't sign token", http.StatusBadRequest)
                return
            }

            s.respond(w, r, tokenString, http.StatusOK)
        }
    }
}

func (s *server) handleUsersPost() http.HandlerFunc {
    type NewUser struct {
        Username string
        Password string
    }

    return func (w http.ResponseWriter, r *http.Request) {
        var newUser NewUser
        err := s.decode(w, r, &newUser)
        if err != nil {
            s.respond(w, r, "Couldn't decode user", http.StatusBadRequest)
            return
        }

        hashed, err := bcrypt.GenerateFromPassword(
            []byte(newUser.Password), bcrypt.DefaultCost)

        user := User{
            Username: newUser.Username,
            PasswordHash: string(hashed),
        }

        if s.db.Create(&user).Error != nil {
            s.respond(w, r, "Could not create user", http.StatusBadRequest)
        } else {
            s.respond(w, r, user, http.StatusCreated)
        }
    }
}

func (s *server) handleUserGet() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
	    s.respond(w, r, "Not implemented", 501)
    }
}

func (s *server) withAuth(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        auth := r.Header.Get("Authorization")
		if auth == "" {
            // no token, just go to endpoint anyway
            next.ServeHTTP(w, r)
            return
        }

        auth = strings.TrimPrefix(auth, "Bearer ")

        token, err := jwt.Parse(auth, func(token *jwt.Token) (interface{}, error) {
            if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
                return nil, fmt.Errorf("Error parsing token")
            } else {
                return s.jwtSecretKey, nil
            }
        })

        if err != nil {
            s.respond(w, r, err.Error(), http.StatusBadRequest)
        }

        if token.Valid {
            claims := token.Claims.(jwt.MapClaims)
            ctx := context.WithValue(r.Context(), "username", claims["username"])
            next.ServeHTTP(w, r.Clone(ctx))
        }
	})
}

func (s *server) handlerSPA(staticPath, indexPath string) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        // get the absolute path to prevent directory traversal
        path, err := filepath.Abs(r.URL.Path)
        if err != nil {
            // if we failed to get the absolute path respond with a 400 bad request
            // and stop
            http.Error(w, err.Error(), http.StatusBadRequest)
            return
        }

        // prepend the path with the path to the static directory
        path = filepath.Join(staticPath, path)

        // check whether a file exists at the given path
        _, err = os.Stat(path)
        if os.IsNotExist(err) {
            // file does not exist, serve index.html
            http.ServeFile(w, r, filepath.Join(staticPath, indexPath))
            return
        } else if err != nil {
            // if we got an error (that wasn't that the file doesn't exist) stating the
            // file, return a 500 internal server error and stop
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        // otherwise, use http.FileServer to serve the static dir
        http.FileServer(http.Dir(staticPath)).ServeHTTP(w, r)
    }
}

func (s *server) respond(w http.ResponseWriter, r *http.Request,
                            data interface{}, status int) {
    w.WriteHeader(status)
    if data != nil {
        err := json.NewEncoder(w).Encode(data)
        if err != nil {
            fmt.Fprintf(w, "Could not endode response")
        }
    }
}

func (s *server) decode(w http.ResponseWriter, r *http.Request,
                                v interface{}) error {
    return json.NewDecoder(r.Body).Decode(v)
}
