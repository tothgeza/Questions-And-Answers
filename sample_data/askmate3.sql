--
-- PostgreSQL database dump

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS pk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS pk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS pk_comment_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS pk_question_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.tag DROP CONSTRAINT IF EXISTS pk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_tag_id CASCADE;

DROP TABLE IF EXISTS public.question;
CREATE TABLE question (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text,
    user_id integer NOT NULL
);

DROP TABLE IF EXISTS public.answer;
CREATE TABLE answer (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text,
    user_id integer NOT NULL,
    accepted boolean DEFAULT FALSE
);

DROP TABLE IF EXISTS public.comment;
CREATE TABLE comment (
    id serial NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer,
    user_id integer NOT NULL
);

DROP TABLE IF EXISTS public.votes;
CREATE TABLE votes (
    question_id integer,
    answer_id integer,
    user_id integer NOT NULL,
    updown boolean
);

DROP TABLE IF EXISTS public.users CASCADE;
CREATE TABLE users (
    id serial NOT NULL,
    username text,
    email_address text,
    registration_date timestamp without time zone,
    reputation integer DEFAULT 0,
    password text
);

DROP TABLE IF EXISTS public.question_tag;
CREATE TABLE question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);

DROP TABLE IF EXISTS public.tag;
CREATE TABLE tag (
    id serial NOT NULL,
    name text
);


ALTER TABLE ONLY answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);

ALTER TABLE ONLY question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);

ALTER TABLE ONLY tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);

ALTER TABLE ONLY users
    ADD CONSTRAINT pk_users_id PRIMARY KEY (id);

ALTER TABLE votes
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;

ALTER TABLE votes
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id) ON DELETE CASCADE;

ALTER TABLE votes
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;


ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id) ON DELETE CASCADE;

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE;

ALTER TABLE ONLY question
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

INSERT INTO users (username, email_address, registration_date, reputation, password) VALUES ('Tibor', 'tibor@blabla.com', '2021-02-15 09:43:00', 0, '$2b$12$.dg5TJl7qIJ0pIJbvWIdiu8M5UpBjnNrus7.Fun6994STU6mdV9u6');
INSERT INTO users (username, email_address, registration_date, reputation, password) VALUES ('Luca', 'luca@blabla.com', '2021-02-12 09:40:00', 15, '$2b$12$.dg5TJl7qIJ0pIJbvWIdiu8M5UpBjnNrus7.Fun6994STU6mdV9u6');
INSERT INTO users (username, email_address, registration_date, reputation, password) VALUES ('Lala', 'lala@blabla.com', '2021-01-15 11:46:00', 0, '$2b$12$.dg5TJl7qIJ0pIJbvWIdiu8M5UpBjnNrus7.Fun6994STU6mdV9u6');
INSERT INTO users (username, email_address, registration_date, reputation, password) VALUES ('Lili', 'lili@blabla.com', '2021-02-16 09:44:00', 0, '$2b$12$.dg5TJl7qIJ0pIJbvWIdiu8M5UpBjnNrus7.Fun6994STU6mdV9u6');
INSERT INTO users (username, email_address, registration_date, reputation, password) VALUES ('Laca', 'laca@blabla.com', '2021-01-18 08:40:00', -2, '$2b$12$.dg5TJl7qIJ0pIJbvWIdiu8M5UpBjnNrus7.Fun6994STU6mdV9u6');
INSERT INTO users (username, email_address, registration_date, reputation, password) VALUES ('Anna', 'anna@blabla.com', '2021-01-11 09:28:00', 35, '$2b$12$.dg5TJl7qIJ0pIJbvWIdiu8M5UpBjnNrus7.Fun6994STU6mdV9u6');
INSERT INTO users (username, email_address, registration_date, reputation, password) VALUES ('Norbi', 'norbi@blabla.com', '2021-01-10 09:22:00', 0, '$2b$12$.dg5TJl7qIJ0pIJbvWIdiu8M5UpBjnNrus7.Fun6994STU6mdV9u6');
INSERT INTO users (username, email_address, registration_date, reputation, password) VALUES ('Kata', 'kata@blabla.com', '2021-01-08 08:22:00', 0, '$2b$12$.dg5TJl7qIJ0pIJbvWIdiu8M5UpBjnNrus7.Fun6994STU6mdV9u6');
INSERT INTO users (username, email_address, registration_date, reputation, password) VALUES ('Misi', 'misi@blabla.com', '2021-01-14 08:43:00', 0, '$2b$12$.dg5TJl7qIJ0pIJbvWIdiu8M5UpBjnNrus7.Fun6994STU6mdV9u6');
INSERT INTO users (username, email_address, registration_date, reputation, password) VALUES ('Emese', 'emese@blabla.com', '2021-01-13 07:40:00', 0, '$2b$12$.dg5TJl7qIJ0pIJbvWIdiu8M5UpBjnNrus7.Fun6994STU6mdV9u6');
INSERT INTO question VALUES (0, '2017-04-28 08:29:00', 29, 0, 'How to make lists in Python?', 'I am totally new to this, any hints?', NULL,1);
INSERT INTO question VALUES (1, '2017-04-29 09:19:00', 15, 0, 'Wordpress loading multiple jQuery Versions', 'I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(".myBook").booklet();

I could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.

BUT in my theme i also using jquery via webpack so the loading order is now following:

jquery
booklet
app.js (bundled file with webpack, including jquery)', 'images/image1.png', 1);
INSERT INTO question VALUES (2, '2017-05-01 10:41:00', 1364, 0, 'Drawing canvas with an image picked with Cordova Camera Plugin', 'I''m getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I''m on IOS, it throws errors such as cross origin issue, or that I''m trying to use an unknown format.
', NULL, 1);
INSERT INTO public.question (id, submission_time, view_number, vote_number, title, message, image, user_id) VALUES (3, '2021-02-18 11:04:02.000000', 13, 3, 'Miből készül a kenyér héja?', 'Szeretnék otthon sütni kenyeret,találtam is pár receptet de egyik sem írja a héját.Az miből készül?Persze gondoltam arra is, hogy csak a "belét"csinálom meg, a gyerekek is azt szeretik, a héját nem eszik meg,de elősször hagyományosan akarom el készíteni.Ötletek?', 'kenyer.jpg', 2);
SELECT pg_catalog.setval('question_id_seq', 3, true);

INSERT INTO public.answer (id, submission_time, vote_number, question_id, message, image, user_id, accepted) VALUES (2, '2017-04-25 14:42:00.000000', 0, 1, 'Look it up in the Python docs', 'images/image2.jpg', 1, false);
INSERT INTO public.answer (id, submission_time, vote_number, question_id, message, image, user_id, accepted) VALUES (1, '2017-04-28 16:49:00.000000', 0, 1, 'You need to use brackets: my_list = []', null, 1, false);
INSERT INTO public.answer (id, submission_time, vote_number, question_id, message, image, user_id, accepted) VALUES (3, '2021-02-18 11:07:19.000000', -1, 3, 'én héj nélkül sütöm mindig.

amikor kihűlt felszeletelem, és a szeletek élét barna ételfestékkel alaposan megkenem...', 'default.png', 3, false);
INSERT INTO public.answer (id, submission_time, vote_number, question_id, message, image, user_id, accepted) VALUES (4, '2021-02-18 11:10:00.000000', 2, 3, 'A kenyér héja a réti héjából készül, a tollait ki kell tépkedni, majd a testét megforgatni lisztben, majd kemencében kisütni.', 'retiheja.jpg', 6, true);
SELECT pg_catalog.setval('answer_id_seq', 4, true);

INSERT INTO public.comment (id, question_id, answer_id, message, submission_time, edited_count, user_id) VALUES (1, 0, null, 'Please clarify the question as it is too vague!', '2017-05-01 05:49:00.000000', 0, 1);
INSERT INTO public.comment (id, question_id, answer_id, message, submission_time, edited_count, user_id) VALUES (2, null, 1, 'I think you could use my_list = list() as well.', '2017-05-02 16:55:00.000000', 0, 1);
INSERT INTO public.comment (id, question_id, answer_id, message, submission_time, edited_count, user_id) VALUES (3, 3, null, 'a kenyér héja? hogy miből készül? ', '2021-02-18 11:11:33.000000', null, 1);
INSERT INTO public.comment (id, question_id, answer_id, message, submission_time, edited_count, user_id) VALUES (4, null, 4, 'Ha sütőben sütöm, hány fokra állítsam?', '2021-02-18 11:13:03.000000', null, 10);
SELECT pg_catalog.setval('comment_id_seq', 4, true);

INSERT INTO public.tag (id, name) VALUES (1, 'python');
INSERT INTO public.tag (id, name) VALUES (2, 'sql');
INSERT INTO public.tag (id, name) VALUES (3, 'css');
INSERT INTO public.tag (id, name) VALUES (4, 'kenyer');

SELECT pg_catalog.setval('tag_id_seq', 4, true);

INSERT INTO public.question_tag (question_id, tag_id) VALUES (0, 1);
INSERT INTO public.question_tag (question_id, tag_id) VALUES (1, 3);
INSERT INTO public.question_tag (question_id, tag_id) VALUES (2, 3);
INSERT INTO public.question_tag (question_id, tag_id) VALUES (3, 4);

INSERT INTO public.votes (question_id, answer_id, user_id, updown) VALUES (3, null, 6, true);
INSERT INTO public.votes (question_id, answer_id, user_id, updown) VALUES (null, 3, 6, false);
INSERT INTO public.votes (question_id, answer_id, user_id, updown) VALUES (3, null, 3, true);
INSERT INTO public.votes (question_id, answer_id, user_id, updown) VALUES (null, 4, 10, true);
INSERT INTO public.votes (question_id, answer_id, user_id, updown) VALUES (3, null, 10, true);
INSERT INTO public.votes (question_id, answer_id, user_id, updown) VALUES (null, 4, 2, true);