defmodule SongscoreWeb.SubjectController do
  import Plug.Conn

  def search(conn) do
    query = conn.params["q"]
    url = 'https://api.spotify.com/v1/search?q=#{query}&type=track'
    headers = [{'Authorization', 'Bearer #{SongscoreWeb.SpotifyToken.get()}'}]
    resp = HTTPoison.get!(url, headers)

    conn
    |> put_resp_content_type("application/json")
    |> send_resp(200, resp.body)
  end
end
