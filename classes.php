<?php
class Review {
	public $id;
	public $user;
	public $subject;
	public $rating;
	public $text;

	public function __construct($id, $subject, $user, $rating, $text) {
		$this->id = $id;
		$this->subject = $subject;
		$this->user = $user;
		$this->rating = $rating;
		$this->text = $text;
	}

	public function toJson() {
		return json_encode($this);
	}
}

class Account {
	public $id;
	public $name;
	public $image;
	public $bio;

	public function __construct($id, $name, $image, $bio) {
		$this->id = $id;
		$this->name = $name;
		$this->image = $image;
		$this->bio = $bio;
	}

	public static function getById($id) {
		return new Account($id, "@angusfindlay", "https://pbs.twimg.com/profile_images/771860008300666880/4kN1xN5S_bigger.jpg", "kung fu kenny fanboy");
		/*
		$conn = new mysqli("localhost", "root", "password", "db");
		$all = array();
		$results = $conn->query("SELECT * FROM Accounts WHERE UserId = '$this->id' ORDER BY id DESC;");
		$conn->close();
		while($m = $results->fetch_assoc()) {
			$all[] = new Message($m['Id'], $m['text'], $m['UserId']);
		}
		return $all;
		*/
	}

	public function getReviews() {
		$reviews = array();
		return $reviews;
	}

	public function getFollowers() {
		$followers = array();
		return $followers;
	}

	public function getFollowing() {
		$following = array();
		return $following;
	}

	public function getFeed($number) {
		return array(
			new Review(
				1, new Subject("More Life", "Dronk", "http://images.genius.com/4672f8523e0fbf7f7848185256e946f4.1000x1000x1.jpg"), $this, 5, "really trash"
			),
		);
	}
}

class Subject { //eg a song or album (or artist?)
	public $name;
	public $artist;
	public $image;
	
	public function __construct($name, $artist, $image) {
		$this->name = $name;
		$this->artist = $artist;
		$this->image = $image;
	}
}

$userAccount = Account::getById(0);
?>
