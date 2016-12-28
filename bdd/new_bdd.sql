-- phpMyAdmin SQL Dump
-- version 4.6.5.1deb1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Dec 02, 2016 at 11:02 AM
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
(1, '', '192.168.20.10', '2016-12-02 11:01:32'),
(2, '', '192.168.20.102', '2016-12-02 11:01:32'),
(3, '', '192.168.20.103', '2016-12-02 11:01:32'),
(4, '', '192.168.20.104', '2016-12-02 11:01:32'),
(5, '', '192.168.20.106', '2016-12-02 11:01:32'),
(6, '', '192.168.20.107', '2016-12-02 11:01:32'),
(7, '', '192.168.20.108', '2016-12-02 11:01:32'),
(8, '', '192.168.20.109', '2016-12-02 11:01:32'),
(9, '', '192.168.20.111', '2016-12-02 11:01:32'),
(10, '', '192.168.20.112', '2016-12-02 11:01:32'),
(11, '', '192.168.20.22', '2016-12-02 11:01:32'),
(12, '', '192.168.20.254', '2016-12-02 11:01:32');

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE `services` (
  `sid` int(11) NOT NULL,
  `mid` int(11) NOT NULL,
  `proto` text NOT NULL,
  `port` int(11) NOT NULL,
  `nom_service` text NOT NULL,
  `state` text NOT NULL,
  `banner` text NOT NULL,
  `version` text NOT NULL,
  `last_view` datetime NOT NULL,
  `manage` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`sid`, `mid`, `proto`, `port`, `nom_service`, `state`, `banner`, `version`, `last_view`, `manage`) VALUES
(1, 1, 'tcp', 22, 'ssh', 'open', 'SSH-2.0-OpenSSH_6.7p1 Debian-5+deb8u3', '6.7p1 Debian 5+deb8u3', '2016-12-02 11:01:32', 0),
(2, 1, 'tcp', 53, 'domain', 'closed', '', '', '2016-12-02 11:01:32', 0),
(3, 1, 'tcp', 67, 'dhcps', 'closed', '', '', '2016-12-02 11:01:32', 0),
(4, 1, 'tcp', 68, 'dhcpc', 'closed', '', '', '2016-12-02 11:01:32', 0),
(5, 1, 'tcp', 80, 'http', 'closed', '', '', '2016-12-02 11:01:32', 0),
(6, 1, 'tcp', 110, 'pop3', 'closed', '', '', '2016-12-02 11:01:32', 0),
(7, 1, 'tcp', 123, 'ntp', 'closed', '', '', '2016-12-02 11:01:32', 0),
(8, 1, 'tcp', 143, 'imap', 'closed', '', '', '2016-12-02 11:01:32', 0),
(9, 1, 'tcp', 193, 'srmp', 'closed', '', '', '2016-12-02 11:01:32', 0),
(10, 1, 'tcp', 389, 'ldap', 'closed', '', '', '2016-12-02 11:01:32', 0),
(11, 1, 'tcp', 443, 'https', 'closed', '', '', '2016-12-02 11:01:32', 0),
(12, 2, 'tcp', 22, 'ssh', 'closed', '', '', '2016-12-02 11:01:32', 0),
(13, 2, 'tcp', 53, 'domain', 'closed', '', '', '2016-12-02 11:01:32', 0),
(14, 2, 'tcp', 67, 'dhcps', 'closed', '', '', '2016-12-02 11:01:32', 0),
(15, 2, 'tcp', 68, 'dhcpc', 'closed', '', '', '2016-12-02 11:01:32', 0),
(16, 2, 'tcp', 80, 'http', 'closed', '', '', '2016-12-02 11:01:32', 0),
(17, 2, 'tcp', 110, 'pop3', 'closed', '', '', '2016-12-02 11:01:32', 0),
(18, 2, 'tcp', 123, 'ntp', 'closed', '', '', '2016-12-02 11:01:32', 0),
(19, 2, 'tcp', 143, 'imap', 'closed', '', '', '2016-12-02 11:01:32', 0),
(20, 2, 'tcp', 193, 'srmp', 'closed', '', '', '2016-12-02 11:01:32', 0),
(21, 2, 'tcp', 389, 'ldap', 'closed', '', '', '2016-12-02 11:01:32', 0),
(22, 2, 'tcp', 443, 'https', 'closed', '', '', '2016-12-02 11:01:32', 0),
(23, 3, 'tcp', 22, 'ssh', 'open', 'SSH-2.0-OpenSSH_6.7p1 Debian-5+deb8u3', '6.7p1 Debian 5+deb8u3', '2016-12-02 11:01:32', 0),
(24, 3, 'tcp', 53, 'domain', 'closed', '', '', '2016-12-02 11:01:32', 0),
(25, 3, 'tcp', 67, 'dhcps', 'closed', '', '', '2016-12-02 11:01:32', 0),
(26, 3, 'tcp', 68, 'dhcpc', 'closed', '', '', '2016-12-02 11:01:32', 0),
(27, 3, 'tcp', 80, 'http', 'closed', '', '', '2016-12-02 11:01:32', 0),
(28, 3, 'tcp', 110, 'pop3', 'closed', '', '', '2016-12-02 11:01:32', 0),
(29, 3, 'tcp', 123, 'ntp', 'closed', '', '', '2016-12-02 11:01:32', 0),
(30, 3, 'tcp', 143, 'imap', 'closed', '', '', '2016-12-02 11:01:32', 0),
(31, 3, 'tcp', 193, 'srmp', 'closed', '', '', '2016-12-02 11:01:32', 0),
(32, 3, 'tcp', 389, 'ldap', 'closed', '', '', '2016-12-02 11:01:32', 0),
(33, 3, 'tcp', 443, 'https', 'closed', '', '', '2016-12-02 11:01:32', 0),
(34, 4, 'tcp', 22, 'ssh', 'open', 'SSH-2.0-OpenSSH_6.7p1 Debian-5+deb8u3', '6.7p1 Debian 5+deb8u3', '2016-12-02 11:01:32', 0),
(35, 4, 'tcp', 53, 'domain', 'closed', '', '', '2016-12-02 11:01:32', 0),
(36, 4, 'tcp', 67, 'dhcps', 'closed', '', '', '2016-12-02 11:01:32', 0),
(37, 4, 'tcp', 68, 'dhcpc', 'closed', '', '', '2016-12-02 11:01:32', 0),
(38, 4, 'tcp', 80, 'http', 'closed', '', '', '2016-12-02 11:01:32', 0),
(39, 4, 'tcp', 110, 'pop3', 'closed', '', '', '2016-12-02 11:01:32', 0),
(40, 4, 'tcp', 123, 'ntp', 'closed', '', '', '2016-12-02 11:01:32', 0),
(41, 4, 'tcp', 143, 'imap', 'closed', '', '', '2016-12-02 11:01:32', 0),
(42, 4, 'tcp', 193, 'srmp', 'closed', '', '', '2016-12-02 11:01:32', 0),
(43, 4, 'tcp', 389, 'ldap', 'closed', '', '', '2016-12-02 11:01:32', 0),
(44, 4, 'tcp', 443, 'https', 'closed', '', '', '2016-12-02 11:01:32', 0),
(45, 5, 'tcp', 22, 'ssh', 'open', 'SSH-2.0-OpenSSH_6.7p1 Debian-5+deb8u3', '6.7p1 Debian 5+deb8u3', '2016-12-02 11:01:32', 0),
(46, 5, 'tcp', 53, 'domain', 'closed', '', '', '2016-12-02 11:01:32', 0),
(47, 5, 'tcp', 67, 'dhcps', 'closed', '', '', '2016-12-02 11:01:32', 0),
(48, 5, 'tcp', 68, 'dhcpc', 'closed', '', '', '2016-12-02 11:01:32', 0),
(49, 5, 'tcp', 80, 'http', 'open', 'Apache/2.4.10 (Debian)', '2.4.10', '2016-12-02 11:01:32', 0),
(50, 5, 'tcp', 110, 'pop3', 'closed', '', '', '2016-12-02 11:01:32', 0),
(51, 5, 'tcp', 123, 'ntp', 'closed', '', '', '2016-12-02 11:01:32', 0),
(52, 5, 'tcp', 143, 'imap', 'closed', '', '', '2016-12-02 11:01:32', 0),
(53, 5, 'tcp', 193, 'srmp', 'closed', '', '', '2016-12-02 11:01:32', 0),
(54, 5, 'tcp', 389, 'ldap', 'closed', '', '', '2016-12-02 11:01:32', 0),
(55, 5, 'tcp', 443, 'http', 'open', 'Apache/2.4.10 (Debian)', '2.4.10', '2016-12-02 11:01:32', 0),
(56, 6, 'tcp', 22, 'ssh', 'open', 'SSH-2.0-OpenSSH_6.7p1 Debian-5+deb8u3', '6.7p1 Debian 5+deb8u3', '2016-12-02 11:01:32', 0),
(57, 6, 'tcp', 53, 'domain', 'closed', '', '', '2016-12-02 11:01:32', 0),
(58, 6, 'tcp', 67, 'dhcps', 'closed', '', '', '2016-12-02 11:01:32', 0),
(59, 6, 'tcp', 68, 'dhcpc', 'closed', '', '', '2016-12-02 11:01:32', 0),
(60, 6, 'tcp', 80, 'http', 'closed', '', '', '2016-12-02 11:01:32', 0),
(61, 6, 'tcp', 110, 'pop3', 'closed', '', '', '2016-12-02 11:01:32', 0),
(62, 6, 'tcp', 123, 'ntp', 'closed', '', '', '2016-12-02 11:01:32', 0),
(63, 6, 'tcp', 143, 'imap', 'closed', '', '', '2016-12-02 11:01:32', 0),
(64, 6, 'tcp', 193, 'srmp', 'closed', '', '', '2016-12-02 11:01:32', 0),
(65, 6, 'tcp', 389, 'ldap', 'open', '', '2.2.X - 2.3.X', '2016-12-02 11:01:32', 0),
(66, 6, 'tcp', 443, 'https', 'closed', '', '', '2016-12-02 11:01:32', 0),
(67, 7, 'tcp', 22, 'ssh', 'closed', '', '', '2016-12-02 11:01:32', 0),
(68, 7, 'tcp', 53, 'domain', 'closed', '', '', '2016-12-02 11:01:32', 0),
(69, 7, 'tcp', 67, 'dhcps', 'closed', '', '', '2016-12-02 11:01:32', 0),
(70, 7, 'tcp', 68, 'dhcpc', 'closed', '', '', '2016-12-02 11:01:32', 0),
(71, 7, 'tcp', 80, 'http', 'closed', '', '', '2016-12-02 11:01:32', 0),
(72, 7, 'tcp', 110, 'pop3', 'closed', '', '', '2016-12-02 11:01:32', 0),
(73, 7, 'tcp', 123, 'ntp', 'closed', '', '', '2016-12-02 11:01:32', 0),
(74, 7, 'tcp', 143, 'imap', 'closed', '', '', '2016-12-02 11:01:32', 0),
(75, 7, 'tcp', 193, 'srmp', 'closed', '', '', '2016-12-02 11:01:32', 0),
(76, 7, 'tcp', 389, 'ldap', 'closed', '', '', '2016-12-02 11:01:32', 0),
(77, 7, 'tcp', 443, 'https', 'closed', '', '', '2016-12-02 11:01:32', 0),
(78, 8, 'tcp', 53, 'domain', 'closed', '', '', '2016-12-02 11:01:32', 0),
(79, 8, 'tcp', 67, 'dhcps', 'closed', '', '', '2016-12-02 11:01:32', 0),
(80, 8, 'tcp', 123, 'ntp', 'closed', '', '', '2016-12-02 11:01:32', 0),
(81, 8, 'tcp', 193, 'srmp', 'closed', '', '', '2016-12-02 11:01:32', 0),
(82, 8, 'tcp', 389, 'ldap', 'closed', '', '', '2016-12-02 11:01:32', 0),
(83, 9, 'tcp', 22, 'ssh', 'open', 'SSH-2.0-OpenSSH_6.7p1 Debian-5+deb8u3', '6.7p1 Debian 5+deb8u3', '2016-12-02 11:01:32', 0),
(84, 9, 'tcp', 53, 'domain', 'open', '', '', '2016-12-02 11:01:32', 0),
(85, 9, 'tcp', 67, 'dhcps', 'closed', '', '', '2016-12-02 11:01:32', 0),
(86, 9, 'tcp', 68, 'dhcpc', 'closed', '', '', '2016-12-02 11:01:32', 0),
(87, 9, 'tcp', 80, 'http', 'closed', '', '', '2016-12-02 11:01:32', 0),
(88, 9, 'tcp', 110, 'pop3', 'closed', '', '', '2016-12-02 11:01:32', 0),
(89, 9, 'tcp', 123, 'ntp', 'closed', '', '', '2016-12-02 11:01:32', 0),
(90, 9, 'tcp', 143, 'imap', 'closed', '', '', '2016-12-02 11:01:32', 0),
(91, 9, 'tcp', 193, 'srmp', 'closed', '', '', '2016-12-02 11:01:32', 0),
(92, 9, 'tcp', 389, 'ldap', 'closed', '', '', '2016-12-02 11:01:32', 0),
(93, 9, 'tcp', 443, 'https', 'closed', '', '', '2016-12-02 11:01:32', 0),
(94, 10, 'tcp', 22, 'ssh', 'open', 'SSH-2.0-OpenSSH_6.7p1 Debian-5+deb8u3', '6.7p1 Debian 5+deb8u3', '2016-12-02 11:01:32', 0),
(95, 10, 'tcp', 53, 'domain', 'closed', '', '', '2016-12-02 11:01:32', 0),
(96, 10, 'tcp', 67, 'dhcps', 'closed', '', '', '2016-12-02 11:01:32', 0),
(97, 10, 'tcp', 68, 'dhcpc', 'closed', '', '', '2016-12-02 11:01:32', 0),
(98, 10, 'tcp', 80, 'http', 'closed', '', '', '2016-12-02 11:01:32', 0),
(99, 10, 'tcp', 110, 'pop3', 'closed', '', '', '2016-12-02 11:01:32', 0),
(100, 10, 'tcp', 123, 'ntp', 'closed', '', '', '2016-12-02 11:01:32', 0),
(101, 10, 'tcp', 143, 'imap', 'closed', '', '', '2016-12-02 11:01:32', 0),
(102, 10, 'tcp', 193, 'srmp', 'closed', '', '', '2016-12-02 11:01:32', 0),
(103, 10, 'tcp', 389, 'ldap', 'closed', '', '', '2016-12-02 11:01:32', 0),
(104, 10, 'tcp', 443, 'https', 'closed', '', '', '2016-12-02 11:01:32', 0),
(105, 11, 'tcp', 22, 'ssh', 'open', 'SSH-2.0-OpenSSH_6.7p1 Debian-5+deb8u3', '6.7p1 Debian 5+deb8u3', '2016-12-02 11:01:32', 0),
(106, 11, 'tcp', 53, 'domain', 'closed', '', '', '2016-12-02 11:01:32', 0),
(107, 11, 'tcp', 67, 'dhcps', 'closed', '', '', '2016-12-02 11:01:32', 0),
(108, 11, 'tcp', 68, 'dhcpc', 'closed', '', '', '2016-12-02 11:01:32', 0),
(109, 11, 'tcp', 80, 'http', 'open', 'nginx/1.10.1 + Phusion Passenger 5.0.30', '1.10.1', '2016-12-02 11:01:32', 0),
(110, 11, 'tcp', 110, 'pop3', 'closed', '', '', '2016-12-02 11:01:32', 0),
(111, 11, 'tcp', 123, 'ntp', 'closed', '', '', '2016-12-02 11:01:32', 0),
(112, 11, 'tcp', 143, 'imap', 'closed', '', '', '2016-12-02 11:01:32', 0),
(113, 11, 'tcp', 193, 'srmp', 'closed', '', '', '2016-12-02 11:01:32', 0),
(114, 11, 'tcp', 389, 'ldap', 'closed', '', '', '2016-12-02 11:01:32', 0),
(115, 11, 'tcp', 443, 'https', 'closed', '', '', '2016-12-02 11:01:32', 0),
(116, 12, 'tcp', 22, 'ssh', 'closed', '', '', '2016-12-02 11:01:32', 0),
(117, 12, 'tcp', 53, 'domain', 'closed', '', '', '2016-12-02 11:01:32', 0),
(118, 12, 'tcp', 67, 'dhcps', 'closed', '', '', '2016-12-02 11:01:32', 0),
(119, 12, 'tcp', 68, 'dhcpc', 'closed', '', '', '2016-12-02 11:01:32', 0),
(120, 12, 'tcp', 80, 'http', 'closed', '', '', '2016-12-02 11:01:32', 0),
(121, 12, 'tcp', 110, 'pop3', 'closed', '', '', '2016-12-02 11:01:32', 0),
(122, 12, 'tcp', 123, 'ntp', 'closed', '', '', '2016-12-02 11:01:32', 0),
(123, 12, 'tcp', 143, 'imap', 'closed', '', '', '2016-12-02 11:01:32', 0),
(124, 12, 'tcp', 193, 'srmp', 'closed', '', '', '2016-12-02 11:01:32', 0),
(125, 12, 'tcp', 389, 'ldap', 'closed', '', '', '2016-12-02 11:01:32', 0),
(126, 12, 'tcp', 443, 'https', 'closed', '', '', '2016-12-02 11:01:32', 0);

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
  MODIFY `sid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=127;
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
