create table article(
    article_ID serial, 
    headline varchar(255), 
    preamble text, 
    article_text text, 
    published varchar(255),
    PRIMARY KEY(article_ID)
);

create table author(
    person_nr integer, 
    author_name varchar (255), 
    notes text, 
    PRIMARY KEY (person_nr)
);

create table article_author(
    article_ID integer REFERENCES article(article_ID), 
    person_nr integer REFERENCES author(person_nr), 
    CONSTRAINT article_author_ID PRIMARY KEY(article_ID, person_nr)
);

create table commenter(
    commenter_ID serial, 
    username varchar(255), 
    comment text, 
    curr_time varchar(255), 
    PRIMARY KEY (commenter_ID)
);

create table comment_in_article(
    commenter_ID integer REFERENCES commenter(commenter_ID),
    article_ID integer REFERENCES article(article_ID),
    CONSTRAINT comment_in_article_ID PRIMARY KEY(commenter_ID, article_ID)
);

create table images(
    image_url varchar(255), 
    alt_text varchar(255), 
    PRIMARY KEY(image_url)
);

create table images_in_article(
    image_url varchar(255) REFERENCES images(image_url), 
    article_ID integer REFERENCES article(article_ID), 
    image_text text, 
    CONSTRAINT images_in_article_ID PRIMARY KEY(image_url, article_ID)
);