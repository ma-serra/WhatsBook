#!/usr/bin/env python3
"""
Quick verification script to check if WhatsBook can be deployed to Vercel.
This script checks the structure and configuration files.
"""
import os
import json

def check_file(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description} missing: {filepath}")
        return False

def main():
    print("=" * 60)
    print("WhatsBook Vercel Deployment Verification")
    print("=" * 60)
    print()
    
    checks = []
    
    # Check essential files
    checks.append(check_file("api/index.py", "Flask API"))
    checks.append(check_file("vercel.json", "Vercel configuration"))
    checks.append(check_file("requirements.txt", "Python dependencies"))
    checks.append(check_file("whatsBook.py", "Core parsing script"))
    checks.append(check_file("DEPLOYMENT.md", "Deployment documentation"))
    checks.append(check_file(".vercelignore", "Vercel ignore file"))
    checks.append(check_file(".gitignore", "Git ignore file"))
    
    print()
    
    # Check vercel.json structure
    if os.path.exists("vercel.json"):
        try:
            with open("vercel.json", "r") as f:
                config = json.load(f)
            if "builds" in config and "routes" in config:
                print("✓ Vercel configuration is valid")
                checks.append(True)
            else:
                print("✗ Vercel configuration is incomplete")
                checks.append(False)
        except json.JSONDecodeError:
            print("✗ Vercel configuration has invalid JSON")
            checks.append(False)
    
    print()
    
    # Check requirements.txt
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r") as f:
            requirements = f.read()
        required_packages = ["Flask", "Pillow", "numpy", "wordcloud"]
        missing = []
        for pkg in required_packages:
            if pkg.lower() not in requirements.lower():
                missing.append(pkg)
        
        if not missing:
            print(f"✓ All required packages in requirements.txt")
            checks.append(True)
        else:
            print(f"✗ Missing packages: {', '.join(missing)}")
            checks.append(False)
    
    print()
    print("=" * 60)
    
    if all(checks):
        print("✅ All checks passed! Ready to deploy to Vercel.")
        print()
        print("Next steps:")
        print("1. Push this repository to GitHub")
        print("2. Go to https://vercel.com/new")
        print("3. Import your repository")
        print("4. Deploy!")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    exit(main())
