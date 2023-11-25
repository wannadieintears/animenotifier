
## Requirements:

1. python == 3.11
2. aiogram == 3.1.1
3. postgresql == 16.1
4. asyncpg == 4.0.3
5. aiohttp == 3.8.6
6. BeautifulSoup4 == 4.12.2

___

## How to install:

1. Create a project in your IDE/IDLE
2. Create a local repository:
```
git init
```
3. Push down this git:
```
git clone https://github.com/wannadieintears/animenotifier.git
```
4. Create 2 tables in your database:
```
CREATE TABLE IF NOT EXISTS public.titles
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 425263474256 CACHE 1 ),
    user_id bigint NOT NULL,
    title text COLLATE pg_catalog."default" NOT NULL,
    notification integer NOT NULL DEFAULT 0,
    CONSTRAINT titles_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.titles
    OWNER to postgres;
```
```
CREATE TABLE IF NOT EXISTS public.last
(
    id integer NOT NULL DEFAULT 1,
    last text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT last_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.last
    OWNER to postgres;
```
5. Install libraries/frameworks:
```
pip install aiogram, asyncpg, bs4
```
6. Create and fill settings.py with: token, host, port, database, user, password
7. Don't forget to write 'parse' to bot (I don't know how to start parsing by default :( )!