# Security Setup - Google API Credentials

**Last Updated:** November 12, 2025
**Status:** ✅ API Key Secured

---

## ✅ What Was Secured

### API Key Stored
Your Google API key has been securely stored in:
```
/Users/elizabethknopf/Documents/claudec/systems/skills-main/boring-business-brand/credentials/.env
```

**Security Measures Applied:**
- ✅ Stored in `.env` file (not committed to git)
- ✅ Protected by `.gitignore` in credentials folder
- ✅ System-wide `.gitignore` updated to block all credential files
- ✅ API key removed from conversation logs (not found in any log.md files)

**Git Protection Added:**
```gitignore
# Environment variables and credentials
.env
.env.*
*.env
credentials/
*credentials.json
*.pickle
*-credentials.json
*.pem
*.key
```

---

## ⚠️ Important: API Key vs OAuth Credentials

### What You Have (API Key)
```
GOOGLE_API_KEY=AIzaSyBp... (secured)
```

**What API Keys Are For:**
- ✅ Google Maps API
- ✅ Google Places API
- ✅ Google Geocoding API
- ✅ YouTube Data API (read-only)
- ❌ **NOT for Google Drive file uploads**

### What You Need (OAuth 2.0 Credentials)

**For Google Drive file uploads, you need:**
1. **OAuth 2.0 Client ID and Secret** (not just an API key)
2. **Desktop application credentials** (JSON file)
3. **User authorization** (one-time browser consent)

**Why OAuth Is Required:**
- Google Drive operations require **user authentication**
- API keys only work for public/anonymous API access
- File uploads need permission to act on behalf of your Google account

---

## 🔧 To Enable Google Drive Uploads

### Step 1: Get OAuth 2.0 Credentials

1. **Go to Google Cloud Console:**
   https://console.cloud.google.com/

2. **Select or Create Project:**
   - Use existing project (if you created one for the API key)
   - Or create new project: "Boring Business AI Scripts"

3. **Enable Google Drive API:**
   - Navigation: APIs & Services → Library
   - Search: "Google Drive API"
   - Click: Enable

4. **Configure OAuth Consent Screen:**
   - Navigation: APIs & Services → OAuth consent screen
   - User Type: External
   - App name: "Boring Business AI - Script Uploader"
   - User support email: your email
   - Developer contact: your email
   - Click: Save and Continue
   - Scopes: Skip (use defaults)
   - Test users: Add your email
   - Click: Save and Continue

5. **Create OAuth 2.0 Client ID:**
   - Navigation: APIs & Services → Credentials
   - Click: "+ Create Credentials" → "OAuth client ID"
   - Application type: **Desktop app**
   - Name: "Boring Business AI Desktop Client"
   - Click: Create

6. **Download Credentials:**
   - Click the download button (↓) next to your new credential
   - Save the JSON file

7. **Move to Credentials Folder:**
   ```bash
   mv ~/Downloads/client_secret_*.json ~/Documents/claudec/systems/skills-main/boring-business-brand/credentials/google-drive-credentials.json
   ```

### Step 2: First-Time Authentication

```bash
cd ~/Documents/claudec/active/Social-Content-Generator/pillar_scripts
python3 upload_to_gdrive.py
```

**What Happens:**
1. Browser opens automatically
2. Sign in to your Google account
3. Grant permissions to access Google Drive
4. Token saved to `credentials/token.pickle`
5. Script proceeds to upload files

**After First Time:**
- No browser popup needed
- Token auto-refreshes when expired
- Just run: `python3 upload_to_gdrive.py`

---

## 📊 Current Setup Status

| Component | Status | Location |
|-----------|--------|----------|
| Google API Key | ✅ Secured | `credentials/.env` |
| OAuth Credentials | ❌ Needed | Download from Cloud Console |
| Auth Token | ⏳ Generated after first auth | `credentials/token.pickle` |
| Upload Script | ✅ Ready | `pillar_scripts/upload_to_gdrive.py` |
| Security Protection | ✅ Active | `.gitignore` configured |

---

## 🔒 Security Best Practices

### Never Commit These Files
The following are automatically excluded from git:
- ✅ `.env` (API keys)
- ✅ `google-drive-credentials.json` (OAuth client secret)
- ✅ `token.pickle` (Access token)
- ✅ `*-credentials.json` (All credential files)
- ✅ `*.key`, `*.pem` (Private keys)

### Verify Git Protection
```bash
cd ~/Documents/claudec/systems
git status
# Should NOT show any credential files
```

### If Credentials Are Exposed
If you accidentally commit credentials:
1. **Revoke immediately** in Google Cloud Console
2. **Generate new credentials**
3. **Force push to remove from git history** (or contact GitHub support)

---

## 🎯 Next Steps

### To Upload Scripts Now

**Option 1: Set Up OAuth (Recommended)**
1. Follow "Step 1: Get OAuth 2.0 Credentials" above
2. Download and save `google-drive-credentials.json`
3. Run `python3 upload_to_gdrive.py` for first-time auth
4. Scripts upload automatically

**Option 2: Manual Upload (Quick Fix)**
```bash
# Open folder
open ~/Documents/claudec/active/Social-Content-Generator/pillar_scripts/

# Open Google Drive
# https://drive.google.com/drive/folders/1KFTbNaKf44tyIVPknDnzshW-DsrJuxnx

# Drag and drop:
# - social_media_scripts_2025-11-09.md
# - SCRIPTS_SUMMARY_2025-11-09.md
# - youtube_scripts_2025-11-11_*.md
# - youtube_scripts_2025-11-12_*.md
```

---

## 📚 Documentation References

- **OAuth 2.0 Setup:** `GOOGLE_DRIVE_INTEGRATION.md`
- **Upload Script Usage:** `pillar_scripts/GOOGLE_DRIVE_INTEGRATION.md`
- **Credentials README:** `credentials/README.md`

---

## ✅ Summary

**What's Protected:**
- ✅ Google API key secured in `.env` file
- ✅ Git configured to never commit credentials
- ✅ No sensitive data found in existing logs
- ✅ Security measures active system-wide

**What's Needed:**
- ⏳ OAuth 2.0 credentials for Drive uploads
- ⏳ One-time browser authentication
- ⏳ Then scripts upload automatically

**Current Files Ready to Upload:**
- 4 markdown files
- ~43 KB of content
- Saved locally in pillar_scripts/

---

**Security Status:** 🟢 Secure
**Upload Status:** 🟡 Pending OAuth Setup
**Next Action:** Download OAuth credentials from Google Cloud Console

