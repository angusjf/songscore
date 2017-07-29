# SongScore

made in python with Flask

https://songscore.herokuapp.com

## command line variables
```export FLASK_APP=songscore```
```export FLASK_DEBUG=1```

## server
to start the server on port 80 from the command line, use ```flask run```.

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

