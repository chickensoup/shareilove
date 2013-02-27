drop table if exists lleaf;
drop table if exists bleaf;
drop table if exists blog;
drop table if exists applying;
drop table if exists donating;

create table bleaf (
	bleaf_id integer primary key autoincrement,
	email text not null,
  	uname text not null,
  	sex text not null,
  	avatar text default ('avatar.jpg')
  	ulevel integer not null,
  	password text not null,
  	rrurl text,
	sinawburl text,
	qqwburl text,
	createtime TIMESTAMP default (datetime('now', 'localtime'))
);

create table lleaf (
	lleaf_id integer primary key autoincrement,
	name text not null,
	sex text not null,
	lleafinfo text not null,
	status integer not null,
	createtime TIMESTAMP default (datetime('now', 'localtime'))
);

create table blog (
	blog_id integer primary key autoincrement,
	bleaf_id integer not null,
	lleaf_id integer not null,
	title text not null,
	blogtext text not null,
	createtime TIMESTAMP default (datetime('now', 'localtime'))
);

create table applying (
	appbleaf_id integer,
	applleaf_id integer
);

create table donating (
	donableaf_id integer,
	donalleaf_id integer
);