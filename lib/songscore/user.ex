defmodule Songscore.User do
  use Ecto.Schema
  import Ecto.Changeset
  @derive {Jason.Encoder, only: [:id, :username, :image]}

  schema "users" do
    field(:image, :string)
    field(:password_hash, :string)
    field(:username, :string)
    has_many(:reviews, Songscore.Review)
    many_to_many(:liked_reviews, Songscore.Review, join_through: "user_likes")
    many_to_many(:disliked_reviews, Songscore.Review, join_through: "user_dislikes")

    timestamps()
  end

  def changeset(user, attrs) do
    user
    |> cast(attrs, [:id, :username, :image, :password_hash])
    |> validate_required([:id, :username])
  end
end
