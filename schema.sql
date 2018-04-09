--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.8
-- Dumped by pg_dump version 10.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: comments; Type: TABLE; Schema: public; Owner: yjrybcwtcrpgic
--

CREATE TABLE public.comments (
    user_id integer,
    review_id integer,
    text text,
    date timestamp without time zone DEFAULT now() NOT NULL,
    id integer NOT NULL,
    CONSTRAINT comments_text_check CHECK ((length(text) > 0))
);


ALTER TABLE public.comments OWNER TO yjrybcwtcrpgic;

--
-- Name: comments_id_seq; Type: SEQUENCE; Schema: public; Owner: yjrybcwtcrpgic
--

CREATE SEQUENCE public.comments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.comments_id_seq OWNER TO yjrybcwtcrpgic;

--
-- Name: comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER SEQUENCE public.comments_id_seq OWNED BY public.comments.id;


--
-- Name: dislikes; Type: TABLE; Schema: public; Owner: yjrybcwtcrpgic
--

CREATE TABLE public.dislikes (
    user_id integer,
    review_id integer
);


ALTER TABLE public.dislikes OWNER TO yjrybcwtcrpgic;

--
-- Name: dislikes_user_id_seq; Type: SEQUENCE; Schema: public; Owner: yjrybcwtcrpgic
--

CREATE SEQUENCE public.dislikes_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dislikes_user_id_seq OWNER TO yjrybcwtcrpgic;

--
-- Name: dislikes_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER SEQUENCE public.dislikes_user_id_seq OWNED BY public.dislikes.user_id;


--
-- Name: follows; Type: TABLE; Schema: public; Owner: yjrybcwtcrpgic
--

CREATE TABLE public.follows (
    follower_id integer,
    following_id integer
);


ALTER TABLE public.follows OWNER TO yjrybcwtcrpgic;

--
-- Name: likes; Type: TABLE; Schema: public; Owner: yjrybcwtcrpgic
--

CREATE TABLE public.likes (
    user_id integer,
    review_id integer
);


ALTER TABLE public.likes OWNER TO yjrybcwtcrpgic;

--
-- Name: notifications; Type: TABLE; Schema: public; Owner: yjrybcwtcrpgic
--

CREATE TABLE public.notifications (
    id integer NOT NULL,
    type text,
    date timestamp without time zone DEFAULT now() NOT NULL,
    CONSTRAINT notifications_type_check CHECK (((type = 'mention'::text) OR (type = 'upvote'::text) OR (type = 'downvote'::text) OR (type = 'comment'::text)))
);


ALTER TABLE public.notifications OWNER TO yjrybcwtcrpgic;

--
-- Name: notifications_id_seq; Type: SEQUENCE; Schema: public; Owner: yjrybcwtcrpgic
--

CREATE SEQUENCE public.notifications_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.notifications_id_seq OWNER TO yjrybcwtcrpgic;

--
-- Name: notifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER SEQUENCE public.notifications_id_seq OWNED BY public.notifications.id;


--
-- Name: reviews; Type: TABLE; Schema: public; Owner: yjrybcwtcrpgic
--

CREATE TABLE public.reviews (
    id integer NOT NULL,
    user_id integer,
    text text,
    subject_id integer,
    score integer NOT NULL,
    date timestamp without time zone DEFAULT now() NOT NULL,
    CONSTRAINT reviews_score_check CHECK (((score >= 0) AND (score <= 5)))
);


ALTER TABLE public.reviews OWNER TO yjrybcwtcrpgic;

--
-- Name: reviews_id_seq; Type: SEQUENCE; Schema: public; Owner: yjrybcwtcrpgic
--

CREATE SEQUENCE public.reviews_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reviews_id_seq OWNER TO yjrybcwtcrpgic;

--
-- Name: reviews_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER SEQUENCE public.reviews_id_seq OWNED BY public.reviews.id;


--
-- Name: subjects; Type: TABLE; Schema: public; Owner: yjrybcwtcrpgic
--

CREATE TABLE public.subjects (
    id integer NOT NULL,
    type text,
    name name NOT NULL,
    image character varying DEFAULT '/static/images/subject.png'::character varying NOT NULL,
    artist_name character varying NOT NULL,
    CONSTRAINT subjects_type_check CHECK (((type = 'album'::text) OR (type = 'song'::text)))
);


ALTER TABLE public.subjects OWNER TO yjrybcwtcrpgic;

--
-- Name: subjects_id_seq; Type: SEQUENCE; Schema: public; Owner: yjrybcwtcrpgic
--

CREATE SEQUENCE public.subjects_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subjects_id_seq OWNER TO yjrybcwtcrpgic;

--
-- Name: subjects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER SEQUENCE public.subjects_id_seq OWNED BY public.subjects.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: yjrybcwtcrpgic
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name text NOT NULL,
    username text NOT NULL,
    email text NOT NULL,
    password text NOT NULL,
    register_date timestamp without time zone DEFAULT now() NOT NULL,
    picture text DEFAULT '/static/images/profile.png'::text NOT NULL
);


ALTER TABLE public.users OWNER TO yjrybcwtcrpgic;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: yjrybcwtcrpgic
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO yjrybcwtcrpgic;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: comments id; Type: DEFAULT; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER TABLE ONLY public.comments ALTER COLUMN id SET DEFAULT nextval('public.comments_id_seq'::regclass);


--
-- Name: notifications id; Type: DEFAULT; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER TABLE ONLY public.notifications ALTER COLUMN id SET DEFAULT nextval('public.notifications_id_seq'::regclass);


--
-- Name: reviews id; Type: DEFAULT; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER TABLE ONLY public.reviews ALTER COLUMN id SET DEFAULT nextval('public.reviews_id_seq'::regclass);


--
-- Name: subjects id; Type: DEFAULT; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER TABLE ONLY public.subjects ALTER COLUMN id SET DEFAULT nextval('public.subjects_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: comments; Type: TABLE DATA; Schema: public; Owner: yjrybcwtcrpgic
--

COPY public.comments (user_id, review_id, text, date, id) FROM stdin;
3	11	test comment hello	2018-04-05 14:07:30.682287	3
3	23	erm think again ya bish	2018-04-08 12:05:14.613168	4
3	26	whatever	2018-04-08 15:13:37.402428	5
\.


--
-- Data for Name: dislikes; Type: TABLE DATA; Schema: public; Owner: yjrybcwtcrpgic
--

COPY public.dislikes (user_id, review_id) FROM stdin;
\.


--
-- Data for Name: follows; Type: TABLE DATA; Schema: public; Owner: yjrybcwtcrpgic
--

COPY public.follows (follower_id, following_id) FROM stdin;
3	5
3	2
3	4
\.


--
-- Data for Name: likes; Type: TABLE DATA; Schema: public; Owner: yjrybcwtcrpgic
--

COPY public.likes (user_id, review_id) FROM stdin;
3	7
\.


--
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: yjrybcwtcrpgic
--

COPY public.notifications (id, type, date) FROM stdin;
\.


--
-- Data for Name: reviews; Type: TABLE DATA; Schema: public; Owner: yjrybcwtcrpgic
--

COPY public.reviews (id, user_id, text, subject_id, score, date) FROM stdin;
7	4	Good beat, solid whipability, but a pretty basic and forgettable Tyler song overall.	3	4	2018-04-04 13:04:04.507081
8	2	erm idk what to say	4	3	2018-04-04 13:04:04.507081
9	5	Great surname 10/10	5	5	2018-04-04 13:04:04.507081
12	3	personally very glad kanye came back out his coma	8	5	2018-04-04 14:55:09.851747
1	3	good stuff <3	1	4	2018-04-04 13:04:04.507081
11	4	WOO WOO	7	5	2018-04-04 13:04:04.507081
5	3	brazy album	2	5	2018-04-04 13:04:04.507081
10	2	ok	6	5	2018-04-04 13:04:04.507081
14	3	for real this is super good, last track gets the feels 10/10	9	5	2018-04-04 19:55:46.392315
15	3	LOGOUT is a jam 	10	4	2018-04-05 08:27:47.895185
16	3	gheeze	11	4	2018-04-06 08:03:16.640207
17	3	the only good rock music	12	5	2018-04-06 12:50:05.200234
18	2	WELL I'VE BEEN CARVED IN FIRE	13	5	2018-04-06 13:18:43.652953
19	4	Literally feels like I'm doing cocaine through my ears	14	5	2018-04-06 13:38:50.978205
20	4	One of the best albums to do work to	15	5	2018-04-06 13:39:25.216223
21	4	mlljkljlkjlkjljljlkj;lkj;lkj;lkj;lkj	16	5	2018-04-06 16:05:40.932896
22	6	I FUCKING LOVE IT AND BEST ALBUM OF 2018 SO FAR	17	5	2018-04-07 22:18:30.916582
23	7	Is shit	18	1	2018-04-07 22:18:55.514876
24	2	10000000 yes	19	3	2018-04-07 22:21:21.090422
25	7	Absolute banger	19	5	2018-04-07 22:21:59.367153
26	6	Its a song not too catchy but has some good real life inserts that make this a solid 3-4 star, overall very impressed by what i. Hearing 	20	4	2018-04-07 22:22:55.405769
27	8	good	21	5	2018-04-07 22:25:48.720097
28	8	scream	22	5	2018-04-07 22:29:44.343295
30	3	the boys are back at it 	23	4	2018-04-08 13:54:53.313791
\.


--
-- Data for Name: subjects; Type: TABLE DATA; Schema: public; Owner: yjrybcwtcrpgic
--

COPY public.subjects (id, type, name, image, artist_name) FROM stdin;
1	album	An Awesome Wave	https://lastfm-img2.akamaized.net/i/u/174s/4bbd6ca7059b413c80d6a31a818b835b.png	alt-J
2	album	Still Brazy (Deluxe)	https://lastfm-img2.akamaized.net/i/u/174s/2136d7d97e1cbd17735320326b0c29ef.png	YG
3	album	OKRA	https://lastfm-img2.akamaized.net/i/u/174s/fb6afd75a2b2ef80f32597f6f70167dc.png	Tyler, the Creator
4	album	Big Fish Theory	https://lastfm-img2.akamaized.net/i/u/174s/85540f3f9e225b93de5972556ceb97d6.png	Vince Staples
5	album	Candylion	https://lastfm-img2.akamaized.net/i/u/174s/15ef4533cfa040b5beb4f4e1afbf5595.png	Gruff Rhys
6	album	For Emma, Forever Ago	https://lastfm-img2.akamaized.net/i/u/174s/d28dafe85cb24915a65f0dfd135c491b.png	Bon Iver
7	album	BOOGIE	https://lastfm-img2.akamaized.net/i/u/174s/f85ada83644d28de9fb0989c83fa8c3e.png	BROCKHAMPTON
8	album	Yeezus	https://lastfm-img2.akamaized.net/i/u/174s/3314a0a30dfd33f292d6a76dfe3085b4.png	Kanye West
9	album	XXX	https://lastfm-img2.akamaized.net/i/u/174s/c32cd109176d4241b2b68183b631a47c.png	Danny Brown
10	album	CARE FOR ME	https://lastfm-img2.akamaized.net/i/u/174s/2b7e64ed4515523ed6b6e79d1593793f.png	Saba
11	album	REDMERCEDES	https://lastfm-img2.akamaized.net/i/u/174s/509ce4049c8ba2fa814e61e550475c19.png	Aminé
12	album	Twin Fantasy	https://lastfm-img2.akamaized.net/i/u/174s/f90546f29c1b4c2dd6efba2df336bdb5.png	Car Seat Headrest
13	album	22, A Million	https://lastfm-img2.akamaized.net/i/u/174s/cd5a54c0665691d78477d301755d7706.png	Bon Iver
14	album	Neō Wax Bloom	https://lastfm-img2.akamaized.net/i/u/174s/50a7053812c29767cf530d1af935d22a.png	Iglooghost
15	album	Migration	https://lastfm-img2.akamaized.net/i/u/174s/0c38acf497e651c79a0a1747b96fab6f.png	Bonobo
16	album	DAMN.	https://lastfm-img2.akamaized.net/i/u/174s/8a59ed3a9c71cb5113325e2026889e4a.png	Kendrick Lamar
17	album	Reasons	https://lastfm-img2.akamaized.net/i/u/174s/91c72d58b03e16303703bac571c2f871.png	S-X
18	album	To Pimp a Butterfly	https://lastfm-img2.akamaized.net/i/u/174s/6c0c2b3d7f95361446aaaad9c64dc798.png	Kendrick Lamar
19	album	'Til It's Over - Single	https://lastfm-img2.akamaized.net/i/u/174s/78e5893b6922317ee7248ff846f86825.png	Anderson .Paak
20	album	Oh What a World		Mouth Breather
21	album	Malibu	https://lastfm-img2.akamaized.net/i/u/174s/99d7a86815b46e4965703b6db19030cf.png	Miley Cyrus
22	album	Collide With the Sky	https://lastfm-img2.akamaized.net/i/u/174s/8d86ef9865474987be20c7cbce363701.png	Pierce The Veil
23	album	Campfire	https://lastfm-img2.akamaized.net/i/u/174s/df19d798dedd21061a72e9a402833348.png	Aminé
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: yjrybcwtcrpgic
--

COPY public.users (id, name, username, email, password, register_date, picture) FROM stdin;
3	Angus	eeee	eee@gmail.com	$5$rounds=535000$1oYAueo/5g8yPGNR$i1BNmM42X1h/jF1wRTgMJPgk6vx76ExySV.oSQPndFA	2018-04-04 13:03:52.590021	/static/images/profile.png
4	Rhys Harris	RhysCHarris	rhys.harris@hotmail.co.uk	$5$rounds=535000$QO/v.8cApMVFIiYV$LFCovXJoiXXLWkW9mL9tjrzh82hpEnQgU0JokU3QaVC	2018-04-04 13:03:52.590021	/static/images/profile.png
5	Rhys	Rhys	rhysharris1234@hotmail.co.uk	$5$rounds=535000$R4KsL.Sbd73s/x65$g65n3Z4B7mJhB7ztQcyFBFZXM.6cNgl7eCh14k5.qD9	2018-04-04 13:03:52.590021	/static/images/profile.png
6	Lewis 	Big Dick Bowen 🍆🍆🍆🍆🍆	loubowen71@gmail.com	$5$rounds=535000$bu.YQXZZLXHE1MUO$awVEj4wzYYXswIzE.vCqIM.OETQQ1hnIeidxmzY6UPC	2018-04-07 22:17:08.511476	/static/images/profile.png
7	Lewis	Lewis	lewis poulter@yahoo.co.uk	$5$rounds=535000$roMhZJz4DDLxC7dX$di5.6UQFoCmddFybhjvEuPv42XPDexLR3qnzd3i/.z7	2018-04-07 22:18:03.987867	/static/images/profile.png
8	Abigail 	ajpscore	19abemail@gmail.com	$5$rounds=535000$QpQFA.p5.MGTOyR.$eikBWcg9/jRczCDr9SQB1dmM2GaUhanjqHNcm09wIi6	2018-04-07 22:19:16.941463	/static/images/profile.png
16	RegisterHerokuTest	RegisterHerokuTest	RegisterHerokuTest	$5$rounds=535000$yv3LmbmRjzJdtbhj$x.J5PIADT1bH2UomyGwjqTkiNflJqW7KalfPyluy9x2	2018-04-08 12:27:47.055727	/static/images/profile.png
2	Hugo	hugo	hugo.findlay@gmail.com	$5$rounds=535000$1H.y5jd146klp6c5$PuPBA6.wgvlHLdTJba4KW/77cXfpshTiOmWA3yR9Fx.	2018-04-04 13:03:52.590021	/static/images/profile.png
17	testdisplayname"; drop table notifications;	testusername	testemail	$5$rounds=535000$4XlpB7gk4es0vSqR$8.9HaSa7ysUbKlgY43P5awVVOM8Q8hd3K7ZqYKfRvI1	2018-04-08 16:29:10.594579	/static/images/profile.png
\.


--
-- Name: comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yjrybcwtcrpgic
--

SELECT pg_catalog.setval('public.comments_id_seq', 5, true);


--
-- Name: dislikes_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yjrybcwtcrpgic
--

SELECT pg_catalog.setval('public.dislikes_user_id_seq', 1, false);


--
-- Name: notifications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yjrybcwtcrpgic
--

SELECT pg_catalog.setval('public.notifications_id_seq', 1, false);


--
-- Name: reviews_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yjrybcwtcrpgic
--

SELECT pg_catalog.setval('public.reviews_id_seq', 30, true);


--
-- Name: subjects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yjrybcwtcrpgic
--

SELECT pg_catalog.setval('public.subjects_id_seq', 23, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yjrybcwtcrpgic
--

SELECT pg_catalog.setval('public.users_id_seq', 17, true);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (id);


--
-- Name: subjects subjects_pkey; Type: CONSTRAINT; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER TABLE ONLY public.subjects
    ADD CONSTRAINT subjects_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: comments comments_review_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_review_id_fkey FOREIGN KEY (review_id) REFERENCES public.reviews(id) ON DELETE CASCADE;


--
-- Name: comments comments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: dislikes dislikes_review_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER TABLE ONLY public.dislikes
    ADD CONSTRAINT dislikes_review_id_fkey FOREIGN KEY (review_id) REFERENCES public.reviews(id) ON DELETE CASCADE;


--
-- Name: dislikes dislikes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER TABLE ONLY public.dislikes
    ADD CONSTRAINT dislikes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: follows follows_follower_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER TABLE ONLY public.follows
    ADD CONSTRAINT follows_follower_id_fkey FOREIGN KEY (follower_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: follows follows_following_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER TABLE ONLY public.follows
    ADD CONSTRAINT follows_following_id_fkey FOREIGN KEY (following_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: reviews reviews_subject_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES public.subjects(id) ON DELETE CASCADE;


--
-- Name: reviews reviews_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: likes votes_review_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER TABLE ONLY public.likes
    ADD CONSTRAINT votes_review_id_fkey FOREIGN KEY (review_id) REFERENCES public.reviews(id) ON DELETE CASCADE;


--
-- Name: likes votes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: yjrybcwtcrpgic
--

ALTER TABLE ONLY public.likes
    ADD CONSTRAINT votes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: LANGUAGE plpgsql; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON LANGUAGE plpgsql TO yjrybcwtcrpgic;


--
-- PostgreSQL database dump complete
--

