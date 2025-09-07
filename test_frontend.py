#!/usr/bin/env python3
"""
Test script to verify frontend functionality with a working backend
Uses basic analysis to avoid performance issues
"""
import sys
import subprocess
import time
import webbrowser

def start_simple_server():
    """Start a simple HTTP server to serve the frontend files"""
    try:
        # Change to frontend directory and start server
        print("🌐 Starting frontend test server...")
        process = subprocess.Popen([
            'python3', '-m', 'http.server', '3024'
        ], cwd='/Users/aref/Documents/Claude Code/GitHub-Repo-Analyzer/frontend')
        
        # Wait for server to start
        time.sleep(2)
        
        # Open browser
        print("🚀 Opening browser at http://localhost:3024")
        webbrowser.open('http://localhost:3024')
        
        print("✅ Frontend test server running!")
        print("📋 Press Ctrl+C to stop the server")
        
        # Keep server running
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping frontend test server...")
        process.terminate()
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    start_simple_server()