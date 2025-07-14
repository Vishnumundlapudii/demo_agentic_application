#!/usr/bin/env python3
"""
Script to diagnose and fix common Streamlit issues
"""

import sys
import importlib
import subprocess

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'streamlit',
        'langgraph', 
        'langchain',
        'requests',
        'python-dotenv',
        'matplotlib',
        'pandas'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package.replace('-', '_'))
            print(f"✅ {package} - OK")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n🔧 Install missing packages:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_file_imports():
    """Check if our custom modules can be imported"""
    try:
        from agents import SimpleAgent
        print("✅ agents.py - OK")
    except Exception as e:
        print(f"❌ agents.py - ERROR: {e}")
        return False
    
    try:
        from multi_agent_workflow import MultiAgentSystem
        print("✅ multi_agent_workflow.py - OK")
    except Exception as e:
        print(f"❌ multi_agent_workflow.py - ERROR: {e}")
        return False
    
    try:
        from e2e_llm_client import initialize_e2e_client
        print("✅ e2e_llm_client.py - OK")
    except Exception as e:
        print(f"❌ e2e_llm_client.py - ERROR: {e}")
        return False
    
    return True

def check_env_file():
    """Check .env file"""
    import os
    
    if os.path.exists('.env'):
        print("✅ .env file exists")
        
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('E2E_API_KEY')
        if api_key:
            print(f"✅ E2E_API_KEY loaded (starts with: {api_key[:10]}...)")
        else:
            print("⚠️ E2E_API_KEY not set in .env")
            
    else:
        print("⚠️ .env file not found")

def test_streamlit_basic():
    """Test basic streamlit functionality"""
    try:
        import streamlit as st
        print("✅ Streamlit import - OK")
        
        # Test if we can run streamlit hello
        result = subprocess.run(['streamlit', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Streamlit CLI - {result.stdout.strip()}")
        else:
            print(f"❌ Streamlit CLI - Error: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Streamlit - ERROR: {e}")

def main():
    print("🔧 Streamlit Issue Diagnostic Tool")
    print("=" * 50)
    
    print("\n1. Checking Dependencies...")
    deps_ok = check_dependencies()
    
    print("\n2. Checking File Imports...")
    imports_ok = check_file_imports()
    
    print("\n3. Checking Environment...")
    check_env_file()
    
    print("\n4. Testing Streamlit...")
    test_streamlit_basic()
    
    print("\n" + "=" * 50)
    
    if deps_ok and imports_ok:
        print("✅ All checks passed! Try running:")
        print("   streamlit run streamlit_app.py")
    else:
        print("❌ Issues found. Fix the errors above and try again.")

if __name__ == "__main__":
    main()