-- Active: 1681841026748@@localhost@3306@test

CREATE DATABASE Shopsphere;
USE Shopsphere;
CREATE TABLE User (Email VARCHAR(120) NOT NULL, Password VARCHAR(128) NOT NULL, PRIMARY KEY (Email));