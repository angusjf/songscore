defmodule SongscoreWeb.Token do
  use Joken.Config

  def token_config do
    # and i drove back 30 hours
    default_claims(default_exp: 30 * 60 * 60)
  end
end
