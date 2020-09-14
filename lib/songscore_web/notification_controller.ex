defmodule SongscoreWeb.NotificationController do
  import Plug.Conn
  import Ecto.Query, only: [from: 2]
  alias Songscore.Repo
  alias Songscore.Notification

  def index(conn) do
    user_id = conn.assigns.claims["id"]

    notifications =
      Repo.all(
        from(n in Notification,
          where: n.user_id == ^user_id,
          order_by: [desc: :inserted_at]
        )
      )

    conn
    |> put_resp_content_type("application/json")
    |> resp(200, Jason.encode_to_iodata!(notifications))
  end

  def create(conn) do
    IO.inspect(conn)
    user_id = conn.assigns.claims["id"]

    from(n in Notification,
      where: n.user_id == ^user_id,
      update: [set: [seen: true]]
    )
    |> Repo.update_all([])

    notifications =
      Repo.all(
        from(n in Notification,
          where: n.user_id == ^user_id and n.seen == false
        )
      )

    conn
    |> put_resp_content_type("application/json")
    |> resp(200, Jason.encode_to_iodata!(notifications))
  end

  def check(conn) do
    user_id = conn.assigns.claims["id"]

    notifications =
      Repo.all(
        from(n in Notification,
          where: n.user_id == ^user_id and n.seen == false
        )
      )

    conn
    |> put_resp_content_type("application/json")
    |> resp(200, Jason.encode_to_iodata!(notifications != []))
  end
end
