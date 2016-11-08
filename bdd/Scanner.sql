-- phpMyAdmin SQL Dump
-- version 4.6.4deb1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 08, 2016 at 04:49 PM
-- Server version: 5.6.30-1
-- PHP Version: 7.0.12-1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Scanner`
--

-- --------------------------------------------------------

--
-- Table structure for table `machines`
--

CREATE TABLE `machines` (
  `mid` int(11) NOT NULL,
  `fqdn` text CHARACTER SET utf8 NOT NULL,
  `ip` text CHARACTER SET utf8 NOT NULL,
  `last_view` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `machines`
--

INSERT INTO `machines` (`mid`, `fqdn`, `ip`, `last_view`) VALUES
(1, '', '192.168.20.10', '2016-11-08 16:43:16'),
(2, '', '192.168.20.102', '2016-11-08 16:43:16'),
(3, 'ntp.i204.fr', '192.168.20.103', '2016-11-08 16:43:16'),
(4, 'syslog.i204.fr', '192.168.20.104', '2016-11-08 16:43:16'),
(5, 'service-management.i204.fr', '192.168.20.106', '2016-11-08 16:43:16'),
(6, 'ldap.i204.fr', '192.168.20.107', '2016-11-08 16:43:16'),
(7, '', '192.168.20.108', '2016-11-08 16:43:16'),
(8, 'stockage.i204.fr', '192.168.20.109', '2016-11-08 16:43:16'),
(9, '', '192.168.20.111', '2016-11-08 16:43:16'),
(10, '', '192.168.20.112', '2016-11-08 16:43:16'),
(11, '', '192.168.20.22', '2016-11-08 16:43:16'),
(12, '', '192.168.20.254', '2016-11-08 16:43:16');

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE `services` (
  `sid` int(11) NOT NULL,
  `mid` int(11) NOT NULL,
  `port` int(11) NOT NULL,
  `proto` text NOT NULL,
  `state` text NOT NULL,
  `banner` text NOT NULL,
  `version` text NOT NULL,
  `last_view` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`sid`, `mid`, `port`, `proto`, `state`, `banner`, `version`, `last_view`) VALUES
(1, 1, 22, 'ssh', 'open', 'SSH-2.0-OpenSSH_6.7p1 Debian-5+deb8u3', '6.7p1 Debian 5+deb8u3', '2016-11-08 16:43:16'),
(2, 1, 53, 'domain', 'closed', '', '', '2016-11-08 16:43:16'),
(3, 1, 67, 'dhcps', 'closed', '', '', '2016-11-08 16:43:16'),
(4, 1, 68, 'dhcpc', 'closed', '', '', '2016-11-08 16:43:16'),
(5, 1, 80, 'http', 'closed', '', '', '2016-11-08 16:43:16'),
(6, 1, 110, 'pop3', 'closed', '', '', '2016-11-08 16:43:16'),
(7, 1, 123, 'ntp', 'closed', '', '', '2016-11-08 16:43:16'),
(8, 1, 143, 'imap', 'closed', '', '', '2016-11-08 16:43:16'),
(9, 1, 193, 'srmp', 'closed', '', '', '2016-11-08 16:43:16'),
(10, 1, 389, 'ldap', 'closed', '', '', '2016-11-08 16:43:16'),
(11, 1, 443, 'https', 'closed', '', '', '2016-11-08 16:43:16'),
(12, 2, 22, 'ssh', 'closed', '', '', '2016-11-08 16:43:16'),
(13, 2, 53, 'domain', 'closed', '', '', '2016-11-08 16:43:16'),
(14, 2, 67, 'dhcps', 'closed', '', '', '2016-11-08 16:43:16'),
(15, 2, 68, 'dhcpc', 'closed', '', '', '2016-11-08 16:43:16'),
(16, 2, 80, 'http', 'closed', '', '', '2016-11-08 16:43:16'),
(17, 2, 110, 'pop3', 'closed', '', '', '2016-11-08 16:43:16'),
(18, 2, 123, 'ntp', 'closed', '', '', '2016-11-08 16:43:16'),
(19, 2, 143, 'imap', 'closed', '', '', '2016-11-08 16:43:16'),
(20, 2, 193, 'srmp', 'closed', '', '', '2016-11-08 16:43:16'),
(21, 2, 389, 'ldap', 'closed', '', '', '2016-11-08 16:43:16'),
(22, 2, 443, 'https', 'closed', '', '', '2016-11-08 16:43:16'),
(23, 3, 22, 'ssh', 'open', 'SSH-2.0-OpenSSH_6.7p1 Debian-5+deb8u3', '6.7p1 Debian 5+deb8u3', '2016-11-08 16:43:16'),
(24, 3, 53, 'domain', 'closed', '', '', '2016-11-08 16:43:16'),
(25, 3, 67, 'dhcps', 'closed', '', '', '2016-11-08 16:43:16'),
(26, 3, 68, 'dhcpc', 'closed', '', '', '2016-11-08 16:43:16'),
(27, 3, 80, 'http', 'closed', '', '', '2016-11-08 16:43:16'),
(28, 3, 110, 'pop3', 'closed', '', '', '2016-11-08 16:43:16'),
(29, 3, 123, 'ntp', 'closed', '', '', '2016-11-08 16:43:16'),
(30, 3, 143, 'imap', 'closed', '', '', '2016-11-08 16:43:16'),
(31, 3, 193, 'srmp', 'closed', '', '', '2016-11-08 16:43:16'),
(32, 3, 389, 'ldap', 'closed', '', '', '2016-11-08 16:43:16'),
(33, 3, 443, 'https', 'closed', '', '', '2016-11-08 16:43:16'),
(34, 4, 22, 'ssh', 'open', 'SSH-2.0-OpenSSH_6.7p1 Debian-5+deb8u3', '6.7p1 Debian 5+deb8u3', '2016-11-08 16:43:16'),
(35, 4, 53, 'domain', 'closed', '', '', '2016-11-08 16:43:16'),
(36, 4, 67, 'dhcps', 'closed', '', '', '2016-11-08 16:43:16'),
(37, 4, 68, 'dhcpc', 'closed', '', '', '2016-11-08 16:43:16'),
(38, 4, 80, 'http', 'closed', '', '', '2016-11-08 16:43:16'),
(39, 4, 110, 'pop3', 'closed', '', '', '2016-11-08 16:43:16'),
(40, 4, 123, 'ntp', 'closed', '', '', '2016-11-08 16:43:16'),
(41, 4, 143, 'imap', 'closed', '', '', '2016-11-08 16:43:16'),
(42, 4, 193, 'srmp', 'closed', '', '', '2016-11-08 16:43:16'),
(43, 4, 389, 'ldap', 'closed', '', '', '2016-11-08 16:43:16'),
(44, 4, 443, 'https', 'closed', '', '', '2016-11-08 16:43:16'),
(45, 5, 22, 'ssh', 'open', 'SSH-2.0-OpenSSH_6.7p1 Debian-5+deb8u3', '6.7p1 Debian 5+deb8u3', '2016-11-08 16:43:16'),
(46, 5, 53, 'domain', 'closed', '', '', '2016-11-08 16:43:16'),
(47, 5, 67, 'dhcps', 'closed', '', '', '2016-11-08 16:43:16'),
(48, 5, 68, 'dhcpc', 'closed', '', '', '2016-11-08 16:43:16'),
(49, 5, 80, 'http', 'open', 'Apache/2.4.10 (Debian)', '2.4.10', '2016-11-08 16:43:16'),
(50, 5, 110, 'pop3', 'closed', '', '', '2016-11-08 16:43:16'),
(51, 5, 123, 'ntp', 'closed', '', '', '2016-11-08 16:43:16'),
(52, 5, 143, 'imap', 'closed', '', '', '2016-11-08 16:43:16'),
(53, 5, 193, 'srmp', 'closed', '', '', '2016-11-08 16:43:16'),
(54, 5, 389, 'ldap', 'closed', '', '', '2016-11-08 16:43:16'),
(55, 5, 443, 'http', 'open', 'Apache/2.4.10 (Debian)', '2.4.10', '2016-11-08 16:43:16'),
(56, 6, 22, 'ssh', 'open', 'SSH-2.0-OpenSSH_6.7p1 Debian-5+deb8u3', '6.7p1 Debian 5+deb8u3', '2016-11-08 16:43:16'),
(57, 6, 53, 'domain', 'closed', '', '', '2016-11-08 16:43:16'),
(58, 6, 67, 'dhcps', 'closed', '', '', '2016-11-08 16:43:16'),
(59, 6, 68, 'dhcpc', 'closed', '', '', '2016-11-08 16:43:16'),
(60, 6, 80, 'http', 'closed', '', '', '2016-11-08 16:43:16'),
(61, 6, 110, 'pop3', 'closed', '', '', '2016-11-08 16:43:16'),
(62, 6, 123, 'ntp', 'closed', '', '', '2016-11-08 16:43:16'),
(63, 6, 143, 'imap', 'closed', '', '', '2016-11-08 16:43:16'),
(64, 6, 193, 'srmp', 'closed', '', '', '2016-11-08 16:43:16'),
(65, 6, 389, 'ldap', 'open', '', '2.2.X - 2.3.X', '2016-11-08 16:43:16'),
(66, 6, 443, 'https', 'closed', '', '', '2016-11-08 16:43:16'),
(67, 7, 22, 'ssh', 'closed', '', '', '2016-11-08 16:43:16'),
(68, 7, 53, 'domain', 'closed', '', '', '2016-11-08 16:43:16'),
(69, 7, 67, 'dhcps', 'closed', '', '', '2016-11-08 16:43:16'),
(70, 7, 68, 'dhcpc', 'closed', '', '', '2016-11-08 16:43:16'),
(71, 7, 80, 'http', 'closed', '', '', '2016-11-08 16:43:16'),
(72, 7, 110, 'pop3', 'closed', '', '', '2016-11-08 16:43:16'),
(73, 7, 123, 'ntp', 'closed', '', '', '2016-11-08 16:43:16'),
(74, 7, 143, 'imap', 'closed', '', '', '2016-11-08 16:43:16'),
(75, 7, 193, 'srmp', 'closed', '', '', '2016-11-08 16:43:16'),
(76, 7, 389, 'ldap', 'closed', '', '', '2016-11-08 16:43:16'),
(77, 7, 443, 'https', 'closed', '', '', '2016-11-08 16:43:16'),
(78, 8, 22, 'ssh', 'closed', '', '', '2016-11-08 16:43:16'),
(79, 8, 53, 'domain', 'closed', '', '', '2016-11-08 16:43:16'),
(80, 8, 67, 'dhcps', 'closed', '', '', '2016-11-08 16:43:16'),
(81, 8, 68, 'dhcpc', 'closed', '', '', '2016-11-08 16:43:16'),
(82, 8, 80, 'http', 'closed', '', '', '2016-11-08 16:43:16'),
(83, 8, 110, 'pop3', 'closed', '', '', '2016-11-08 16:43:16'),
(84, 8, 123, 'ntp', 'closed', '', '', '2016-11-08 16:43:16'),
(85, 8, 143, 'imap', 'closed', '', '', '2016-11-08 16:43:16'),
(86, 8, 193, 'srmp', 'closed', '', '', '2016-11-08 16:43:16'),
(87, 8, 389, 'ldap', 'closed', '', '', '2016-11-08 16:43:16'),
(88, 8, 443, 'https', 'closed', '', '', '2016-11-08 16:43:16'),
(89, 9, 22, 'ssh', 'open', 'SSH-2.0-OpenSSH_6.7p1 Debian-5+deb8u3', '6.7p1 Debian 5+deb8u3', '2016-11-08 16:43:16'),
(90, 9, 53, 'domain', 'open', '', '', '2016-11-08 16:43:16'),
(91, 9, 67, 'dhcps', 'closed', '', '', '2016-11-08 16:43:16'),
(92, 9, 68, 'dhcpc', 'closed', '', '', '2016-11-08 16:43:16'),
(93, 9, 80, 'http', 'closed', '', '', '2016-11-08 16:43:16'),
(94, 9, 110, 'pop3', 'closed', '', '', '2016-11-08 16:43:16'),
(95, 9, 123, 'ntp', 'closed', '', '', '2016-11-08 16:43:16'),
(96, 9, 143, 'imap', 'closed', '', '', '2016-11-08 16:43:16'),
(97, 9, 193, 'srmp', 'closed', '', '', '2016-11-08 16:43:16'),
(98, 9, 389, 'ldap', 'closed', '', '', '2016-11-08 16:43:16'),
(99, 9, 443, 'https', 'closed', '', '', '2016-11-08 16:43:16'),
(100, 10, 22, 'ssh', 'open', 'SSH-2.0-OpenSSH_6.7p1 Debian-5+deb8u3', '6.7p1 Debian 5+deb8u3', '2016-11-08 16:43:16'),
(101, 10, 53, 'domain', 'closed', '', '', '2016-11-08 16:43:16'),
(102, 10, 67, 'dhcps', 'closed', '', '', '2016-11-08 16:43:16'),
(103, 10, 68, 'dhcpc', 'closed', '', '', '2016-11-08 16:43:16'),
(104, 10, 80, 'http', 'closed', '', '', '2016-11-08 16:43:16'),
(105, 10, 110, 'pop3', 'closed', '', '', '2016-11-08 16:43:16'),
(106, 10, 123, 'ntp', 'closed', '', '', '2016-11-08 16:43:16'),
(107, 10, 143, 'imap', 'closed', '', '', '2016-11-08 16:43:16'),
(108, 10, 193, 'srmp', 'closed', '', '', '2016-11-08 16:43:16'),
(109, 10, 389, 'ldap', 'closed', '', '', '2016-11-08 16:43:16'),
(110, 10, 443, 'https', 'closed', '', '', '2016-11-08 16:43:16'),
(111, 11, 22, 'ssh', 'open', 'SSH-2.0-OpenSSH_6.7p1 Debian-5+deb8u3', '6.7p1 Debian 5+deb8u3', '2016-11-08 16:43:16'),
(112, 11, 53, 'domain', 'closed', '', '', '2016-11-08 16:43:16'),
(113, 11, 67, 'dhcps', 'closed', '', '', '2016-11-08 16:43:16'),
(114, 11, 68, 'dhcpc', 'closed', '', '', '2016-11-08 16:43:16'),
(115, 11, 80, 'http', 'open', 'nginx/1.10.1 + Phusion Passenger 5.0.30', '1.10.1', '2016-11-08 16:43:16'),
(116, 11, 110, 'pop3', 'closed', '', '', '2016-11-08 16:43:16'),
(117, 11, 123, 'ntp', 'closed', '', '', '2016-11-08 16:43:16'),
(118, 11, 143, 'imap', 'closed', '', '', '2016-11-08 16:43:16'),
(119, 11, 193, 'srmp', 'closed', '', '', '2016-11-08 16:43:16'),
(120, 11, 389, 'ldap', 'closed', '', '', '2016-11-08 16:43:16'),
(121, 11, 443, 'https', 'closed', '', '', '2016-11-08 16:43:16'),
(122, 12, 22, 'ssh', 'closed', '', '', '2016-11-08 16:43:16'),
(123, 12, 53, 'domain', 'closed', '', '', '2016-11-08 16:43:16'),
(124, 12, 67, 'dhcps', 'closed', '', '', '2016-11-08 16:43:16'),
(125, 12, 68, 'dhcpc', 'closed', '', '', '2016-11-08 16:43:16'),
(126, 12, 80, 'http', 'closed', '', '', '2016-11-08 16:43:16'),
(127, 12, 110, 'pop3', 'closed', '', '', '2016-11-08 16:43:16'),
(128, 12, 123, 'ntp', 'closed', '', '', '2016-11-08 16:43:16'),
(129, 12, 143, 'imap', 'closed', '', '', '2016-11-08 16:43:16'),
(130, 12, 193, 'srmp', 'closed', '', '', '2016-11-08 16:43:16'),
(131, 12, 389, 'ldap', 'closed', '', '', '2016-11-08 16:43:16'),
(132, 12, 443, 'https', 'closed', '', '', '2016-11-08 16:43:16');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `machines`
--
ALTER TABLE `machines`
  ADD PRIMARY KEY (`mid`),
  ADD KEY `mid` (`mid`) USING BTREE,
  ADD KEY `last_view` (`last_view`) USING BTREE;

--
-- Indexes for table `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`sid`),
  ADD KEY `mid` (`mid`) USING BTREE,
  ADD KEY `sid` (`sid`) USING BTREE,
  ADD KEY `last_view` (`last_view`) USING BTREE,
  ADD KEY `port` (`port`) USING BTREE;

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `machines`
--
ALTER TABLE `machines`
  MODIFY `mid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
--
-- AUTO_INCREMENT for table `services`
--
ALTER TABLE `services`
  MODIFY `sid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=133;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `services`
--
ALTER TABLE `services`
  ADD CONSTRAINT `fk_mid` FOREIGN KEY (`mid`) REFERENCES `machines` (`mid`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
