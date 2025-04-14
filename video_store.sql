-- Author: Angel Siwele
-- Created: 28/107/2023 
-- Purpose: create database and tables
-- PROLOGUE
-- This Database is designed to store, update and fetch records for the a video rental system. 
-- This database will store information about customers, videos and hire records. This system
-- has a server and client side applications. This is the server side application that connects to
-- a MySQL database called video_store.sql .

use MySQL;
-- drop/delete database if you want to remove all records
-- DROP DATABASE IF EXISTS  video_store;
-- create database
CREATE DATABASE IF NOT EXISTS  video_store;
use  video_store;

-- create customers table
CREATE TABLE customers(
custId INT PRIMARY KEY AUTO_INCREMENT,
fName VARCHAR(40)  NOT NULL,
sName VARCHAR(40)  NOT NULL,
address VARCHAR(40)  NOT NULL,
phone VARCHAR(10) NOT NULL UNIQUE  
);
-- create videos table
CREATE TABLE videos(
videoId INT PRIMARY KEY AUTO_INCREMENT,
-- videoVer INT NOT NULL ,
vname VARCHAR(15) NOT NULL,
videoType VARCHAR(1) NOT NULL ,
dateAdded  VARCHAR(20) NOT NULL
);
-- create hire table
CREATE TABLE hire(
custId INT NOT NULL,
videoId INT NOT NULL,
dateHired VARCHAR(20) NOT NULL,
dateReturn VARCHAR(20) ,
FOREIGN KEY (videoId) REFERENCES videos(videoId),
FOREIGN KEY (custId) REFERENCES customers(custId))
;

-- insert dates
-- INSERT INTO videos (vname,video_type,dateAdded) VALUES ("Spider Man","R",(SELECT CURDATE()))