defmodule Songscore.Subject do
  use Ecto.Schema
  import Ecto.Changeset
  @derive {Jason.Encoder, only: [:id, :artist, :image, :spotify_id, :kind, :title]}

  schema "subjects" do
    field(:artist, :string)
    field(:image, :string)
    field(:spotify_id, :string)
    field(:kind, :string)
    field(:title, :string)
    has_many(:reviews, Songscore.Review)

    timestamps()
  end

  def changeset(subject, attrs) do
    subject
    |> cast(attrs, [:title, :artist, :image, :kind, :spotify_id])
    |> validate_required([:title, :artist, :image, :kind, :spotify_id])
  end
end
