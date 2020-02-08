package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"path/filepath"
    "strings"
    "context"
    "time"
	"github.com/gorilla/mux"

	jwt "github.com/dgrijalva/jwt-go"
    bcrypt "golang.org/x/crypto/bcrypt"
)

type spaHandler struct {
    staticPath string
    indexPath  string
}

type CredentialsWeb struct {
    Username string `json:"username"`
    Password string `json:"password"`
}

type UserAndTokenWeb struct {
    User UserWeb `json:"user"`
    Token string `json:"token"`
}

type UserWeb struct {
    ID        int    `json:"id"`
	Username  string `json:"username"`
	Image     string `json:"image,omitempty"`
}

type ReviewWeb struct {
	ID        int        `json:"id"`
	Text      string     `json:"text,omitempty"`
	Stars     int        `json:"stars"`
	User      UserWeb    `json:"user"`
	Subject   SubjectWeb `json:"subject"`
    CreatedAt time.Time  `json:"createdAt"`
}

type SubjectWeb struct {
	ID     int         `json:"id"`
	Title  string      `json:"title"`
	Artist string      `json:"artist,omitempty"`
	Image  string      `json:"image,omitempty"`
	Kind   SubjectKind `json:"kind,omitempty"`
}

func (s *server) routes() {
    api := s.router.PathPrefix("/api").Subrouter()
    api.Use(s.withAuth)
    // api.Use(s.log)
	api.HandleFunc("/feeds/{username}", s.handleFeedGet()).Methods("GET")
	api.HandleFunc("/reviews/{id}", s.handleReviewGet()).Methods("GET")
	api.HandleFunc("/reviews", s.handleReviewPost()).Methods("POST")
	api.HandleFunc("/auth", s.handleAuthLogin()).Methods("POST")
	api.HandleFunc("/users", s.handleUsersPost()).Methods("POST")
	api.HandleFunc("/users/{username}", s.handleUserGet()).Methods("Get")
	api.HandleFunc("/users/{username}/reviews", s.handleUserReviewsGet()).Methods("Get")
    api.PathPrefix("/").Handler(s.handleApiNotFound())

    s.router.PathPrefix("/").Handler(s.handlerSPA("build", "index.html"))
}

func (s *server) handleFeedGet() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
        // TODO
        var reviews []ReviewModel
        if s.db.Find(&reviews).Error != nil {
            s.respond(w, r, "Couldn't find feed", http.StatusBadRequest)
            return
        }

        reviewsWeb := make([]ReviewWeb, 0, len(reviews))
        for _, review := range reviews {
            reviewsWeb = append(reviewsWeb, s.ReviewToWeb(review))
        }

        s.respond(w, r, reviewsWeb, http.StatusOK)
    }
}

func (s *server) handleReviewGet() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
        params := mux.Vars(r)
        id, ok := params["id"]
        if ok {
            var review ReviewModel
            if s.db.Where("ID = ?", id).Find(&review).Error != nil {
                s.respond(w, r, "No review with that ID found", http.StatusNotFound)
            } else {
                s.respond(w, r, s.ReviewToWeb(review), http.StatusOK)
            }
        } else {
            s.respond(w, r, "Bad Request, No Id", http.StatusBadRequest)
        }
    }
}

func (s *server) handleReviewPost() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
        var review ReviewWeb
        err := s.decode(w, r, &review)
        if err != nil {
            s.respond(w, r, "Couldn't decode review", http.StatusBadRequest)
        } else {
            id, ok := s.getUserId(r)
            if ok {
                if review.User.ID == id {
                    model := s.ReviewToModel(review, true)
                    s.db.Create(&model)
                    s.respond(w, r, s.ReviewToWeb(model), http.StatusCreated)
                } else {
                    s.respond(w, r, "That user is not you", http.StatusForbidden)
                }
            } else {
                s.respond(w, r, "Could not get user id", http.StatusForbidden)
            }
        }
    }
}

func (s *server) handleAuthLogin() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
        var credentials CredentialsWeb
        decodeErr := s.decode(w, r, &credentials)
        if decodeErr != nil {
            s.respond(w, r, "Couldn't decode", http.StatusBadRequest)
            return
        }

        var user UserModel
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
            tokenString, err := s.getTokenString(user)

            if err != nil {
                s.respond(w, r, "Couldn't sign token", http.StatusBadRequest)
                return
            }

            userAndToken := UserAndTokenWeb{
                User: s.UserToWeb(user),
                Token: tokenString,
            }

            s.respond(w, r, userAndToken, http.StatusOK)
        }
    }
}

func (s *server) getTokenString(model UserModel) (string, error) {
    token := jwt.New(jwt.SigningMethodHS256)
    claims := token.Claims.(jwt.MapClaims)
    claims["user_id"] = model.ID
    return token.SignedString(s.jwtSecretKey)
}

func (s *server) handleUsersPost() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
        var newUser CredentialsWeb
        err := s.decode(w, r, &newUser)
        if err != nil {
            s.respond(w, r, "Couldn't decode user", http.StatusBadRequest)
            return
        }

        hashed, err := bcrypt.GenerateFromPassword(
            []byte(newUser.Password), bcrypt.DefaultCost)

        user := UserModel{
            Username: newUser.Username,
            PasswordHash: string(hashed),
        }

        if s.db.Create(&user).Error != nil {
            s.respond(w, r, "Could not create user", http.StatusBadRequest)
        } else {
            var createdUser UserModel

            if s.db.Where("USERNAME = ?", user.Username).Find(&createdUser).Error != nil {
                s.respond(w, r, "Couldn't new find user", http.StatusNotFound)
                return
            } else {
                tokenString, err := s.getTokenString(createdUser)

                if err != nil {
                    s.respond(w, r, "Couldn't sign token", http.StatusBadRequest)
                    return
                }

                userAndToken := UserAndTokenWeb{
                    User: s.UserToWeb(createdUser),
                    Token: tokenString,
                }
                s.respond(w, r, userAndToken, http.StatusCreated)
            }
        }
    }
}

func (s *server) handleUserGet() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
        params := mux.Vars(r)
        username, ok := params["username"]
        if ok {
            var userModel UserModel
            if s.db.Where("USERNAME = ?", username).Find(&userModel).Error != nil {
	            s.respond(w, r, "User not found!", http.StatusNotFound)
                return
            }
            userWeb := s.UserToWeb(userModel)
            s.respond(w, r, userWeb, http.StatusOK)
        } else {
	        s.respond(w, r, "Param not found!", http.StatusBadRequest)
        }
    }
}

func (s *server) handleUserReviewsGet() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
        params := mux.Vars(r)
        username, ok := params["username"]
        if ok {
            var userModel UserModel
            if s.db.Where("USERNAME = ?", username).Find(&userModel).Error != nil {
	            s.respond(w, r, "User not found!", http.StatusNotFound)
                return
            }
            var reviewModels []ReviewModel
            if s.db.Where("USER_ID = ?", userModel.ID).Find(&reviewModels).Error != nil {
                s.respond(w, r, "Database Error", http.StatusNotFound)
                return
            }
            reviewsWeb := make([]ReviewWeb, 0, len(reviewModels))
            for _, review := range reviewModels {
                reviewsWeb = append(reviewsWeb, s.ReviewToWeb(review))
            }
            s.respond(w, r, reviewsWeb, http.StatusOK)
        } else {
	        s.respond(w, r, "Param not found!", http.StatusBadRequest)
        }
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
            ctx := context.WithValue(r.Context(), "user_id", claims["user_id"])
            next.ServeHTTP(w, r.Clone(ctx))
        }
	})
}

func (s *server) log(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        fmt.Printf(" -> %s", r.URL)
        next.ServeHTTP(w, r)
	})
}

func (s *server) handleApiNotFound() http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        s.respond(w, r, "Not Found", http.StatusNotFound)
    }
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

func (s *server) getUserId(r *http.Request) (int, bool) {
    id, ok := r.Context().Value("user_id").(float64)
    return int(id), ok
}
