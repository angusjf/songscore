package main

import (
    "encoding/json"
	"net/http"
	"net/url"
    "encoding/base64"
    "time"
    "strconv"
    "strings"
    "io"
    "fmt"
)

type SpotifyToken struct {
    AccessToken string `json:"access_token"`
    ExpiresIn int `json:"expires_in"`
}

func getSpotifyToken(id, secret string) ([]byte, time.Time, error) {
    // REQUEST BODY PARAMETER: grant_type=client_credentials
    data := url.Values{}
    data.Set("grant_type", "client_credentials")

    // POST
    // https://accounts.spotify.com/api/token
    req, err := http.NewRequest(
        "POST",
        "https://accounts.spotify.com/api/token",
        strings.NewReader(data.Encode()),
    )

    // HEADER: "Authorization: Basic ZjM4ZjAw...WY0MzE"
    spotifyAuth := base64.StdEncoding.EncodeToString([]byte(id + ":" + secret))
    req.Header.Set("Authorization", "Basic " + spotifyAuth)
    req.Header.Add("Content-Type", "application/x-www-form-urlencoded")
    req.Header.Add("Content-Length", strconv.Itoa(len(data.Encode())))

    // SEND!
    client := &http.Client{}
    resp, err := client.Do(req)
    defer resp.Body.Close()

    /// PARSE
    if err != nil {
        return nil, time.Now(), err
    } else {
        var data SpotifyToken
        json.NewDecoder(resp.Body).Decode(&data)
        exp := time.Now().Add(time.Duration(data.ExpiresIn) * time.Second)
        return []byte(data.AccessToken), exp, nil
    }
}

func getSpotifyResults(token, query string, dst io.Writer) error {
    spotify_api_url, _ := url.Parse(
        "https://api.spotify.com/v1/search",
    )

    x := spotify_api_url.Query()
    x.Add("q", query)
    x.Add("type", "track")
    spotify_api_url.RawQuery = x.Encode()

    req, _ := http.NewRequest(
        "GET",
        spotify_api_url.String(),
        nil,
    )

    req.Header.Set("Authorization", "Bearer " + string(token))

    client := &http.Client{}
    resp, _ := client.Do(req)
    defer resp.Body.Close()

    fmt.Printf(" >>>>>>> %s\n", resp.Status)

    io.Copy(dst, resp.Body)
    return nil
}
