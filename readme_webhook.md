# 🚀 Discord Webhook Setup and Usage in Raspberry Pi 3 Project

This document explains how to set up a Discord webhook and use it in a Raspberry Pi 3-based project to send notifications directly to a Discord channel.

---

## 🤔 1. What is a Discord Webhook?

A Discord webhook is a simple URL that allows external applications to send messages directly into a specific channel on a Discord server. In our project, the webhook is used to send notifications from the Raspberry Pi 3.

---

## 🔧 2. How to Create a Discord Webhook

1. Open the Discord server where you want to receive messages.
2. Select the channel where you want the webhook messages to be sent.
3. Click on **Channel Settings** (the gear icon ⚙️ next to the channel name).
4. In the menu, select the **Integrations** tab.
5. Click on **Webhooks**.
6. Choose **New Webhook**.
7. Name the webhook and select the channel for messages.
8. Click **Copy Webhook URL** 📋.
9. Save this URL you will need it in python code.

---

## 💻 3. Setting Up the Webhook URL in Raspberry Pi Code

Save the webhook URL in the WEBHOOK variable in the printer_monitor.py file.

---

## 📤 4. Sending Messages to Discord Using Raspberry Pi 3

The Raspberry Pi can send a message by making an HTTP POST request to the webhook URL. The message is in JSON format, where the `content` field contains the text to display in the Discord channel.

### Line in printer_monitor.py file that you need to change

```python
WEBHOOK = "your_webhook_url"