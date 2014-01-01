# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.6.12)
# Database: development
# Generation Time: 2013-10-15 09:53:52 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table categories
# ------------------------------------------------------------

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;

INSERT INTO `categories` (`id`, `name`, `parent_id`)
VALUES
	(1,'Physics',NULL),
	(2,'Mathematics',NULL),
	(3,'Chemistry',NULL),
	(4,'Condensed Matter',1),
	(5,'Ultra-cold Gases',1),
	(6,'Material Science',1),
	(7,'Disordered Systems and Neural Networks',1),
	(8,'Mesoscale and Nanoscale Physics',1),
	(9,'Quantum Optics',1),
	(10,'Soft Condensed Matter',1),
	(11,'Statistical Mechanics',1),
	(12,'Quantum Chemistry',1),
	(13,'Astrophysics',1),
	(14,'Cosmology',1),
	(15,'High Energy Physics',1),
	(16,'Atomic Physics',1),
	(17,'Computer Science',NULL),
	(18,'Economy',NULL),
	(19,'Statistics',NULL),
	(20,'Psychology',NULL),
	(21,'Philosophy',NULL),
	(22,'History',NULL);

/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table journals
# ------------------------------------------------------------

LOCK TABLES `journals` WRITE;
/*!40000 ALTER TABLE `journals` DISABLE KEYS */;

INSERT INTO `journals` (`id`, `title`, `short_title`, `url`, `last_checked`, `next_check`, `metadata_update`, `favicon`)
VALUES
	(1,'Physical Review Letter','PRL','http://feeds.aps.org/rss/recent/prl.xml','2013-01-01 00:00:00','2013-01-01 00:00:00','2013-01-01 00:00:00','http://publish.aps.org/favicon.ico'),
	(2,'Nature','Nature','http://feeds.nature.com/NatureLatestResearch','2013-01-01 00:00:00','2013-01-01 00:00:00','2013-01-01 00:00:00','http://www.nature.com/favicon.ico'),
	(3,'arXiv Quantum Gases','arXiv:cond-mat.quant-gas','http://export.arxiv.org/rss/cond-mat.quant-gas','2013-01-01 00:00:00','2013-01-01 00:00:00','2013-01-01 00:00:00','http://arxiv.org/favicon.ico'),
	(4,'arXiv Disordered Systems and Neural Networks','arXiv:cond-mat.dis-nn','http://export.arxiv.org/rss/cond-mat.dis-nn/','2013-01-01 00:00:00','2013-01-01 00:00:00','2013-01-01 00:00:00','http://arxiv.org/favicon.ico'),
	(5,'arXiv Material Science','arXiv:cond-mat.mtrl-sci','http://export.arxiv.org/rss/cond-mat.mtrl-sci','2013-01-01 00:00:00','2013-01-01 00:00:00','2013-01-01 00:00:00','http://arxiv.org/favicon.ico'),
	(6,'arXiv Mesoscale and Nanoscale Physics','arXiv:cond-mat.mes-hall','http://export.arxiv.org/rss/cond-mat.mes-hall/','2013-01-01 00:00:00','2013-01-01 00:00:00','2013-01-01 00:00:00','http://arxiv.org/favicon.ico'),
	(7,'arXiv Other Condensed Matter','arXiv:cond-mat.other','http://export.arxiv.org/rss/cond-mat.other/','2013-01-01 00:00:00','2013-01-01 00:00:00','2013-01-01 00:00:00','http://arxiv.org/favicon.ico'),
	(8,'arXiv Soft Condensed Matter','arXiv:cond-mat.soft','http://export.arxiv.org/rss/cond-mat.soft/','2013-01-01 00:00:00','2013-01-01 00:00:00','2013-01-01 00:00:00','http://arxiv.org/favicon.ico'),
	(9,'arXiv Statistical Mechanics','arXiv:cond-mat.stat-mech','http://export.arxiv.org/rss/cond-mat.stat-mech','2013-01-01 00:00:00','2013-01-01 00:00:00','2013-01-01 00:00:00','http://arxiv.org/favicon.ico'),
	(10,'arXiv Superconductivity','arXiv:cond-mat.supr-con','http://export.arxiv.org/rss/cond-mat.supr-con','2013-01-01 00:00:00','2013-01-01 00:00:00','2013-01-01 00:00:00','http://arxiv.org/favicon.ico'),
	(11,'arXiv Strongly Correlated Electrons','arXiv:cond-mat.str-el','http://export.arxiv.org/rss/cond-mat.str-el','2013-01-01 00:00:00','2013-01-01 00:00:00','2013-01-01 00:00:00','http://arxiv.org/favicon.ico'),
	(12,'Nature Physics','Nature Physics','http://feeds.nature.com/nphys/rss/current','2013-01-01 00:00:00','2013-01-01 00:00:00','2013-01-01 00:00:00','http://www.nature.com/favicon.ico'),
	(13,'New Journal of Physics','NJP','http://iopscience.iop.org/1367-2630/?rss=1','2013-01-01 00:00:00','2013-01-01 00:00:00','2013-01-01 00:00:00',NULL),
	(14,'Science','Science','http://www.sciencemag.org/rss/current.xml','2013-01-01 00:00:00','2013-01-01 00:00:00','2013-01-01 00:00:00',NULL);

/*!40000 ALTER TABLE `journals` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table journals_categories
# ------------------------------------------------------------

LOCK TABLES `journals_categories` WRITE;
/*!40000 ALTER TABLE `journals_categories` DISABLE KEYS */;

INSERT INTO `journals_categories` (`journal_id`, `category_id`)
VALUES
	(1,1),
	(12,1),
	(13,1),
	(14,1),
	(2,1),
	(3,5);

/*!40000 ALTER TABLE `journals_categories` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table paths
# ------------------------------------------------------------

LOCK TABLES `paths` WRITE;
/*!40000 ALTER TABLE `paths` DISABLE KEYS */;

INSERT INTO `paths` (`id`, `journal_id`, `type`, `path`)
VALUES
	(3,1,'abstract','//div[@class=\"aps-abstractbox\"]/p'),
	(4,2,'abstract','//*[@id=\"abstract\"]/div/p'),
	(5,2,'abstract','//*[@id=\"first-paragraph\"]/p'),
	(6,3,'abstract','//*[@id=\"abs\"]/div[2]/blockquote'),
	(7,4,'abstract','//*[@id=\"abs\"]/div[2]/blockquote'),
	(8,5,'abstract','//*[@id=\"abs\"]/div[2]/blockquote'),
	(9,6,'abstract','//*[@id=\"abs\"]/div[2]/blockquote'),
	(10,7,'abstract','//*[@id=\"abs\"]/div[2]/blockquote'),
	(11,8,'abstract','//*[@id=\"abs\"]/div[2]/blockquote'),
	(12,9,'abstract','//*[@id=\"abs\"]/div[2]/blockquote'),
	(13,10,'abstract','//*[@id=\"abs\"]/div[2]/blockquote'),
	(14,11,'abstract','//*[@id=\"abs\"]/div[2]/blockquote'),
	(15,14,'abstract','//*[@id=\"abstract-3\"]'),
	(16,13,'abstract','//*[@id=\"articleAbsctract\"]'),
	(17,2,'abstract','//*[@id=\"first-paragraph\"]/p[2]');

/*!40000 ALTER TABLE `paths` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
