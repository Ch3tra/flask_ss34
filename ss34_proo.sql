-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Nov 12, 2023 at 03:34 PM
-- Server version: 5.7.36
-- PHP Version: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ss34_proo`
--

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
CREATE TABLE IF NOT EXISTS `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8_unicode_520_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_520_ci;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`id`, `name`) VALUES
(1, 'coca');

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
CREATE TABLE IF NOT EXISTS `product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8_unicode_520_ci NOT NULL,
  `price` float NOT NULL DEFAULT '0',
  `cost` float NOT NULL DEFAULT '0',
  `image` varchar(255) COLLATE utf8_unicode_520_ci DEFAULT NULL,
  `cid` decimal(10,0) NOT NULL,
  `discount` decimal(10,0) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=19 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_520_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`id`, `name`, `price`, `cost`, `image`, `cid`, `discount`) VALUES
(1, 'coca', 1.5, 1, NULL, '1', '0'),
(3, 'string', 2.3, 2, NULL, '1', '0'),
(9, 'spy', 2.6, 1, NULL, '1', '10'),
(5, 'abc', 3.2, 2, NULL, '1', '0'),
(13, 'angkor', 3.5, 2.5, NULL, '1', '0'),
(12, 'jinro', 3, 2, NULL, '1', '10'),
(11, 'cambodia', 3.5, 2, NULL, '1', '15'),
(14, 'tiger', 2.3, 1.5, NULL, '1', '5'),
(15, 'anchor', 3.8, 2, NULL, '1', '5'),
(16, 'singha', 2, 2, NULL, '1', '20'),
(17, 'crown', 4, 3.5, NULL, '1', '0'),
(18, 'bayon', 2, 2, NULL, '1', '0');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
