BEGIN TRANSACTION;
drop table if exists lleaf;
drop table if exists bleaf;
drop table if exists blog;
drop table if exists applying;
drop table if exists donating;

CREATE TABLE applying (
	appbleaf_id integer,
	applleaf_id integer
);

CREATE TABLE bleaf (avatar TEXT, bleaf_id integer PRIMARY KEY, email text, uname text, sex text, ulevel integer, password text, rrurl text, sinawburl text, qqwburl text, createtime TIMESTAMP);
INSERT INTO bleaf VALUES('http://www.gravatar.com/avatar/10ee730182aa8d50b46425e89cde4be8',1,'393312416@qq.com','qkj','男',0,'sha1$rW7nVDYp$9b997f4a59bb9d111e373281a0cf34bdfcfd5969',NULL,NULL,NULL,'2013-02-24 18:42:41.577362');
INSERT INTO bleaf VALUES('http://www.gravatar.com/avatar/e3463374c5e5f98c748b1a1a250a2fa3',2,'sophia4everyoung@gmail.com','小风扇','女',0,'sha1$fCK2XQRy$2bc648784ed06f29a7d6d293c96d9097c7697ef6',NULL,NULL,NULL,'2013-02-23 04:22:47.904352');
INSERT INTO bleaf VALUES('http://www.gravatar.com/avatar/5d4b6ee85984bc9bc1d27c141f807f05',3,'666@666.666',666,'男',0,'sha1$7ByRESSD$6bd3fd042356a1d6a951506411dd3fb76edaa17d',NULL,NULL,NULL,'2013-02-24 18:47:46.657128');

CREATE TABLE blog (
	blog_id integer primary key autoincrement,
	bleaf_id integer not null,
	lleaf_id integer not null,
	title text not null,
	blogtext text not null,
	createtime TIMESTAMP default (datetime('now', 'localtime'))
);

CREATE TABLE donating (
	donableaf_id integer,
	donalleaf_id integer
);

CREATE TABLE lleaf (
	lleaf_id integer primary key autoincrement,
	avatar text,
	name text not null,
	sex text not null,
	lleafinfo text not null,
	status integer not null,
	createtime TIMESTAMP default (datetime('now', 'localtime'))
);
COMMIT;
