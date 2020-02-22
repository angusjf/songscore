package main

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
	ID        int          `json:"id"`
	Text      string       `json:"text,omitempty"`
	Stars     int          `json:"stars"`
	User      UserWeb      `json:"user"`
	Subject   SubjectWeb   `json:"subject"`
    CreatedAt int64        `json:"createdAt"`
    Likes     []UserWeb    `json:"likes"`
    Dislikes  []UserWeb    `json:"dislikes"`
    Comments  []CommentWeb `json:"comments"`
}

type CommentWeb struct {
	ID   int     `json:"id"`
	Text string  `json:"text"`
	User UserWeb `json:"user"`
    ReviewID int `json:"reviewID"`
}

type SubjectWeb struct {
	ID     int    `json:"id"`
	Title  string `json:"title"`
	Artist string `json:"artist"`
	Image  string `json:"image"`
	Kind   string `json:"kind"`
    SpotifyID string `json:"spotifyId"`
}

type NotificationWeb struct {
    ID int `json:"id"`
    Text string `json:"text"`
    CreatedAt int64 `json:"createdAt"`
}
