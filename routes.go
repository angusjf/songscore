package main

import (
    "encoding/json"
	"fmt"
	"net/http"
	"os"
	"path/filepath"
    "strings"
    "context"
	"github.com/gorilla/mux"
    "time"

	jwt "github.com/dgrijalva/jwt-go"
    bcrypt "golang.org/x/crypto/bcrypt"
)

func (s *server) routes() {
    api := s.router.PathPrefix("/api").Subrouter()

    api.Use(s.withAuth)
    api.Use(s.log)

	api.HandleFunc("/feeds/{username}", s.handleFeedGet()).Methods("GET")

	api.HandleFunc("/reviews", s.handleReviewPost()).Methods("POST")
	api.HandleFunc("/reviews/{id}", s.handleReviewDelete()).Methods("DELETE")
	api.HandleFunc("/reviews/{id}", s.handleReviewGet()).Methods("GET")
	api.HandleFunc("/reviews/{id}/like", s.handleReviewLikePost()).Methods("POST")
	api.HandleFunc("/reviews/{id}/dislike", s.handleReviewDisikePost()).Methods("POST")
	api.HandleFunc("/reviews/{id}/comments", s.handleReviewCommentPost()).Methods("POST")

	api.HandleFunc("/users", s.handleUsersPost()).Methods("POST")
	api.HandleFunc("/users/{username}", s.handleUserGet()).Methods("GET")
	api.HandleFunc("/users/{username}/reviews", s.handleUserReviewsGet()).Methods("GET")
	api.HandleFunc("/users/{username}/available", s.handleUsernameAvailableGet()).Methods("GET")
	api.HandleFunc("/users/{username}/followers", s.handleUserFollowersGet()).Methods("GET")
	api.HandleFunc("/users/{username}/following", s.handleUserFollowingGet()).Methods("GET")
	api.HandleFunc("/users/{username}/follow", s.handleUserFollowPost()).Methods("POST")

	api.HandleFunc("/subjects/search", s.handleSubjectsSearchGet()).Methods("GET")

	api.HandleFunc("/auth", s.handleAuthLogin()).Methods("POST")

    api.PathPrefix("/").Handler(s.handleApiNotFound())

    s.router.PathPrefix("/").Handler(s.handlerSPA("build", "index.html"))
}

// FEEDS

func (s *server) handleFeedGet() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
        // TODO
        var reviews []ReviewModel
        err := s.db.Preload("Dislikers").
                    Preload("Likers").
                    Preload("Comments").
                    Order("CREATED_AT desc").
                    Find(&reviews).
                    Error
        if err != nil {
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

// REVIEWS

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
                    model := s.NewReviewToModel(review)
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

func (s *server) handleReviewDelete() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
        params := mux.Vars(r)
        id, ok := params["id"]
        if ok {
            var review ReviewModel
            err := s.db.Where("ID = ?", id).
                        Find(&review).
                        Error
            web := s.ReviewToWeb(review)
            if err != nil || s.db.Where("ID = ?", id).Delete(&ReviewModel{}).Error != nil {
                s.respond(w, r, "No review with that ID found", http.StatusNotFound)
            } else {
                s.respond(w, r, web, http.StatusOK)
            }
        } else {
            s.respond(w, r, "Bad Request, No Id", http.StatusBadRequest)
        }
    }
}

func (s *server) handleReviewGet() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
        params := mux.Vars(r)
        id, ok := params["id"]
        if ok {
            var review ReviewModel
            err := s.db.Preload("Dislikers").
                        Preload("Likers").
                        Preload("Comments").
                        Where("ID = ?", id).
                        Find(&review).
                        Error
            if err != nil {
                s.respond(w, r, "No review with that ID found", http.StatusNotFound)
            } else {
                s.respond(w, r, s.ReviewToWeb(review), http.StatusOK)
            }
        } else {
            s.respond(w, r, "Bad Request, No Id", http.StatusBadRequest)
        }
    }
}

func (s * server) handleReviewLikePost() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
        params := mux.Vars(r)
        id, ok := params["id"]
        if ok {
            var review ReviewModel
            err := s.db.Where("ID = ?", id).
                        Preload("Dislikers").
                        Preload("Likers").
                        Preload("Comments").
                        Find(&review).
                        Error
            if err != nil {
                s.respond(w, r, "No review with that ID found", http.StatusNotFound)
            } else {
                var userModel UserModel
                userId, ok := s.getUserId(r)
                if !ok || s.db.Where("ID = ?", userId).Find(&userModel).Error != nil {
                    s.respond(w, r, "Could not get logged in user", http.StatusInternalServerError)
                } else {
                    review.Likers = append(review.Likers, &userModel)
                    if s.db.Save(&review).Error != nil {
                        s.respond(w, r, "Could not update review", http.StatusInternalServerError)
                    }
                    s.respond(w, r, s.ReviewToWeb(review), http.StatusOK)
                }
            }
        } else {
            s.respond(w, r, "Bad Request, No Id", http.StatusBadRequest)
        }
    }
}

func (s * server) handleReviewDisikePost() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
        params := mux.Vars(r)
        id, ok := params["id"]
        if ok {
            var review ReviewModel
            err := s.db.Where("ID = ?", id).
                        Preload("Dislikers").
                        Preload("Likers").
                        Preload("Comments").
                        Find(&review).
                        Error
            if err != nil {
                s.respond(w, r, "No review with that ID found", http.StatusNotFound)
            } else {
                var userModel UserModel
                userId, ok := s.getUserId(r)
                if !ok || s.db.Where("ID = ?", userId).Find(&userModel).Error != nil {
                    s.respond(w, r, "Could not get logged in user", http.StatusInternalServerError)
                } else {
                    review.Dislikers = append(review.Dislikers, &userModel)
                    if s.db.Save(&review).Error != nil {
                        s.respond(w, r, "Could not update review", http.StatusInternalServerError)
                    }
                    s.respond(w, r, s.ReviewToWeb(review), http.StatusOK)
                }
            }
        } else {
            s.respond(w, r, "Bad Request, No Id", http.StatusBadRequest)
        }
    }
}

func (s *server) handleReviewCommentPost() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
        params := mux.Vars(r)
        id, ok := params["id"]
        if ok {
            var review ReviewModel
            err := s.db.Where("ID = ?", id).
                        Preload("Dislikers").
                        Preload("Likers").
                        Preload("Comments").
                        Find(&review).
                        Error
            if err != nil {
                s.respond(w, r, "No review with that ID found", http.StatusNotFound)
            } else {
                var userModel UserModel
                userId, ok := s.getUserId(r)
                if !ok || s.db.Where("ID = ?", userId).Find(&userModel).Error != nil {
                    s.respond(w, r, "Could not get logged in user", http.StatusInternalServerError)
                } else {
                    var comment CommentWeb
                    s.decode(w, r, &comment)
                    review.Comments = append(review.Comments, s.CommentToModel(comment))
                    if s.db.Save(&review).Error != nil {
                        s.respond(w, r, "Could not update review", http.StatusInternalServerError)
                    }
                    s.respond(w, r, s.ReviewToWeb(review), http.StatusOK)
                }
            }
        } else {
            s.respond(w, r, "Bad Request, No Id", http.StatusBadRequest)
        }
    }
}

// USERS

func (s *server) handleUsersPost() http.HandlerFunc {
    type NewUserWeb struct {
        Username string `json:"username"`
        Password string `json:"password"`
        Image string `json:"image"`
    }

    return func (w http.ResponseWriter, r *http.Request) {
        var newUser NewUserWeb
        err := s.decode(w, r, &newUser)
        if err != nil {
            s.respond(w, r, "Couldn't decode user", http.StatusBadRequest)
            return
        }

        hashed, err := bcrypt.GenerateFromPassword(
            []byte(newUser.Password), bcrypt.DefaultCost)

        user := UserModel{
            Username: newUser.Username,
            Image: newUser.Image,
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

func (s *server) handleUsernameAvailableGet() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
        params := mux.Vars(r)
        username, ok := params["username"]
        if ok {
            var count int
            if s.db.Model(&UserModel{}).Where("USERNAME = ?", username).Count(&count).Error != nil {
                s.respond(w, r, "Error checking username availabilty", http.StatusInternalServerError)
            } else {
                s.respond(w, r, count == 0, http.StatusOK)
            }
        } else {
	        s.respond(w, r, "Param not found!", http.StatusBadRequest)
        }
    }
}

func (s *server) handleUserFollowersGet() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
        params := mux.Vars(r)
        username, ok := params["username"]
        if ok {
            var userModel UserModel
            if s.db.Where("USERNAME = ?", username).Find(&userModel).Error != nil {
	            s.respond(w, r, "User not found!", http.StatusNotFound)
                return
            }
            /*
            followers := make([]UserWeb, 0, len(userModel.Followers))
            for _, user := range userModel.Followers {

            }
            s.respond(w, r, followers, http.StatusOK)
            */
        } else {
	        s.respond(w, r, "Param not found!", http.StatusBadRequest)
        }
    }
}

func (s *server) handleUserFollowingGet() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
        params := mux.Vars(r)
        username, ok := params["username"]
        if ok {
            var userModel UserModel
            if s.db.Where("USERNAME = ?", username).Find(&userModel).Error != nil {
	            s.respond(w, r, "User not found!", http.StatusNotFound)
                return
            }
            /*
            s.respond(w, r, , http.StatusOK)
            */
        } else {
	        s.respond(w, r, "Param not found!", http.StatusBadRequest)
        }
    }
}

func (s *server) handleUserFollowPost() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
        params := mux.Vars(r)
        username, ok := params["username"]
        if ok {
            var userModel UserModel
            if s.db.Where("USERNAME = ?", username).Find(&userModel).Error != nil {
	            s.respond(w, r, "User not found!", http.StatusNotFound)
                return
            }
            /*
            s.respond(w, r, , http.StatusOK)
            */
        } else {
	        s.respond(w, r, "Param not found!", http.StatusBadRequest)
        }
    }
}

// SUBJECTS

func (s *server) handleSubjectsSearchGet() http.HandlerFunc {
    return func (w http.ResponseWriter, r *http.Request) {
        if time.Now().After(s.spotifyExp) {
            // get new token
            var spotifyErr error
            s.spotifyToken, s.spotifyExp, spotifyErr = getSpotifyToken(s.spotifyId, s.spotifySecret)
            if spotifyErr != nil {
                s.respond(w, r, "Spotify token not found", http.StatusInternalServerError)
            }
        }
        query := r.URL.Query().Get("q")
        if query == "" {
            s.respond(w, r, "query param q not found", http.StatusInternalServerError)
            return
        }
        err := getSpotifyResults(string(s.spotifyToken), query, w)
        if err != nil {
            s.respond(w, r, "Spotify API error", http.StatusInternalServerError)
            return
        }
    }
}

// AUTH

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

// MIDDLEWARE

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
        fmt.Printf(" -> %s\n", r.URL)
        next.ServeHTTP(w, r)
	})
}

// NOT FOUND

func (s *server) handleApiNotFound() http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        s.respond(w, r, "Not Found", http.StatusNotFound)
    }
}

// SINGLE PAGE APPLICATION

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

// HELPERS

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
