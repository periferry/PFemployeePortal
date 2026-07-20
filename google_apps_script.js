/**
 * Periferry Employee Tracker Backend
 * Google Apps Script Web App
 * 
 * Paste this script into Extensions -> Apps Script of your spreadsheet.
 * Deploy as a Web App: Execute as "Me", Access "Anyone".
 */

function doGet(e) {
  return handleRequest(e);
}

function doPost(e) {
  return handleRequest(e);
}

function handleRequest(e) {
  // CORS setup
  var headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
  };
  
  try {
    initDatabase();
    
    var params = e.parameter;
    var action = params.action;
    
    // Parse post data if applicable
    var postData = null;
    if (e.postData && e.postData.contents) {
      try {
        postData = JSON.parse(e.postData.contents);
        if (!action && postData.action) {
          action = postData.action;
        }
      } catch (err) {
        // Not JSON post data or couldn't parse
      }
    }
    
    if (!action) {
      return jsonResponse({ success: false, error: "No action specified" }, headers);
    }
    
    var sheet = SpreadsheetApp.getActiveSpreadsheet();
    
    switch (action) {
      case "login":
        return loginUser(sheet, postData || params);
        
      case "log_time":
        return logTime(sheet, postData || params);
        
      case "get_user_tasks":
        return getUserTasks(sheet, postData || params);
        
      case "add_tasks":
        return addTasks(sheet, postData);
        
      case "update_task_status":
        return updateTaskStatus(sheet, postData);
        
      case "save_summary":
        return saveSummary(sheet, postData);
        
      case "get_manager_data":
        return getManagerData(sheet);
        
      case "get_all_users":
        return getAllUsers(sheet);
        
      case "manage_users":
        return manageUsers(sheet, postData);
        
      case "save_leaves":
        return saveLeaves(sheet, postData);
        
      case "save_leaves_bulk":
        return saveLeavesBulk(sheet, postData);
        
      case "update_tasks_bulk":
        return updateTasksBulk(sheet, postData);
        
      case "reset_database":
        return resetDatabase(sheet);
        
      default:
        return jsonResponse({ success: false, error: "Unknown action: " + action }, headers);
    }
  } catch (error) {
    return jsonResponse({ success: false, error: error.toString() }, headers);
  }
}

function jsonResponse(data, headers) {
  var output = ContentService.createTextOutput(JSON.stringify(data));
  output.setMimeType(ContentService.MimeType.JSON);
  return output;
}

// ----------------------------------------------------
// DATABASE INITIALIZATION
// ----------------------------------------------------
function initDatabase() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheets = ss.getSheets();
  var sheetNames = sheets.map(function(s) { return s.getName(); });
  
  var required = ["Users", "TimeLogs", "Tasks", "DailySummaries", "Leaves"];
  var allExist = required.every(function(name) {
    return sheetNames.indexOf(name) !== -1;
  });
  
  if (allExist) {
    var usersSheet = ss.getSheetByName("Users");
    if (usersSheet && usersSheet.getLastRow() <= 1) {
      seedDefaultUsers(usersSheet);
    }
    return;
  }
  
  // 1. Users Sheet
  var usersSheet = ss.getSheetByName("Users");
  if (!usersSheet) {
    usersSheet = ss.insertSheet("Users");
    usersSheet.appendRow(["username", "password", "role"]);
  }
  if (usersSheet.getLastRow() <= 1) {
    seedDefaultUsers(usersSheet);
  }
  
  // 2. TimeLogs Sheet
  var logsSheet = ss.getSheetByName("TimeLogs");
  if (!logsSheet) {
    logsSheet = ss.insertSheet("TimeLogs");
    logsSheet.appendRow(["username", "date", "login_time", "logout_time", "total_hours"]);
  }
  
  // 3. Tasks Sheet
  var tasksSheet = ss.getSheetByName("Tasks");
  if (!tasksSheet) {
    tasksSheet = ss.insertSheet("Tasks");
    tasksSheet.appendRow(["task_id", "username", "date", "title", "status", "created_at", "updated_at"]);
  }
  
  // 4. DailySummaries Sheet
  var summariesSheet = ss.getSheetByName("DailySummaries");
  if (!summariesSheet) {
    summariesSheet = ss.insertSheet("DailySummaries");
    summariesSheet.appendRow(["username", "date", "summary", "created_at"]);
  }
  
  // 5. Leaves Sheet
  var leavesSheet = ss.getSheetByName("Leaves");
  if (!leavesSheet) {
    leavesSheet = ss.insertSheet("Leaves");
    leavesSheet.appendRow(["username", "month", "casual_leaves", "medical_leaves"]);
  }
}

function seedDefaultUsers(usersSheet) {
  usersSheet.clearContents();
  usersSheet.getRange(1, 1, 1, 3).setValues([["username", "password", "role"]]);
  var defaults = [
    ["gopika", "gopika@pf", "employee"],
    ["anurag", "anurag@pf", "employee,manager"],
    ["hana", "8376ti.ger3110", "employee,manager,developer"],
    ["soumita", "soumita@pf", "employee"],
    ["nishant", "nishant@pf", "employee,manager"],
    ["sai", "sai@PF", "employee"]
  ];
  for (var i = 0; i < defaults.length; i++) {
    usersSheet.appendRow(defaults[i]);
  }
}

// Helper to get today's date in YYYY-MM-DD local time
function getLocalDateString() {
  var d = new Date();
  var month = "" + (d.getMonth() + 1);
  var day = "" + d.getDate();
  var year = d.getFullYear();
  if (month.length < 2) month = "0" + month;
  if (day.length < 2) day = "0" + day;
  return [year, month, day].join("-");
}

// Helper to get local time string in HH:MM:SS
function getLocalTimeString() {
  var d = new Date();
  var hours = "" + d.getHours();
  var minutes = "" + d.getMinutes();
  var seconds = "" + d.getSeconds();
  if (hours.length < 2) hours = "0" + hours;
  if (minutes.length < 2) minutes = "0" + minutes;
  if (seconds.length < 2) seconds = "0" + seconds;
  return [hours, minutes, seconds].join(":");
}

// ----------------------------------------------------
// CONTROLLERS / ACTIONS
// ----------------------------------------------------

function loginUser(sheet, data) {
  var username = (data.username || "").trim().toLowerCase();
  var password = data.password || "";
  
  var usersSheet = sheet.getSheetByName("Users");
  var rows = usersSheet.getDataRange().getValues();
  
  for (var i = 1; i < rows.length; i++) {
    var u = rows[i][0].toString().trim().toLowerCase();
    var p = rows[i][1].toString();
    var r = rows[i][2].toString();
    
    if (u === username && p === password) {
      // Find today's check-in status
      var status = getAttendanceStatus(sheet, username);
      return jsonResponse({
        success: true,
        user: {
          username: rows[i][0].toString(), // return original casing
          role: r
        },
        attendance: status
      });
    }
  }
  
  return jsonResponse({ success: false, error: "Invalid username or password" });
}

function getAttendanceStatus(sheet, username) {
  var logsSheet = sheet.getSheetByName("TimeLogs");
  var rows = logsSheet.getDataRange().getValues();
  var today = getLocalDateString();
  
  for (var i = rows.length - 1; i >= 1; i--) {
    var user = rows[i][0].toString().trim().toLowerCase();
    var dateVal = rows[i][1];
    
    // Handle spreadsheet date objects or strings
    var dateStr = "";
    if (dateVal instanceof Date) {
      var month = "" + (dateVal.getMonth() + 1);
      var day = "" + dateVal.getDate();
      var year = dateVal.getFullYear();
      if (month.length < 2) month = "0" + month;
      if (day.length < 2) day = "0" + day;
      dateStr = [year, month, day].join("-");
    } else {
      dateStr = dateVal.toString().trim();
    }
    
    if (user === username && dateStr === today) {
      return {
        is_logged_in: rows[i][3].toString() === "", // if logout_time is blank, user is checked-in
        login_time: rows[i][2].toString(),
        logout_time: rows[i][3].toString(),
        total_hours: rows[i][4] ? parseFloat(rows[i][4]) : null
      };
    }
  }
  
  return { is_logged_in: false, login_time: null, logout_time: null, total_hours: 0 };
}

function parseTimeStringToSeconds(val) {
  if (!val) return 0;
  if (val instanceof Date) {
    return val.getHours() * 3600 + val.getMinutes() * 60 + val.getSeconds();
  }
  var str = val.toString().trim();
  if (str.indexOf(":") === -1) return 0;
  
  // Check if it's a full Date string (contains GMT or UTC or is non-numeric at start)
  if (str.indexOf("GMT") !== -1 || str.indexOf("UTC") !== -1 || isNaN(str.charAt(0))) {
    try {
      var d = new Date(str);
      if (!isNaN(d.getTime())) {
        return d.getHours() * 3600 + d.getMinutes() * 60 + d.getSeconds();
      }
    } catch(e) {}
  }
  
  var parts = str.split(":");
  var h = parseInt(parts[0]) || 0;
  var m = parseInt(parts[1]) || 0;
  var s = parseInt(parts[2]) || 0;
  return h * 3600 + m * 60 + s;
}

function logTime(sheet, data) {
  var username = (data.username || "").trim().toLowerCase();
  var type = data.type; // "login" or "logout"
  
  var logsSheet = sheet.getSheetByName("TimeLogs");
  var today = getLocalDateString();
  var nowTime = getLocalTimeString();
  
  var status = getAttendanceStatus(sheet, username);
  
  if (type === "login") {
    if (status.is_logged_in) {
      return jsonResponse({ success: false, error: "Already checked in" });
    }
    logsSheet.appendRow([username, today, nowTime, "", ""]);
    return jsonResponse({ success: true, attendance: { is_logged_in: true, login_time: nowTime, logout_time: "", total_hours: null } });
  } else if (type === "logout") {
    var rows = logsSheet.getDataRange().getValues();
    for (var i = rows.length - 1; i >= 1; i--) {
      var user = rows[i][0].toString().trim().toLowerCase();
      var dateVal = rows[i][1];
      
      var dateStr = "";
      if (dateVal instanceof Date) {
        var month = "" + (dateVal.getMonth() + 1);
        var day = "" + dateVal.getDate();
        var year = dateVal.getFullYear();
        if (month.length < 2) month = "0" + month;
        if (day.length < 2) day = "0" + day;
        dateStr = [year, month, day].join("-");
      } else {
        dateStr = dateVal.toString().trim();
      }
      
      if (user === username && dateStr === today && rows[i][3].toString() === "") {
        var loginStr = rows[i][2].toString();
        
        // Calculate total hours using robust parsing
        var totalHours = 0;
        try {
          var loginSecs = parseTimeStringToSeconds(rows[i][2]);
          var logoutSecs = parseTimeStringToSeconds(nowTime);
          
          var diff = logoutSecs - loginSecs;
          if (diff < 0) diff = 0;
          totalHours = (diff / 3600).toFixed(2);
        } catch (err) {
          totalHours = 0;
        }
        
        // Update logout time and total hours
        logsSheet.getRange(i + 1, 4).setValue(nowTime);
        logsSheet.getRange(i + 1, 5).setValue(totalHours);
        
        return jsonResponse({
          success: true,
          attendance: {
            is_logged_in: false,
            login_time: loginStr,
            logout_time: nowTime,
            total_hours: parseFloat(totalHours)
          }
        });
      }
    }
    return jsonResponse({ success: false, error: "No active check-in session found for today" });
  }
  
  return jsonResponse({ success: false, error: "Invalid log type" });
}

function getUserTasks(sheet, data) {
  var username = (data.username || "").trim().toLowerCase();
  
  var tasksSheet = sheet.getSheetByName("Tasks");
  var rows = tasksSheet.getDataRange().getValues();
  var today = getLocalDateString();
  var userTasks = [];
  
  for (var i = 1; i < rows.length; i++) {
    var user = rows[i][1].toString().trim().toLowerCase();
    var dateVal = rows[i][2];
    
    var dateStr = "";
    if (dateVal instanceof Date) {
      var month = "" + (dateVal.getMonth() + 1);
      var day = "" + dateVal.getDate();
      var year = dateVal.getFullYear();
      if (month.length < 2) month = "0" + month;
      if (day.length < 2) day = "0" + day;
      dateStr = [year, month, day].join("-");
    } else {
      dateStr = dateVal.toString().trim();
    }
    
    // We get all tasks for the user that are active today or created today, or we can just fetch all of them
    // Let's fetch all tasks for this user so they keep their Kanban board history, 
    // but filter to show those created within the last 7 days or all. Let's just return all of them!
    if (user === username) {
      userTasks.push({
        task_id: rows[i][0].toString(),
        username: rows[i][1].toString(),
        date: dateStr,
        title: rows[i][3].toString(),
        status: rows[i][4].toString(),
        created_at: rows[i][5].toString(),
        updated_at: rows[i][6].toString()
      });
    }
  }
  
  // Also get today's summary if submitted
  var summariesSheet = sheet.getSheetByName("DailySummaries");
  var summaryRows = summariesSheet.getDataRange().getValues();
  var todaySummary = "";
  for (var j = 1; j < summaryRows.length; j++) {
    var sUser = summaryRows[j][0].toString().trim().toLowerCase();
    var sDateVal = summaryRows[j][1];
    
    var sDateStr = "";
    if (sDateVal instanceof Date) {
      var sMonth = "" + (sDateVal.getMonth() + 1);
      var sDay = "" + sDateVal.getDate();
      var sYear = sDateVal.getFullYear();
      if (sMonth.length < 2) sMonth = "0" + sMonth;
      if (sDay.length < 2) sDay = "0" + sDay;
      sDateStr = [sYear, sMonth, sDay].join("-");
    } else {
      sDateStr = sDateVal.toString().trim();
    }
    
    if (sUser === username && sDateStr === today) {
      todaySummary = summaryRows[j][2].toString();
      break;
    }
  }
  
  return jsonResponse({ success: true, tasks: userTasks, today_summary: todaySummary });
}

function addTasks(sheet, data) {
  var username = (data.username || "").trim().toLowerCase();
  var tasks = data.tasks || []; // Array of titles
  
  var tasksSheet = sheet.getSheetByName("Tasks");
  var today = getLocalDateString();
  var now = new Date().toISOString();
  
  var added = [];
  for (var i = 0; i < tasks.length; i++) {
    var title = (tasks[i] || "").trim();
    if (title === "") continue;
    
    var taskId = Utilities.getUuid();
    var row = [taskId, username, today, title, "todo", now, now];
    tasksSheet.appendRow(row);
    
    added.push({
      task_id: taskId,
      username: username,
      date: today,
      title: title,
      status: "todo",
      created_at: now,
      updated_at: now
    });
  }
  
  return jsonResponse({ success: true, added: added });
}

function updateTaskStatus(sheet, data) {
  var taskId = data.task_id;
  var status = data.status; // "todo", "inprogress", "completed"
  
  var tasksSheet = sheet.getSheetByName("Tasks");
  var rows = tasksSheet.getDataRange().getValues();
  var now = new Date().toISOString();
  
  for (var i = 1; i < rows.length; i++) {
    if (rows[i][0].toString() === taskId) {
      tasksSheet.getRange(i + 1, 5).setValue(status);
      tasksSheet.getRange(i + 1, 7).setValue(now);
      return jsonResponse({ success: true, task_id: taskId, status: status, updated_at: now });
    }
  }
  
  return jsonResponse({ success: false, error: "Task not found" });
}

function saveSummary(sheet, data) {
  var username = (data.username || "").trim().toLowerCase();
  var summaryText = data.summary || "";
  
  var summariesSheet = sheet.getSheetByName("DailySummaries");
  var rows = summariesSheet.getDataRange().getValues();
  var today = getLocalDateString();
  var now = new Date().toISOString();
  
  // Check if summary already exists for today
  for (var i = 1; i < rows.length; i++) {
    var user = rows[i][0].toString().trim().toLowerCase();
    var dateVal = rows[i][1];
    
    var dateStr = "";
    if (dateVal instanceof Date) {
      var month = "" + (dateVal.getMonth() + 1);
      var day = "" + dateVal.getDate();
      var year = dateVal.getFullYear();
      if (month.length < 2) month = "0" + month;
      if (day.length < 2) day = "0" + day;
      dateStr = [year, month, day].join("-");
    } else {
      dateStr = dateVal.toString().trim();
    }
    
    if (user === username && dateStr === today) {
      summariesSheet.getRange(i + 1, 3).setValue(summaryText);
      summariesSheet.getRange(i + 1, 4).setValue(now);
      return jsonResponse({ success: true, date: today, summary: summaryText, updated: true });
    }
  }
  
  // Insert new summary
  summariesSheet.appendRow([username, today, summaryText, now]);
  return jsonResponse({ success: true, date: today, summary: summaryText, updated: false });
}

function getManagerData(sheet) {
  // Get time logs
  var logsSheet = sheet.getSheetByName("TimeLogs");
  var logsRows = logsSheet.getDataRange().getValues();
  var timeLogs = [];
  
  for (var i = 1; i < logsRows.length; i++) {
    var dateVal = logsRows[i][1];
    var dateStr = "";
    if (dateVal instanceof Date) {
      var month = "" + (dateVal.getMonth() + 1);
      var day = "" + dateVal.getDate();
      var year = dateVal.getFullYear();
      if (month.length < 2) month = "0" + month;
      if (day.length < 2) day = "0" + day;
      dateStr = [year, month, day].join("-");
    } else {
      dateStr = dateVal.toString().trim();
    }
    
    timeLogs.push({
      username: logsRows[i][0].toString(),
      date: dateStr,
      login_time: logsRows[i][2].toString(),
      logout_time: logsRows[i][3].toString(),
      total_hours: logsRows[i][4] ? parseFloat(logsRows[i][4]) : 0
    });
  }
  
  // Get all tasks
  var tasksSheet = sheet.getSheetByName("Tasks");
  var tasksRows = tasksSheet.getDataRange().getValues();
  var tasks = [];
  
  for (var j = 1; j < tasksRows.length; j++) {
    var tDateVal = tasksRows[j][2];
    var tDateStr = "";
    if (tDateVal instanceof Date) {
      var tMonth = "" + (tDateVal.getMonth() + 1);
      var tDay = "" + tDateVal.getDate();
      var tYear = tDateVal.getFullYear();
      if (tMonth.length < 2) tMonth = "0" + tMonth;
      if (tDay.length < 2) tDay = "0" + tDay;
      tDateStr = [tYear, tMonth, tDay].join("-");
    } else {
      tDateStr = tDateVal.toString().trim();
    }
    
    tasks.push({
      task_id: tasksRows[j][0].toString(),
      username: tasksRows[j][1].toString(),
      date: tDateStr,
      title: tasksRows[j][3].toString(),
      status: tasksRows[j][4].toString(),
      created_at: tasksRows[j][5].toString(),
      updated_at: tasksRows[j][6].toString()
    });
  }
  
  // Get all summaries
  var summariesSheet = sheet.getSheetByName("DailySummaries");
  var summariesRows = summariesSheet.getDataRange().getValues();
  var summaries = [];
  
  for (var k = 1; k < summariesRows.length; k++) {
    var sDateVal = summariesRows[k][1];
    var sDateStr = "";
    if (sDateVal instanceof Date) {
      var sMonth = "" + (sDateVal.getMonth() + 1);
      var sDay = "" + sDateVal.getDate();
      var sYear = sDateVal.getFullYear();
      if (sMonth.length < 2) sMonth = "0" + sMonth;
      if (sDay.length < 2) sDay = "0" + sDay;
      sDateStr = [sYear, sMonth, sDay].join("-");
    } else {
      sDateStr = sDateVal.toString().trim();
    }
    
    summaries.push({
      username: summariesRows[k][0].toString(),
      date: sDateStr,
      summary: summariesRows[k][2].toString(),
      created_at: summariesRows[k][3].toString()
    });
  }
  
  // Get all leaves
  var leavesSheet = sheet.getSheetByName("Leaves");
  if (!leavesSheet) {
    leavesSheet = sheet.insertSheet("Leaves");
    leavesSheet.appendRow(["username", "month", "casual_leaves", "medical_leaves"]);
  }
  var leavesRows = leavesSheet.getDataRange().getValues();
  var leaves = [];
  
  for (var m = 1; m < leavesRows.length; m++) {
    leaves.push({
      username: leavesRows[m][0].toString(),
      month: leavesRows[m][1].toString(),
      casual_leaves: parseFloat(leavesRows[m][2]) || 0,
      medical_leaves: parseFloat(leavesRows[m][3]) || 0
    });
  }
  
  return jsonResponse({
    success: true,
    time_logs: timeLogs,
    tasks: tasks,
    summaries: summaries,
    leaves: leaves
  });
}

function getAllUsers(sheet) {
  var usersSheet = sheet.getSheetByName("Users");
  var rows = usersSheet.getDataRange().getValues();
  var users = [];
  
  for (var i = 1; i < rows.length; i++) {
    users.push({
      username: rows[i][0].toString(),
      password: rows[i][1].toString(),
      role: rows[i][2].toString()
    });
  }
  
  return jsonResponse({ success: true, users: users });
}

function manageUsers(sheet, data) {
  var subAction = data.sub_action; // "add", "edit", "delete"
  var usersSheet = sheet.getSheetByName("Users");
  var rows = usersSheet.getDataRange().getValues();
  
  var username = (data.username || "").trim();
  var password = (data.password || "").trim();
  var role = (data.role || "employee").trim();
  
  if (!username) {
    return jsonResponse({ success: false, error: "Username is required" });
  }
  
  var lowerUser = username.toLowerCase();
  
  if (subAction === "add") {
    // Check if user already exists
    for (var i = 1; i < rows.length; i++) {
      if (rows[i][0].toString().trim().toLowerCase() === lowerUser) {
        return jsonResponse({ success: false, error: "User already exists" });
      }
    }
    usersSheet.appendRow([username, password, role]);
    return jsonResponse({ success: true, message: "User added successfully" });
    
  } else if (subAction === "edit") {
    var origUser = data.orig_username || username;
    var lowerOrig = origUser.trim().toLowerCase();
    
    for (var j = 1; j < rows.length; j++) {
      if (rows[j][0].toString().trim().toLowerCase() === lowerOrig) {
        // Update user
        usersSheet.getRange(j + 1, 1).setValue(username);
        usersSheet.getRange(j + 1, 2).setValue(password);
        usersSheet.getRange(j + 1, 3).setValue(role);
        return jsonResponse({ success: true, message: "User updated successfully" });
      }
    }
    return jsonResponse({ success: false, error: "User not found" });
    
  } else if (subAction === "delete") {
    for (var k = 1; k < rows.length; k++) {
      if (rows[k][0].toString().trim().toLowerCase() === lowerUser) {
        usersSheet.deleteRow(k + 1);
        return jsonResponse({ success: true, message: "User deleted successfully" });
      }
    }
    return jsonResponse({ success: false, error: "User not found" });
  }
  
  return jsonResponse({ success: false, error: "Invalid management action" });
}

function saveLeaves(sheet, data) {
  var username = (data.username || "").trim().toLowerCase();
  var month = (data.month || "").trim(); // YYYY-MM
  var casual = parseFloat(data.casual_leaves) || 0;
  var medical = parseFloat(data.medical_leaves) || 0;
  
  if (!username || !month) {
    return jsonResponse({ success: false, error: "Username and month are required" });
  }
  
  var leavesSheet = sheet.getSheetByName("Leaves");
  if (!leavesSheet) {
    leavesSheet = sheet.insertSheet("Leaves");
    leavesSheet.appendRow(["username", "month", "casual_leaves", "medical_leaves"]);
  }
  var rows = leavesSheet.getDataRange().getValues();
  
  for (var i = 1; i < rows.length; i++) {
    var u = rows[i][0].toString().trim().toLowerCase();
    var m = rows[i][1].toString().trim();
    if (u === username && m === month) {
      // Update existing record
      leavesSheet.getRange(i + 1, 3).setValue(casual);
      leavesSheet.getRange(i + 1, 4).setValue(medical);
      return jsonResponse({ success: true, message: "Leaves updated successfully" });
    }
  }
  
  // Append new record
  leavesSheet.appendRow([username, month, casual, medical]);
  return jsonResponse({ success: true, message: "Leaves logged successfully" });
}

function resetDatabase(sheet) {
  // Clear TimeLogs sheet (keeping headers)
  var logsSheet = sheet.getSheetByName("TimeLogs");
  if (logsSheet) {
    logsSheet.clearContents();
    logsSheet.getRange(1, 1, 1, 5).setValues([["username", "date", "login_time", "logout_time", "total_hours"]]);
  }
  
  // Clear Tasks sheet (keeping headers)
  var tasksSheet = sheet.getSheetByName("Tasks");
  if (tasksSheet) {
    tasksSheet.clearContents();
    tasksSheet.getRange(1, 1, 1, 7).setValues([["task_id", "username", "date", "title", "status", "created_at", "updated_at"]]);
  }
  
  // Clear DailySummaries sheet (keeping headers)
  var summariesSheet = sheet.getSheetByName("DailySummaries");
  if (summariesSheet) {
    summariesSheet.clearContents();
    summariesSheet.getRange(1, 1, 1, 4).setValues([["username", "date", "summary", "created_at"]]);
  }
  
  // Clear Leaves sheet (keeping headers)
  var leavesSheet = sheet.getSheetByName("Leaves");
  if (leavesSheet) {
    leavesSheet.clearContents();
    leavesSheet.getRange(1, 1, 1, 4).setValues([["username", "month", "casual_leaves", "medical_leaves"]]);
  }
  
  return jsonResponse({ success: true, message: "Database reset completed successfully." });
}

function saveLeavesBulk(sheet, data) {
  var updates = data.updates || [];
  var leavesSheet = sheet.getSheetByName("Leaves");
  if (!leavesSheet) {
    leavesSheet = sheet.insertSheet("Leaves");
    leavesSheet.appendRow(["username", "month", "casual_leaves", "medical_leaves"]);
  }
  var rows = leavesSheet.getDataRange().getValues();
  
  var keyToRowIndex = {};
  for (var i = 1; i < rows.length; i++) {
    var u = rows[i][0].toString().trim().toLowerCase();
    var m = rows[i][1].toString().trim();
    keyToRowIndex[u + "_" + m] = i + 1;
  }
  
  for (var j = 0; j < updates.length; j++) {
    var item = updates[j];
    var username = (item.username || "").trim().toLowerCase();
    var month = (item.month || "").trim();
    var casual = parseFloat(item.casual_leaves) || 0;
    var medical = parseFloat(item.medical_leaves) || 0;
    
    if (!username || !month) continue;
    
    var key = username + "_" + month;
    if (keyToRowIndex[key]) {
      var rowIndex = keyToRowIndex[key];
      leavesSheet.getRange(rowIndex, 3).setValue(casual);
      leavesSheet.getRange(rowIndex, 4).setValue(medical);
    } else {
      leavesSheet.appendRow([username, month, casual, medical]);
      rows = leavesSheet.getDataRange().getValues();
      keyToRowIndex[key] = rows.length;
    }
  }
  
  return jsonResponse({ success: true, message: "Bulk leaves saved successfully" });
}

function updateTasksBulk(sheet, data) {
  var updates = data.updates || [];
  var tasksSheet = sheet.getSheetByName("Tasks");
  var rows = tasksSheet.getDataRange().getValues();
  
  var idToRowIndex = {};
  for (var i = 1; i < rows.length; i++) {
    var tid = rows[i][0].toString().trim();
    idToRowIndex[tid] = i + 1;
  }
  
  var nowStr = getLocalTimeString() + " " + getLocalDateString();
  
  for (var j = 0; j < updates.length; j++) {
    var item = updates[j];
    var tid = (item.task_id || "").toString().trim();
    var newStatus = (item.status || "").toString().trim();
    
    if (idToRowIndex[tid]) {
      var rowIndex = idToRowIndex[tid];
      tasksSheet.getRange(rowIndex, 5).setValue(newStatus);
      tasksSheet.getRange(rowIndex, 7).setValue(nowStr);
    }
  }
  
  return jsonResponse({ success: true, message: "Bulk task status updated successfully" });
}
