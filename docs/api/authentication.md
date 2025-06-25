Authentication Guide
====================

Authentication
==============

SysPonto uses Django's built-in authentication system with session-based authentication and CSRF protection for web security.

🔐 Authentication Flow
----------------------

### 1\. Login Process

#### Web Login

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   httpPOST /login/  Content-Type: application/x-www-form-urlencoded  username=your_username&password=your_password   `

**Success Response (302 Redirect):**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   httpHTTP/1.1 302 Found  Location: /dashboard/  Set-Cookie: sessionid=abc123...; HttpOnly  Set-Cookie: csrftoken=xyz789...; HttpOnly   `

**Error Response (200 with form errors):**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   html  Invalid username or password     `

#### API Login Check

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   httpGET /api/auth/status/   `

**Response:**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "authenticated": true,      "user": {          "id": 1,          "username": "john_doe",          "role": "student",          "full_name": "John Doe"      }  }   `

### 2\. Session Management

Django automatically manages sessions via cookies:

*   **Session Cookie**: sessionid - Contains encrypted session data
    
*   **CSRF Cookie**: csrftoken - Protection against cross-site request forgery
    
*   **Session Expiry**: Configurable (default: 2 weeks for "Remember Me")
    

### 3\. CSRF Protection

All state-changing requests require CSRF token:

#### Getting CSRF Token

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   javascript// From cookie  function getCSRFToken() {      return document.cookie          .split('; ')          .find(row => row.startsWith('csrftoken='))          ?.split('=')[1];  }  // From form  function getCSRFTokenFromForm() {      return document.querySelector('[name=csrfmiddlewaretoken]').value;  }   `

#### Using CSRF Token

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   httpPOST /api/generate-code/  Content-Type: application/x-www-form-urlencoded  X-CSRFToken: your_csrf_token  class_session_id=123   `

👥 Role-Based Access Control
----------------------------

### User Roles

SysPonto implements three main roles:

#### 1\. Student Role

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# Permissions  - Submit attendance codes  - View own attendance history  - Submit absence justifications  - Access student dashboard   `

#### 2\. Teacher Role

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# Permissions (includes student permissions)  - Generate attendance codes  - Validate student attendance  - Run AI validation  - Manage class sessions  - View class analytics  - Access teacher dashboard   `

#### 3\. Administrator Role

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# Permissions (includes all permissions)  - Manage users (create, update, delete)  - Manage courses and sessions  - System configuration  - Global analytics  - Access admin dashboard   `

### Permission Decorators

The API uses Django decorators for access control:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# From attendance/views.py  @login_required(login_url='/login/')  @user_passes_test(is_teacher, login_url='/login/')  def generate_code_api_view(request):      # Only authenticated teachers can access      pass  @login_required(login_url='/login/')  @user_passes_test(is_student, login_url='/login/')  def submit_attendance_code(request):      # Only authenticated students can access      pass   `

🔧 Implementation Examples
--------------------------

### Python Requests Session

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pythonimport requests  class SysPontoAuth:      def __init__(self, base_url):          self.base_url = base_url          self.session = requests.Session()          self.csrf_token = None      def login(self, username, password):          # Get login page to retrieve CSRF token          response = self.session.get(f"{self.base_url}/login/")          # Extract CSRF token from cookies          self.csrf_token = self.session.cookies.get('csrftoken')          # Perform login          login_data = {              'username': username,              'password': password,              'csrfmiddlewaretoken': self.csrf_token          }          response = self.session.post(              f"{self.base_url}/login/",              data=login_data          )          # Check if redirect occurred (successful login)          return response.status_code == 302      def api_request(self, method, endpoint, data=None):          url = f"{self.base_url}{endpoint}"          headers = {              'X-CSRFToken': self.csrf_token or self.session.cookies.get('csrftoken')          }          return self.session.request(              method=method,              url=url,              data=data,              headers=headers          )  # Usage  api = SysPontoAuth('http://localhost:8000')  if api.login('prof.silva', 'password123'):      response = api.api_request('POST', '/api/generate-code/', {          'class_session_id': '1'      })      print(response.json())   `

### JavaScript Fetch API

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML``   javascriptclass SysPontoAuth {      constructor(baseUrl) {          this.baseUrl = baseUrl;          this.csrfToken = null;      }      async login(username, password) {          // Get CSRF token          await this.getCSRFToken();          const formData = new FormData();          formData.append('username', username);          formData.append('password', password);          formData.append('csrfmiddlewaretoken', this.csrfToken);          const response = await fetch(`${this.baseUrl}/login/`, {              method: 'POST',              body: formData,              credentials: 'include' // Include cookies          });          return response.ok;      }      async getCSRFToken() {          const response = await fetch(`${this.baseUrl}/login/`, {              credentials: 'include'          });          // Extract CSRF token from cookie          this.csrfToken = this.getCookie('csrftoken');      }      async apiRequest(method, endpoint, data = {}) {          const url = `${this.baseUrl}${endpoint}`;          const options = {              method: method,              credentials: 'include',              headers: {                  'X-CSRFToken': this.csrfToken,                  'Content-Type': 'application/x-www-form-urlencoded'              }          };          if (method !== 'GET' && data) {              options.body = new URLSearchParams(data);          }          const response = await fetch(url, options);          return response.json();      }      getCookie(name) {          const value = `; ${document.cookie}`;          const parts = value.split(`; ${name}=`);          if (parts.length === 2) return parts.pop().split(';').shift();      }  }  // Usage  const auth = new SysPontoAuth('http://localhost:8000');  await auth.login('student1', 'password123');  const result = await auth.apiRequest('POST', '/api/submit-attendance/', {      attendance_code: 'ABC123',      simulated_latitude: '41.5369',      simulated_longitude: '-8.4239'  });   ``

### cURL Examples

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bash# Login and save cookies  curl -X POST http://localhost:8000/login/ \    -d "username=prof.silva&password=password123" \    -c cookies.txt \    -b cookies.txt  # Extract CSRF token from cookies  CSRF_TOKEN=$(grep csrftoken cookies.txt | cut -f7)  # Make authenticated API request  curl -X POST http://localhost:8000/api/generate-code/ \    -b cookies.txt \    -H "X-CSRFToken: $CSRF_TOKEN" \    -d "class_session_id=1"   `

🚨 Security Considerations
--------------------------

### Best Practices

1.  python# settings.pySECURE\_SSL\_REDIRECT = TrueSESSION\_COOKIE\_SECURE = TrueCSRF\_COOKIE\_SECURE = True
    
2.  javascriptasync function apiRequest(endpoint, data) { const response = await fetch(endpoint, { method: 'POST', body: data, credentials: 'include' }); if (response.status === 403) { // Session expired, redirect to login window.location.href = '/login/'; return; } return response.json();}
    
3.  javascript// Check user role before showing UI elementsif (user.role === 'teacher') { showTeacherControls();} else if (user.role === 'student') { showStudentControls();}
    

### Common Authentication Errors

#### 1\. Missing CSRF Token (403 Forbidden)

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "status": "error",      "message": "CSRF token missing or incorrect"  }   `

**Solution**: Include X-CSRFToken header in requests

#### 2\. Session Expired (401 Unauthorized)

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "status": "error",       "message": "Authentication required"  }   `

**Solution**: Redirect user to login page

#### 3\. Insufficient Permissions (403 Forbidden)

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "status": "error",      "message": "Permission denied"  }   `

**Solution**: Check user role and permissions

🔄 Session Management
---------------------

### Extending Session Lifetime

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# views.py - Remember me functionality  def login_view(request):      if request.method == 'POST':          # ... authentication logic ...          if remember_me:              request.session.set_expiry(1209600)  # 2 weeks          else:              request.session.set_expiry(0)  # Browser session   `

### Logout Implementation

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   httpPOST /logout/  X-CSRFToken: your_csrf_token   `

**Response:**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   httpHTTP/1.1 302 Found  Location: /  Set-Cookie: sessionid=; expires=Thu, 01 Jan 1970 00:00:00 GMT  Set-Cookie: csrftoken=; expires=Thu, 01 Jan 1970 00:00:00 GMT   `

📱 Mobile App Integration
-------------------------

For mobile applications, consider implementing token-based authentication alongside session authentication:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# Future enhancement - Token authentication  from rest_framework.authtoken.models import Token  def get_auth_token(request):      if request.user.is_authenticated:          token, created = Token.objects.get_or_create(user=request.user)          return JsonResponse({'token': token.key})   `
