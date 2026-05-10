"""文件传输模块单元测试"""

import unittest
from unittest.mock import Mock, MagicMock, patch
import os
import tempfile
from pathlib import Path

from file_transfer.sftp_client import SFTPClient, FileInfo


class MockSFTPAttr:
    """模拟SFTP文件属性"""
    def __init__(self, filename, size, mtime, mode):
        self.filename = filename
        self.st_size = size
        self.st_mtime = mtime
        self.st_mode = mode


class TestSFTPClient(unittest.TestCase):
    """SFTP客户端测试"""

    def setUp(self):
        """测试前准备"""
        self.mock_ssh = Mock()
        self.mock_ssh.is_connected.return_value = True
        self.mock_sftp = Mock()
        self.mock_ssh.get_sftp_client.return_value = self.mock_sftp

    def test_init_success(self):
        """测试初始化成功"""
        client = SFTPClient(self.mock_ssh)
        self.assertIsNotNone(client._sftp)
        self.mock_ssh.is_connected.assert_called_once()

    def test_init_not_connected(self):
        """测试未连接时初始化失败"""
        self.mock_ssh.is_connected.return_value = False
        with self.assertRaises(ConnectionError):
            SFTPClient(self.mock_ssh)

    def test_upload_success(self):
        """测试上传成功"""
        client = SFTPClient(self.mock_ssh)

        # 创建临时文件
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"test content")
            temp_file = f.name

        try:
            progress_called = []
            def progress_callback(p):
                progress_called.append(p)

            result = client.upload(temp_file, "/remote/test.txt", progress_callback)

            self.assertTrue(result)
            self.mock_sftp.put.assert_called_once()
        finally:
            os.unlink(temp_file)

    def test_upload_file_not_found(self):
        """测试上传不存在的文件"""
        client = SFTPClient(self.mock_ssh)
        result = client.upload("/nonexistent/file.txt", "/remote/test.txt")
        self.assertFalse(result)

    def test_download_success(self):
        """测试下载成功"""
        client = SFTPClient(self.mock_ssh)

        with tempfile.TemporaryDirectory() as tmpdir:
            local_path = os.path.join(tmpdir, "downloaded.txt")

            progress_called = []
            def progress_callback(p):
                progress_called.append(p)

            result = client.download("/remote/test.txt", local_path, progress_callback)

            self.assertTrue(result)
            self.mock_sftp.get.assert_called_once()

    def test_list_dir(self):
        """测试列出目录"""
        client = SFTPClient(self.mock_ssh)

        # 模拟文件列表
        import stat
        mock_attrs = [
            MockSFTPAttr("file1.txt", 1024, 1234567890, stat.S_IFREG | 0o644),
            MockSFTPAttr("dir1", 0, 1234567890, stat.S_IFDIR | 0o755),
        ]
        self.mock_sftp.listdir_attr.return_value = mock_attrs

        files = client.list_dir("/remote/path")

        self.assertEqual(len(files), 2)
        self.assertEqual(files[0].name, "dir1")
        self.assertTrue(files[0].is_dir)
        self.assertEqual(files[1].name, "file1.txt")
        self.assertFalse(files[1].is_dir)

    def test_remove_file(self):
        """测试删除文件"""
        client = SFTPClient(self.mock_ssh)
        result = client.remove("/remote/test.txt")

        self.assertTrue(result)
        self.mock_sftp.remove.assert_called_once_with("/remote/test.txt")

    def test_mkdir(self):
        """测试创建目录"""
        client = SFTPClient(self.mock_ssh)
        result = client.mkdir("/remote/newdir")

        self.assertTrue(result)
        self.mock_sftp.mkdir.assert_called_once_with("/remote/newdir")

    def test_rename(self):
        """测试重命名"""
        client = SFTPClient(self.mock_ssh)
        result = client.rename("/remote/old.txt", "/remote/new.txt")

        self.assertTrue(result)
        self.mock_sftp.rename.assert_called_once_with("/remote/old.txt", "/remote/new.txt")

    def test_chdir(self):
        """测试切换目录"""
        client = SFTPClient(self.mock_ssh)
        result = client.chdir("/remote/path")

        self.assertTrue(result)
        self.mock_sftp.chdir.assert_called_once_with("/remote/path")

    def test_close(self):
        """测试关闭连接"""
        client = SFTPClient(self.mock_ssh)
        client.close()

        self.mock_sftp.close.assert_called_once()
        self.assertIsNone(client._sftp)


class TestFileInfo(unittest.TestCase):
    """文件信息测试"""

    def test_file_info_creation(self):
        """测试创建文件信息"""
        info = FileInfo(
            name="test.txt",
            size=1024,
            is_dir=False,
            mtime=1234567890,
            permissions="-rw-r--r--"
        )

        self.assertEqual(info.name, "test.txt")
        self.assertEqual(info.size, 1024)
        self.assertFalse(info.is_dir)
        self.assertEqual(info.mtime, 1234567890)
        self.assertEqual(info.permissions, "-rw-r--r--")


class TestFileBrowser(unittest.TestCase):
    """文件浏览器测试"""

    def test_format_size(self):
        """测试文件大小格式化"""
        from file_transfer.file_browser import FileListWidget

        self.assertEqual(FileListWidget._format_size(512), "512.0 B")
        self.assertEqual(FileListWidget._format_size(1024), "1.0 KB")
        self.assertEqual(FileListWidget._format_size(1024 * 1024), "1.0 MB")
        self.assertEqual(FileListWidget._format_size(1024 * 1024 * 1024), "1.0 GB")


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestSFTPClient))
    suite.addTests(loader.loadTestsFromTestCase(TestFileInfo))
    suite.addTests(loader.loadTestsFromTestCase(TestFileBrowser))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print(f"\n{'='*70}")
    print(f"测试完成: {result.testsRun} 个测试")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print(f"{'='*70}")

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
