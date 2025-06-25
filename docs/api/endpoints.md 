docs/api/endpoints.md - Complete API Endpoints Reference
========================================================

API Endpoints
=============

Complete reference for all SysPonto API endpoints based on the actual Django implementation.

📋 Base Information
-------------------

*   **Base URL**: http://localhost:8000 (development)
    
*   **Authentication**: Session-based with CSRF protection
    
*   **Content-Type**: application/x-www-form-urlencoded for most endpoints
    
*   **Response Format**: JSON
    

🔑 Attendance Management
------------------------

### Generate Attendance Code

Generate a new attendance code for a class session.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   httpPOST /api/generate-code/   `

**Authentication**: Teacher role required

**Parameters**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "class_session_id": "string (required)" // ID of the class session  }   `

**Response**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "status": "success",      "message": "Código gerado com sucesso!",      "code": "ABC123",      "expires_at": "2024-01-15T14:30:00Z",      "class_session_id": "1"  }   `

**Error Responses**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "status": "error",      "message": "Class session ID is required."  }   `

**Example**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bashcurl -X POST http://localhost:8000/api/generate-code/ \    -b cookies.txt \    -H "X-CSRFToken: your_csrf_token" \    -d "class_session_id=1"   `

### Submit Attendance Code

Submit an attendance code as a student.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   httpPOST /api/submit-attendance/   `

**Authentication**: Student role required

**Parameters**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "attendance_code": "string (required)",     // 6-character attendance code      "simulated_latitude": "number (optional)",  // Student's latitude      "simulated_longitude": "number (optional)", // Student's longitude      "simulated_ip": "string (optional)"         // Student's IP address  }   `

**Response**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "status": "success",      "message": "Código de presença enviado com sucesso. Aguarda validação do professor."  }   `

**Error Responses**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json// Invalid code  {      "status": "error",      "message": "Código de presença inválido."  }  // Expired code  {      "status": "error",       "message": "Código de presença expirado."  }  // Already submitted  {      "status": "info",      "message": "Já enviou a presença para esta aula."  }   `

**Example**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bashcurl -X POST http://localhost:8000/api/submit-attendance/ \    -b cookies.txt \    -H "X-CSRFToken: your_csrf_token" \    -d "attendance_code=ABC123&simulated_latitude=41.5369&simulated_longitude=-8.4239"   `

### Run AI Validation

Trigger AI validation for an attendance record.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   httpPOST /api/run-ai-validation/   `

**Authentication**: Teacher role required

**Parameters**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "attendance_record_id": "string (required)", // ID of attendance record      "class_session_id": "string (required)"      // ID of class session  }   `

**Response**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "status": "success",      "aiResult": {          "isFraudulent": false,          "fraudExplanation": "No issues detected."      },      "attendance_record_id": "123"  }   `

### Validate Attendance

Mark an attendance record as present (teacher validation).

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   httpPOST /api/validate-attendance/   `

**Authentication**: Teacher role required

**Parameters**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "attendance_record_id": "string (required)" // ID of attendance record  }   `

**Response**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "status": "success",      "message": "Attendance validated successfully."  }   `

### Get Session Submissions

Retrieve all attendance submissions for a class session.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   httpGET /api/get-session-submissions/   `

**Authentication**: Teacher role required

**Parameters**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   class_session_id=123   `

**Response**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "status": "success",      "submissions": [          {              "id": "456",              "name": "John Doe",              "timestamp": "2024-01-15T10:30:00Z",              "simulatedIp": "192.168.1.100",              "simulatedGeolocation": {                  "latitude": 41.5369,                  "longitude": -8.4239              },              "aiResult": {                  "isFraudulent": false,                  "fraudExplanation": "Location validation passed"              },              "is_present": true,              "class_session_id": "123"          }      ]  }   `

📝 Absence Justification
------------------------

### Submit Justification

Submit an absence justification with optional document.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   httpPOST /api/submit-justification/   `

**Authentication**: Student role required

**Content-Type**: multipart/form-data

**Parameters**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "class_session_id": "string (required)",      "description": "string (required)",      // Reason for absence      "document": "file (optional)",           // Supporting document      "is_late_arrival": "boolean (optional)"  // true for late arrival, false for absence  }   `

**Response**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "status": "success",      "message": "Justificação de ausência enviada!",      "justification_id": "789"  }   `

**Error Responses**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json// Missing required fields  {      "status": "error",      "message": "Todos os campos são obrigatórios."  }  // File too large  {      "status": "error",      "message": "Ficheiro muito grande. Máximo 5MB."  }  // Duplicate justification  {      "status": "error",      "message": "Já enviou uma justificação para esta aula."  }   `

👥 Student Dashboard APIs
-------------------------

### Get Current Classes

Get classes currently running for the student.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   httpGET /api/student/current-classes/   `

**Authentication**: Student role required

**Response**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "status": "success",      "current_classes": [          {              "id": 1,              "course_name": "Web Development",              "start_datetime": "2024-01-15T14:00:00Z",              "end_datetime": "2024-01-15T17:00:00Z"          }      ]  }   `

### Get Today's Classes

Get all classes scheduled for today.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   httpGET /api/student/today-classes/   `

**Authentication**: Student role required

**Response**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "status": "success",      "today_classes": [          {              "id": 1,              "course_name": "Web Development",              "start_datetime": "2024-01-15T14:00:00Z",               "end_datetime": "2024-01-15T17:00:00Z"          },          {              "id": 2,              "course_name": "Database Design",              "start_datetime": "2024-01-15T18:30:00Z",              "end_datetime": "2024-01-15T21:30:00Z"          }      ]  }   `

### Get Weekly Classes

Get all classes for the current week.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   httpGET /api/student/weekly-classes/   `

**Authentication**: Student role required

**Response**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "status": "success",      "weekly_classes": [          // Array of class objects similar to today-classes      ]  }   `

### Get Attendance History

Get student's attendance history.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   httpGET /api/student/attendance-history/   `

**Authentication**: Student role required

**Parameters**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   limit=10 (optional, default: 10)   `

**Response**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "status": "success",      "attendance_history": [          {              "id": "123",              "course_name": "Web Development",              "timestamp": "2024-01-15T10:30:00Z",              "is_present": true,              "status": "Present",              "session_date": "2024-01-15"          }      ]  }   `

🏫 Admin Management APIs
------------------------

_Note: These APIs are implemented in the admin\_views.py file but may require additional URL configuration_

### Create User

Create a new user account.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   httpPOST /api/admin/create-user/   `

**Authentication**: Administrator role required

**Parameters**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "username": "string (required)",      "email": "string (required)",      "first_name": "string (optional)",      "last_name": "string (optional)",      "role": "string (required)", // 'student', 'teacher', 'admin'      "password": "string (required)"  }   `

**Response**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "status": "success",      "message": "Utilizador john_doe criado com sucesso!",      "user_id": 123  }   `

### Create Course

Create a new course.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   httpPOST /api/admin/create-course/   `

**Authentication**: Administrator role required

**Parameters**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "name": "string (required)",      "code": "string (required)",      "description": "string (optional)",      "teachers": ["array of teacher IDs"]  }   `

**Response**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "status": "success",       "message": "Curso Web Development criado com sucesso!",      "course_id": 456  }   `

### Create Class Session

Create a new class session.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   httpPOST /api/admin/create-session/   `

**Authentication**: Administrator role required

**Parameters**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "course_id": "string (required)",      "date": "string (required)",        // YYYY-MM-DD format      "start_time": "string (required)",  // HH:MM format      "end_time": "string (required)"     // HH:MM format  }   `

**Response**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "status": "success",      "message": "Sessão criada para Web Development em 2024-01-15!",      "session_id": 789  }   `

🌐 WebSocket APIs {#websockets}
-------------------------------

### Real-time Attendance Updates

Connect to WebSocket for real-time attendance notifications.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   javascript// WebSocket connection  const socket = new WebSocket('ws://localhost:8000/ws/attendance/class_session_123/');  socket.onmessage = function(event) {      const data = JSON.parse(event.data);      console.log('Real-time update:', data);  };   `

**Message Types**:

#### Student Submission

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "type": "class_session_message",      "message": "Student john_doe has submitted attendance",      "context": {          "type": "student_submitted",          "id": "456",          "name": "John Doe",           "timestamp": "2024-01-15T10:30:00Z",          "simulatedIp": "192.168.1.100",          "simulatedGeolocation": {              "latitude": 41.5369,              "longitude": -8.4239          },          "is_present": false      }  }   `

#### AI Validation Result

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "type": "class_session_message",      "message": "AI validation completed",      "context": {          "type": "ai_result_updated_for_teacher",          "record_id": "456",          "aiResult": {              "isFraudulent": false,              "fraudExplanation": "Location validation passed"          }      }  }   `

#### Code Generation

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "type": "class_session_message",       "message": "New code ABC123 generated",      "context": {          "type": "code_generated_for_teacher",          "code": "ABC123",          "expires_at": "2024-01-15T14:30:00Z"      }  }   `

❌ Error Handling
----------------

### Common HTTP Status Codes

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   CodeMeaningDescription200OKRequest successful302FoundRedirect (often after successful login)400Bad RequestInvalid parameters401UnauthorizedAuthentication required403ForbiddenPermission denied or CSRF token missing404Not FoundResource not found500Internal Server ErrorServer error   `

### Standard Error Format

All API errors follow this format:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "status": "error",      "message": "Human-readable error description",      "errors": {          "field_name": ["Specific validation errors"]      }  }   `

### Common Error Scenarios

#### 1\. CSRF Token Missing

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   httpHTTP/1.1 403 Forbidden  Content-Type: application/json  {      "status": "error",      "message": "CSRF verification failed"  }   `

**Solution**: Include X-CSRFToken header

#### 2\. Session Expired

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   httpHTTP/1.1 302 Found  Location: /login/   `

**Solution**: Redirect to login page

#### 3\. Invalid Attendance Code

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "status": "error",      "message": "Código de presença inválido."  }   `

#### 4\. Permission Denied

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "status": "error",       "message": "Permission denied."  }   `

### Error Handling Example

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   javascriptasync function handleAPIRequest(endpoint, data) {      try {          const response = await fetch(endpoint, {              method: 'POST',              headers: {                  'Content-Type': 'application/x-www-form-urlencoded',                  'X-CSRFToken': getCSRFToken()              },              body: new URLSearchParams(data),              credentials: 'include'          });          // Handle different response types          if (response.redirected) {              // Likely redirected to login              window.location.href = response.url;              return;          }          const result = await response.json();          if (result.status === 'success') {              return result;          } else {              throw new Error(result.message || 'Unknown error occurred');          }      } catch (error) {          console.error('API Error:', error);          // Handle specific error types          if (error.message.includes('CSRF')) {              // Refresh page to get new CSRF token              window.location.reload();          } else if (error.message.includes('Authentication')) {              // Redirect to login              window.location.href = '/login/';          } else {              // Show user-friendly error              showErrorMessage(error.message);          }          throw error;      }  }  // Usage example  try {      const result = await handleAPIRequest('/api/submit-attendance/', {          attendance_code: 'ABC123',          simulated_latitude: '41.5369',          simulated_longitude: '-8.4239'      });      showSuccessMessage(result.message);  } catch (error) {      // Error already handled in handleAPIRequest  }   `

📊 API Usage Analytics
----------------------

Based on the SysPonto implementation, here are the most commonly used endpoints:

### High-Traffic Endpoints

1.  **/api/submit-attendance/** - Used by all students during class
    
2.  **/api/generate-code/** - Used by teachers at class start
    
3.  **/api/get-session-submissions/** - Real-time teacher monitoring
    
4.  **/api/validate-attendance/** - Teacher approval actions
    

### Medium-Traffic Endpoints

1.  **/api/student/current-classes/** - Dashboard refreshes
    
2.  **/api/student/today-classes/** - Daily schedule views
    
3.  **/api/run-ai-validation/** - Fraud detection triggers
    
4.  **/api/submit-justification/** - Absence submissions
    

### Low-Traffic Endpoints

1.  **Admin APIs** - User/course management
    
2.  **Analytics APIs** - Reporting and statistics
    
3.  **/api/student/weekly-classes/** - Calendar views
    
4.  **/api/student/attendance-history/** - History reviews
    

🔗 Integration Patterns
-----------------------

### Pattern 1: Student Mobile App

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   javascriptclass StudentApp {      constructor() {          this.api = new SysPontoAPI('https://your-domain.com');          this.currentLocation = null;      }      async initialize() {          // Get user location          this.currentLocation = await this.getCurrentLocation();          // Load today's classes          const classes = await this.api.getTodayClasses();          this.displayClasses(classes);          // Set up periodic refresh          setInterval(() => this.refreshCurrentClasses(), 60000);      }      async submitAttendance(code) {          const result = await this.api.submitAttendance(              code,              this.currentLocation.latitude,              this.currentLocation.longitude          );          this.showResult(result);          await this.refreshAttendanceHistory();      }      async getCurrentLocation() {          return new Promise((resolve, reject) => {              navigator.geolocation.getCurrentPosition(                  position => resolve({                      latitude: position.coords.latitude,                      longitude: position.coords.longitude                  }),                  error => {                      // Fallback to approximate location                      resolve({                          latitude: 41.5369,                          longitude: -8.4239                      });                  }              );          });      }  }   `

### Pattern 2: Teacher Dashboard Integration

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML``   javascriptclass TeacherDashboard {      constructor() {          this.api = new SysPontoAPI('https://your-domain.com');          this.websocket = null;          this.activeSessionId = null;      }      async initialize() {          // Load today's sessions          const sessions = await this.loadTodaySessions();          this.displaySessions(sessions);          // Set up WebSocket for real-time updates          this.setupWebSocket();      }      async generateCode(sessionId) {          const result = await this.api.generateCode(sessionId);          if (result.status === 'success') {              this.displayCode(result.code, result.expires_at);              this.activeSessionId = sessionId;              // Connect to session-specific WebSocket              this.connectToSession(sessionId);              // Start monitoring submissions              this.startMonitoring(sessionId);          }      }      setupWebSocket() {          if (this.activeSessionId) {              const wsUrl = `ws://${window.location.host}/ws/attendance/class_session_${this.activeSessionId}/`;              this.websocket = new WebSocket(wsUrl);              this.websocket.onmessage = (event) => {                  const data = JSON.parse(event.data);                  this.handleRealtimeUpdate(data);              };          }      }      handleRealtimeUpdate(data) {          switch (data.context?.type) {              case 'student_submitted':                  this.addSubmissionToList(data.context);                  break;              case 'ai_result_updated_for_teacher':                  this.updateAIResult(data.context);                  break;          }      }      async validateAllPending() {          const submissions = await this.api.getSessionSubmissions(this.activeSessionId);          const pending = submissions.filter(s => !s.is_present);          for (const submission of pending) {              await this.api.validateAttendance(submission.id);          }          this.refreshSubmissionsList();      }  }   ``

### Pattern 3: LMS Integration

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# Example Django integration with external LMS  class LMSIntegration:      def __init__(self, lms_api_key, sysponto_base_url):          self.lms_api_key = lms_api_key          self.sysponto = SysPontoAPI(sysponto_base_url)      def sync_attendance_to_lms(self, course_id, session_date):          # Get attendance data from SysPonto          session = self.get_session_by_course_and_date(course_id, session_date)          submissions = self.sysponto.get_session_submissions(session.id)          # Format for LMS          attendance_data = []          for submission in submissions:              attendance_data.append({                  'student_id': submission['student_id'],                  'course_id': course_id,                  'date': session_date,                  'status': 'present' if submission['is_present'] else 'absent',                  'timestamp': submission['timestamp']              })          # Send to LMS          return self.send_to_lms(attendance_data)      def send_to_lms(self, attendance_data):          # Implementation depends on LMS API          pass   `

🚀 Performance Optimization
---------------------------

### Caching Strategies

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# In views.py - Add caching for frequently accessed data  from django.core.cache import cache  def get_session_submissions(request):      class_session_id = request.GET.get('class_session_id')      cache_key = f'submissions_{class_session_id}'      # Try to get from cache first      submissions = cache.get(cache_key)      if submissions is None:          # Query database if not in cache          submissions = AttendanceRecord.objects.filter(              class_session_id=class_session_id          ).select_related('student').order_by('timestamp')          # Cache for 30 seconds          cache.set(cache_key, submissions, 30)      return JsonResponse({'status': 'success', 'submissions': submissions})   `

### Database Query Optimization

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# Optimized queries with select_related and prefetch_related  def get_student_dashboard_data(request):      today = timezone.now().date()      # Optimize queries with proper joins      today_sessions = ClassSession.objects.filter(          course__course_enrollments__student=request.user,          date=today      ).select_related('course').order_by('start_time')      attendance_history = AttendanceRecord.objects.filter(          student=request.user      ).select_related(          'class_session__course'      ).order_by('-timestamp')[:10]      return {          'today_sessions': today_sessions,          'attendance_history': attendance_history      }   `

### API Response Compression

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# settings.py - Enable GZip compression  MIDDLEWARE = [      'django.middleware.gzip.GZipMiddleware',      # ... other middleware  ]   `

🧪 Testing the API
------------------

### Unit Tests Example

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# tests/test_api.py  from django.test import TestCase, Client  from django.contrib.auth import get_user_model  from courses.models import Course, ClassSession  from attendance.models import AttendanceCode  User = get_user_model()  class AttendanceAPITestCase(TestCase):      def setUp(self):          self.client = Client()          # Create test users          self.teacher = User.objects.create_user(              username='test_teacher',              password='test123',              role='teacher'          )          self.student = User.objects.create_user(              username='test_student',               password='test123',              role='student'          )          # Create test course and session          self.course = Course.objects.create(              name='Test Course',              code='TEST001'          )          self.course.teachers.add(self.teacher)          self.session = ClassSession.objects.create(              course=self.course,              date=timezone.now().date(),              start_time=timezone.now().time(),              end_time=(timezone.now() + timedelta(hours=2)).time()          )      def test_generate_code_as_teacher(self):          # Login as teacher          self.client.login(username='test_teacher', password='test123')          # Generate code          response = self.client.post('/api/generate-code/', {              'class_session_id': self.session.id          })          self.assertEqual(response.status_code, 200)          data = response.json()          self.assertEqual(data['status'], 'success')          self.assertIn('code', data)          self.assertEqual(len(data['code']), 6)      def test_submit_attendance_as_student(self):          # Create attendance code          code = AttendanceCode.objects.create(              class_session=self.session,              code='TEST01',              expires_at=timezone.now() + timedelta(minutes=10)          )          # Login as student          self.client.login(username='test_student', password='test123')          # Submit attendance          response = self.client.post('/api/submit-attendance/', {              'attendance_code': 'TEST01',              'simulated_latitude': '41.5369',              'simulated_longitude': '-8.4239'          })          self.assertEqual(response.status_code, 200)          data = response.json()          self.assertEqual(data['status'], 'success')      def test_unauthorized_access(self):          # Try to generate code without authentication          response = self.client.post('/api/generate-code/', {              'class_session_id': self.session.id          })          # Should redirect to login          self.assertEqual(response.status_code, 302)   `

### API Integration Tests

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# tests/test_integration.py  class AttendanceWorkflowTestCase(TestCase):      def test_complete_attendance_workflow(self):          """Test the complete attendance submission workflow"""          # 1. Teacher logs in and generates code          self.client.login(username='teacher', password='test123')          response = self.client.post('/api/generate-code/', {              'class_session_id': self.session.id          })          code_data = response.json()          attendance_code = code_data['code']          # 2. Student logs in and submits attendance          self.client.logout()          self.client.login(username='student', password='test123')          response = self.client.post('/api/submit-attendance/', {              'attendance_code': attendance_code,              'simulated_latitude': '41.5369',              'simulated_longitude': '-8.4239'          })          self.assertEqual(response.json()['status'], 'success')          # 3. Teacher validates attendance          self.client.logout()          self.client.login(username='teacher', password='test123')          # Get submission ID          submissions = self.client.get('/api/get-session-submissions/', {              'class_session_id': self.session.id          }).json()          submission_id = submissions['submissions'][0]['id']          # Validate attendance          response = self.client.post('/api/validate-attendance/', {              'attendance_record_id': submission_id          })          self.assertEqual(response.json()['status'], 'success')          # 4. Verify attendance is marked as present          record = AttendanceRecord.objects.get(id=submission_id)          self.assertTrue(record.is_present)   `

📚 SDK Development
------------------

### Python SDK Template

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python# sysponto_sdk.py  import requests  from typing import Optional, Dict, Any  class SysPontoSDK:      def __init__(self, base_url: str):          self.base_url = base_url.rstrip('/')          self.session = requests.Session()          self.csrf_token: Optional[str] = None      def login(self, username: str, password: str) -> bool:          """Login and establish session"""          # Get CSRF token          response = self.session.get(f"{self.base_url}/login/")          self.csrf_token = self.session.cookies.get('csrftoken')          # Login          login_data = {              'username': username,              'password': password,              'csrfmiddlewaretoken': self.csrf_token          }          response = self.session.post(f"{self.base_url}/login/", data=login_data)          return response.status_code == 302      def generate_attendance_code(self, session_id: str) -> Dict[str, Any]:          """Generate attendance code for a class session"""          return self._post('/api/generate-code/', {              'class_session_id': session_id          })      def submit_attendance(self, code: str, latitude: float = None, longitude: float = None) -> Dict[str, Any]:          """Submit attendance code"""          data = {'attendance_code': code}          if latitude and longitude:              data.update({                  'simulated_latitude': str(latitude),                  'simulated_longitude': str(longitude)              })          return self._post('/api/submit-attendance/', data)      def get_today_classes(self) -> Dict[str, Any]:          """Get today's classes for current user"""          return self._get('/api/student/today-classes/')      def _get(self, endpoint: str, params: Dict = None) -> Dict[str, Any]:          """Make authenticated GET request"""          response = self.session.get(f"{self.base_url}{endpoint}", params=params)          return response.json()      def _post(self, endpoint: str, data: Dict) -> Dict[str, Any]:          """Make authenticated POST request"""          headers = {'X-CSRFToken': self.csrf_token}          response = self.session.post(              f"{self.base_url}{endpoint}",              data=data,              headers=headers          )          return response.json()  # Usage example  sdk = SysPontoSDK('http://localhost:8000')  if sdk.login('student1', 'password123'):      classes = sdk.get_today_classes()      print(f"Today's classes: {classes}")      # Submit attendance      result = sdk.submit_attendance('ABC123', 41.5369, -8.4239)      print(f"Attendance result: {result}")   `

### JavaScript SDK Template

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML``   javascript// sysponto-sdk.js  class SysPontoSDK {      constructor(baseUrl) {          this.baseUrl = baseUrl.replace(/\/$/, '');          this.csrfToken = null;      }      async login(username, password) {          // Get CSRF token          await this._getCSRFToken();          const formData = new FormData();          formData.append('username', username);          formData.append('password', password);          formData.append('csrfmiddlewaretoken', this.csrfToken);          const response = await fetch(`${this.baseUrl}/login/`, {              method: 'POST',              body: formData,              credentials: 'include'          });          return response.ok;      }      async generateAttendanceCode(sessionId) {          return this._post('/api/generate-code/', {              class_session_id: sessionId          });      }      async submitAttendance(code, latitude = null, longitude = null) {          const data = { attendance_code: code };          if (latitude && longitude) {              data.simulated_latitude = latitude.toString();              data.simulated_longitude = longitude.toString();          }          return this._post('/api/submit-attendance/', data);      }      async getTodayClasses() {          return this._get('/api/student/today-classes/');      }      async _get(endpoint, params = {}) {          const url = new URL(`${this.baseUrl}${endpoint}`);          Object.keys(params).forEach(key =>               url.searchParams.append(key, params[key])          );          const response = await fetch(url, {              credentials: 'include'          });          return response.json();      }      async _post(endpoint, data) {          const response = await fetch(`${this.baseUrl}${endpoint}`, {              method: 'POST',              headers: {                  'Content-Type': 'application/x-www-form-urlencoded',                  'X-CSRFToken': this.csrfToken              },              body: new URLSearchParams(data),              credentials: 'include'          });          return response.json();      }      async _getCSRFToken() {          const response = await fetch(`${this.baseUrl}/login/`, {              credentials: 'include'          });          this.csrfToken = this._getCookie('csrftoken');      }      _getCookie(name) {          const value = `; ${document.cookie}`;          const parts = value.split(`; ${name}=`);          if (parts.length === 2) return parts.pop().split(';').shift();      }  }  // Usage  const sdk = new SysPontoSDK('http://localhost:8000');  await sdk.login('student1', 'password123');  const classes = await sdk.getTodayClasses();  console.log('Today\'s classes:', classes);  const result = await sdk.submitAttendance('ABC123', 41.5369, -8.4239);  console.log('Attendance result:', result);   ``

📖 Additional Resources
-----------------------

### Related Documentation

*   [**Authentication Guide**](authentication.md) - Detailed authentication implementation
    
*   [**User Guide**](../user-guide/index.md) - End-user documentation
    
*   [**WebSocket Integration**](../technical/websockets.md) - Real-time features
    
*   [**Deployment Guide**](../technical/deployment.md) - Production setup
    

### External Resources

*   [**Django REST Framework**](https://www.django-rest-framework.org/) - For future API enhancements
    
*   [**Django Channels**](https://channels.readthedocs.io/) - WebSocket implementation
    
*   [**Postman Collection**](https://documenter.getpostman.com/sysponto) - API testing collection