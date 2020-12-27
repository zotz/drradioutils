-- phpMyAdmin SQL Dump
-- version 4.4.15.10
-- https://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Dec 27, 2020 at 09:32 PM
-- Server version: 5.5.64-MariaDB
-- PHP Version: 5.4.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `rivz`
--

-- --------------------------------------------------------

--
-- Table structure for table `rivque`
--

CREATE TABLE IF NOT EXISTS `rivque` (
  `BidId` bigint(20) NOT NULL,
  `MainBid` tinyint(1) NOT NULL,
  `ParentBid` bigint(20) DEFAULT NULL,
  `CUT_NAME` char(12) COLLATE utf8_unicode_ci NOT NULL,
  `CART_NUMBER` int(10) NOT NULL,
  `ARTIST` char(255) COLLATE utf8_unicode_ci NOT NULL,
  `TITLE` char(255) COLLATE utf8_unicode_ci NOT NULL,
  `BidAmt` decimal(6,2) unsigned NOT NULL,
  `OBidAmt` decimal(6,2) unsigned NOT NULL,
  `BidTime` datetime NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=377 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `rivque`
--

INSERT INTO `rivque` (`BidId`, `MainBid`, `ParentBid`, `CUT_NAME`, `CART_NUMBER`, `ARTIST`, `TITLE`, `BidAmt`, `OBidAmt`, `BidTime`) VALUES
(374, 1, NULL, '010001_001', 10001, 'Rupert & The Rolling Coins', 'The Mail', '5.00', '1.00', '2020-12-27 13:15:26'),
(375, 0, 374, '010001_001', 10001, 'Rupert & The Rolling Coins', 'The Mail', '2.00', '2.00', '2020-12-27 13:15:36'),
(376, 0, 374, '010001_001', 10001, 'Rupert & The Rolling Coins', 'The Mail', '2.00', '2.00', '2020-12-27 13:15:45');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `rivque`
--
ALTER TABLE `rivque`
  ADD PRIMARY KEY (`BidId`);

--
-- AUTO_INCREMENT for dumped tables
--
