package main

import (
    "encoding/base64"
    "net/http"
    "golang.org/x/image/draw"
    "image"
    _ "image/png"
    "image/jpeg"
    "bytes"
    "fmt"
    "strings"
)

func compress(in string) string {
    if in == "" {
        return ""
    }
    in = strings.TrimPrefix(in, "data:image/png;base64,")
    in = strings.TrimPrefix(in, "data:image/jpeg;base64,")
    fmt.Println(in[0:20])

    bs, decode64err := base64.StdEncoding.DecodeString(in)
    inbuf := bytes.NewBuffer(bs)
    if decode64err != nil {
        panic(decode64err)
    }

    src, _, decodeImgErr := image.Decode(inbuf)
    if decodeImgErr != nil {
        panic(decodeImgErr)
    }

    shrunk := image.NewRGBA(image.Rect(0, 0, 256, 256))

    draw.BiLinear.Scale(shrunk, shrunk.Bounds(), src, src.Bounds(), draw.Src, nil)

    options := jpeg.Options {
        Quality: jpeg.DefaultQuality,
    }

    buffer := new(bytes.Buffer)

    jpeg.Encode(buffer, shrunk, &options)

    encoded := base64.StdEncoding.EncodeToString(buffer.Bytes())

    url := fmt.Sprintf("data:image/jpeg;base64,%s", encoded)
    return url

}

func imageUrlToBase64(url string) (string, error) {
    resp, getErr := http.Get(url)
    defer resp.Body.Close()
    if getErr != nil {
        return "", getErr
    } else {
        src, _, err := image.Decode(resp.Body)
        if err != nil {
            return "", err
        }

        shrunk := image.NewRGBA(image.Rect(0, 0, 256, 256))

        draw.BiLinear.Scale(shrunk, shrunk.Bounds(), src, src.Bounds(), draw.Src, nil)

        options := jpeg.Options {
            Quality: jpeg.DefaultQuality,
        }

        buffer := new(bytes.Buffer)

        jpeg.Encode(buffer, shrunk, &options)

        encoded := base64.StdEncoding.EncodeToString(buffer.Bytes())

        url := fmt.Sprintf("data:image/jpeg;base64,%s", encoded)

        return url, nil
    }
}
