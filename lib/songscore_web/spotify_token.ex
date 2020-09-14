defmodule SongscoreWeb.SpotifyToken do
  use Agent

  def start_link(_opts) do
    Agent.start_link(fn -> {"", Time.new(0, 0, 0)} end, name: :tokens)
  end

  def get() do
    {token, exp} = Agent.get(:tokens, & &1)

    if Time.utc_now() > exp do
      {new_token, new_exp} = get_fresh_token()
      :ok = Agent.update(:tokens, fn _ -> {new_token, new_exp} end)
      new_token
    else
      token
    end
  end

  defp get_fresh_token() do
    id = System.fetch_env!("SPOTIFY_CLIENT_ID")
    secret = System.fetch_env!("SPOTIFY_CLIENT_SECRET")

    # REQUEST BODY PARAMETER: grant_type=client_credentials
    data = {:form, [{"grant_type", "client_credentials"}]}
    data_size = byte_size("grant_type") + byte_size("client_credentials")

    # HEADER: "Authorization: Basic ZjM4ZjAw...WY0MzE"
    spotifyAuth = Base.encode64("#{id}:#{secret}")

    headers = [
      {"Authorization", "Basic #{spotifyAuth}"},
      {"Content-Type", "application/x-www-form-urlencoded"},
      {"Content-Length", data_size}
    ]

    resp = HTTPoison.post!("https://accounts.spotify.com/api/token", data, headers)
    body = Jason.decode!(resp.body)

    access_token = body["access_token"]
    exp = Time.add(Time.utc_now(), body["expires_in"], :second)

    {access_token, exp}
  end
end
