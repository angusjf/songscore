<?php
$userAccount = Account::getById(0);

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

	public static function addToDatabase($subjectId, $userId, $rating, $text) {
		include "connect.php";
		$statement = $conn->prepare("INSERT INTO Reviews(subjectId, userId, rating, text) VALUES(?, ?, ?, ?);");
		$statement->bind_param("iiis", $subject, $user, $rating, $text);
		$statement->execute();
		$statement->close();
		$conn->close();
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
			$feed[] = new Review(1, new Subject(1), $this, 5, "really trash", "July 20");
			// $feed[] = 
			// SELECT * FROM Reviews WHERE Review.UserId IN (SELECT * FROM Follows where User);
		}
		return $feed;
	}

	public static function getByUsername($username) {
		/*
		$conn = new mysqli($servername, $username, $password, $database);
		$all = array();
		$results = $conn->query("INSERT INTO Reviews() );
		$conn->close();
		while($m = $results->fetch_assoc()) {
			$all[] = new Message($m['Id'], $m['text'], $m['UserId']);
		}
		return $all;
		*/
		Account::getById(1);
	}
}

class Subject { //eg a song or album (or artist?)
	public $name;
	public $artist;
	public $image;
	
	public function __construct($mbid) {
		$this->name = "More Life";
		$this->artist = "Dronk";
		$this->image = "http://images.genius.com/4672f8523e0fbf7f7848185256e946f4.1000x1000x1.jpg";
	}
}
?>
