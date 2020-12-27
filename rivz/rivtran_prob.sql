-- phpMyAdmin SQL Dump
-- version 4.4.15.10
-- https://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Dec 27, 2020 at 09:36 PM
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
-- Table structure for table `rivtran`
--

CREATE TABLE IF NOT EXISTS `rivtran` (
  `TranId` bigint(20) NOT NULL,
  `BidId` bigint(20) NOT NULL,
  `ParentBid` bigint(20) DEFAULT NULL,
  `CUT_NAME` char(12) COLLATE utf8_unicode_ci NOT NULL,
  `CART_NUMBER` int(11) NOT NULL,
  `ARTIST` char(255) COLLATE utf8_unicode_ci NOT NULL,
  `TITLE` char(255) COLLATE utf8_unicode_ci NOT NULL,
  `BidAmt` decimal(6,2) NOT NULL,
  `OBidAmt` decimal(6,2) NOT NULL,
  `BidTime` datetime NOT NULL,
  `LiveQueTime` datetime NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=643 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `rivtran`
--

INSERT INTO `rivtran` (`TranId`, `BidId`, `ParentBid`, `CUT_NAME`, `CART_NUMBER`, `ARTIST`, `TITLE`, `BidAmt`, `OBidAmt`, `BidTime`, `LiveQueTime`) VALUES
(617, 373, 371, '010001_001', 10001, 'Rupert & The Rolling Coins', 'The Mail', '3.00', '3.00', '2020-12-27 13:04:18', '2020-12-27 13:12:06'),
(616, 372, 371, '010001_001', 10001, 'Rupert & The Rolling Coins', 'The Mail', '2.00', '2.00', '2020-12-27 13:04:06', '2020-12-27 13:12:06'),
(615, 371, NULL, '010001_001', 10001, 'Rupert & The Rolling Coins', 'The Mail', '6.00', '0.00', '2020-12-27 13:03:53', '2020-12-27 13:12:06');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `rivtran`
--
ALTER TABLE `rivtran`
  ADD PRIMARY KEY (`TranId`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `rivtran`
--
ALTER TABLE `rivtran`
  MODIFY `TranId` bigint(20) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=643;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
