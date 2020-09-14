defmodule SongscoreWeb.Router do
  use Plug.Router

  alias SongscoreWeb.{
    AuthController,
    NotificationController,
    ReviewController,
    SubjectController,
    UserController
  }

  plug(Plug.Logger, log: :debug)
  plug(CORSPlug)

  plug(Plug.Static,
    at: "/",
    from: :songscore,
    gzip: false,
    only: ~w(main.js assets favicon.ico)
  )

  plug(:add_auth)
  plug(:match)

  plug(Plug.Parsers,
    parsers: [:json],
    pass: ["application/json"],
    json_decoder: Jason
  )

  plug(:dispatch)

  get "/" do
    conn
    |> send_file(200, "priv/static/index.html")
  end

  get("/api/feeds/:username", do: ReviewController.feed(conn))

  post("/api/reviews", do: ReviewController.create(conn))
  delete("/api/reviews/:review_id", do: ReviewController.delete(conn))
  get("/api/reviews/:review_id", do: ReviewController.show(conn))
  post("/api/reviews/:review_id/like", do: ReviewController.like(conn))
  post("/api/reviews/:review_id/dislike", do: ReviewController.dislike(conn))
  post("/api/reviews/:review_id/comments", do: ReviewController.comment(conn))

  post("/api/users", do: UserController.create(conn))
  put("/api/users", do: UserController.update(conn))
  get("/api/users/:username", do: UserController.show(conn))
  get("/api/users/:username/reviews", do: UserController.reviews(conn))
  get("/api/users/:username/available", do: UserController.available(conn))
  get("/api/users/:username/followers", do: UserController.followers(conn))
  get("/api/users/:username/following", do: UserController.following(conn))
  post("/api/users/:username/follow", do: UserController.follow(conn))

  get("/api/subjects/search", do: SubjectController.search(conn))

  get("/api/notifications/new", do: NotificationController.check(conn))
  get("/api/notifications", do: NotificationController.index(conn))
  post("/api/notifications", do: NotificationController.create(conn))

  post("/api/auth", do: AuthController.create(conn))

  match(_, do: send_resp(conn, 404, "route not found!"))

  def add_auth(conn, _) do
    if get_req_header(conn, "authorization") != [] do
      result =
        conn
        |> get_req_header("authorization")
        |> List.first()
        |> String.trim_leading("Bearer ")
        |> SongscoreWeb.Token.verify_and_validate()

      case result do
        {:ok, claims} ->
          conn
          |> assign(:claims, claims)

        {:error, _} ->
          conn
          |> send_resp(401, "invalid or expired token")
          |> halt
      end
    else
      conn
    end
  end
end
