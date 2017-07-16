<?php
class Review {
	public $id;
	public $user;
	public $subject;
	public $score;
	public $text;

	public function __construct($id, $subject, $user, $score, $text) {
		$this->id = $id;
		$this->subject = $subject;
		$this->user = $user;
		$this->score = $score;
		$this->text = $text;
	}

	public function toHtml() {
		return "
		<div class='review'>
			<img class='userPicture' src='{$this->user->image}'>
			<div class='userName'>{$this->user->name}</div>
			<img class='subjectPicture' src='{$this->subject->image}'>
			<div class='subjectName'>{$this->subject->name}</div>
			<div class='rating'>{$this->rating}</div>
			<div class='text'>{$this->text}</div>
		</div>
		";
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
		$this->name = name;
		$this->artist = artist;
		$this->image = image;
	}
}

$userAccount = Account::getById(0);
?>
