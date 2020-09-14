import Mix.Config

config :joken,
  default_signer: "secret"

config :songscore, Songscore.Repo,
  adapter: Ecto.Adapters.Postgres,
  url: System.fetch_env!("DATABASE_URL"),
  show_sensitive_data_on_connection_error: true,
  ssl: true
