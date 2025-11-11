# Credentials Directory

This directory stores Google Cloud OAuth credentials for Google Drive integration.

## Required Files

**google-drive-credentials.json**
- OAuth 2.0 client secret from Google Cloud Console
- Type: Desktop application credentials
- Download from: https://console.cloud.google.com/apis/credentials

**token.pickle** (auto-generated)
- Cached access token for Google Drive API
- Created automatically after first authentication
- Auto-refreshed when expired

## Setup Instructions

1. **Create Google Cloud Project**
   - Go to https://console.cloud.google.com/
   - Create new project or select existing

2. **Enable Google Drive API**
   - Navigate to APIs & Services > Library
   - Search for "Google Drive API"
   - Click Enable

3. **Configure OAuth Consent Screen**
   - Go to APIs & Services > OAuth consent screen
   - Choose "External" user type
   - Add application name and support email
   - Add your email to test users

4. **Create OAuth Credentials**
   - Go to APIs & Services > Credentials
   - Click "Create Credentials" > "OAuth client ID"
   - Application type: "Desktop app"
   - Name it "Boring Business AI - Social Scripts"
   - Click "Create"

5. **Download Credentials**
   - Click the download button (↓) next to your new credential
   - Save the JSON file to this directory as:
     `google-drive-credentials.json`

6. **Run Authentication**
   ```bash
   cd ~/Documents/claudec/active/Social-Content-Generator/pillar_scripts
   python upload_to_gdrive.py
   ```
   - Browser will open for OAuth consent
   - Sign in with your Google account
   - Grant permissions
   - Token saved automatically

## Security

⚠️ **DO NOT COMMIT THESE FILES TO GIT**

The `.gitignore` in this directory prevents credential files from being tracked.

Files in this directory contain sensitive authentication data:
- `google-drive-credentials.json` - OAuth client secret
- `token.pickle` - Access and refresh tokens

Never share these files or commit them to version control.

## Troubleshooting

**Credentials not found:**
```bash
# Check file exists
ls -la ~/Documents/claudec/systems/skills-main/boring-business-brand/credentials/
```

**Authentication failed:**
```bash
# Delete cached token and re-authenticate
rm ~/Documents/claudec/systems/skills-main/boring-business-brand/credentials/token.pickle
python upload_to_gdrive.py
```

**Permission denied:**
```bash
# Verify file permissions
chmod 600 google-drive-credentials.json
```

## File Locations

**Credentials:**
```
~/Documents/claudec/systems/skills-main/boring-business-brand/credentials/
├── google-drive-credentials.json  (you download this)
├── token.pickle                   (auto-generated)
├── .gitignore                     (prevents git commits)
└── README.md                      (this file)
```

**Upload Script:**
```
~/Documents/claudec/active/Social-Content-Generator/pillar_scripts/
└── upload_to_gdrive.py
```

## References

- **Google Cloud Console:** https://console.cloud.google.com/
- **Google Drive API Docs:** https://developers.google.com/drive/api/guides/about-sdk
- **OAuth 2.0 Guide:** https://developers.google.com/identity/protocols/oauth2

---

**Last Updated:** November 10, 2025
**Maintained By:** Boring Business AI Brand System
