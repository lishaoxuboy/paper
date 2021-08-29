/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50717
Source Host           : localhost:3306
Source Database       : paper1

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2021-08-29 12:06:05
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for auther
-- ----------------------------
DROP TABLE IF EXISTS `auther`;
CREATE TABLE `auther` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL COMMENT '作者名字',
  `english_name` varchar(255) DEFAULT NULL COMMENT '作者英文名',
  `org` varchar(255) DEFAULT NULL COMMENT '单位',
  `email` varchar(255) DEFAULT NULL COMMENT '工作邮箱',
  `addr` varchar(255) DEFAULT NULL COMMENT '联系地址',
  `job_title` varchar(255) DEFAULT NULL COMMENT '职称',
  `phone` varchar(128) DEFAULT NULL COMMENT '联系方式',
  `wechat` varchar(255) DEFAULT NULL COMMENT '微信',
  `paper_id` int(11) DEFAULT NULL COMMENT '作者关联的论文id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auther
-- ----------------------------
INSERT INTO `auther` VALUES ('47', '56', 'english_name', '78', '78', '78', '助理研究员', '78', '78', '2');
INSERT INTO `auther` VALUES ('48', 'shukai', '', '南加大', 'kaishu@usc.edu', '3335 S FIGUEROA ST, APT 544', '国内学生', '15657932699', '1', '1');
INSERT INTO `auther` VALUES ('49', '南加大2', 'english_name', '2', 'kaishu@usc.edu', '1', '工程师', '3', '124323423', '1');
INSERT INTO `auther` VALUES ('67', '56', 'english_name', '67090', '67', '67', '副研究员', '67', '67', '3');

-- ----------------------------
-- Table structure for paper
-- ----------------------------
DROP TABLE IF EXISTS `paper`;
CREATE TABLE `paper` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text COMMENT '论文名字',
  `number` varchar(255) DEFAULT NULL COMMENT '论文编号',
  `key_word` text COMMENT '论文关键字',
  `abstract` text COMMENT '论文关摘要',
  `pdf_path` varchar(255) DEFAULT NULL COMMENT '上传的论文的pdf',
  `word_path` varchar(255) DEFAULT NULL COMMENT '上传的论文的word',
  `pdf_name` varchar(255) DEFAULT NULL COMMENT 'pdf文件名字',
  `word_name` varchar(255) DEFAULT NULL COMMENT 'word文档名字',
  `manage_author_id` int(11) DEFAULT NULL COMMENT '管理改论文的作者，作者可能有多个',
  `user_id` int(11) DEFAULT NULL COMMENT '改论文所属的用户ID',
  `create_date` varchar(255) DEFAULT NULL COMMENT '创建日期',
  `comments` varchar(255) DEFAULT NULL COMMENT '管理员提出的建议',
  `status` varchar(128) DEFAULT NULL COMMENT '状态 1：未批注 2: 已批注 3: 被采纳（也就是''待付款''）  4：已拒稿 5:已付款 ',
  `money` varchar(255) DEFAULT NULL COMMENT '订单金额',
  `pay_mode` varchar(128) DEFAULT NULL COMMENT '付款方式',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of paper
-- ----------------------------
INSERT INTO `paper` VALUES ('1', '舒凯真帅', '1624554790711635', '1234567', '发卡机阀打开链接法拉第时间发按收费sdas', 'static\\uploads\\0386fa6c-3a2d-32af-9003-feef72a57c83.pdf', 'static\\uploads\\c45cba12-3b38-3bbf-a115-4f633feb9b43.docx', 'stock price.pdf', 'stock price.docx', '48', '5', '2021-06-25 01:13:10', null, '1', null, null);
INSERT INTO `paper` VALUES ('2', '12', '16246079227748942', '12', '12', 'static\\uploads\\27c80006-dfec-3993-a55d-cf9c63a181dd.pdf', 'static\\uploads\\38773ef2-9a8e-3a29-a65b-c50d44536ab5.docx', '证据目录.pdf', '民事起诉状（余娟-法人）.docx', '47', '6', '2021-06-25 15:58:42', null, '1', null, null);
INSERT INTO `paper` VALUES ('3', 'SNDNDSDKAS DLKA', '16249723872699587', 'SDSDSDSDSD', 'SDSADADA', 'static\\uploads\\d1f78b70-565f-3b10-b295-17ab65d63e99.pdf', 'static\\uploads\\06ac9022-2ce4-3f9e-86f1-8d9c45c23ee4.docx', '（云顶1+3）智慧景区运行监测大数据平台2003.pdf', '硬件呼叫器操作流程.docx', '67', '6', '2021-06-29 21:13:07', null, '1', null, null);

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL COMMENT '名字',
  `account` varchar(255) DEFAULT NULL COMMENT '账号',
  `password` varchar(255) DEFAULT NULL COMMENT '密码',
  `email_addr` varchar(255) DEFAULT NULL COMMENT '邮箱地址',
  `role` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', 'admin', 'admin', '21232f297a57a5a743894a0e4a801fc3', '15194576294@163.com', '2');
INSERT INTO `user` VALUES ('5', '舒凯', 'shukai', 'c510bd6a9d6552a653dd66e6cbd85c1e', '15657932699@163.com', '1');
INSERT INTO `user` VALUES ('6', 'lsxboy', 'lsxboy', '2be9bd7a3434f7038ca27d1918de58bd', '18855346981@163.com', '1');
