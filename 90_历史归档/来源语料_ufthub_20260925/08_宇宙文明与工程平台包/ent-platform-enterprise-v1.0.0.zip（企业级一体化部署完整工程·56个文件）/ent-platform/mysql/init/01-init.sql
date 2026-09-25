-- =============================================================================
-- 首次初始化脚本: 仅在 data/mysql 为空(首次启动)时自动执行
-- 业务库/账号由 compose 环境变量创建, 这里只建自动化任务所需表结构样例
-- =============================================================================

-- 自动化任务表 (Worker 领取/回写)
CREATE TABLE IF NOT EXISTS `rpa_task` (
  `id`            BIGINT       NOT NULL AUTO_INCREMENT COMMENT '主键',
  `task_no`       VARCHAR(64)  NOT NULL COMMENT '任务唯一编号',
  `task_type`     VARCHAR(32)  NOT NULL DEFAULT 'web' COMMENT 'web/ocr/mixed',
  `payload`       JSON         NULL COMMENT '任务参数(URL/参数等)',
  `status`        TINYINT      NOT NULL DEFAULT 0 COMMENT '0待执行 1执行中 2成功 3失败',
  `result_text`   MEDIUMTEXT   NULL COMMENT 'OCR/抓取结果文本',
  `snapshot_path` VARCHAR(255) NULL COMMENT '共享卷截图路径 /data/...',
  `retry_count`   INT          NOT NULL DEFAULT 0,
  `err_msg`       VARCHAR(1000) NULL,
  `created_at`    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_task_no` (`task_no`),
  KEY `idx_status_created` (`status`, `created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='RPA自动化任务表';

-- 给业务账号授权 (库名/账号与 .env 保持一致; 首次启动环境变量已建账号, 这里补权限)
-- GRANT ALL PRIVILEGES ON appdb.* TO 'appuser'@'%';
-- FLUSH PRIVILEGES;
