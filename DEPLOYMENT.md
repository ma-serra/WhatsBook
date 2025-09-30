# WhatsBook Deployment Guide

## Deploying to Vercel

This application has been configured to deploy on Vercel. Follow these steps:

### Prerequisites

1. A Vercel account (sign up at https://vercel.com)
2. Vercel CLI installed (optional, but recommended)

### Method 1: Using Vercel Dashboard (Easiest)

1. Push this repository to GitHub (if not already done)
2. Go to https://vercel.com/new
3. Import your GitHub repository
4. Vercel will automatically detect the configuration
5. Click "Deploy"
6. Your application will be live in a few minutes!

### Method 2: Using Vercel CLI

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy from the project directory:
   ```bash
   vercel
   ```

4. Follow the prompts. For production deployment:
   ```bash
   vercel --prod
   ```

### Environment Variables

No environment variables are required for basic functionality.

### Features

- Upload WhatsApp chat exports (.zip or .txt files)
- Automatic conversion to LaTeX format
- Download the generated .tex file
- Compile with pdfLaTeX to create a PDF book

### Local Development

To run the application locally:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Flask development server:
   ```bash
   python api/index.py
   ```

3. Open http://localhost:5000 in your browser

### File Limits

- Maximum file size: 50 MB
- Supported formats: .zip (WhatsApp export) or .txt (_chat.txt file)

### Troubleshooting

If you encounter issues:

1. Check that all dependencies are listed in `requirements.txt`
2. Verify that the `vercel.json` configuration is correct
3. Check Vercel deployment logs for detailed error messages
4. Ensure your WhatsApp export is in the correct format

### Support

For issues or questions about WhatsBook, please refer to the main README.md or open an issue on GitHub.
