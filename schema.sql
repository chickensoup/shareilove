drop table if exists raising;
drop table if exists applying;
drop table if exists donating;

CREATE TABLE raising (
	id integer primary key autoincrement,
	bleaf_id integer,
	lleaf_id integer,
	createtime TIMESTAMP default (datetime('now', 'localtime'))
);

CREATE TABLE applying (
	id integer primary key autoincrement,
	bleaf_id integer,
	lleaf_id integer,
	createtime TIMESTAMP default (datetime('now', 'localtime'))
);

CREATE TABLE donating (
	id integer primary key autoincrement,
	bleaf_id integer,
	lleaf_id integer,
	createtime TIMESTAMP default (datetime('now', 'localtime'))
);
