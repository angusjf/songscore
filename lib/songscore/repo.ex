defmodule Songscore.Repo do
  use Ecto.Repo,
    otp_app: :songscore,
    adapter: Ecto.Adapters.Postgres
end
