# Email Auto-Unsubscriber 🚀

An intelligent tool that helps you reclaim your inbox by automatically unsubscribing from unwanted email subscriptions in Gmail.

<div align="center">
  <img src="https://github.com/user-attachments/assets/b0807537-c3da-469a-b459-2c5e7d81bf88" width="80%" alt="Development Journey Banner" className="flex justify-between item-center">
</div>

## 🌟 Key Features

- **Smart Gmail Integration**: Secure connection using OAuth2
- **Intelligent Processing**: 
  - Finds hidden unsubscribe links in email headers and body
  - Groups emails by sender to avoid duplicate unsubscribes
  - Handles both one-click and form-based unsubscribe pages
- **Progress Tracking**: 
  - Real-time console updates
  - Detailed logging of all actions
  - CSV export of results
- **Safety First**:
  - Rate limiting to avoid Gmail API restrictions
  - Automatic retry on failed attempts
  - Backup of all processed links

## 🚀 Quick Start

1. **Set Up Your Environment**
```bash
git clone https://github.com/rahulsamant37/Email-Auto_UnSubscriber.git
cd email-auto-unsubscriber
pip install -r requirements.txt
```

2. **Configure Credentials**
- Create a `.env` file in the project root
- Add your Gmail credentials:
```ini
EMAIL="your.email@gmail.com"
PASSWORD="your-app-password"
```

3. **Run the Tool**
```bash
python main.py
```

## 📋 Prerequisites

- Python 3.8+
- Gmail account
- Gmail App Password (for 2FA-enabled accounts)
- Required packages listed in `requirements.txt`

## 🔒 Security Note

This tool requires a Gmail App Password. Never use your regular Gmail password!

To set up an App Password:
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Step Verification
3. Generate an App Password at [App Passwords](https://myaccount.google.com/apppasswords)

## 📊 Output Files

The tool generates two key files:

| File | Description |
|------|-------------|
| `unsubscribe_links.txt` | Complete list of discovered unsubscribe links |
| `unsubscribe_services.csv` | Structured data with sender info and results |

![image](https://github.com/user-attachments/assets/b8983c11-819e-4781-8b54-0c9f03821158)

![image](https://github.com/user-attachments/assets/6c70c3e2-a7b8-498d-9ab5-2fd90453faab)


## 📈 Progress Monitoring

Watch your unsubscribe progress in real-time:
```
✓ Connected to Gmail
📧 Found 150 subscription emails
🔍 Identified 45 unique services
⚡ Processing unsubscribe requests...
[====================] 100% Complete
✅ Successfully unsubscribed: 42
❌ Failed attempts: 3
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for personal use only. Ensure you have proper authorization to access the Gmail account you're using. The developers are not responsible for any misuse or violations of terms of service.

## 🐛 Troubleshooting

Common issues and solutions:

- **API Rate Limits**: The tool automatically handles Gmail API quotas
- **Connection Issues**: Check your App Password and internet connection
- **Unsubscribe Failures**: Some services may require manual unsubscription

For more help, check our [Issues](https://github.com/rahulsamant37/Email-Auto_UnSubscriber/issues) page.