defmodule Songscore.MixProject do
  use Mix.Project

  def project do
    [
      app: :songscore,
      version: "0.1.0",
      elixir: "~> 1.10",
      start_permanent: Mix.env() == :prod,
      deps: deps()
    ]
  end

  def application do
    [
      extra_applications: [:logger],
      mod: {Songscore.Application, []}
    ]
  end

  defp deps do
    [
      {:httpoison, "~> 1.6"},
      {:bcrypt_elixir, "~> 2.0"},
      {:joken, "~> 2.0"},
      {:cors_plug, "~> 1.5"},
      {:ecto_sql, "~> 3.4"},
      {:postgrex, ">= 0.0.0"},
      {:jason, "~> 1.0"},
      {:plug_cowboy, "~> 2.0"}
    ]
  end
end
