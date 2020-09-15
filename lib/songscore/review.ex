defmodule Songscore.Review do
  use Ecto.Schema
  import Ecto.Changeset

  @derive {Jason.Encoder,
           only: [:id, :stars, :text, :user, :subject, :comments, :likes, :dislikes, :inserted_at]}

  schema "reviews" do
    field(:stars, :integer)
    field(:text, :string)
    belongs_to(:user, Songscore.User)
    belongs_to(:subject, Songscore.Subject)
    has_many(:comments, Songscore.Comment)
    many_to_many(:likes, Songscore.User, join_through: "user_likes")
    many_to_many(:dislikes, Songscore.User, join_through: "user_dislikes")

    timestamps()
  end

  def changeset(review, attrs) do
    review
    |> cast(attrs, [:text, :stars])
    |> validate_required([:stars])
    |> assoc_constraint(:user)
    |> cast_assoc(:subject)
    |> assoc_constraint(:subject)
  end
end
