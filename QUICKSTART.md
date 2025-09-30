# WhatsBook - Quick Start Guide

## 🚀 Deploy to Vercel in 3 Steps

### Step 1: Push to GitHub
Your repository should already be on GitHub at: `ma-serra/WhatsBook`

### Step 2: Import to Vercel
1. Go to [vercel.com/new](https://vercel.com/new)
2. Click "Import Git Repository"
3. Select `ma-serra/WhatsBook`
4. Vercel will automatically detect the configuration from `vercel.json`

### Step 3: Deploy
1. Click "Deploy"
2. Wait 2-3 minutes for the build to complete
3. Your app will be live at `https://whatsbook-xxxxx.vercel.app`

## 📱 Using the Web App

Once deployed, users can:

1. **Upload WhatsApp Export**
   - Go to WhatsApp → Chat → Menu (⋮) → More → Export Chat
   - Upload the `.zip` file to your deployed app

2. **Convert to LaTeX**
   - Click "Convert to LaTeX" button
   - Wait for processing (usually < 30 seconds for normal chats)

3. **Download & Compile**
   - Download the generated `whatsbook_content.tex` file
   - Compile with pdfLaTeX to create the final PDF book

## 🎨 Features

### Web Interface
- Modern, responsive design
- Drag & drop file upload
- Real-time progress feedback
- Mobile-friendly
- No installation required

### Processing
- Handles both `.zip` and `.txt` files
- Automatic extraction of compressed exports
- Full LaTeX formatting
- Image path handling
- Date parsing and formatting

## 🔧 Technical Details

### Architecture
- **Frontend**: HTML5 + JavaScript (vanilla, no frameworks)
- **Backend**: Python Flask API
- **Deployment**: Vercel Serverless Functions
- **Storage**: Temporary (files are processed and deleted)

### Limits
- Max file size: 50 MB
- Processing timeout: 60 seconds (Vercel limit)
- No persistent storage (stateless processing)

## 🐛 Troubleshooting

### Deployment Issues
If deployment fails, check:
1. All files are committed to GitHub
2. `vercel.json` is valid JSON
3. `requirements.txt` contains all dependencies
4. Python version is compatible (3.9+)

### Runtime Issues
If the app doesn't work after deployment:
1. Check Vercel deployment logs
2. Verify file upload size is under 50 MB
3. Ensure WhatsApp export is in the correct format
4. Try with the test data first

### Common Errors
- **"No module named 'PIL'"**: Dependencies not installed (Vercel should handle this automatically)
- **"File too large"**: Export is over 50 MB (try exporting without media)
- **"Invalid file format"**: Make sure you're uploading a WhatsApp export

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [WhatsApp Export Guide](https://faq.whatsapp.com/android/chats/how-to-save-your-chat-history/)

## 🆘 Support

For issues specific to:
- **Deployment**: Check [DEPLOYMENT.md](./DEPLOYMENT.md)
- **WhatsBook functionality**: See main [README.md](./README.md)
- **Bug reports**: Open an issue on GitHub

---

**Happy Chat Archiving! 📚💬**
