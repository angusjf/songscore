defmodule SongscoreWeb.UserController do
  import Plug.Conn
  import Ecto.Query, only: [from: 2]
  alias Songscore.Repo
  alias Songscore.User
  alias Songscore.Review

  def create(conn) do
    data = conn.params
    hashed_password = Bcrypt.hash_pwd_salt(data["password"])

    user = %User{
      image: data["image"],
      password_hash: hashed_password,
      username: data["username"]
    }

    new_user = Repo.insert!(user)

    conn
    |> put_resp_content_type("application/json")
    |> resp(200, Jason.encode_to_iodata!(new_user))
  end

  def update(conn) do
    %{"id" => id} = conn.assigns.claims

    changed_user =
      Repo.get!(User, id)
      |> IO.inspect()
      |> User.changeset(conn.params)
      |> Repo.update!()

    claims = %{
      "id" => changed_user.id,
      "username" => changed_user.username
    }

    token = SongscoreWeb.Token.generate_and_sign!(claims)

    conn
    |> put_resp_content_type("application/json")
    |> resp(200, Jason.encode_to_iodata!(%{user: changed_user, token: token}))
  end

  def show(conn) do
    %{"username" => username} = conn.params
    user = Repo.one!(from(u in User, where: u.username == ^username))

    conn
    |> put_resp_content_type("application/json")
    |> resp(200, Jason.encode_to_iodata!(user))
  end

  def reviews(conn) do
    %{"username" => username} = conn.params

    reviews =
      Repo.all(
        from(r in Review,
          join: u in User,
          on: u.id == r.user_id,
          where: u.username == ^username,
          limit: 10,
          order_by: [desc: :inserted_at]
        )
      )
      |> Repo.preload([:user, :subject, :comments, :likes, :dislikes])
      |> Repo.preload(comments: [:user])

    conn
    |> put_resp_content_type("application/json")
    |> resp(200, Jason.encode_to_iodata!(reviews))
  end

  def available(conn) do
    %{"username" => username} = conn.params
    users = Repo.all(from(u in User, where: u.username == ^username))

    conn
    |> put_resp_content_type("application/json")
    |> resp(200, Jason.encode_to_iodata!(users == []))
  end

  def followers(conn) do
    # TODO
    %{"username" => username} = conn.params
    _user = Repo.one!(from(u in User, where: u.username == ^username))
    followers = []

    conn
    |> put_resp_content_type("application/json")
    |> resp(200, Jason.encode_to_iodata!(followers))
  end

  def following(conn) do
    # TODO
    %{"username" => username} = conn.params
    _user = Repo.one!(from(u in User, where: u.username == ^username))
    following = []

    conn
    |> put_resp_content_type("application/json")
    |> resp(200, Jason.encode_to_iodata!(following))
  end

  def follow(conn) do
    # TODO
    %{"username" => username} = conn.params
    _user = Repo.one!(from(u in User, where: u.username == ^username))

    conn
    |> resp(200, "unimplemented!")
  end
end
