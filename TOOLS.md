# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod

### SSH 代理（临时使用）

- **文件位置**: /root/ssh-proxy/proxy
- **开启命令**: cd /root/ssh-proxy && nohup ./proxy > /tmp/ssh_proxy.log 2>&1 &
- **本地端口**: 127.0.0.1:55555
- **使用场景**: 访问 HuggingFace 等被墙的网站
- **重要规则**: 临时使用，不用时关闭，不要永久配置
- **注意**: 关闭代理时只关55555端口，不要影响12222端口

### 开发电脑 SSH 隧道（长期保持）

- **文件位置**: /root/ssh-proxy/dev_pc
- **开启命令**: cd /root/ssh-proxy && nohup ./dev_pc > /tmp/dev_pc.log 2>&1 &
- **本地端口**: 127.0.0.1:12222
- **跳板机**: fang@221.7.221.10:51622
- **目标电脑**: 10.10.30.39:22 (内网)
- **SSH命令**: ssh -N -L 12222:10.10.30.39:22 -p 51622 fang@221.7.221.10
- **连接开发电脑**: ssh -p 12222 D@127.0.0.1
- **重要规则**: ⚠️ **保持长期运行，不要关闭**
- **断开处理**: 如断开，通知方，需要动态密钥重连
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
