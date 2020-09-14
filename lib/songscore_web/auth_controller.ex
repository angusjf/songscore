defmodule SongscoreWeb.AuthController do
  import Plug.Conn
  import Ecto.Query, only: [from: 2]
  alias Songscore.Repo
  alias Songscore.User

  def create(conn) do
    username = conn.params["username"]
    password = conn.params["password"]
    user = Repo.one!(from(u in User, where: u.username == ^username))

    if Bcrypt.verify_pass(password, user.password_hash) do
      claims = %{
        "id" => user.id,
        "username" => user.username
      }

      token = SongscoreWeb.Token.generate_and_sign!(claims)

      conn
      |> put_resp_content_type("application/json")
      |> resp(200, Jason.encode_to_iodata!(%{user: user, token: token}))
    else
      conn
      |> resp(401, "Incorrect Password!")
    end
  end
end
