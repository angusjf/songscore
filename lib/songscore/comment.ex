defmodule Songscore.Comment do
  use Ecto.Schema
  import Ecto.Changeset
  @derive {Jason.Encoder, only: [:text, :user, :review_id]}

  schema "comments" do
    field(:text, :string)
    belongs_to(:user, Songscore.User)
    belongs_to(:review, Songscore.Review)

    timestamps()
  end

  def changeset(comment, attrs) do
    comment
    |> cast(attrs, [:id, :text])
    |> validate_required([:text])
  end
end
