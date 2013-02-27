BEGIN TRANSACTION;
CREATE TABLE applying (
	appbleaf_id integer,
	applleaf_id integer
);
CREATE TABLE bleaf (avatar TEXT, bleaf_id integer PRIMARY KEY, email text, uname text, sex text, ulevel integer, password text, rrurl text, sinawburl text, qqwburl text, createtime TIMESTAMP);
INSERT INTO bleaf VALUES('avatar.jpg',1,'444@444.444',444,'女',0,'sha1$CemqvvMd$823c8fd75102cd183c943c7b8e07853a9face3b4',NULL,NULL,NULL,'2013-02-21 09:46:44.077309');
INSERT INTO bleaf VALUES('avatar.jpg',2,'444@44.444',444,'男',0,'sha1$UjxQ8K4A$3990d9cecfd348a2a4042aca818634058c163301',NULL,NULL,NULL,'2013-02-21 10:15:10.019710');
INSERT INTO bleaf VALUES('avatar.jpg',3,'555@555.555',555,'男',0,'sha1$kmf0ad4X$98c470e5b665afa0166dc49b8812a877fb60a5e9',NULL,NULL,NULL,'2013-02-21 19:55:42.560258');
INSERT INTO bleaf VALUES('avatar.jpg',4,'1111@1111.1111',1111,'男',0,'sha1$VPZZ2x4A$0a31d4e9ec21d10a8b51a0fffb03e61f66b633b0',NULL,NULL,NULL,'2013-02-21 20:11:48.898138');
INSERT INTO bleaf VALUES('avatar.jpg',5,'sophia4everyoung@gmail.com','小风扇','女',0,'sha1$fCK2XQRy$2bc648784ed06f29a7d6d293c96d9097c7697ef6',NULL,NULL,NULL,'2013-02-23 04:22:47.904352');
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
	name text not null,
	sex text not null,
	lleafinfo text not null,
	status integer not null,
	createtime TIMESTAMP default (datetime('now', 'localtime'))
);
INSERT INTO lleaf VALUES(1,'阿迪发发','男','阿迪发发的撒放大萨',0,'2013-02-21 09:22:27');
INSERT INTO lleaf VALUES(2,'小叶子二号','男','小叶子二号',0,'2013-02-21 09:22:50');
INSERT INTO lleaf VALUES(3,'小叶子王哲·','男',111111111111111111,0,'2013-02-21 19:54:32');
INSERT INTO lleaf VALUES(4,1231312,'男','213adfadfafafdsaf',0,'2013-02-23 07:35:59');
CREATE TABLE sqlite_sequence(name,seq);
INSERT INTO sqlite_sequence VALUES('lleaf',4);
COMMIT;
