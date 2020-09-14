defmodule Songscore.Notification do
  use Ecto.Schema
  import Ecto.Changeset
  @derive {Jason.Encoder, only: [:id, :text, :seen, :user_id, :review_id, :inserted_at]}

  schema "notifications" do
    field(:text, :string)
    field(:seen, :boolean)
    belongs_to(:user, Songscore.User)
    belongs_to(:review, Songscore.Review)

    timestamps()
  end

  def changeset(notification, attrs) do
    notification
    |> cast(attrs, [:id, :text, :seen, :user_id, :review_id])
    |> validate_required([:text, :user_id, :review_id])
  end
end
