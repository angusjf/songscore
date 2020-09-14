defmodule Songscore.Application do
  use Application

  def start(_type, _args) do
    children = [
      Plug.Cowboy.child_spec(
        scheme: :http,
        plug: SongscoreWeb.Router,
        options: [port: 4000]
      ),
      Songscore.Repo,
      SongscoreWeb.SpotifyToken
    ]

    opts = [strategy: :one_for_one, name: Songscore.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
