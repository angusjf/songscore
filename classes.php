<?php
class Review {
	public $id;
	public $user;
	public $subject;
	public $rating;
	public $text;
	public $date;

	public function __construct($id, $subject, $user, $rating, $text, $date) {
		$this->id = $id;
		$this->subject = $subject;
		$this->user = $user;
		$this->rating = $rating;
		$this->text = $text;
		$this->date = $date;
	}

	public static function addToDatabase($subject, $user, $rating, $text) {
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
}

class Account {
	public $id;
	public $username;
	public $name;
	public $image;
	public $bio;

	public function __construct($id, $username, $name, $image, $bio) {
		$this->id = $id;
		$this->username = $username;
		$this->name = $name;
		$this->image = $image;
		$this->bio = $bio;
	}

	public static function getById($id) {
		return new Account($id, "@angusfindlay", "Angus Findlay", "https://pbs.twimg.com/profile_images/771860008300666880/4kN1xN5S_bigger.jpg", "kung fu kenny fanboy");
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
		$feed = [];
		for ($i = 0; $i < $number; $i++) {
			$feed[] = new Review(1, new Subject("More Life", "Dronk", "http://images.genius.com/4672f8523e0fbf7f7848185256e946f4.1000x1000x1.jpg"), $this, 5, "really trash", "July 20");
			// $feed[] = 
			// SELECT * FROM Reviews WHERE Review.UserId IN (SELECT * FROM Follows where User);
		}
		return $feed;
	}

	public static function getByUsername($username) {
		Account::getById(1);
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
