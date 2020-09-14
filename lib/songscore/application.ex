defmodule Songscore.Application do
  use Application

  def start(_type, _args) do
    {port, ""} = Integer.parse(System.fetch_env!("PORT"))

    children = [
      Plug.Cowboy.child_spec(
        scheme: :http,
        plug: SongscoreWeb.Router,
        options: [port: port]
      ),
      Songscore.Repo,
      SongscoreWeb.SpotifyToken
    ]

    opts = [strategy: :one_for_one, name: Songscore.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
