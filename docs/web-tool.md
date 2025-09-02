# Web 在线工具

Rimetool 提供了友好的 Web 界面，让你无需安装任何软件就能使用词库转换功能。

## 在线访问

**🌐 [立即使用 Web 工具](https://your-domain.com)**

或者你可以在本地启动 Web 服务：

```bash
 python -m rimetool web
```

然后访问：`http://localhost:5023（默认)`

## 本地部署

如果你想在自己的服务器上部署 Web 工具：

### Docker 部署（暂不可用)

```bash
docker run -d -p 5023:5023 --name rimetool your-registry/rimetool:latest
```

### Python部署

```bash
# 安装rimetool
uv tool install rimetool  #推荐使用uv安装
pip install rimetool

# 启动服务
python rimetool web

```

`python rimetool web` 可选参数

- --host #  服务器主机地址（默认：0.0.0.0） 
- --port # 服务器端口（默认：5023）
- --debug  #'启用调试模式

### 环境变量

可以通过环境变量配置：

- `FLASK_ENV`: 运行环境（development/production）
- `PORT`: 服务端口（默认 5023）
- `MAX_UPLOAD_SIZE`: 最大上传文件大小

## 反馈和建议

如果你在使用过程中遇到问题或有改进建议，欢迎：

- [提交 Issue](https://github.com/B-Beginner/rimetool/issues)
- [发起讨论](https://github.com/B-Beginner/rimetool/discussions)
- [贡献代码](https://github.com/B-Beginner/rimetool/pulls)
