-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Dec 03, 2023 at 12:50 PM
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
  `categoryId` int(11) NOT NULL AUTO_INCREMENT,
  `categoryName` varchar(100) COLLATE utf8_unicode_520_ci NOT NULL,
  `categoryDesc` varchar(255) COLLATE utf8_unicode_520_ci DEFAULT NULL,
  PRIMARY KEY (`categoryId`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_520_ci;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`categoryId`, `categoryName`, `categoryDesc`) VALUES
(1, 'Soft Drink', 'asgdasdfasdfasxjcviahsklvhksv'),
(2, 'asdf', 'asdf'),
(3, 'sdf', 'asdf'),
(4, 'asdf', 'asdf');

-- --------------------------------------------------------

--
-- Table structure for table `credential`
--

DROP TABLE IF EXISTS `credential`;
CREATE TABLE IF NOT EXISTS `credential` (
  `userId` int(11) NOT NULL AUTO_INCREMENT,
  `username` text COLLATE utf8_unicode_520_ci NOT NULL,
  `password_hash` text COLLATE utf8_unicode_520_ci NOT NULL,
  PRIMARY KEY (`userId`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_520_ci;

--
-- Dumping data for table `credential`
--

INSERT INTO `credential` (`userId`, `username`, `password_hash`) VALUES
(1, 'dev', 'scrypt:32768:8:1$YN64L4HTtujOpf0J$297e869627b41ce07faa550bda5c556944c3145715f95fb0cc7d87a764b65ce83c6b79667f86c4b3b6285280ada11a7e99317519fe380e785d094986a2ea2a90'),
(2, 'admin', 'scrypt:32768:8:1$mffQfEopbIc2NvUS$fe1f5b4c82fcf065d27a0b6c0fbd8aa42a07d1f61bf6b3a7c9d90edd563fde7e0729fcc6ca70a6eb301bcdfc3bc1d25e1f1726408f5c97e17f81166ef94fe765');

-- --------------------------------------------------------

--
-- Table structure for table `currency`
--

DROP TABLE IF EXISTS `currency`;
CREATE TABLE IF NOT EXISTS `currency` (
  `currencyId` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(50) COLLATE utf8_unicode_520_ci NOT NULL,
  `currencyName` varchar(50) COLLATE utf8_unicode_520_ci NOT NULL,
  `currencySymbol` varchar(50) COLLATE utf8_unicode_520_ci NOT NULL,
  `currencyRate` double NOT NULL,
  `is_default` int(11) DEFAULT NULL,
  PRIMARY KEY (`currencyId`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_520_ci;

--
-- Dumping data for table `currency`
--

INSERT INTO `currency` (`currencyId`, `code`, `currencyName`, `currencySymbol`, `currencyRate`, `is_default`) VALUES
(1, 'sadf', 'sdf', 'asdf', 234, NULL),
(2, 'asdf', 'asdf', 'asd', 234, NULL),
(3, '1234', '23', '345', 12, NULL),
(4, 'asdf', '234', 'asdf', 234, 1);

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` (
  `customerId` int(11) NOT NULL AUTO_INCREMENT,
  `customerName` varchar(255) COLLATE utf8_unicode_520_ci NOT NULL,
  `image` varchar(255) COLLATE utf8_unicode_520_ci NOT NULL DEFAULT 'default_img',
  `status` varchar(50) COLLATE utf8_unicode_520_ci DEFAULT NULL,
  PRIMARY KEY (`customerId`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_520_ci;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`customerId`, `customerName`, `image`, `status`) VALUES
(5, 'chetraou', 'default_img', 'active'),
(6, 'st', 'default_img', 's'),
(7, 'sdf', 'default_img', 'sadf'),
(8, 'asdf', 'default_img', 'asdf'),
(9, 'asdf', 'default_img', 'asdf');

-- --------------------------------------------------------

--
-- Table structure for table `pcategory`
--

DROP TABLE IF EXISTS `pcategory`;
CREATE TABLE IF NOT EXISTS `pcategory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8_unicode_520_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_520_ci;

--
-- Dumping data for table `pcategory`
--

INSERT INTO `pcategory` (`id`, `name`) VALUES
(3, 'gaming'),
(4, 'professional'),
(5, 'office'),
(6, 'old-school'),
(7, 'weird-one');

-- --------------------------------------------------------

--
-- Table structure for table `pproduct`
--

DROP TABLE IF EXISTS `pproduct`;
CREATE TABLE IF NOT EXISTS `pproduct` (
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
-- Dumping data for table `pproduct`
--

INSERT INTO `pproduct` (`id`, `name`, `price`, `cost`, `image`, `cid`, `discount`) VALUES
(1, 'coca', 1.5, 1, NULL, '7', '0'),
(3, 'string', 2.3, 2, NULL, '3', '0'),
(9, 'spy', 2.6, 1, NULL, '6', '10'),
(5, 'abc', 3.2, 2, NULL, '5', '0'),
(13, 'angkor', 3.5, 2.5, NULL, '5', '0'),
(12, 'jinro', 3, 2, NULL, '6', '10'),
(11, 'cambodia', 3.5, 2, NULL, '4', '15'),
(14, 'tiger', 2.3, 1.5, NULL, '7', '5'),
(15, 'anchor', 3.8, 2, NULL, '4', '5'),
(16, 'singha', 2, 2, NULL, '7', '20'),
(17, 'crown', 4, 3.5, NULL, '3', '0'),
(18, 'bayon', 2, 2, NULL, '5', '0');

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
CREATE TABLE IF NOT EXISTS `product` (
  `productId` int(11) NOT NULL AUTO_INCREMENT,
  `categoryId` int(11) NOT NULL,
  `productName` varchar(60) COLLATE utf8_unicode_520_ci NOT NULL,
  `productDesc` varchar(255) COLLATE utf8_unicode_520_ci NOT NULL,
  `productCost` double NOT NULL,
  `image` varchar(255) COLLATE utf8_unicode_520_ci NOT NULL DEFAULT 'default_img',
  `productPrice` double DEFAULT NULL,
  `status` varchar(50) COLLATE utf8_unicode_520_ci DEFAULT NULL,
  PRIMARY KEY (`productId`),
  KEY `fk_product_category` (`categoryId`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_520_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`productId`, `categoryId`, `productName`, `productDesc`, `productCost`, `image`, `productPrice`, `status`) VALUES
(1, 2, 'sdf', 'sadhf', 34.5, 'sdf.jfif', NULL, NULL),
(3, 4, 'asdf', 'asdf', 34, 'default_img', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
CREATE TABLE IF NOT EXISTS `student` (
  `sid` int(11) NOT NULL AUTO_INCREMENT,
  `firstName` varchar(60) COLLATE utf8_unicode_520_ci NOT NULL,
  `lastName` varchar(60) COLLATE utf8_unicode_520_ci NOT NULL,
  `birthday` varchar(50) COLLATE utf8_unicode_520_ci NOT NULL,
  `gender` varchar(20) COLLATE utf8_unicode_520_ci NOT NULL,
  `email` varchar(50) COLLATE utf8_unicode_520_ci NOT NULL,
  `phoneNumber` varchar(30) COLLATE utf8_unicode_520_ci NOT NULL,
  `subject` varchar(50) COLLATE utf8_unicode_520_ci NOT NULL,
  `image` varchar(255) COLLATE utf8_unicode_520_ci NOT NULL DEFAULT 'default_img',
  PRIMARY KEY (`sid`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_520_ci;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`sid`, `firstName`, `lastName`, `birthday`, `gender`, `email`, `phoneNumber`, `subject`, `image`) VALUES
(8, 'ou', 'chetra', '2023-11-11', 'Male', 'chetra@yahoo.com', '098475873', 'English', 'ou_chetra.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `userId` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(60) COLLATE utf8_unicode_520_ci NOT NULL,
  `image` varchar(255) COLLATE utf8_unicode_520_ci NOT NULL DEFAULT 'default_img',
  `status` varchar(50) COLLATE utf8_unicode_520_ci DEFAULT NULL,
  PRIMARY KEY (`userId`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_520_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`userId`, `username`, `image`, `status`) VALUES
(1, 'tst', 'default_img', 'ast'),
(2, 'sadf', 'sadf.jpg', 'sadf'),
(3, 'asdf', 'default_img', 'asdf');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
