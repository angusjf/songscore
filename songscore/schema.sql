drop table if exists users;
create table users (
	id int primary key autoincrement,
	name varchar not null,
	username varchar not null unique,
	image varchar not null
)

drop table if exists reviews;
create table reviews (
	id int primary key autoincrement,
	userid int foreign key references users(id),
	mbid int not null,
	rating int not null check (rating <=5 and rating >= 0),
	upvotes int default 0 check (upvotes >= 0),
	downvotes int default 0 check (downvotes >= 0),
	date datetime default getdate()
);

drop table if exists replies;
create table replies (
	userid int foreign key references users(id),
	reviewid int foreign key references reviews(id),
	text varchar not null,
	upvotes int default 0 check (upvotes >= 0),
	downvotes int default 0 check (downvotes >= 0)
);
