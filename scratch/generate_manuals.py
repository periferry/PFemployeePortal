import os
import subprocess

current_dir = r"c:\D Drive\Task Tracking"
dest_dir = os.path.join(current_dir, "manual_assets")

# HTML Content for Employee Manual
employee_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>PeriFerry Employee Portal - User Manual</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    @page {
      size: A4;
      margin: 20mm;
    }
    
    body {
      font-family: 'Poppins', sans-serif;
      color: #1e293b;
      background-color: #ffffff;
      margin: 0;
      padding: 0;
      line-height: 1.6;
      font-size: 13px;
    }
    
    .page-break {
      page-break-before: always;
      break-before: page;
    }
    
    /* Cover Page styling */
    .cover-page {
      height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 60px;
      box-sizing: border-box;
      background: linear-gradient(135deg, #070c1e 0%, #1f3c7e 100%);
      color: white;
      page-break-after: always;
      break-after: page;
    }
    
    .cover-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .brand-logo-text {
      font-size: 26px;
      font-weight: 800;
      letter-spacing: 0.5px;
      color: #ffffff;
    }
    
    .brand-tagline {
      font-size: 10px;
      font-weight: 600;
      color: #c8469e;
      text-transform: uppercase;
      letter-spacing: 2px;
    }
    
    .cover-body {
      margin-top: auto;
      margin-bottom: auto;
    }
    
    .cover-body h1 {
      font-size: 40px;
      font-weight: 800;
      line-height: 1.15;
      margin: 0;
      color: #ffffff;
    }
    
    .cover-body h1 span {
      background: linear-gradient(135deg, #c8469e 0%, #5046b6 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    
    .cover-body p {
      font-size: 16px;
      color: #94a3b8;
      margin-top: 15px;
      max-width: 500px;
      font-weight: 300;
    }
    
    .cover-footer {
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      padding-top: 25px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11px;
      color: #64748b;
      font-weight: 500;
    }
    
    /* Inner Page Elements */
    .header-bar {
      border-bottom: 2px solid #5046b6;
      padding-bottom: 8px;
      margin-bottom: 25px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .header-bar h2 {
      font-size: 13px;
      font-weight: 700;
      color: #1f3c7e;
      margin: 0;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    
    .header-bar span {
      font-size: 10px;
      color: #64748b;
      font-weight: 500;
    }
    
    h2.section-title {
      font-size: 20px;
      font-weight: 800;
      color: #1f3c7e;
      margin-top: 0;
      margin-bottom: 18px;
      display: flex;
      align-items: center;
    }
    
    h2.section-title::after {
      content: '';
      flex-grow: 1;
      height: 1px;
      background: #e2e8f0;
      margin-left: 15px;
    }
    
    h3.subsection-title {
      font-size: 14px;
      font-weight: 700;
      color: #5046b6;
      margin-top: 22px;
      margin-bottom: 10px;
    }
    
    p {
      margin-top: 0;
      margin-bottom: 12px;
      color: #334155;
    }
    
    /* Table of Contents */
    .index-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 25px;
    }
    
    .index-table td {
      padding: 10px 0;
      border-bottom: 1px dashed #cbd5e1;
      font-size: 13px;
    }
    
    .index-table .section-num {
      font-weight: 700;
      color: #5046b6;
      width: 30px;
    }
    
    .index-table .section-name {
      font-weight: 500;
      color: #1e293b;
    }
    
    .index-table .page-num {
      text-align: right;
      font-weight: 700;
      color: #64748b;
    }
    
    /* Callouts */
    .callout {
      background-color: #f8fafc;
      border-left: 4px solid #5046b6;
      padding: 12px 18px;
      border-radius: 0 12px 12px 0;
      margin: 18px 0;
    }
    
    .callout-title {
      font-weight: 700;
      color: #1f3c7e;
      margin-bottom: 4px;
      font-size: 12px;
    }
    
    .callout-content {
      font-size: 12px;
      color: #475569;
      margin: 0;
    }
    
    /* Screenshots */
    .app-screenshot {
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      padding: 8px;
      background-color: #f8fafc;
      margin: 20px 0;
      text-align: center;
    }
    
    .app-screenshot img {
      max-width: 100%;
      max-height: 250px;
      border-radius: 8px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.04);
      object-fit: contain;
    }
    
    .app-screenshot-caption {
      font-size: 10px;
      color: #64748b;
      margin-top: 8px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    
    /* Steps list */
    .steps-list {
      counter-reset: steps-counter;
      list-style-type: none;
      padding-left: 0;
      margin: 15px 0;
    }
    
    .steps-list li {
      position: relative;
      padding-left: 35px;
      margin-bottom: 15px;
      font-size: 13px;
    }
    
    .steps-list li::before {
      counter-increment: steps-counter;
      content: counter(steps-counter);
      position: absolute;
      left: 0;
      top: 1px;
      background: linear-gradient(135deg, #1f3c7e 0%, #5046b6 100%);
      color: white;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 10px;
      font-weight: 700;
    }
  </style>
</head>
<body>

  <!-- COVER PAGE -->
  <div class="cover-page">
    <div class="cover-header">
      <div class="brand-logo-text">PeriFerry</div>
      <div class="brand-tagline">Portal Manual</div>
    </div>
    <div class="cover-body">
      <h1>Employee Portal<br><span>User Manual</span></h1>
      <p>A comprehensive step-by-step workflow guide to logging attendance, submitting daily planners, and syncing Kanban task boards.</p>
    </div>
    <div class="cover-footer">
      <div>PeriFerry Employee Portal &bull; Version 2.0</div>
      <div>Published July 2026</div>
    </div>
  </div>

  <!-- PAGE 2: TABLE OF CONTENTS -->
  <div class="header-bar">
    <h2>Table of Contents</h2>
    <span>Index</span>
  </div>
  
  <h2 class="section-title">Manual Index</h2>
  <p>Use the index below to navigate the portal features, setup installation steps, and daily employee reporting routines.</p>
  
  <table class="index-table">
    <tr>
      <td class="section-num">1.</td>
      <td class="section-name">Introduction to PeriFerry Employee Portal</td>
      <td class="page-num">Page 3</td>
    </tr>
    <tr>
      <td class="section-num">2.</td>
      <td class="section-name">One-Click Installation Wizard Guide</td>
      <td class="page-num">Page 4</td>
    </tr>
    <tr>
      <td class="section-num">3.</td>
      <td class="section-name">Daily Attendance: Login & Welcome Console</td>
      <td class="page-num">Page 5</td>
    </tr>
    <tr>
      <td class="section-num">4.</td>
      <td class="section-name">Planner and Kanban Tasks Workspace</td>
      <td class="page-num">Page 6</td>
    </tr>
    <tr>
      <td class="section-num">5.</td>
      <td class="section-name">Local Changes & Database Synchronization</td>
      <td class="page-num">Page 7</td>
    </tr>
    <tr>
      <td class="section-num">6.</td>
      <td class="section-name">Troubleshooting & Session Guidelines</td>
      <td class="page-num">Page 8</td>
    </tr>
  </table>

  <div class="callout" style="margin-top: 50px;">
    <div class="callout-title">Important Notice for Employees</div>
    <p class="callout-content">Always check in immediately upon starting work. All daily tasks must be submitted and synced to guarantee correct working hour tracking. Carry forward leaves accumulate at a rate of 1.0 day/month.</p>
  </div>

  <!-- PAGE 3: INTRODUCTION -->
  <div class="page-break"></div>
  <div class="header-bar">
    <h2>1. Introduction</h2>
    <span>Employee Guide</span>
  </div>
  
  <h2 class="section-title">Introduction to the Portal</h2>
  <p>The <strong>PeriFerry Employee Portal</strong> is a standalone, desktop application designed to track tasks, organize projects, and record attendance. The portal coordinates tasks using a local-first interface, linking directly to a centralized spreadsheet backend via Google Apps Script.</p>
  
  <h3 class="subsection-title">Key Core Capabilities</h3>
  <p>Our portal helps you coordinate your day-to-day workflow with maximum efficiency:</p>
  <ul style="padding-left: 20px; margin: 10px 0;">
    <li style="margin-bottom: 8px;"><strong>Attendance Log-In & Log-Out</strong>: Precise record of check-in and check-out timestamps, showing active durations.</li>
    <li style="margin-bottom: 8px;"><strong>Daily Task Planner</strong>: Input task targets at check-in that automatically populate your Kanban columns.</li>
    <li style="margin-bottom: 8px;"><strong>Unsaved local buffer</strong>: Move, complete, and add tasks without waiting for network spinners. Everything updates instantly!</li>
    <li style="margin-bottom: 8px;"><strong>Bulk Sync Action</strong>: Sync all task shifts and updates in a single click, saving bandwidth and system speed.</li>
  </ul>

  <div class="app-screenshot">
    <img src="manual_assets/media__1783335724533.png" alt="Portal Selection Page">
    <div class="app-screenshot-caption">Figure 1.1: Multi-role Portal dashboard entry screen</div>
  </div>

  <!-- PAGE 4: INSTALLATION -->
  <div class="page-break"></div>
  <div class="header-bar">
    <h2>2. Installation Wizard</h2>
    <span>Employee Guide</span>
  </div>
  
  <h2 class="section-title">One-Click Installation Guide</h2>
  <p>To deploy the portal on your local system, you no longer need complex command prompts, environment setup, or copy-pasting Google Apps Script URL configuration files.</p>
  
  <h3 class="subsection-title">Installing the Application</h3>
  <p>Follow these quick setup steps to prepare your portal workspace:</p>
  
  <ul class="steps-list">
    <li>Download the standalone installer file: <strong>PeriFerry Employee Portal Setup.exe</strong>.</li>
    <li>Double-click the setup file to launch the installation wizard. A beautiful setup console decorated with the official company logo will appear.</li>
    <li>Click the primary <strong>"Install Now"</strong> button. The wizard automatically:
      <ul style="padding-left: 20px; margin: 5px 0;">
        <li>Copies binary assets to your user profile (<code>%LocalAppData%\PeriFerry Employee Portal</code>).</li>
        <li>Bypasses standard administrator prompt restrictions (no admin privileges required).</li>
        <li>Pre-configures the spreadsheet connection URL so you never have to input it manually.</li>
        <li>Injects launch shortcuts onto your <strong>Desktop</strong> and Windows <strong>Start Menu</strong>.</li>
      </ul>
    </li>
    <li>Once setup is complete, double-click the desktop shortcut to launch the app!</li>
  </ul>

  <div class="app-screenshot">
    <img src="manual_assets/media__1783332305688.png" alt="Login screen">
    <div class="app-screenshot-caption">Figure 2.1: App Login Portal entry screen</div>
  </div>

  <!-- PAGE 5: DAILY ATTENDANCE ROUTINE -->
  <div class="page-break"></div>
  <div class="header-bar">
    <h2>3. Daily Attendance</h2>
    <span>Employee Guide</span>
  </div>
  
  <h2 class="section-title">Check-in / Check-out Routine</h2>
  <p>The daily workflow routine begins and ends with check-in and check-out logs. Entering incorrect check-in steps will lead to inaccurate duration statistics on your working sheets.</p>
  
  <h3 class="subsection-title">Logging Check-In</h3>
  <ul class="steps-list">
    <li>Open the app, write your unique employee credentials, and click <strong>"Sign In"</strong>.</li>
    <li>In the top right banner, click the blue <strong>"Log In"</strong> button.</li>
    <li>The portal shifts focus to the <strong>"Plan Your Day"</strong> inputs. Enter the sub-task descriptors you intend to work on today, clicking <strong>"Add Task Row"</strong> to append entries.</li>
    <li>Click <strong>"Submit Daily Plan"</strong>. This logs your starting check-in timestamp and loads the task board.</li>
  </ul>
  
  <h3 class="subsection-title">Logging Check-Out</h3>
  <ul class="steps-list">
    <li>Click the red <strong>"Log Out"</strong> button in the Welcome bar.</li>
    <li>The Daily Summary box will automatically compose a description list of all tasks you completed during the shift.</li>
    <li>Adjust the summary if necessary, then click <strong>"Confirm Check-Out"</strong>. Your check-out timestamp is saved, session timer ceases, and task cards clear.</li>
  </ul>

  <div class="app-screenshot">
    <img src="manual_assets/media__1783339855607.png" alt="Welcome banner and Logger button">
    <div class="app-screenshot-caption">Figure 3.1: Welcome banner containing status timers and attendance controls</div>
  </div>

  <!-- PAGE 6: PLANNER & KANBAN TASKS WORKSPACE -->
  <div class="page-break"></div>
  <div class="header-bar">
    <h2>4. Kanban Tasks Workspace</h2>
    <span>Employee Guide</span>
  </div>
  
  <h2 class="section-title">Managing Your Kanban Board</h2>
  <p>All tasks submitted during check-in automatically populate the <strong>"To Do"</strong> column of your board. You can control, organize, and transition these tasks throughout the day.</p>
  
  <h3 class="subsection-title">Kanban Column Roles</h3>
  <ul style="padding-left: 20px; margin: 10px 0;">
    <li style="margin-bottom: 8px;"><strong>To Do</strong>: Tasks planned for the day, awaiting execution.</li>
    <li style="margin-bottom: 8px;"><strong>In Progress</strong>: Tasks currently being processed. You should shift tasks here to represent active focus.</li>
    <li style="margin-bottom: 8px;"><strong>Completed</strong>: Finished tasks. Items placed here are automatically compiled into your daily summary list during check-out.</li>
  </ul>
  
  <h3 class="subsection-title">Transitioning Tasks Locally</h3>
  <p>Instead of lagging system performance with slow network overlays, task shifts are updated instantly in the local UI buffer:</p>
  <ul class="steps-list">
    <li>To begin a task, click the <strong>"Start Task"</strong> button. The card moves instantly to "In Progress".</li>
    <li>To complete a task, click the green <strong>"Complete"</strong> button. The card moves instantly to "Completed".</li>
    <li>To move a task back, click the <strong>"Move Back"</strong> button.</li>
  </ul>

  <div class="app-screenshot">
    <img src="manual_assets/media__1783340172079.png" alt="Kanban board columns">
    <div class="app-screenshot-caption">Figure 4.1: Kanban Board columns with action controllers</div>
  </div>

  <!-- PAGE 7: LOCAL CHANGES & SYNCHRONIZATION -->
  <div class="page-break"></div>
  <div class="header-bar">
    <h2>5. Local Changes & Sync</h2>
    <span>Employee Guide</span>
  </div>
  
  <h2 class="section-title">Synchronizing Workspace Changes</h2>
  <p>To offer a fluid, responsive user experience, the portal uses a **Local-First Buffer** for Kanban actions. Changes are stored locally in application memory, avoiding network lag while you work.</p>
  
  <h3 class="subsection-title">The Unsaved Sync Indicator</h3>
  <p>When you modify tasks (e.g., move a card, complete an item), a blue indicator button appears in the top-right corner of the Kanban container:</p>
  <div class="callout">
    <div class="callout-title">Sync Changes (X) Button</div>
    <p class="callout-content">The button shows the count of changes (X) currently queued in the local buffer waiting to write to the server database.</p>
  </div>
  
  <h3 class="subsection-title">Syncing Your Changes</h3>
  <ul class="steps-list">
    <li>Organize, drag, or complete your tasks locally as needed.</li>
    <li>Once you are ready to write these updates to the server, click the blue <strong>"Sync Changes (X)"</strong> button.</li>
    <li>A loader will display briefly as the app packs all moves into a single, highly optimized batch request.</li>
    <li>A "Task board changes synced successfully!" alert confirms that your progress has been safely logged. The button will disappear.</li>
  </ul>

  <div class="callout" style="border-left-color: #c8469e;">
    <div class="callout-title" style="color: #c8469e;">Crucial Sync Rule</div>
    <p class="callout-content">Always click the "Sync Changes" button before closing the application or checking out. Unsynced changes will not register on sheets database reports!</p>
  </div>

  <!-- PAGE 8: TROUBLESHOOTING & FAQs -->
  <div class="page-break"></div>
  <div class="header-bar">
    <h2>6. Troubleshooting & FAQs</h2>
    <span>Employee Guide</span>
  </div>
  
  <h2 class="section-title">Troubleshooting Guidelines</h2>
  <p>Here are standard guidelines and solutions for common questions regarding application behavior.</p>
  
  <h3 class="subsection-title">Frequently Asked Questions</h3>
  
  <p><strong>Q: Why does my check-in time display Na:Na:Na or missing values?</strong><br>
  A: This occurs due to cached browser session issues. To resolve it, sign out using the logout icon in the top header panel, close the application, reopen it, and sign back in to start a clean session.</p>
  
  <p><strong>Q: What happens if I forget to click "Sync Changes" before closing the app?</strong><br>
  A: Unsynced moves will remain in the local app cache. When you log back in on the same machine, the changes will load, but the spreadsheet database will not show them until you click the Sync button.</p>
  
  <p><strong>Q: How do my leaves accrue?</strong><br>
  A: Casual leaves carry forward to the next month and accumulate at a rate of 1.0 day per month (accrual starts fresh from July 2026). Medical leaves accrue at 1.0 day/month but do not carry forward.</p>

  <div class="callout" style="border-left-color: #64748b;">
    <div class="callout-title" style="color: #475569;">Tech Support</div>
    <p class="callout-content">For persistent issues, spreadsheet link overrides, or credential changes, please contact your System Developer or HR Manager.</p>
  </div>

</body>
</html>
"""

# HTML Content for Manager Manual
manager_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>PeriFerry Control Panel - Manager & HR Manual</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    @page {
      size: A4;
      margin: 20mm;
    }
    
    body {
      font-family: 'Poppins', sans-serif;
      color: #1e293b;
      background-color: #ffffff;
      margin: 0;
      padding: 0;
      line-height: 1.6;
      font-size: 13px;
    }
    
    .page-break {
      page-break-before: always;
      break-before: page;
    }
    
    /* Cover Page styling */
    .cover-page {
      height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 60px;
      box-sizing: border-box;
      background: linear-gradient(135deg, #070c1e 0%, #5046b6 100%);
      color: white;
      page-break-after: always;
      break-after: page;
    }
    
    .cover-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .brand-logo-text {
      font-size: 26px;
      font-weight: 800;
      letter-spacing: 0.5px;
      color: #ffffff;
    }
    
    .brand-tagline {
      font-size: 10px;
      font-weight: 600;
      color: #c8469e;
      text-transform: uppercase;
      letter-spacing: 2px;
    }
    
    .cover-body {
      margin-top: auto;
      margin-bottom: auto;
    }
    
    .cover-body h1 {
      font-size: 40px;
      font-weight: 800;
      line-height: 1.15;
      margin: 0;
      color: #ffffff;
    }
    
    .cover-body h1 span {
      background: linear-gradient(135deg, #c8469e 0%, #1f3c7e 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    
    .cover-body p {
      font-size: 16px;
      color: #94a3b8;
      margin-top: 15px;
      max-width: 500px;
      font-weight: 300;
    }
    
    .cover-footer {
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      padding-top: 25px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11px;
      color: #64748b;
      font-weight: 500;
    }
    
    /* Inner Page Elements */
    .header-bar {
      border-bottom: 2px solid #c8469e;
      padding-bottom: 8px;
      margin-bottom: 25px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .header-bar h2 {
      font-size: 13px;
      font-weight: 700;
      color: #5046b6;
      margin: 0;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    
    .header-bar span {
      font-size: 10px;
      color: #64748b;
      font-weight: 500;
    }
    
    h2.section-title {
      font-size: 20px;
      font-weight: 800;
      color: #5046b6;
      margin-top: 0;
      margin-bottom: 18px;
      display: flex;
      align-items: center;
    }
    
    h2.section-title::after {
      content: '';
      flex-grow: 1;
      height: 1px;
      background: #e2e8f0;
      margin-left: 15px;
    }
    
    h3.subsection-title {
      font-size: 14px;
      font-weight: 700;
      color: #1f3c7e;
      margin-top: 22px;
      margin-bottom: 10px;
    }
    
    p {
      margin-top: 0;
      margin-bottom: 12px;
      color: #334155;
    }
    
    /* Table of Contents */
    .index-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 25px;
    }
    
    .index-table td {
      padding: 10px 0;
      border-bottom: 1px dashed #cbd5e1;
      font-size: 13px;
    }
    
    .index-table .section-num {
      font-weight: 700;
      color: #c8469e;
      width: 30px;
    }
    
    .index-table .section-name {
      font-weight: 500;
      color: #1e293b;
    }
    
    .index-table .page-num {
      text-align: right;
      font-weight: 700;
      color: #64748b;
    }
    
    /* Callouts */
    .callout {
      background-color: #f8fafc;
      border-left: 4px solid #c8469e;
      padding: 12px 18px;
      border-radius: 0 12px 12px 0;
      margin: 18px 0;
    }
    
    .callout-title {
      font-weight: 700;
      color: #5046b6;
      margin-bottom: 4px;
      font-size: 12px;
    }
    
    .callout-content {
      font-size: 12px;
      color: #475569;
      margin: 0;
    }
    
    /* Screenshots */
    .app-screenshot {
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      padding: 8px;
      background-color: #f8fafc;
      margin: 20px 0;
      text-align: center;
    }
    
    .app-screenshot img {
      max-width: 100%;
      max-height: 250px;
      border-radius: 8px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.04);
      object-fit: contain;
    }
    
    .app-screenshot-caption {
      font-size: 10px;
      color: #64748b;
      margin-top: 8px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    
    /* Steps list */
    .steps-list {
      counter-reset: steps-counter;
      list-style-type: none;
      padding-left: 0;
      margin: 15px 0;
    }
    
    .steps-list li {
      position: relative;
      padding-left: 35px;
      margin-bottom: 15px;
      font-size: 13px;
    }
    
    .steps-list li::before {
      counter-increment: steps-counter;
      content: counter(steps-counter);
      position: absolute;
      left: 0;
      top: 1px;
      background: linear-gradient(135deg, #c8469e 0%, #5046b6 100%);
      color: white;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 10px;
      font-weight: 700;
    }
  </style>
</head>
<body>

  <!-- COVER PAGE -->
  <div class="cover-page">
    <div class="cover-header">
      <div class="brand-logo-text">PeriFerry</div>
      <div class="brand-tagline">Portal Manual</div>
    </div>
    <div class="cover-body">
      <h1>Control Panel<br><span>Manager & HR Guide</span></h1>
      <p>A reference guide to analyzing employee hours, inspecting Kanban boards, administering leaves, and managing database credentials.</p>
    </div>
    <div class="cover-footer">
      <div>PeriFerry Manager Portal &bull; Version 2.0</div>
      <div>Published July 2026</div>
    </div>
  </div>

  <!-- PAGE 2: TABLE OF CONTENTS -->
  <div class="header-bar">
    <h2>Table of Contents</h2>
    <span>Index</span>
  </div>
  
  <h2 class="section-title">Manual Index</h2>
  <p>Use the index below to navigate the HR statistics, Kanban monitoring systems, leaves editor, and developer administration parameters.</p>
  
  <table class="index-table">
    <tr>
      <td class="section-num">1.</td>
      <td class="section-name">Dashboard Navigation & Multi-Role Access</td>
      <td class="page-num">Page 3</td>
    </tr>
    <tr>
      <td class="section-num">2.</td>
      <td class="section-name">Attendance Logs & Weekly Hours Chart</td>
      <td class="page-num">Page 4</td>
    </tr>
    <tr>
      <td class="section-num">3.</td>
      <td class="section-name">Monitoring Employee Kanban Boards</td>
      <td class="page-num">Page 5</td>
    </tr>
    <tr>
      <td class="section-num">4.</td>
      <td class="section-name">HR Leaves Tracker (Local Batch-saving)</td>
      <td class="page-num">Page 6</td>
    </tr>
    <tr>
      <td class="section-num">5.</td>
      <td class="section-name">Developer Panel: User Credentials & Database Reset</td>
      <td class="page-num">Page 7</td>
    </tr>
    <tr>
      <td class="section-num">6.</td>
      <td class="section-name">Database Setup & Backend Optimization</td>
      <td class="page-num">Page 8</td>
    </tr>
  </table>

  <div class="callout" style="margin-top: 50px;">
    <div class="callout-title">Database Performance Optimization</div>
    <p class="callout-content">The backend Apps Script functions are optimized to read and evaluate sheet availability in a single roundtrip. Always deploy the portal script as a "New Web App Version" to preserve efficiency.</p>
  </div>

  <!-- PAGE 3: DASHBOARD NAVIGATION -->
  <div class="page-break"></div>
  <div class="header-bar">
    <h2>1. Dashboard Entry</h2>
    <span>Manager & HR Guide</span>
  </div>
  
  <h2 class="section-title">Multi-Role Selection</h2>
  <p>Managers and developers can access multiple portals depending on their assigned access roles. Authorized accounts (e.g. <code>anurag</code> or <code>hana</code>) are presented with the selector dashboard on login.</p>
  
  <h3 class="subsection-title">Dashboard Entry Options</h3>
  <ul style="padding-left: 20px; margin: 10px 0;">
    <li style="margin-bottom: 8px;"><strong>Employee Portal</strong>: Allows managers to check in and manage their own task lists just like normal employees.</li>
    <li style="margin-bottom: 8px;"><strong>Manager / HR Portal</strong>: Access analytics charts, attendance logs, and leaves tracker.</li>
    <li style="margin-bottom: 8px;"><strong>Developer / Admin Panel</strong>: Modify user lists, update passwords, override URLs, and reset data.</li>
  </ul>
  
  <h3 class="subsection-title">Security & Session Isolation</h3>
  <p>To avoid session leakage, the portal includes the following security rules:</p>
  <ul class="steps-list">
    <li><strong>Auto-Purge DOM Elements</strong>: Switching dashboards or logging out completely wipes out all cached task cards and user details from the DOM.</li>
    <li><strong>Access Guards</strong>: Single-role users (e.g. Gopika) can never access the role selection dashboard. The "Switch Dashboard" button is hidden from their view entirely.</li>
  </ul>

  <div class="app-screenshot">
    <img src="manual_assets/media__1783335724533.png" alt="Dashboard Selector">
    <div class="app-screenshot-caption">Figure 1.1: Branded dashboard selector window</div>
  </div>

  <!-- PAGE 4: ATTENDANCE & ANALYTICS -->
  <div class="page-break"></div>
  <div class="header-bar">
    <h2>2. Attendance & Stats</h2>
    <span>Manager & HR Guide</span>
  </div>
  
  <h2 class="section-title">HR Attendance Analytics</h2>
  <p>The manager interface displays live operational statistics of the workforce. When employees log in or out, their details update dynamically in the spreadsheet backend database.</p>
  
  <h3 class="subsection-title">Live Attendance Indicators</h3>
  <p>The system displays attendance records categorized with color-coded status badges:</p>
  <ul style="padding-left: 20px; margin: 10px 0;">
    <li style="margin-bottom: 8px;"><strong>Active Session (Green)</strong>: Employees currently logged-in. The session indicator pulses to represent an active workday.</li>
    <li style="margin-bottom: 8px;"><strong>Offline/Log-out (Slate)</strong>: Employees who have checked-out. Their logout time and total hours logged are visible.</li>
    <li style="margin-bottom: 8px;"><strong>Absent (Bordered Slate)</strong>: Employees who haven't logged any attendance for the selected date.</li>
  </ul>

  <h3 class="subsection-title">Weekly Working Hours Chart</h3>
  <p>At the top of the analytics dashboard, a bar chart summarizes the total working hours accumulated by each employee over the last 7 days. This helps HR detect workload imbalances instantly.</p>

  <div class="app-screenshot">
    <img src="manual_assets/media__1783340388480.png" alt="Manager Stats">
    <div class="app-screenshot-caption">Figure 2.1: HR Dashboard showing live stats, attendance records, and charts</div>
  </div>

  <!-- PAGE 5: KANBAN MONITORING -->
  <div class="page-break"></div>
  <div class="header-bar">
    <h2>3. Kanban Monitoring</h2>
    <span>Manager & HR Guide</span>
  </div>
  
  <h2 class="section-title">Monitoring Task Progress</h2>
  <p>Managers can inspect any employee's live task board to review progress, verify task completion, and audit project statuses.</p>
  
  <h3 class="subsection-title">How to inspect a Kanban Board</h3>
  <ul class="steps-list">
    <li>Click on the <strong>"Employee Kanban Boards"</strong> tab on the manager dashboard.</li>
    <li>Use the dropdown menu <strong>"Select Employee"</strong> to choose the specific worker.</li>
    <li>The interface instantly renders their daily board columns: <strong>To Do</strong>, <strong>In Progress</strong>, and <strong>Completed</strong>.</li>
    <li>Review the task descriptions. Card colors and layouts indicate their respective columns.</li>
  </ul>

  <div class="callout" style="border-left-color: #5046b6;">
    <div class="callout-title" style="color: #5046b6;">Sync Audit Note</div>
    <p class="callout-content">If an employee reports that they have completed tasks, but they do not show in the manager's board view, verify that the employee has clicked the blue "Sync Changes" button on their client terminal.</p>
  </div>

  <div class="app-screenshot">
    <img src="manual_assets/media__1783340172079.png" alt="Kanban Audit">
    <div class="app-screenshot-caption">Figure 3.1: Kanban audit workspace for task progress inspection</div>
  </div>

  <!-- PAGE 6: LEAVES MANAGEMENT -->
  <div class="page-break"></div>
  <div class="header-bar">
    <h2>4. Leaves Management</h2>
    <span>Manager & HR Guide</span>
  </div>
  
  <h2 class="section-title">HR Leaves Tracker</h2>
  <p>The manager can adjust casual and medical leaves taken per month for each employee. The interface operates locally to prevent annoying load screens on every click.</p>
  
  <h3 class="subsection-title">Leaves Accrual & Carry Forward Rules</h3>
  <ul style="padding-left: 20px; margin: 10px 0;">
    <li style="margin-bottom: 8px;"><strong>Casual Leaves (CL)</strong>: Accrue at a rate of <strong>1.0 day per month</strong> (accrual started fresh from July 2026). Unused CL is carried forward to subsequent months.</li>
    <li style="margin-bottom: 8px;"><strong>Medical Leaves (ML)</strong>: Accrue at a rate of <strong>1.0 day per month</strong>. Unused ML is forfeited at month-end and does not carry forward.</li>
  </ul>

  <h3 class="subsection-title">How to Modify and Sync Leaves</h3>
  <ul class="steps-list">
    <li>Select the target month using the <strong>"Select Month"</strong> input.</li>
    <li>Locate the target employee. Click the <strong>"+"</strong> or <strong>"-"</strong> buttons to adjust taken leaves in half-day increments. The values and remaining balances recalculate instantly in the UI.</li>
    <li>A blue <strong>"Save Leave Changes (X)"</strong> button will appear, tracking the number of modified records.</li>
    <li>Click the button once you are done making changes. This sends a single batch update to Google Sheets, updating all records instantly!</li>
  </ul>

  <div class="app-screenshot">
    <img src="manual_assets/media__1783591797801.png" alt="Leaves Tracker Grid">
    <div class="app-screenshot-caption">Figure 4.1: Leaves grid showing buttons, accrued logs, and sync status</div>
  </div>

  <!-- PAGE 7: DEVELOPER PANEL -->
  <div class="page-break"></div>
  <div class="header-bar">
    <h2>5. Developer Admin</h2>
    <span>Manager & HR Guide</span>
  </div>
  
  <h2 class="section-title">Developer & Admin Control Panel</h2>
  <p>The <strong>Developer/Admin Portal</strong> provides backend data settings and system control panels. Access is restricted to authorized developer accounts.</p>
  
  <h3 class="subsection-title">Employee Credentials Management</h3>
  <p>The panel lists all registered employees in the system. You can perform the following modifications:</p>
  <ul style="padding-left: 20px; margin: 10px 0;">
    <li style="margin-bottom: 8px;"><strong>Add User</strong>: Click <strong>"Add User"</strong>, write a unique username, password, and select access roles.</li>
    <li style="margin-bottom: 8px;"><strong>Edit User</strong>: Edit existing usernames, credentials, and roles. Click <strong>"Save User"</strong> to sync.</li>
    <li style="margin-bottom: 8px;"><strong>Delete User</strong>: Click the trashcan icon next to any employee to remove their database record.</li>
  </ul>

  <h3 class="subsection-title">Database Settings & Reset Operations</h3>
  <ul class="steps-list">
    <li><strong>Script URL Configuration</strong>: Displays the current Google Apps Script connection. Developers can override this URL if the spreadsheet is migrated.</li>
    <li><strong>Reset Database (Clear Transactional Data)</strong>: Clicking this button prompts for confirmation, then wipes out all attendance logs, daily task boards, leave records, and daily summaries to start fresh (registered users are preserved).</li>
  </ul>

  <div class="callout" style="border-left-color: #ef4444;">
    <div class="callout-title" style="color: #b91c1c;">Caution: Reset Action</div>
    <p class="callout-content">Resetting the database is irreversible. Ensure you download a backup copies of the Google Spreadsheet before completing this operation.</p>
  </div>

  <!-- PAGE 8: TECHNICAL ARCHITECTURE -->
  <div class="page-break"></div>
  <div class="header-bar">
    <h2>6. Technical Guide</h2>
    <span>Manager & HR Guide</span>
  </div>
  
  <h2 class="section-title">Technical Architecture & Deploy</h2>
  <p>The system is built as a hybrid desktop webview app. The frontend HTML/JS logic is served locally inside PyWebView, proxying requests to Google Sheets.</p>
  
  <h3 class="subsection-title">Spreadsheet Layout Sheets</h3>
  <p>The Google Spreadsheet contains five critical sheets that the Apps Script backend reads/writes:</p>
  <table style="width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 11px;">
    <thead>
      <tr style="background-color: #f1f5f9; text-align: left; font-weight: bold; border-bottom: 2px solid #cbd5e1;">
        <th style="padding: 8px;">Sheet Name</th>
        <th style="padding: 8px;">Columns</th>
        <th style="padding: 8px;">Description</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom: 1px solid #e2e8f0;">
        <td style="padding: 8px; font-weight: bold;">Users</td>
        <td style="padding: 8px;">username, password, role</td>
        <td style="padding: 8px;">Credential and role lists.</td>
      </tr>
      <tr style="border-bottom: 1px solid #e2e8f0;">
        <td style="padding: 8px; font-weight: bold;">TimeLogs</td>
        <td style="padding: 8px;">username, date, login_time, logout_time, total_hours</td>
        <td style="padding: 8px;">Daily attendance logs.</td>
      </tr>
      <tr style="border-bottom: 1px solid #e2e8f0;">
        <td style="padding: 8px; font-weight: bold;">Tasks</td>
        <td style="padding: 8px;">task_id, username, date, title, status, created_at, updated_at</td>
        <td style="padding: 8px;">Employee Kanban board tasks.</td>
      </tr>
      <tr style="border-bottom: 1px solid #e2e8f0;">
        <td style="padding: 8px; font-weight: bold;">DailySummaries</td>
        <td style="padding: 8px;">username, date, summary, created_at</td>
        <td style="padding: 8px;">Work summaries written at checkout.</td>
      </tr>
      <tr style="border-bottom: 1px solid #e2e8f0;">
        <td style="padding: 8px; font-weight: bold;">Leaves</td>
        <td style="padding: 8px;">username, month, casual_leaves, medical_leaves</td>
        <td style="padding: 8px;">Monthly leaves records.</td>
      </tr>
    </tbody>
  </table>

  <div class="callout" style="border-left-color: #64748b; margin-top: 25px;">
    <div class="callout-title" style="color: #475569;">Apps Script Deployment</div>
    <p class="callout-content">Ensure that your Apps Script is deployed under Web App configurations with "Execute as Me" and "Access: Anyone" settings. This is mandatory for PyWebView to authenticate proxy calls.</p>
  </div>

</body>
</html>
"""

# Write HTML files
employee_html_path = os.path.join(current_dir, "employee_manual.html")
manager_html_path = os.path.join(current_dir, "manager_manual.html")

with open(employee_html_path, "w", encoding="utf-8") as f:
    f.write(employee_html)
print("Wrote employee_manual.html")

with open(manager_html_path, "w", encoding="utf-8") as f:
    f.write(manager_html)
print("Wrote manager_manual.html")

# Path to Edge application
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

edge_cmd_emp = [
    edge_path,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={os.path.join(current_dir, 'Employee_Portal_Employee_Manual.pdf')}",
    "--display-header-footer",
    "--header-template= ",
    "--footer-template=<div style='font-size:9px; font-family:Arial; width:100%; text-align:right; padding-right:45px; color:#64748b;'>Page <span class='pageNumber'></span> of <span class='totalPages'></span></div>",
    employee_html_path
]

edge_cmd_mgr = [
    edge_path,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={os.path.join(current_dir, 'Employee_Portal_Manager_Manual.pdf')}",
    "--display-header-footer",
    "--header-template= ",
    "--footer-template=<div style='font-size:9px; font-family:Arial; width:100%; text-align:right; padding-right:45px; color:#64748b;'>Page <span class='pageNumber'></span> of <span class='totalPages'></span></div>",
    manager_html_path
]

try:
    print("Printing Employee Manual to PDF...")
    subprocess.run(edge_cmd_emp, check=True)
    print("Employee Manual PDF created successfully!")
    
    print("Printing Manager Manual to PDF...")
    subprocess.run(edge_cmd_mgr, check=True)
    print("Manager Manual PDF created successfully!")
except subprocess.CalledProcessError as e:
    print(f"Error printing to PDF: {e}")
