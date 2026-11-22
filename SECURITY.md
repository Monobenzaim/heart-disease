# 🔒 Security Guidelines

## ⚠️ CRITICAL: Protecting Sensitive Information

This project handles medical data and uses API keys. Follow these guidelines to keep everything secure.

## 🔑 API Keys & Secrets

### ❌ NEVER Commit These:
- API keys (Groq, OpenAI, etc.)
- Environment variables with secrets
- Configuration files with credentials
- Token files
- Password files

### ✅ Safe Practices:

1. **Use Environment Variables**
   ```bash
   # Linux/Mac
   export GROQ_API_KEY="your_key_here"

   # Windows CMD
   set GROQ_API_KEY=your_key_here

   # Windows PowerShell
   $env:GROQ_API_KEY="your_key_here"
   ```

2. **Use .env File (Never Commit!)**
   ```bash
   # Copy template
   cp .env.example .env

   # Edit with your keys
   nano .env
   ```

3. **Use Streamlit Secrets**
   ```toml
   # .streamlit/secrets.toml (auto-ignored)
   GROQ_API_KEY = "your_key_here"
   ```

## 🏥 Patient Data Protection

### ❌ NEVER Commit:
- Real patient names
- Patient IDs
- Medical records
- Personal health information (PHI)
- Generated reports with real data

### ✅ Safe Practices:

1. **Use Fake Data for Development**
   ```python
   patient_info = {
       'name': 'John Doe',  # Fake name
       'id': 'DEMO123',     # Demo ID
       'age': 63
   }
   ```

2. **Generated Files Are Auto-Ignored**
   - `reports/*.pdf` → Ignored
   - `reports/*.json` → Ignored
   - Use these directories freely

3. **For Thesis/Demos**
   - Use synthetic data
   - Anonymize any real data
   - Label clearly as "SAMPLE"

## 📊 Data Files

### What's Included in Git:
- ✅ Public datasets (heart.csv) - anonymized
- ✅ Sample data for testing
- ✅ Code and documentation

### What's Excluded:
- ❌ Large model files (*.pkl > 10MB)
- ❌ Generated reports
- ❌ Benchmark results
- ❌ Personal datasets

## 🛡️ Security Checklist

Before committing to Git:

- [ ] No API keys in code
- [ ] No passwords or tokens
- [ ] No real patient data
- [ ] No .env file
- [ ] No credential files
- [ ] `.gitignore` is up to date
- [ ] Reviewed `git status`
- [ ] Checked `git diff`

## 🚨 If You Accidentally Commit Secrets

### Immediate Actions:

1. **Rotate the Key Immediately**
   - Go to Groq console
   - Revoke compromised key
   - Generate new key

2. **Remove from Git History**
   ```bash
   # Use BFG Repo-Cleaner or git-filter-branch
   # This is complex - prevent it instead!
   ```

3. **Force Push (Dangerous!)**
   ```bash
   git reset --hard HEAD~1
   git push --force origin main
   ```

## 🔐 Deployment Security

### For Production:

1. **Use Secret Management**
   - AWS Secrets Manager
   - Azure Key Vault
   - Google Secret Manager
   - Environment variables on hosting platform

2. **Streamlit Cloud**
   - Use Streamlit Secrets
   - Settings → Secrets
   - Never hardcode keys

3. **Docker**
   ```dockerfile
   # Pass as build args
   ARG GROQ_API_KEY
   ENV GROQ_API_KEY=$GROQ_API_KEY
   ```

## 📱 Sharing Your Project

### Safe to Share:
- ✅ GitHub repository (without secrets)
- ✅ Demo videos (with fake data)
- ✅ Code samples
- ✅ Documentation
- ✅ Thesis/paper (anonymized results)

### Never Share:
- ❌ Your .env file
- ❌ API keys in screenshots
- ❌ Real patient data
- ❌ Credentials in demo videos

## 🎓 For Thesis/Academic Use

### Publishing Requirements:

1. **Code Repository**
   - Share on GitHub (no secrets)
   - Include .env.example
   - Document setup clearly

2. **Data Sharing**
   - Use public datasets only
   - Cite data sources
   - Follow dataset licenses

3. **Results Sharing**
   - Anonymize everything
   - Use aggregated statistics
   - No individual patient results

## ⚖️ Compliance Considerations

### HIPAA (US Healthcare)
- Encrypt patient data
- Access controls
- Audit logs
- Data retention policies

### GDPR (EU Data Protection)
- Right to erasure
- Data minimization
- Explicit consent
- Privacy by design

### General Best Practices
- Principle of least privilege
- Regular security audits
- Incident response plan
- User training

## 📞 Reporting Security Issues

If you find a security vulnerability:

1. **DO NOT** create a public GitHub issue
2. Email the maintainer privately
3. Describe the issue clearly
4. Allow time for fix before disclosure

## 📚 Resources

- [Groq Security Best Practices](https://console.groq.com/docs/security)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/)

## ✅ Current Protections

This project already includes:

- ✅ Comprehensive `.gitignore`
- ✅ `.env.example` template
- ✅ Patient data directories ignored
- ✅ API key patterns blocked
- ✅ Security documentation
- ✅ Safe coding practices

---

**Remember: Security is not a one-time task, it's an ongoing practice!**

Stay safe! 🔒
