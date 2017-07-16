# SongSearch

## server
to start the server on port 80 from the command line, use ```sudo php -S localhost:80```.

(you only need ```sudo``` if you're using port 80)

## json
example structure for json file sent from getfeed.php
```
{
	"user" : {
		"image" : "https://www.example.com/img.jpg",
		"name" : "findlang"
	},
	"subject" : {
		"image" : "https://www.example.com/img.jpg",
		"name" : "POWER"
	},
	"rating" : 4,
	"text" : "i thought this song was really #terrible"
}
```
