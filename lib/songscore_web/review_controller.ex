defmodule SongscoreWeb.ReviewController do
  import Plug.Conn
  import Ecto.Query, only: [from: 2]
  alias Songscore.{Repo, Review, Notification, Comment, User}

  def feed(conn) do
    reviews =
      Repo.all(from(r in Review, order_by: [desc: :inserted_at], limit: 6))
      |> Repo.preload([:user, :subject, :comments, :likes, :dislikes])
      |> Repo.preload(comments: [:user])

    conn
    |> put_resp_content_type("application/json")
    |> resp(200, Jason.encode_to_iodata!(reviews))
  end

  def show(conn) do
    %{"review_id" => id} = conn.params
    {id, ""} = Integer.parse(id)
    review = Repo.get!(Review, id)

    conn
    |> put_resp_content_type("application/json")
    |> resp(200, Jason.encode_to_iodata!(review))
  end

  def create(conn) do
    data = conn.params

    new_review =
      Repo.get!(User, data["user"]["id"])
      |> Ecto.build_assoc(:reviews)
      |> Repo.preload([:subject, :user, :comments, :likes, :dislikes])
      |> Review.changeset(data)
      |> IO.inspect
      |> Repo.insert!

    conn
    |> put_resp_content_type("application/json")
    |> resp(200, Jason.encode_to_iodata!(new_review))
  end

  def delete(conn) do
    %{"review_id" => id} = conn.params
    {id_int, ""} = Integer.parse(id)

    old_review =
      Repo.get(Review, id_int)
      |> Repo.preload([:subject, :user, :comments, :likes, :dislikes])
      |> Repo.delete!

    conn
    |> put_resp_content_type("application/json")
    |> resp(200, Jason.encode_to_iodata!(old_review))
  end

  def like(conn) do
    data = conn.params

    {review_id, ""} = Integer.parse(data["review_id"])

    review =
      Repo.one!(review_id)
      |> Repo.preload(:subject)

    # TODO

    username = data["user"]["username"]
    subject_name = review.subject.title

    Repo.insert(%Notification{
      text: "@#{username} disliked your review of #{subject_name}",
      seen: false,
      user_id: data["user"]["id"],
      review_id: review_id
    })

    conn
    |> put_resp_content_type("application/json")
    |> resp(200, Jason.encode_to_iodata!(review))
  end

  def dislike(conn) do
    data = conn.params

    {review_id, ""} = Integer.parse(data["review_id"])

    review =
      Repo.one!(review_id)
      |> Repo.preload(:subject)

    username = data["user"]["username"]
    subject_name = review.subject.title

    # TODO
    Repo.insert(%Notification{
      text: "@#{username} disliked your review of #{subject_name}",
      seen: false,
      user_id: data["user"]["id"],
      review_id: review_id
    })

    Repo.update!(review)
      # |> Repo.preload(:tags)
      # |> Ecto.Changeset.cast(params, [:title]) # No need to allow :tags as we put them directly
      # |> Ecto.Changeset.put_assoc(:likes, tags) # Explicitly set the tags

    conn
    |> put_resp_content_type("application/json")
    |> resp(200, Jason.encode_to_iodata!(review))
  end

  def comment(conn) do
    data = conn.params

    {review_id, ""} = Integer.parse(data["review_id"])

    Repo.insert!(%Comment{
      text: data["text"],
      user_id: data["user"]["id"],
      review_id: review_id
    })

    review =
      Repo.get!(Review, review_id)
      |> Repo.preload([:user, :subject, :comments, :likes, :dislikes])
      |> Repo.preload(comments: [:user])

    username = data["user"]["username"]
    subject_name = review.subject.title

    Repo.insert(%Notification{
      text: "@#{username} commented on your review of #{subject_name}",
      seen: false,
      user_id: data["user"]["id"],
      review_id: review_id
    })

    conn
    |> put_resp_content_type("application/json")
    |> resp(200, Jason.encode_to_iodata!(review))
  end
end
