<h1 align="center">🤖 Discord Moderation Bot</h1>

<p align="center">
  <b>A powerful and efficient Discord bot for server moderation!</b>
</p>

---

## 🚀 Features

- 🛡️ **Admin Commands** (Mute, Ban, Unmute, Kick, Warn, etc.)
- 📜 **Warning System** (Persistent storage of warnings, auto-moderation)
- 🔇 **Timed Muting** (Automatically unmutes users after a specified duration)
- 📋 **Ban & Mute Lists** (Check banned or muted users)
- 🔎 **User ID Lookup**
- ✅ **Permission Checks** (Ensures only admins or server owners can execute commands)
- ❌ **Error Handling** (Handles missing arguments, permission errors, and command failures)

---

## 🛠️ Installation

### **1️⃣ Prerequisites**
- Python 3.8+
- `discord.py` library (`pip install discord.py`)

### **2️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/discord-bot.git
cd mybot
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Configure the Bot**
1. Rename `.env.example` to `.env`
2. Add your **Discord bot token** and other configurations inside `.env`

### **5️⃣ Run the Bot**
```bash
python bot.py
```

---

## 📝 Commands

| Command | Description | Usage |
|---------|-------------|----------|
| `!warn` | Warns a user | `!warn @User Reason` |
| `!warnings` | Shows a user's warnings | `!warnings @User` |
| `!clearwarnings` | Clears warnings for a user | `!clearwarnings @User` |
| `!mute` | Mutes a user | `!mute @User [Duration]` |
| `!unmute` | Unmutes a user | `!unmute @User` |
| `!ban` | Bans a user | `!ban @User Reason` |
| `!banlist` | Shows banned users | `!banlist` |
| `!mutedlist` | Shows muted users | `!mutedlist` |
| `!id` | Gets a user ID | `!id @User` |

---

## 🔧 Configuration
The bot stores warnings, bans, and mute details in a JSON file using `json_utils`. Ensure that the necessary storage files exist before running the bot.

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 💬 Support
For issues or contributions, create a GitHub issue or submit a pull request.

🌟 **Star the repo if you find it useful!** 🚀

