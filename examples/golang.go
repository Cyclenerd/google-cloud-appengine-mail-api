package main

// Send email via Mail API
// https://github.com/Cyclenerd/google-cloud-appengine-mail-api

import (
  "fmt"
  "net/http"
  "net/url"
  "io/ioutil"
  "strings"
)

func main() {

  api_password := "YOUR_API_PASSWORD"

  api_url := "https://PROJECT_ID.REGION_ID.r.appspot.com/messages"

  data := url.Values{}
  data.Set("to", "test@nkn-it.de")
  data.Set("subject", "Go Example")
  data.Set("text", "This is a simple test.")

  client := &http.Client{}
  req, err := http.NewRequest("POST", api_url, strings.NewReader(data.Encode()))
  req.SetBasicAuth("api", api_password)
  req.Header.Add("Content-Type", "application/x-www-form-urlencoded")
  res, err := client.Do(req)

  body, err := ioutil.ReadAll(res.Body)
  if err != nil {
    fmt.Println(err)
    return
  }
  fmt.Println(string(body))
}