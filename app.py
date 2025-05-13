#!/usr/bin/env python3
import os
import subprocess
import webbrowser
from flask import Flask, render_template, jsonify, request, send_from_directory

app = Flask(__name__)

# Configuration
LOCAL_DIR = os.path.join(os.path.expanduser("~"), "glitch-webkit", "gLiTcH-ToolKit")
PORT = 5000

def get_tools():
    """Get list of available tools with proper categorization"""
    tools = []
    if os.path.exists(LOCAL_DIR):
        for entry in os.listdir(LOCAL_DIR):
            full_path = os.path.join(LOCAL_DIR, entry)
            if os.path.isfile(full_path) and not entry.startswith('.'):
                # Skip desktop files and READMEs
                if entry.lower().endswith(('.desktop', '.md')):
                    continue
                
                # Determine tool type
                if entry.lower().endswith('.py'):
                    tool_type = 'python'
                elif entry.lower().endswith('.sh'):
                    tool_type = 'bash'
                else:
                    # Check if file is executable
                    tool_type = 'executable' if os.access(full_path, os.X_OK) else 'unknown'
                
                tools.append({
                    'name': entry,
                    'path': full_path,
                    'type': tool_type,
                    'description': get_tool_description(entry)
                })
    return sorted(tools, key=lambda x: x['name'].lower())

def get_tool_description(tool_name):
    """Get a brief description for known tools"""
    descriptions = {
        'Boot-Repair.sh': 'Fix bootloader issues',
        'Brave-Browser-Install.sh': 'Install Brave browser',
        'docker-setup.sh': 'Set up Docker environment',
        'firewall-setup.sh': 'Configure system firewall',
        'system-info.sh': 'Display system information',
        'network-speed-test.sh': 'Test network connection speed',
        'password-generator.py': 'Generate secure passwords',
        'vpn-setup.sh': 'Configure VPN connection',
        # Add more descriptions as needed
    }
    return descriptions.get(tool_name, 'Linux system tool')

@app.route('/')
def index():
    tools = get_tools()
    return render_template('index.html', 
                         tools=tools,
                         terminal_icon='utilities-x-terminal.svg',
                         logo='alienarena.svg',
                         toolkit_path=LOCAL_DIR)

@app.route('/run_tool', methods=['POST'])
def run_tool():
    data = request.json
    tool_name = data.get('tool_name')
    tool_path = os.path.join(LOCAL_DIR, tool_name)
    
    if not os.path.exists(tool_path):
        return jsonify({'error': f'Tool not found at {tool_path}'}), 404
    
    try:
        # Determine execution method based on file type
        if tool_path.endswith('.py'):
            result = subprocess.run(['python3', tool_path], capture_output=True, text=True)
        elif tool_path.endswith('.sh'):
            result = subprocess.run(['bash', tool_path], capture_output=True, text=True)
        elif os.access(tool_path, os.X_OK):
            result = subprocess.run([tool_path], capture_output=True, text=True)
        else:
            return jsonify({'error': 'Unsupported file type'}), 400
        
        return jsonify({
            'output': result.stdout,
            'error': result.stderr,
            'returncode': result.returncode
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

def open_browser():
    """Open web browser after short delay"""
    webbrowser.open_new_tab(f"http://localhost:{PORT}")

if __name__ == '__main__':
    # Open browser after 1 second delay
    import threading
    timer = threading.Timer(1, open_browser)
    timer.start()
    
    app.run(host='0.0.0.0', port=PORT, debug=True)