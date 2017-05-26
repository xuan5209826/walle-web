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

 Date: 05/26/2017 22:27:01 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

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
--  Table structure for `my`
-- ----------------------------
DROP TABLE IF EXISTS `my`;
CREATE TABLE `my` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` int(1) NOT NULL DEFAULT '0' COMMENT '成交的所有收',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `permission`
-- ----------------------------
DROP TABLE IF EXISTS `permission`;
CREATE TABLE `permission` (
  `id` int(15) NOT NULL AUTO_INCREMENT,
  `name_cn` varchar(30) NOT NULL COMMENT '模块中文名称',
  `name_en` varchar(30) NOT NULL COMMENT '模块英文名称',
  `pid` int(6) NOT NULL COMMENT '父模块id，顶级pid为0',
  `type` enum('action','controller','module') DEFAULT 'action' COMMENT '类型',
  `sequence` int(11) DEFAULT '0' COMMENT '排序序号sprintf("%2d%2d%2d", module_id, controller_id, 自增两位数)',
  `archive` tinyint(1) NOT NULL DEFAULT '0' COMMENT '归档：0有效，1无效',
  `icon` varchar(30) DEFAULT '' COMMENT '模块',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='权限表';

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
--  Table structure for `role`
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL COMMENT '角色名称',
  `permission_ids` text COMMENT '权限id列表,逗号分隔',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8 COMMENT='角色表';

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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COMMENT='服务器记录表';

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
--  Table structure for `task`
-- ----------------------------
DROP TABLE IF EXISTS `task`;
CREATE TABLE `task` (
  `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '记录id',
  `user_id` bigint(21) unsigned NOT NULL COMMENT '用户id',
  `project_id` int(11) NOT NULL COMMENT '项目id',
  `action` int(1) DEFAULT '0' COMMENT '0全新上线，2回滚',
  `status` tinyint(1) NOT NULL COMMENT '状态0：新建提交，1审核通过，2审核拒绝，3上线完成，4上线失败',
  `title` varchar(100) NOT NULL COMMENT '上线单标题',
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COMMENT='上线单记录表';

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
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8 COMMENT='用户表';

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

SET FOREIGN_KEY_CHECKS = 1;
