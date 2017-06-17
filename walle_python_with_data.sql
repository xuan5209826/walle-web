/*
 Navicat Premium Data Transfer

 Source Server         : localdata
 Source Server Type    : MySQL
 Source Server Version : 50704
 Source Host           : localhost
 Source Database       : walle_python

 Target Server Type    : MySQL
 Target Server Version : 50704
 File Encoding         : utf-8

 Date: 06/12/2017 19:35:33 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `access`
-- ----------------------------
DROP TABLE IF EXISTS `access`;
CREATE TABLE `access` (
  `id` int(15) NOT NULL AUTO_INCREMENT,
  `name_cn` varchar(30) NOT NULL COMMENT '模块中文名称',
  `name_en` varchar(30) NOT NULL COMMENT '模块英文名称',
  `pid` int(6) NOT NULL COMMENT '父模块id，顶级pid为0',
  `type` enum('action','controller','module') DEFAULT 'action' COMMENT '类型',
  `sequence` int(11) DEFAULT '0' COMMENT '排序序号sprintf("%2d%2d%2d", module_id, controller_id, 自增两位数)',
  `archive` tinyint(1) DEFAULT '0' COMMENT '归档：0有效，1无效',
  `icon` varchar(30) DEFAULT '' COMMENT '模块',
  `fe_url` varchar(100) DEFAULT '' COMMENT '前端url',
  `fe_visible` tinyint(1) DEFAULT '1' COMMENT '前端是否展示该模块 0不展示，1展示',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=utf8 COMMENT='权限表';

-- ----------------------------
--  Records of `access`
-- ----------------------------
BEGIN;
INSERT INTO `access` VALUES ('1', '用户中心', '', '0', 'module', '10001', '0', 'leaf', 'xx.yy.zz', '1', '2017-06-11 23:11:38', '2017-06-12 00:15:29'), ('2', '配置中心', '', '0', 'module', '10002', '0', 'leaf', 'xx.yy.zz', '1', '2017-06-11 23:11:52', '2017-06-12 00:15:29'), ('3', '上线单', '', '0', 'module', '10003', '0', 'leaf', 'xx.yy.zz', '1', '2017-06-11 23:12:45', '2017-06-12 00:15:29'), ('11', '用户管理', '', '1', 'controller', '10101', '0', 'leaf', 'xx.yy.zz', '1', '2017-06-11 23:13:51', '2017-06-12 00:15:29'), ('12', '用户组', '', '1', 'controller', '10102', '0', 'leaf', 'xx.yy.zz', '1', '2017-06-11 23:14:11', '2017-06-12 00:15:29'), ('13', '角色', '', '1', 'controller', '10103', '0', 'leaf', 'xx.yy.zz', '1', '2017-06-11 23:14:44', '2017-06-12 00:15:29'), ('14', '环境管理', '', '2', 'controller', '10201', '0', 'leaf', 'xx.yy.zz', '1', '2017-06-11 23:15:30', '2017-06-12 00:15:29'), ('15', '服务器管理', '', '2', 'controller', '10202', '0', 'leaf', 'xx.yy.zz', '1', '2017-06-11 23:15:51', '2017-06-12 00:15:29'), ('16', '项目管理', '', '2', 'controller', '10203', '0', 'leaf', 'xx.yy.zz', '1', '2017-06-11 23:16:18', '2017-06-12 00:15:29'), ('101', '查看', '', '11', 'action', '11101', '0', 'leaf', 'xx.yy.zz', '1', '2017-06-11 23:17:12', '2017-06-12 00:15:29'), ('102', '修改', '', '11', 'action', '11102', '0', 'leaf', 'xx.yy.zz', '1', '2017-06-11 23:17:26', '2017-06-12 00:15:29'), ('103', '新增', '', '11', 'action', '11103', '0', 'leaf', 'xx.yy.zz', '1', '2017-06-11 23:17:59', '2017-06-12 00:15:29'), ('104', '删除', '', '11', 'action', '11104', '0', 'leaf', 'xx.yy.zz', '1', '2017-06-11 23:18:16', '2017-06-12 00:15:29');
COMMIT;

-- ----------------------------
--  Table structure for `alembic_version`
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `environment`
-- ----------------------------
DROP TABLE IF EXISTS `environment`;
CREATE TABLE `environment` (
  `id` int(10) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `name` varchar(100) DEFAULT 'master' COMMENT '环境名称',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态：0无效，1有效',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COMMENT='项目环境配置表';

-- ----------------------------
--  Records of `environment`
-- ----------------------------
BEGIN;
INSERT INTO `environment` VALUES ('2', '开发环境', '1', '2017-03-08 17:26:07', '2017-05-14 10:37:37'), ('3', '腾讯云测试联调', '1', '2017-05-13 11:26:42', '2017-05-13 11:26:42'), ('5', '一个可以删除的环境', '1', '2017-05-14 10:38:12', '2017-05-14 10:38:12'), ('6', '一个可以删除环境', '1', '2017-05-14 10:40:47', '2017-05-14 10:40:47'), ('7', '一个可以删环境', '1', '2017-05-14 10:42:23', '2017-05-14 10:42:23'), ('8', '一个可以环境', '1', '2017-05-14 10:42:58', '2017-05-14 10:42:58'), ('9', '开发环境火', '1', '2017-05-14 10:46:31', '2017-05-14 23:46:58'), ('10', '生产环境要在', '1', '2017-05-14 23:47:13', '2017-05-14 23:47:13');
COMMIT;

-- ----------------------------
--  Table structure for `foo`
-- ----------------------------
DROP TABLE IF EXISTS `foo`;
CREATE TABLE `foo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `foo`
-- ----------------------------
BEGIN;
INSERT INTO `foo` VALUES ('1', '中test005', 'wushuiyong0095@walle-web.io', '2017-05-22 22:45:14', '2017-05-22 22:45:14'), ('2', 'wushuiyong1', 'wushuiyong1@walle-web.io', '2017-05-22 23:17:48', '2017-05-22 23:17:48'), ('3', 'wushuiyong2', 'wushuiyong2@walle-web.io', '2017-05-22 23:17:48', '2017-05-22 23:17:48');
COMMIT;

-- ----------------------------
--  Table structure for `project`
-- ----------------------------
DROP TABLE IF EXISTS `project`;
CREATE TABLE `project` (
  `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '记录id',
  `user_id` int(10) NOT NULL COMMENT '添加项目的用户id',
  `name` varchar(100) DEFAULT 'master' COMMENT '项目名字',
  `environment_id` int(1) NOT NULL COMMENT 'environment的id',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态：0无效，1有效',
  `version` varchar(40) DEFAULT '' COMMENT '线上当前版本，用于快速回滚',
  `excludes` text COMMENT '要排除的文件',
  `target_user` varchar(50) NOT NULL COMMENT '目标机器的登录用户',
  `target_root` varchar(200) NOT NULL COMMENT '目标机器的 server 目录',
  `target_library` varchar(200) NOT NULL COMMENT '目标机器的版本库',
  `server_ids` text COMMENT '目标机器列表',
  `task_vars` text COMMENT '高级环境变量',
  `prev_deploy` text COMMENT '部署前置任务',
  `post_deploy` text COMMENT '同步之前任务',
  `prev_release` text COMMENT '同步之前目标机器执行的任务',
  `post_release` text COMMENT '同步之后目标机器执行的任务',
  `keep_version_num` int(3) NOT NULL DEFAULT '20' COMMENT '线上版本保留数',
  `repo_url` varchar(200) DEFAULT '' COMMENT 'git地址',
  `repo_username` varchar(50) DEFAULT '' COMMENT '版本管理系统的用户名，一般为svn的用户名',
  `repo_password` varchar(50) DEFAULT '' COMMENT '版本管理系统的密码，一般为svn的密码',
  `repo_mode` varchar(50) DEFAULT 'branch' COMMENT '上线方式：branch/tag',
  `repo_type` varchar(10) DEFAULT 'git' COMMENT '上线方式：git/svn',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COMMENT='项目配置表';

-- ----------------------------
--  Records of `project`
-- ----------------------------
BEGIN;
INSERT INTO `project` VALUES ('1', '1', '瓦力自部署', '1', '1', '12121', '*.log', 'work', '/tmp/walle/root', '/tmp/walle/library', '1,3,2', 'debug=1;\\napp=auotapp.py', 'echo prev_deploy; pwd', 'echo post_deploy; pwd', 'echo prev_release; pwd', 'echo post_release; pwd', '13', 'git@github.com:meolu/walden.git', '', '', 'branch', 'git', '2017-03-11 23:30:53', '2017-05-27 14:40:57'), ('2', '1', '瓦力自部署05', '1', null, null, '*.log', 'work', '/tmp/walle/root', '/tmp/walle/library', '1,3,2', 'debug=1;\\napp=auotapp.py', 'echo prev_deploy; pwd', 'echo post_deploy; pwd', 'echo prev_release; pwd', 'echo post_release; pwd', '15', 'git@github.com:meolu/walden.git', '', '', 'branch', null, '2017-05-25 14:53:21', '2017-05-26 21:59:21'), ('3', '1', 'walden-瓦尔登02', '1', null, null, '*.log', 'work', '/tmp/walle/root', '/tmp/walle/library', '1,3,2', 'debug=1;\\napp=auotapp.py', 'echo prev_deploy', 'echo post_deploy', 'echo prev_release', 'echo post_release', '10', 'git@github.com:meolu/walle-web.git', '', '', 'branch', null, '2017-05-25 15:02:18', '2017-05-25 15:02:18'), ('4', '1', '瓦力自部署01', '1', null, null, '*.log', 'work', '/tmp/walle/root', '/tmp/walle/library', '1,3,2', 'debug=1;\\napp=auotapp.py', 'echo prev_deploy', 'echo post_deploy', 'echo prev_release', 'echo post_release', '10', 'git@github.com:meolu/walle-web.git', '', '', 'branch', null, '2017-05-25 23:48:06', '2017-05-25 23:48:06');
COMMIT;

-- ----------------------------
--  Table structure for `project_server`
-- ----------------------------
DROP TABLE IF EXISTS `project_server`;
CREATE TABLE `project_server` (
  `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '记录id',
  `project_id` int(10) NOT NULL COMMENT '项目名字',
  `server_id` int(10) NOT NULL COMMENT '被打标签的实物id： 如 server.id',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COMMENT='项目与服务器关系表';

-- ----------------------------
--  Records of `project_server`
-- ----------------------------
BEGIN;
INSERT INTO `project_server` VALUES ('1', '1', '1', '2017-03-11 23:37:50', '2017-03-11 23:37:50'), ('2', '1', '2', '2017-03-11 23:37:56', '2017-03-11 23:37:56'), ('3', '1', '3', '2017-03-11 23:38:03', '2017-03-11 23:38:03');
COMMIT;

-- ----------------------------
--  Table structure for `role`
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL COMMENT '角色名称',
  `access_ids` text COMMENT '权限id列表,逗号分隔',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8 COMMENT='角色表';

-- ----------------------------
--  Records of `role`
-- ----------------------------
BEGIN;
INSERT INTO `role` VALUES ('1', '测试同学', '1,2,3,11,12,13,15,16,101,102,103,104,', '2017-03-24 13:52:09', '2017-06-12 19:25:51'), ('2', '测试同学2', '', '2017-03-26 13:23:44', '2017-05-14 16:38:25'), ('5', '业务端', '', '2017-05-11 09:41:58', '2017-05-11 09:41:58'), ('6', '没用的', '', '2017-05-14 16:44:41', '2017-05-14 16:44:41'), ('7', '业务端ss', '', '2017-05-14 16:50:02', '2017-05-14 16:50:02'), ('8', '业务端ss', '', '2017-05-14 16:51:06', '2017-05-14 16:51:06'), ('9', '业务端sss', '', '2017-05-14 16:51:06', '2017-05-14 16:51:06'), ('10', '业务端sss大', '', '2017-05-14 16:52:29', '2017-05-14 16:52:29'), ('11', '业务端', '', '2017-05-14 16:53:06', '2017-05-14 16:53:06');
COMMIT;

-- ----------------------------
--  Table structure for `server`
-- ----------------------------
DROP TABLE IF EXISTS `server`;
CREATE TABLE `server` (
  `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '记录id',
  `name` varchar(100) DEFAULT '' COMMENT 'server name',
  `host` varchar(100) NOT NULL COMMENT 'ip/host',
  `port` int(1) DEFAULT '22' COMMENT 'ssh port',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COMMENT='服务器记录表';

-- ----------------------------
--  Records of `server`
-- ----------------------------
BEGIN;
INSERT INTO `server` VALUES ('1', 'dev-wushuiyong', '172.16.0.231', '22', '2017-03-11 23:34:27', '2017-03-11 23:34:27'), ('2', 'mkt-dev-ky', '172.16.0.194', '22', '2017-03-11 23:35:12', '2017-03-11 23:35:12'), ('3', 'mkt-dev-yindongyang', '172.16.0.177', '22', '2017-03-11 23:37:18', '2017-03-11 23:37:18');
COMMIT;

-- ----------------------------
--  Table structure for `tag`
-- ----------------------------
DROP TABLE IF EXISTS `tag`;
CREATE TABLE `tag` (
  `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '记录id',
  `name` varchar(100) DEFAULT 'master' COMMENT '标签',
  `label` varchar(20) NOT NULL COMMENT '标签类型：server, ',
  `label_id` int(10) NOT NULL COMMENT '被打标签的实物id： 如 server.id',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8 COMMENT='tag 标签表';

-- ----------------------------
--  Records of `tag`
-- ----------------------------
BEGIN;
INSERT INTO `tag` VALUES ('1', '用户端FE', 'user_group', '0', '2017-05-08 19:56:19', '2017-05-10 21:07:38'), ('2', '营销中心', 'user_group', '0', '2017-05-08 19:57:05', '2017-05-08 19:57:05'), ('3', 'xx吴水永的新组xx', 'user_group', '0', '2017-05-08 20:52:55', '2017-05-11 23:34:45'), ('11', '吴水永的新组', 'user_group', '0', '2017-05-11 22:44:46', '2017-05-11 22:44:46'), ('13', '吴水永新增用户组', 'user_group', '0', '2017-05-14 23:13:57', '2017-05-14 23:13:57'), ('14', '吴水永新增用户组吕', 'user_group', '0', '2017-05-23 17:16:51', '2017-05-23 17:16:51'), ('15', '吴水永测试组', 'user_group', '0', '2017-05-23 17:23:40', '2017-05-23 17:23:40'), ('16', '吴水永测试组在', 'user_group', '0', '2017-05-23 17:25:30', '2017-05-23 17:25:30'), ('17', '吴水永测试组在', 'user_group', '0', '2017-05-23 17:26:10', '2017-05-23 17:26:10'), ('18', '吴水永测试组在在', 'user_group', '0', '2017-05-23 17:27:33', '2017-05-23 17:27:33'), ('19', '吴水永测试组在在在', 'user_group', '0', '2017-05-23 17:28:56', '2017-05-23 17:28:56'), ('20', '吴水永测试组在在在在', 'user_group', '0', '2017-05-23 17:30:01', '2017-05-23 17:30:01'), ('21', '吴水永测试组在在在在', 'user_group', '0', '2017-05-23 17:30:23', '2017-05-23 17:30:23'), ('22', '吴水永测试组在在在在', 'user_group', '0', '2017-05-23 17:31:10', '2017-05-23 17:31:10'), ('23', '吴水永测试组在在在在', 'user_group', '0', '2017-05-23 17:31:44', '2017-05-23 17:31:44'), ('24', '吴水永测试组在在在在', 'user_group', '0', '2017-05-23 17:31:44', '2017-05-23 17:31:44'), ('25', '吴水永测试组01', 'user_group', '0', '2017-05-23 17:31:44', '2017-05-23 17:31:44'), ('26', '吴水永测试组02', 'user_group', '0', '2017-05-23 17:44:19', '2017-05-23 17:44:19'), ('27', '吴水永测试组03', 'user_group', '0', '2017-05-23 17:44:53', '2017-05-23 17:44:53'), ('28', '吴水永测试组04', 'user_group', '0', '2017-05-23 17:47:37', '2017-05-23 17:47:37'), ('29', '吴水永测试组05', 'user_group', '0', '2017-05-23 17:48:33', '2017-05-23 17:48:33'), ('30', '吴水永测试组05', 'user_group', '0', '2017-05-23 17:48:33', '2017-05-23 17:48:33'), ('31', '这都有？', 'user_group', '0', '2017-05-23 17:54:24', '2017-05-23 17:54:24'), ('32', '吴水永新增用户组不', 'user_group', '0', '2017-05-23 18:02:48', '2017-05-23 18:02:48'), ('33', '吴水永新增用户组不有', 'user_group', '0', '2017-05-23 18:06:20', '2017-05-23 18:06:20'), ('34', '吴水永新增用003', 'user_group', '0', '2017-05-23 18:37:56', '2017-05-23 18:37:56');
COMMIT;

-- ----------------------------
--  Table structure for `task`
-- ----------------------------
DROP TABLE IF EXISTS `task`;
CREATE TABLE `task` (
  `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '记录id',
  `name` varchar(100) NOT NULL COMMENT '上线单标题',
  `user_id` bigint(21) unsigned NOT NULL COMMENT '用户id',
  `project_id` int(11) NOT NULL COMMENT '项目id',
  `action` int(1) DEFAULT '0' COMMENT '0全新上线，2回滚',
  `status` tinyint(1) NOT NULL COMMENT '状态0：新建提交，1审核通过，2审核拒绝，3上线完成，4上线失败',
  `link_id` varchar(100) DEFAULT '' COMMENT '上线的软链号',
  `ex_link_id` varchar(100) DEFAULT '' COMMENT '被替换的上次上线的软链号',
  `servers` text COMMENT '上线的机器',
  `commit_id` varchar(40) DEFAULT '' COMMENT 'git commit id',
  `branch` varchar(100) DEFAULT 'master' COMMENT '选择上线的分支',
  `file_transmission_mode` smallint(3) NOT NULL DEFAULT '1' COMMENT '上线文件模式: 1.全量所有文件 2.指定文件列表',
  `file_list` text COMMENT '文件列表，svn上线方式可能会产生',
  `enable_rollback` int(1) NOT NULL DEFAULT '1' COMMENT '能否回滚此版本0：no 1：yes',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8 COMMENT='上线单记录表';

-- ----------------------------
--  Records of `task`
-- ----------------------------
BEGIN;
INSERT INTO `task` VALUES ('1', 'Demo 测试上线单', '1', '1', '0', '1', 'prev_link_id_test', 'prev_link_id_test', '172.16.0.231,172.16.0.177', '5bf82db', 'master', '1', null, '1', '2017-03-11 23:41:24', '2017-03-11 23:45:10'), ('2', '测试使用 vue 2.0', '1', '1', '0', '1', 'vue_import', 'prev_link_id_test', '172.16.0.231,172.16.0.177', '5bf82db', 'master', '1', null, '1', '2017-03-12 17:31:55', '2017-03-12 17:32:11'), ('3', '到底 vue2 与 jinja 2 会产生什么样的火花呢？', '1', '1', '0', '1', 'vue_jinja', 'vue_import', '172.16.0.231,172.16.0.177', '5bf82db', 'master', '1', null, '1', '2017-03-12 17:32:59', '2017-03-12 17:33:29'), ('6', '提交一个测试上线单', '1', '1', '0', '0', '', '', '127.0.0.1,192.168.0.1', 'a89eb23c', 'master', '0', '*.log', '1', '2017-05-27 14:50:37', '2017-05-27 14:50:37'), ('7', '提交一个测试上线单', '1', '1', '0', '0', '', '', '127.0.0.1,192.168.0.1', 'a89eb23c', 'master', '0', '*.log', '1', '2017-05-27 14:53:42', '2017-05-27 14:53:42'), ('8', '提交一个测试上线单', '1', '1', '0', '0', '', '', '127.0.0.1,192.168.0.1', 'a89eb23c', 'master', '0', '*.log', '1', '2017-05-27 15:37:39', '2017-05-27 15:37:39'), ('9', '提交一个测试上线单', '1', '1', '0', '0', '', '', '127.0.0.1,192.168.0.1', 'a89eb23c', 'master', '0', '*.log', '1', '2017-05-27 15:38:56', '2017-05-27 15:38:56'), ('10', '提交一个测试上线单', '1', '1', '0', '0', '', '', '127.0.0.1,192.168.0.1', 'a89eb23c', 'master', '0', '*.log', '1', '2017-05-27 15:40:04', '2017-05-27 15:40:04'), ('11', '提交一个测试上线单', '1', '1', '0', '0', '', '', '127.0.0.1,192.168.0.1', 'a89eb23c', 'master', '0', '*.log', '1', '2017-05-27 16:48:38', '2017-05-27 16:48:38');
COMMIT;

-- ----------------------------
--  Table structure for `task_record`
-- ----------------------------
DROP TABLE IF EXISTS `task_record`;
CREATE TABLE `task_record` (
  `id` bigint(10) NOT NULL AUTO_INCREMENT COMMENT '记录id',
  `stage` varchar(20) DEFAULT NULL COMMENT '阶段',
  `sequence` int(10) DEFAULT NULL COMMENT '序列号',
  `user_id` int(21) unsigned NOT NULL COMMENT '用户id',
  `task_id` bigint(11) NOT NULL COMMENT 'Task id',
  `status` tinyint(1) NOT NULL COMMENT '状态0：新建提交，1审核通过，2审核拒绝，3上线完成，4上线失败',
  `command` text COMMENT '命令与参数',
  `success` text COMMENT '成功返回信息',
  `error` text COMMENT '错误信息',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=122 DEFAULT CHARSET=utf8 COMMENT='任务执行记录表';

-- ----------------------------
--  Records of `task_record`
-- ----------------------------
BEGIN;
INSERT INTO `task_record` VALUES ('98', 'prev_deploy', '1', '33', '1', '1', 'whoami', 'wushuiyong', '', '2017-03-15 18:32:51', '2017-03-15 18:32:51'), ('99', 'prev_deploy', '1', '33', '32', '1', 'python --version', 'Python 2.7.10', '', '2017-03-15 18:32:51', '2017-03-15 18:32:51'), ('100', 'prev_deploy', '1', '33', '32', '1', 'git --version', 'git version 2.2.2', '', '2017-03-15 18:32:51', '2017-03-15 18:32:51'), ('101', 'prev_deploy', '1', '33', '32', '1', 'mkdir -p None', '', '', '2017-03-15 18:32:51', '2017-03-15 18:32:51'), ('102', 'prev_deploy', '1', '33', '1', '1', 'whoami', 'wushuiyong', '', '2017-03-15 18:34:16', '2017-03-15 18:34:16'), ('103', 'prev_deploy', '1', '33', '32', '1', 'python --version', 'Python 2.7.10', '', '2017-03-15 18:34:16', '2017-03-15 18:34:16'), ('104', 'prev_deploy', '1', '33', '32', '1', 'git --version', 'git version 2.2.2', '', '2017-03-15 18:34:16', '2017-03-15 18:34:16'), ('105', 'prev_deploy', '1', '33', '32', '1', 'mkdir -p None', '', '', '2017-03-15 18:34:16', '2017-03-15 18:34:16'), ('106', 'prev_deploy', '1', '33', '1', '1', 'whoami', 'wushuiyong', '', '2017-03-15 18:34:57', '2017-03-15 18:34:57'), ('107', 'prev_deploy', '1', '33', '32', '1', 'python --version', 'Python 2.7.10', '', '2017-03-15 18:34:58', '2017-03-15 18:34:58'), ('108', 'prev_deploy', '1', '33', '32', '1', 'git --version', 'git version 2.2.2', '', '2017-03-15 18:34:58', '2017-03-15 18:34:58'), ('109', 'prev_deploy', '1', '33', '32', '1', 'mkdir -p /Users/wushuiyong/workspace/meolu/data/codebase/walle-web', '', '', '2017-03-15 18:34:58', '2017-03-15 18:34:58'), ('110', 'prev_deploy', '1', '33', '1', '1', 'whoami', 'wushuiyong', '', '2017-03-15 18:36:28', '2017-03-15 18:36:28'), ('111', 'prev_deploy', '1', '33', '32', '1', 'python --version', 'Python 2.7.10', '', '2017-03-15 18:36:28', '2017-03-15 18:36:28'), ('112', 'prev_deploy', '1', '33', '32', '1', 'git --version', 'git version 2.2.2', '', '2017-03-15 18:36:28', '2017-03-15 18:36:28'), ('113', 'prev_deploy', '1', '33', '32', '1', 'mkdir -p /Users/wushuiyong/workspace/meolu/data/codebase/walle-web', '', '', '2017-03-15 18:36:28', '2017-03-15 18:36:28'), ('114', 'prev_deploy', '1', '33', '1', '1', 'whoami', 'wushuiyong', '', '2017-03-16 11:02:28', '2017-03-16 11:02:28'), ('115', 'prev_deploy', '1', '33', '32', '1', 'python --version', 'Python 2.7.10', '', '2017-03-16 11:02:29', '2017-03-16 11:02:29'), ('116', 'prev_deploy', '1', '33', '32', '1', 'git --version', 'git version 2.2.2', '', '2017-03-16 11:02:29', '2017-03-16 11:02:29'), ('117', 'prev_deploy', '1', '33', '32', '1', 'mkdir -p /Users/wushuiyong/workspace/meolu/data/codebase/walle-web', '', '', '2017-03-16 11:02:29', '2017-03-16 11:02:29'), ('118', 'prev_deploy', '1', '33', '1', '1', 'whoami', 'wushuiyong', '', '2017-03-16 11:03:47', '2017-03-16 11:03:47'), ('119', 'prev_deploy', '1', '33', '32', '1', 'python --version', 'Python 2.7.10', '', '2017-03-16 11:03:47', '2017-03-16 11:03:47'), ('120', 'prev_deploy', '1', '33', '32', '1', 'git --version', 'git version 2.2.2', '', '2017-03-16 11:03:47', '2017-03-16 11:03:47'), ('121', 'prev_deploy', '1', '33', '32', '1', 'mkdir -p /Users/wushuiyong/workspace/meolu/data/codebase/walle-web', '', '', '2017-03-16 11:03:47', '2017-03-16 11:03:47');
COMMIT;

-- ----------------------------
--  Table structure for `user`
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL COMMENT '用户昵称',
  `is_email_verified` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否邮箱认证',
  `email` varchar(50) NOT NULL COMMENT '邮箱',
  `password` varchar(100) NOT NULL COMMENT '密码',
  `password_hash` varchar(50) DEFAULT NULL COMMENT 'hash',
  `avatar` varchar(100) DEFAULT 'default.jpg' COMMENT '头像图片地址',
  `role_id` int(6) NOT NULL COMMENT '角色id',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态: 0新建，1正常，2冻结',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COMMENT='用户表';

-- ----------------------------
--  Records of `user`
-- ----------------------------
BEGIN;
INSERT INTO `user` VALUES ('1', 'wushuiyong', '1', 'wushuiyong@renrenche.com', '', '', 'default.jpg', '1', '1', '2017-03-17 09:03:09', '2017-03-17 09:03:09'), ('2', 'wushuiyong@local.com', '0', 'wushuiyong@walle-web.io', 'pbkdf2:sha1:1000$59T3110Q$7703684fd0bb722985b037703329c82891acd84b', '', null, '0', '0', '2017-03-20 19:05:44', '2017-05-23 17:49:50'), ('3', 'wushuiyong@walle-web.ios', '0', 'wushuiyong@walle-web.ios', 'pbkdf2:sha1:1000$KSjsIBCf$762bf8c30adc6eef288df31547dbd80fa8b81c93', '', null, '0', '0', '2017-04-13 15:03:57', '2017-05-23 17:49:50'), ('4', 'wushuiyong@walle-web.ioss', '0', 'wushuiyong@walle-web.ioss', 'pbkdf2:sha1:1000$We4EXI4O$c363470dbc91d9bf897fec3a76fdedeaf5f564b8', '', null, '0', '0', '2017-04-13 15:03:57', '2017-05-23 17:49:50'), ('7', 'x吴水永的新组x', '0', 'demo02@walle.com', 'pbkdf2:sha1:1000$3jENzbZ3$345e44980dcf44ffab60f16b35a913dca93677ab', '', null, '1', '0', '2017-05-11 22:33:35', '2017-05-23 17:49:50'), ('8', '中文啦', '0', 'demo03@walle.com', 'pbkdf2:sha1:1000$DButSYQG$d3fe6a80e23461e565ca1a8b8f9ee8302e7a29a7', '', null, '2', '0', '2017-05-11 23:39:11', '2017-05-23 17:49:50'), ('9', '中文啦', '0', 'demo06@walle.com', 'pbkdf2:sha1:1000$AjTbiwj6$991080c601009c612ae81647c797334cffdf4aa6', null, null, '2', '0', '2017-05-13 22:16:14', '2017-05-23 17:49:50'), ('10', 'x吴水永的新组x', '0', 'demo07@walle.com', 'pbkdf2:sha1:1000$V6VewIqF$7eec3681b0994abe8f1be769319a6a276f4658fc', null, null, '1', '0', '2017-05-13 23:12:44', '2017-05-23 17:49:50');
COMMIT;

-- ----------------------------
--  Table structure for `user_group`
-- ----------------------------
DROP TABLE IF EXISTS `user_group`;
CREATE TABLE `user_group` (
  `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '记录id',
  `user_id` int(10) DEFAULT '0' COMMENT '用户id',
  `group_id` int(10) DEFAULT '0' COMMENT '用户组id',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=90 DEFAULT CHARSET=utf8 COMMENT='用户组关联表';

-- ----------------------------
--  Records of `user_group`
-- ----------------------------
BEGIN;
INSERT INTO `user_group` VALUES ('1', '13', '1', '2017-05-08 19:56:38', '2017-05-08 19:56:38'), ('2', '1', '1', '2017-05-10 20:53:42', '2017-05-10 20:53:42'), ('45', '8', '11', '2017-05-11 22:44:46', '2017-05-11 22:44:46'), ('46', '1', '11', '2017-05-11 22:44:46', '2017-05-11 22:44:46'), ('47', '2', '11', '2017-05-11 22:44:46', '2017-05-11 22:44:46'), ('52', '1', '3', '2017-05-11 23:29:43', '2017-05-11 23:29:43'), ('54', '15', '3', '2017-05-11 23:32:07', '2017-05-11 23:32:07'), ('56', '13', '3', '2017-05-11 23:34:45', '2017-05-11 23:34:45'), ('57', '1', '13', '2017-05-14 23:13:57', '2017-05-14 23:13:57'), ('58', '13', '13', '2017-05-14 23:13:57', '2017-05-14 23:13:57'), ('59', '18', '13', '2017-05-14 23:13:57', '2017-05-14 23:13:57'), ('60', '1', '14', '2017-05-23 17:16:51', '2017-05-23 17:16:51'), ('61', '1', '15', '2017-05-23 17:23:40', '2017-05-23 17:23:40'), ('62', '1', '16', '2017-05-23 17:25:30', '2017-05-23 17:25:30'), ('63', '1', '17', '2017-05-23 17:26:10', '2017-05-23 17:26:10'), ('64', '1', '18', '2017-05-23 17:27:33', '2017-05-23 17:27:33'), ('65', '1', '19', '2017-05-23 17:28:56', '2017-05-23 17:28:56'), ('66', '1', '20', '2017-05-23 17:30:01', '2017-05-23 17:30:01'), ('67', '1', '21', '2017-05-23 17:30:23', '2017-05-23 17:30:23'), ('68', '1', '22', '2017-05-23 17:31:10', '2017-05-23 17:31:10'), ('69', '1', '23', '2017-05-23 17:31:44', '2017-05-23 17:31:44'), ('70', '1', '24', '2017-05-23 17:31:44', '2017-05-23 17:31:44'), ('71', '1', '25', '2017-05-23 17:31:44', '2017-05-23 17:31:44'), ('72', '1', '26', '2017-05-23 17:44:19', '2017-05-23 17:44:19'), ('73', '1', '27', '2017-05-23 17:44:53', '2017-05-23 17:44:53'), ('74', '1', '28', '2017-05-23 17:47:37', '2017-05-23 17:47:37'), ('75', '1', '29', '2017-05-23 17:48:33', '2017-05-23 17:48:33'), ('76', '3', '29', '2017-05-23 17:48:33', '2017-05-23 17:48:33'), ('77', '2', '29', '2017-05-23 17:48:33', '2017-05-23 17:48:33'), ('78', '1', '30', '2017-05-23 17:48:33', '2017-05-23 17:48:33'), ('79', '3', '30', '2017-05-23 17:48:33', '2017-05-23 17:48:33'), ('80', '2', '30', '2017-05-23 17:48:33', '2017-05-23 17:48:33'), ('81', '4', '30', '2017-05-23 17:48:33', '2017-05-23 17:48:33'), ('82', '1', '31', '2017-05-23 17:54:24', '2017-05-23 17:54:24'), ('83', '3', '31', '2017-05-23 17:54:24', '2017-05-23 17:54:24'), ('84', '2', '31', '2017-05-23 17:54:24', '2017-05-23 17:54:24'), ('86', '1', '32', '2017-05-23 18:02:48', '2017-05-23 18:02:48'), ('87', '1', '33', '2017-05-23 18:06:20', '2017-05-23 18:06:20'), ('88', '1', '34', '2017-05-23 18:37:56', '2017-05-23 18:37:56'), ('89', '3', '34', '2017-05-23 18:37:56', '2017-05-23 18:37:56');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
