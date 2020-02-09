package main

import (
    "fmt"
    "encoding/base64"
    "net/http"
    "io/ioutil"
)

func imageUrlToBase64(url string) (string, error) {
    resp, getErr := http.Get(url)
    defer resp.Body.Close()
    if getErr != nil {
        return "", getErr
    } else {
        data, readErr := ioutil.ReadAll(resp.Body)
        if readErr != nil {
            return "", readErr
        }
        str := fmt.Sprintf("data:image/png;base64,%s", base64.StdEncoding.EncodeToString(data))
        return str, nil
    }
}
