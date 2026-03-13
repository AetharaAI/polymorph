# Prompt for Codex 5.4: Agent Harness Environment Fix

Here's a comprehensive prompt you can give to Codex 5.4 to systematically fix your Agent Harness environment:

---

## 📝 Prompt for Codex 5.4

```markdown
# Task: Fix Agent Harness Environment - System-Level Repairs Required

## Context
I'm running the AetherOps Agentic Harness for Autonomous Persistent Digital Intelligence on my local laptop (not VM). The harness is running inside a Docker container that was originally configured for self-hosted model inference, but now I need it working with GPT-5.4 (just released today).

## Current State (Verified Issues)

### ✅ What Works
- Web search tools (web_search, tavily_search, brave_search) - all 3 paths functional
- Python execution (execute_python) - file operations work
- npm/project commands - dependency installation works
- Basic shell commands (pwd, mkdir -p) - minimal shell available

### ❌ What's Broken (Critical)

1. **Playwright Browser Tests Fail**
   ```
   Error: browserType.launch: ... 
   chrome-headless-shell: error while loading shared libraries: 
   libglib-2.0.so.0: cannot open shared object file: No such file or directory
   ```
   
2. **HTTP Check Tool Fails**
   ```
   Error: "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: 
   unable to get local issuer certificate (_ssl.c:1016)"
   ```

3. **Shell Limitations**
   - `ls -la` fails: "invalid option -- 'l'" 
   - Using minimal/busybox shell instead of full GNU coreutils

4. **Unverified Tools** (need testing after fixes):
   - Email sending (send_email) - only dry_run tested
   - Lead management (log_lead, list_leads) - CSV ops not tested
   - Background processes (start_process, stop_process) - not tested
   - MCP tools availability - not explored

## Environment Details

**Container Type**: Docker container on local laptop
**Shell Profile**: `project` mode (allows project build/test commands)
**Workspace Path**: `/app/backend/workspaces/c773ce06-1d22-4369-94c7-56af4103b4d8/`
**Current Model**: GPT-5.4 (self-hosted previously, now using cloud endpoint)

## Required Fixes (In Order of Priority)

### Fix 1: Install Playwright System Dependencies
Run these commands in the container to install Chromium browser dependencies:

```bash
# First, identify the base image and install packages accordingly
# For Debian/Ubuntu-based containers:
apt-get update && apt-get install -y \
  libglib2.0-0 \
  libgtk-3-0 \
  libx11-xcb1 \
  libxcb-dri3-0 \
  libxrandr2 \
  libxcomposite1 \
  libxcursor1 \
  libxdamage1 \
  libxi6 \
  libxtst6 \
  libasound2 \
  libpango-1.0-0 \nlibpangocairo-1.0-0 \nlibatk1.0-0 \nlibdbus-1-3 \nlibatspi2.0-0 \nlibxkbcommon0 \nlibxfixes3 \nlibfontconfig1 \nlibfreetype6 \nlibcairo2 \nlibjpeg-turbo8 \nlibpng16-16

# Then reinstall Playwright browsers with proper deps:
npx playwright install-deps chromium
npx playwright install chromium
```

**Verification**: Run `npx playwright test tests/sanity.spec.ts` after install

### Fix 2: Install SSL Certificate Bundle
Fix HTTPS validation issues:

```bash
apt-get update && apt-get install -y ca-certificates curl gnupg
update-ca-certificates
```

**Verification**: Run `http_check` against `https://example.com` after install

### Fix 3: Replace Minimal Shell with Full Bash (Optional but Recommended)

If the container uses busybox/shell without coreutils:

```bash
apt-get update && apt-get install -y bash coreutils procps vim git
# Then configure default shell if needed:
chsh -s /bin/bash $USER  # or set in dockerfile for root user
```

**Verification**: Test `ls -la`, `ps aux`, `top` commands after install

### Fix 4: Verify Python Environment

```bash
python3 --version
pip3 list | grep -E "(playwright|httpx|requests)"
# If missing dependencies, install them:
pip3 install httpx requests pytest pytest-httpx
```

### Fix 5: Test All Tool Categories Systematically

After fixes, run this verification suite:

```bash
# Test shell commands
ls -la tests/
ps aux | grep python

# Test Python file ops  
python3 -c "with open('test_file.txt', 'w') as f: f.write('test'); print('OK')"

# Test HTTP without SSL (for now)
curl -k https://example.com || curl http://example.com

# Test email dry-run (if SMTP configured)
python3 -c "from send_email import send_email; print('Module available')"

# Test lead management CSV ops  
python3 -c "import csv; open('workspace/profit/leads.csv', 'a').close(); print('CSV OK')"

# Test background processes  
python3 -c "import subprocess; p = subprocess.Popen(['sleep', '5']); print('Process OK')"
```

## Alternative Workaround Strategy (If Container Fixes Not Possible)

If you cannot modify the container directly, implement these workarounds:

### Workaround A: Use Python Instead of Shell for File Ops
```python
import os, subprocess, sys

def shell_safe(command):
    """Execute shell commands via Python subprocess with proper error handling"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout + result.stderr, result.returncode == 0
    except Exception as e:
        return str(e), False

def list_files(path='.'):
    """Replace ls command with Python"""
    return os.listdir(path)

def create_file(filename, content):
    """Replace write_file shell commands"""
    with open(filename, 'w') as f:
        f.write(content)
```

### Workaround B: Use pytest + httpx Instead of Playwright for API Testing

Create `tests/api_test.py`:
```python
import httpx
import pytest

@pytest.mark.asyncio  
async def test_api_health():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://api.example.com/health', timeout=10)
        assert response.status_code == 200
        
@pytest.mark.asyncio  
async def test_web_scraping():
    async with httpx.AsyncClient() as client:  
        response = await client.get('https://example.com', timeout=10)  
        assert response.status_code == 200  
        assert 'Example Domain' in response.text  
```

Run with: `pytest tests/api_test.py`

### Workaround C: Skip SSL Verification for Testing (Development Only)

For http_check tool, add SSL bypass option for dev environments:

```python  
import ssl, httpx

def http_check_bypass_ssl(url):  
    """HTTP check without SSL verification for testing"""  
    try:  
        context = ssl.create_default_context()  
        context.check_hostname = False  
        context.verify_mode = ssl.CERT_NONE  
        async with httpx.AsyncClient(verify=context) as client:  
            response = await client.get(url)  
            return {'status': response.status_code, 'body': response.text[:500]}  
    except Exception as e:  
        return {'error': str(e)}  
```

## Success Criteria Checklist

After implementing fixes, verify these all pass:

- [ ] `npx playwright test` runs successfully with Chromium browser tests  
- [ ] `http_check https://example.com` returns status 200 without SSL error  
- [ ] `ls -la tests/` shows directory contents properly  
- [ ] Python execute_python can create/read/write files in workspace  
- [ ] Email send_email dry_run shows proper preview format  
- [ ] Lead management CSV ops work (log_lead creates entries, list_leads reads them)  
- [ ] Background process management works (start_process creates PID, stop_process terminates it)  
- [ ] MCP tools are discoverable and functional if available  

## Testing Strategy After Fixes

Run this comprehensive test sequence:

```bash
# 1. Environment verification  
pwd && ls -la && python3 --version && node --version && git --version  

# 2. Playwright test suite  
npx playwright test tests/sanity.spec.ts  

# 3. HTTP validation  
http_check https://example.com  

# 4. Python capabilities test  
python3 << 'EOF'  
import os, sys  
print("Python version:", sys.version)  
print("Working directory:", os.getcwd())  
print("Files in tests/:", os.listdir('tests') if os.path.exists('tests') else "No tests dir")  
EOF  

# 5. Project command test  
run_project_command "npm test" || echo "No npm test script defined"  

# 6. Integration test suite run  
pytest tests/ -v --tb=short  

# 7. Full harness validation  
echo "=== AGENT HARNESS VALIDATION COMPLETE ==="  
```

## Expected Outcome

After these fixes, the Agent Harness should be fully operational with:
- ✅ Browser automation via Playwright for E2E testing  
- ✅ HTTPS endpoint validation via HTTP check tool  
- ✅ Full shell command capabilities for file operations  
- ✅ Complete tool suite verification across all categories  
- ✅ Ready for production autonomous agent workflows  

## Notes for Implementation

1. **Container Access**: You have root/admin access to the Docker container since it's running locally on your laptop
2. **Priority Order**: Fix Playwright deps first (most critical), then SSL certs, then shell utilities  
3. **Testing**: Run verification tests immediately after each fix to confirm success before moving to next fix  
4. **Documentation**: Document any custom fixes in a `FIXES.md` file in the workspace root for future reference  

--- 

**Start with Fix 1 (Playwright dependencies) and report back the output of each step so we can verify success before proceeding.**
```

---

## 🎯 Quick Summary for Codex 5.4

You can also give Codex a shorter version if needed:

```markdown
Fix my AetherOps Agent Harness Docker container environment. Current issues: Playwright fails due to missing libglib2.0.so.0, HTTP check fails due to SSL cert issues, shell is minimal/busybox without coreutils. 

Required fixes in order: 
1. Install Playwright system deps (libgtk-3, libx11-xcb, etc.) via apt-get 
2. Install CA certificates via apt-get install ca-certificates && update-ca-certificates 
3. Install bash/coreutils if shell is minimal 
4. Verify all tools work after fixes 

Container is on my local laptop, you have full access to run apt-get commands inside it. Start with Playwright deps fix and verify with npx playwright test after installation.
```

Would you like me to create any specific implementation scripts or documentation files to accompany this prompt?