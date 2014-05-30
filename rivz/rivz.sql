-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 01, 2014 at 08:23 AM
-- Server version: 5.5.35
-- PHP Version: 5.3.10-1ubuntu3.10

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `rivz`
--

-- --------------------------------------------------------

--
-- Stand-in structure for view `rivendellcart`
--
CREATE TABLE IF NOT EXISTS `rivendellcart` (
`NUMBER` int(10) unsigned
,`TYPE` int(10) unsigned
,`GROUP_NAME` char(10)
,`TITLE` char(255)
,`ARTIST` char(255)
,`ALBUM` char(255)
,`YEAR` date
,`ISRC` char(12)
,`LABEL` char(64)
,`CONDUCTOR` char(64)
,`CLIENT` char(64)
,`AGENCY` char(64)
,`PUBLISHER` char(64)
,`COMPOSER` char(64)
,`USER_DEFINED` char(255)
,`SONG_ID` char(32)
,`BPM` int(10) unsigned
,`USAGE_CODE` int(11)
,`FORCED_LENGTH` int(10) unsigned
,`AVERAGE_LENGTH` int(10) unsigned
,`LENGTH_DEVIATION` int(10) unsigned
,`AVERAGE_SEGUE_LENGTH` int(10) unsigned
,`AVERAGE_HOOK_LENGTH` int(10) unsigned
,`CUT_QUANTITY` int(10) unsigned
,`LAST_CUT_PLAYED` int(10) unsigned
,`PLAY_ORDER` int(10) unsigned
,`VALIDITY` int(10) unsigned
,`START_DATETIME` datetime
,`END_DATETIME` datetime
,`ENFORCE_LENGTH` enum('N','Y')
,`PRESERVE_PITCH` enum('N','Y')
,`ASYNCRONOUS` enum('N','Y')
,`OWNER` char(64)
,`MACROS` text
,`SCHED_CODES` varchar(255)
,`NOTES` text
,`METADATA_DATETIME` datetime
,`USE_EVENT_LENGTH` enum('N','Y')
);
-- --------------------------------------------------------

--
-- Stand-in structure for view `rivendellcuts`
--
CREATE TABLE IF NOT EXISTS `rivendellcuts` (
`CUT_NAME` char(12)
,`CART_NUMBER` int(10) unsigned
,`EVERGREEN` enum('N','Y')
,`DESCRIPTION` char(64)
,`OUTCUE` char(64)
,`ISRC` char(12)
,`ISCI` char(32)
,`LENGTH` int(10) unsigned
,`ORIGIN_DATETIME` datetime
,`START_DATETIME` datetime
,`END_DATETIME` datetime
,`SUN` enum('N','Y')
,`MON` enum('N','Y')
,`TUE` enum('N','Y')
,`WED` enum('N','Y')
,`THU` enum('N','Y')
,`FRI` enum('N','Y')
,`SAT` enum('N','Y')
,`START_DAYPART` time
,`END_DAYPART` time
,`ORIGIN_NAME` char(64)
,`WEIGHT` int(10) unsigned
,`LAST_PLAY_DATETIME` datetime
,`UPLOAD_DATETIME` datetime
,`PLAY_COUNTER` int(10) unsigned
,`LOCAL_COUNTER` int(10) unsigned
,`VALIDITY` int(10) unsigned
,`CODING_FORMAT` int(10) unsigned
,`SAMPLE_RATE` int(10) unsigned
,`BIT_RATE` int(10) unsigned
,`CHANNELS` int(10) unsigned
,`PLAY_GAIN` int(11)
,`START_POINT` int(11)
,`END_POINT` int(11)
,`FADEUP_POINT` int(11)
,`FADEDOWN_POINT` int(11)
,`SEGUE_START_POINT` int(11)
,`SEGUE_END_POINT` int(11)
,`SEGUE_GAIN` int(11)
,`HOOK_START_POINT` int(11)
,`HOOK_END_POINT` int(11)
,`TALK_START_POINT` int(11)
,`TALK_END_POINT` int(11)
);
-- --------------------------------------------------------

--
-- Stand-in structure for view `rivendellmain`
--
CREATE TABLE IF NOT EXISTS `rivendellmain` (
`ARTIST` char(255)
,`TITLE` char(255)
,`NUMBER` int(10) unsigned
,`GROUP_NAME` char(10)
,`CART_NUMBER` int(10) unsigned
,`CUT_NAME` char(12)
);
-- --------------------------------------------------------

--
-- Table structure for table `rivque`
--

CREATE TABLE IF NOT EXISTS `rivque` (
  `BidId` bigint(20) NOT NULL AUTO_INCREMENT,
  `MainBid` tinyint(1) NOT NULL,
  `ParentBid` bigint(20) DEFAULT NULL,
  `CUT_NAME` char(12) COLLATE utf8_unicode_ci NOT NULL,
  `CART_NUMBER` int(10) NOT NULL,
  `ARTIST` char(255) COLLATE utf8_unicode_ci NOT NULL,
  `TITLE` char(255) COLLATE utf8_unicode_ci NOT NULL,
  `BidAmt` decimal(6,2) unsigned NOT NULL,
  `OBidAmt` decimal(6,2) unsigned NOT NULL,
  `BidTime` datetime NOT NULL,
  PRIMARY KEY (`BidId`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=141 ;

-- --------------------------------------------------------

--
-- Table structure for table `rivtran`
--

CREATE TABLE IF NOT EXISTS `rivtran` (
  `TranId` bigint(20) NOT NULL AUTO_INCREMENT,
  `BidId` bigint(20) NOT NULL,
  `ParentBid` bigint(20) DEFAULT NULL,
  `CUT_NAME` char(12) COLLATE utf8_unicode_ci NOT NULL,
  `CART_NUMBER` int(11) NOT NULL,
  `ARTIST` char(255) COLLATE utf8_unicode_ci NOT NULL,
  `TITLE` char(255) COLLATE utf8_unicode_ci NOT NULL,
  `BidAmt` decimal(6,2) NOT NULL,
  `OBidAmt` decimal(6,2) NOT NULL,
  `BidTime` datetime NOT NULL,
  `LiveQueTime` datetime NOT NULL,
  PRIMARY KEY (`TranId`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=718 ;


-- --------------------------------------------------------

--
-- Structure for view `rivendellcart`
--
DROP TABLE IF EXISTS `rivendellcart`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `rivendellcart` AS select `Rivendell`.`CART`.`NUMBER` AS `NUMBER`,`Rivendell`.`CART`.`TYPE` AS `TYPE`,`Rivendell`.`CART`.`GROUP_NAME` AS `GROUP_NAME`,`Rivendell`.`CART`.`TITLE` AS `TITLE`,`Rivendell`.`CART`.`ARTIST` AS `ARTIST`,`Rivendell`.`CART`.`ALBUM` AS `ALBUM`,`Rivendell`.`CART`.`YEAR` AS `YEAR`,`Rivendell`.`CART`.`ISRC` AS `ISRC`,`Rivendell`.`CART`.`LABEL` AS `LABEL`,`Rivendell`.`CART`.`CONDUCTOR` AS `CONDUCTOR`,`Rivendell`.`CART`.`CLIENT` AS `CLIENT`,`Rivendell`.`CART`.`AGENCY` AS `AGENCY`,`Rivendell`.`CART`.`PUBLISHER` AS `PUBLISHER`,`Rivendell`.`CART`.`COMPOSER` AS `COMPOSER`,`Rivendell`.`CART`.`USER_DEFINED` AS `USER_DEFINED`,`Rivendell`.`CART`.`SONG_ID` AS `SONG_ID`,`Rivendell`.`CART`.`BPM` AS `BPM`,`Rivendell`.`CART`.`USAGE_CODE` AS `USAGE_CODE`,`Rivendell`.`CART`.`FORCED_LENGTH` AS `FORCED_LENGTH`,`Rivendell`.`CART`.`AVERAGE_LENGTH` AS `AVERAGE_LENGTH`,`Rivendell`.`CART`.`LENGTH_DEVIATION` AS `LENGTH_DEVIATION`,`Rivendell`.`CART`.`AVERAGE_SEGUE_LENGTH` AS `AVERAGE_SEGUE_LENGTH`,`Rivendell`.`CART`.`AVERAGE_HOOK_LENGTH` AS `AVERAGE_HOOK_LENGTH`,`Rivendell`.`CART`.`CUT_QUANTITY` AS `CUT_QUANTITY`,`Rivendell`.`CART`.`LAST_CUT_PLAYED` AS `LAST_CUT_PLAYED`,`Rivendell`.`CART`.`PLAY_ORDER` AS `PLAY_ORDER`,`Rivendell`.`CART`.`VALIDITY` AS `VALIDITY`,`Rivendell`.`CART`.`START_DATETIME` AS `START_DATETIME`,`Rivendell`.`CART`.`END_DATETIME` AS `END_DATETIME`,`Rivendell`.`CART`.`ENFORCE_LENGTH` AS `ENFORCE_LENGTH`,`Rivendell`.`CART`.`PRESERVE_PITCH` AS `PRESERVE_PITCH`,`Rivendell`.`CART`.`ASYNCRONOUS` AS `ASYNCRONOUS`,`Rivendell`.`CART`.`OWNER` AS `OWNER`,`Rivendell`.`CART`.`MACROS` AS `MACROS`,`Rivendell`.`CART`.`SCHED_CODES` AS `SCHED_CODES`,`Rivendell`.`CART`.`NOTES` AS `NOTES`,`Rivendell`.`CART`.`METADATA_DATETIME` AS `METADATA_DATETIME`,`Rivendell`.`CART`.`USE_EVENT_LENGTH` AS `USE_EVENT_LENGTH` from `Rivendell`.`CART`;

-- --------------------------------------------------------

--
-- Structure for view `rivendellcuts`
--
DROP TABLE IF EXISTS `rivendellcuts`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `rivendellcuts` AS select `Rivendell`.`CUTS`.`CUT_NAME` AS `CUT_NAME`,`Rivendell`.`CUTS`.`CART_NUMBER` AS `CART_NUMBER`,`Rivendell`.`CUTS`.`EVERGREEN` AS `EVERGREEN`,`Rivendell`.`CUTS`.`DESCRIPTION` AS `DESCRIPTION`,`Rivendell`.`CUTS`.`OUTCUE` AS `OUTCUE`,`Rivendell`.`CUTS`.`ISRC` AS `ISRC`,`Rivendell`.`CUTS`.`ISCI` AS `ISCI`,`Rivendell`.`CUTS`.`LENGTH` AS `LENGTH`,`Rivendell`.`CUTS`.`ORIGIN_DATETIME` AS `ORIGIN_DATETIME`,`Rivendell`.`CUTS`.`START_DATETIME` AS `START_DATETIME`,`Rivendell`.`CUTS`.`END_DATETIME` AS `END_DATETIME`,`Rivendell`.`CUTS`.`SUN` AS `SUN`,`Rivendell`.`CUTS`.`MON` AS `MON`,`Rivendell`.`CUTS`.`TUE` AS `TUE`,`Rivendell`.`CUTS`.`WED` AS `WED`,`Rivendell`.`CUTS`.`THU` AS `THU`,`Rivendell`.`CUTS`.`FRI` AS `FRI`,`Rivendell`.`CUTS`.`SAT` AS `SAT`,`Rivendell`.`CUTS`.`START_DAYPART` AS `START_DAYPART`,`Rivendell`.`CUTS`.`END_DAYPART` AS `END_DAYPART`,`Rivendell`.`CUTS`.`ORIGIN_NAME` AS `ORIGIN_NAME`,`Rivendell`.`CUTS`.`WEIGHT` AS `WEIGHT`,`Rivendell`.`CUTS`.`LAST_PLAY_DATETIME` AS `LAST_PLAY_DATETIME`,`Rivendell`.`CUTS`.`UPLOAD_DATETIME` AS `UPLOAD_DATETIME`,`Rivendell`.`CUTS`.`PLAY_COUNTER` AS `PLAY_COUNTER`,`Rivendell`.`CUTS`.`LOCAL_COUNTER` AS `LOCAL_COUNTER`,`Rivendell`.`CUTS`.`VALIDITY` AS `VALIDITY`,`Rivendell`.`CUTS`.`CODING_FORMAT` AS `CODING_FORMAT`,`Rivendell`.`CUTS`.`SAMPLE_RATE` AS `SAMPLE_RATE`,`Rivendell`.`CUTS`.`BIT_RATE` AS `BIT_RATE`,`Rivendell`.`CUTS`.`CHANNELS` AS `CHANNELS`,`Rivendell`.`CUTS`.`PLAY_GAIN` AS `PLAY_GAIN`,`Rivendell`.`CUTS`.`START_POINT` AS `START_POINT`,`Rivendell`.`CUTS`.`END_POINT` AS `END_POINT`,`Rivendell`.`CUTS`.`FADEUP_POINT` AS `FADEUP_POINT`,`Rivendell`.`CUTS`.`FADEDOWN_POINT` AS `FADEDOWN_POINT`,`Rivendell`.`CUTS`.`SEGUE_START_POINT` AS `SEGUE_START_POINT`,`Rivendell`.`CUTS`.`SEGUE_END_POINT` AS `SEGUE_END_POINT`,`Rivendell`.`CUTS`.`SEGUE_GAIN` AS `SEGUE_GAIN`,`Rivendell`.`CUTS`.`HOOK_START_POINT` AS `HOOK_START_POINT`,`Rivendell`.`CUTS`.`HOOK_END_POINT` AS `HOOK_END_POINT`,`Rivendell`.`CUTS`.`TALK_START_POINT` AS `TALK_START_POINT`,`Rivendell`.`CUTS`.`TALK_END_POINT` AS `TALK_END_POINT` from `Rivendell`.`CUTS`;

-- --------------------------------------------------------

--
-- Structure for view `rivendellmain`
--
DROP TABLE IF EXISTS `rivendellmain`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `rivendellmain` AS select `Rivendell`.`CART`.`ARTIST` AS `ARTIST`,`Rivendell`.`CART`.`TITLE` AS `TITLE`,`Rivendell`.`CART`.`NUMBER` AS `NUMBER`,`Rivendell`.`CART`.`GROUP_NAME` AS `GROUP_NAME`,`Rivendell`.`CUTS`.`CART_NUMBER` AS `CART_NUMBER`,`Rivendell`.`CUTS`.`CUT_NAME` AS `CUT_NAME` from (`Rivendell`.`CART` join `Rivendell`.`CUTS`) where (`Rivendell`.`CART`.`NUMBER` = `Rivendell`.`CUTS`.`CART_NUMBER`) group by `Rivendell`.`CUTS`.`CART_NUMBER`;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
