@echo off
echo 上传 MedGemma V7.4 优化脚本到开发电脑
echo ============================================

echo 本地文件: C:\tmp\full_test_v7.4_300cases.py
echo 远程文件: e:\ai_test_MedGemma\ai\other\scripts\full_test_v7.4_300cases.py

echo.
echo 请在开发电脑执行以下操作：

echo.
echo 1. 启动 WinSCP 或其它SCP客户端
echo.
echo 2. 连接到: 127.0.0.1:12222
echo    用户名: D
echo    密码: [请从方伟获取]
echo.
echo 3. 上传文件:
echo    本地: C:\tmp\full_test_v7.4_300cases.py
echo    远程: e:\ai_test_MedGemma\ai\other\scripts\full_test_v7.4_300cases.py
echo.
echo 4. 上传完成后，在开发电脑执行:
echo    cd e:\ai_test_MedGemma\ai\other\scripts
echo    copy full_test_v7.4_300cases.py full_test_v7.4_300cases_backup.py
echo.
echo 5. 运行测试:
echo    cd e:\ai_test_MedGemma\ai\other
echo    python scripts\full_test_v7.4_300cases.py

pause
