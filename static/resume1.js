// ---------- DATA MODELS (existing + new sections) ----------
let photoBase64 = "";

let educations = [
  { degree: "B.Tech Computer Science", institution: "Institution Name", year: "Year - Present", score: "8.5 CGPA" },
  { degree: "12th Standard", institution: "Institution Name", year: "2021", score: "77%" },
  { degree: "10th Standard", institution: "Institution Name", year: "2019", score: "87%" }
];

let experiences = [
  { title: "Experience Title", company: "Company Name/  Department", duration: "Duration", description: "Write Some  Experience in this section in that company" }
];

// NEW DATA ARRAYS
let certifications = [
  { name: "Certification Name", issuer: "Issue Authority Name", date: "Date", credential: "Verified Certificate / Not Verified" }
];
let projects = [
  { title: "E-Commerce Dashboard", tech: "React, Node.js, MongoDB", duration: "2024", description: "Built a full-stack dashboard with real-time analytics, inventory tracking, and order management system." },
  { title: "AI-Based Resume Screener", tech: "Python, NLP, Flask", duration: "2023", description: "Developed a machine learning model to rank resumes based on job descriptions, improving recruitment efficiency." }
];

let extraCurricular = [
  { activity: "National Level Hackathon", role: "Team Leader", year: "2024", description: "Secured top 10 among 200+ teams; developed a sustainable tech solution for waste management." },
  { activity: "College Coding Club", role: "Core Coordinator", year: "2023-Present", description: "Organized coding workshops and hackathons, mentored 50+ students in web development." }
];

let skillsList = ["MS Excel", "Documentation & Data Handling", "Report Preparation", "Git & GitHub", "Node.js", "React JS", "Organizational Skills", "Teamwork & Communication"];
let awardsList = ["Top Performer Award during Cost Management Internship", "Best Student Project Award"];

// ---------- PHOTO UPLOAD WITH OPTIMIZATION ----------
document.getElementById('photoUpload').addEventListener('change', function(e) {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function(ev) {
      const img = new Image();
      img.onload = function() {
        // Create canvas to resize and compress photo
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        // Calculate new dimensions (max 150px for width/height to keep photo small)
        let width = img.width;
        let height = img.height;
        const maxSize = 150;
        
        if (width > height) {
          if (width > maxSize) {
            height = (height * maxSize) / width;
            width = maxSize;
          }
        } else {
          if (height > maxSize) {
            width = (width * maxSize) / height;
            height = maxSize;
          }
        }
        
        canvas.width = width;
        canvas.height = height;
        ctx.drawImage(img, 0, 0, width, height);
        
        // Compress photo with 0.7 quality
        photoBase64 = canvas.toDataURL('image/jpeg', 0.7);
        updateResumePreview();
      };
      img.src = ev.target.result;
    };
    reader.readAsDataURL(file);
  } else {
    photoBase64 = "";
    updateResumePreview();
  }
});

// Helper: escape HTML
function escapeHtml(str) { 
  if(!str) return ''; 
  return str.replace(/[&<>]/g, function(m) { 
    if(m==='&') return '&amp;'; 
    if(m==='<') return '&lt;'; 
    if(m==='>') return '&gt;'; 
    return m;
  }); 
}

// ---------- RENDER DYNAMIC FORMS (includes new sections) ----------
function renderForms() {
  // Education Form
  const eduDiv = document.getElementById('edu-list');
  eduDiv.innerHTML = '';
  educations.forEach((edu, idx) => {
    const div = document.createElement('div');
    div.className = 'dynamic-item';
    div.innerHTML = `
      <input type="text" value="${escapeHtml(edu.degree)}" placeholder="Degree" style="flex:2">
      <input type="text" value="${escapeHtml(edu.institution)}" placeholder="Institution" style="flex:2">
      <input type="text" value="${escapeHtml(edu.year)}" placeholder="Year" style="flex:1">
      <input type="text" value="${escapeHtml(edu.score)}" placeholder="Score" style="flex:1">
      <button class="remove-btn" onclick="removeEducation(${idx})">x</button>
    `;
    eduDiv.appendChild(div);
    const inputs = div.querySelectorAll('input');
    inputs[0].oninput = (e) => { educations[idx].degree = e.target.value; updateResumePreview(); };
    inputs[1].oninput = (e) => { educations[idx].institution = e.target.value; updateResumePreview(); };
    inputs[2].oninput = (e) => { educations[idx].year = e.target.value; updateResumePreview(); };
    inputs[3].oninput = (e) => { educations[idx].score = e.target.value; updateResumePreview(); };
  });

  // Experience Form
  const expDiv = document.getElementById('exp-list');
  expDiv.innerHTML = '';
  experiences.forEach((exp, idx) => {
    const div = document.createElement('div');
    div.className = 'dynamic-item';
    div.innerHTML = `
      <input type="text" value="${escapeHtml(exp.title)}" placeholder="Title" style="flex:2">
      <input type="text" value="${escapeHtml(exp.company)}" placeholder="Company" style="flex:1">
      <input type="text" value="${escapeHtml(exp.duration)}" placeholder="Duration" style="flex:1">
      <textarea placeholder="Description" style="flex:2; min-height:60px;">${escapeHtml(exp.description)}</textarea>
      <button class="remove-btn" onclick="removeExperience(${idx})">x</button>
    `;
    expDiv.appendChild(div);
    const inputs = div.querySelectorAll('input');
    const txt = div.querySelector('textarea');
    inputs[0].oninput = (e) => { experiences[idx].title = e.target.value; updateResumePreview(); };
    inputs[1].oninput = (e) => { experiences[idx].company = e.target.value; updateResumePreview(); };
    inputs[2].oninput = (e) => { experiences[idx].duration = e.target.value; updateResumePreview(); };
    txt.oninput = (e) => { experiences[idx].description = e.target.value; updateResumePreview(); };
  });

  // Certifications Form
  const certDiv = document.getElementById('cert-list');
  certDiv.innerHTML = '';
  certifications.forEach((cert, idx) => {
    const div = document.createElement('div');
    div.className = 'dynamic-item';
    div.innerHTML = `
      <input type="text" value="${escapeHtml(cert.name)}" placeholder="Certification Name" style="flex:2">
      <input type="text" value="${escapeHtml(cert.issuer)}" placeholder="Issuer" style="flex:1">
      <input type="text" value="${escapeHtml(cert.date)}" placeholder="Date" style="flex:1">
      <input type="text" value="${escapeHtml(cert.credential)}" placeholder="Credential ID / Details" style="flex:2">
      <button class="remove-btn" onclick="removeCertification(${idx})">x</button>
    `;
    certDiv.appendChild(div);
    const inputs = div.querySelectorAll('input');
    inputs[0].oninput = (e) => { certifications[idx].name = e.target.value; updateResumePreview(); };
    inputs[1].oninput = (e) => { certifications[idx].issuer = e.target.value; updateResumePreview(); };
    inputs[2].oninput = (e) => { certifications[idx].date = e.target.value; updateResumePreview(); };
    inputs[3].oninput = (e) => { certifications[idx].credential = e.target.value; updateResumePreview(); };
  });

  // Projects Form
  const projDiv = document.getElementById('project-list');
  projDiv.innerHTML = '';
  projects.forEach((proj, idx) => {
    const div = document.createElement('div');
    div.className = 'dynamic-item';
    div.innerHTML = `
      <input type="text" value="${escapeHtml(proj.title)}" placeholder="Project Title" style="flex:2">
      <input type="text" value="${escapeHtml(proj.tech)}" placeholder="Technologies" style="flex:2">
      <input type="text" value="${escapeHtml(proj.duration)}" placeholder="Year / Duration" style="flex:1">
      <textarea placeholder="Description" style="flex:3; min-height:60px;">${escapeHtml(proj.description)}</textarea>
      <button class="remove-btn" onclick="removeProject(${idx})">x</button>
    `;
    projDiv.appendChild(div);
    const inputs = div.querySelectorAll('input');
    const txt = div.querySelector('textarea');
    inputs[0].oninput = (e) => { projects[idx].title = e.target.value; updateResumePreview(); };
    inputs[1].oninput = (e) => { projects[idx].tech = e.target.value; updateResumePreview(); };
    inputs[2].oninput = (e) => { projects[idx].duration = e.target.value; updateResumePreview(); };
    txt.oninput = (e) => { projects[idx].description = e.target.value; updateResumePreview(); };
  });

  // Extra-Curricular Activities Form
  const extraDiv = document.getElementById('extra-list');
  extraDiv.innerHTML = '';
  extraCurricular.forEach((extra, idx) => {
    const div = document.createElement('div');
    div.className = 'dynamic-item';
    div.innerHTML = `
      <input type="text" value="${escapeHtml(extra.activity)}" placeholder="Activity Name" style="flex:2">
      <input type="text" value="${escapeHtml(extra.role)}" placeholder="Role / Position" style="flex:2">
      <input type="text" value="${escapeHtml(extra.year)}" placeholder="Year / Duration" style="flex:1">
      <textarea placeholder="Description / Achievements" style="flex:3; min-height:60px;">${escapeHtml(extra.description)}</textarea>
      <button class="remove-btn" onclick="removeExtraCurricular(${idx})">x</button>
    `;
    extraDiv.appendChild(div);
    const inputs = div.querySelectorAll('input');
    const txt = div.querySelector('textarea');
    inputs[0].oninput = (e) => { extraCurricular[idx].activity = e.target.value; updateResumePreview(); };
    inputs[1].oninput = (e) => { extraCurricular[idx].role = e.target.value; updateResumePreview(); };
    inputs[2].oninput = (e) => { extraCurricular[idx].year = e.target.value; updateResumePreview(); };
    txt.oninput = (e) => { extraCurricular[idx].description = e.target.value; updateResumePreview(); };
  });

  // Skills Form
  const skillsDiv = document.getElementById('skills-list');
  skillsDiv.innerHTML = '';
  skillsList.forEach((skill, idx) => {
    const div = document.createElement('div');
    div.className = 'dynamic-item';
    div.innerHTML = `<input type="text" value="${escapeHtml(skill)}" style="flex:1"><button class="remove-btn" onclick="removeSkill(${idx})">x</button>`;
    skillsDiv.appendChild(div);
    div.querySelector('input').oninput = (e) => { skillsList[idx] = e.target.value; updateResumePreview(); };
  });

  // Awards Form
  const awardsDiv = document.getElementById('awards-list');
  awardsDiv.innerHTML = '';
  awardsList.forEach((award, idx) => {
    const div = document.createElement('div');
    div.className = 'dynamic-item';
    div.innerHTML = `<input type="text" value="${escapeHtml(award)}" style="flex:1"><button class="remove-btn" onclick="removeAward(${idx})">x</button>`;
    awardsDiv.appendChild(div);
    div.querySelector('input').oninput = (e) => { awardsList[idx] = e.target.value; updateResumePreview(); };
  });
}

// Remove / Add functions (existing + new)
window.removeEducation = (i) => { educations.splice(i,1); renderForms(); updateResumePreview(); };
window.removeExperience = (i) => { experiences.splice(i,1); renderForms(); updateResumePreview(); };
window.removeCertification = (i) => { certifications.splice(i,1); renderForms(); updateResumePreview(); };
window.removeProject = (i) => { projects.splice(i,1); renderForms(); updateResumePreview(); };
window.removeExtraCurricular = (i) => { extraCurricular.splice(i,1); renderForms(); updateResumePreview(); };
window.removeSkill = (i) => { skillsList.splice(i,1); renderForms(); updateResumePreview(); };
window.removeAward = (i) => { awardsList.splice(i,1); renderForms(); updateResumePreview(); };

function addEducation() { educations.push({ degree: "", institution: "", year: "", score: "" }); renderForms(); updateResumePreview(); }
function addExperience() { experiences.push({ title: "", company: "", duration: "", description: "" }); renderForms(); updateResumePreview(); }
function addCertification() { certifications.push({ name: "", issuer: "", date: "", credential: "" }); renderForms(); updateResumePreview(); }
function addProject() { projects.push({ title: "", tech: "", duration: "", description: "" }); renderForms(); updateResumePreview(); }
function addExtraCurricular() { extraCurricular.push({ activity: "", role: "", year: "", description: "" }); renderForms(); updateResumePreview(); }
function addSkill() { skillsList.push(""); renderForms(); updateResumePreview(); }
function addAward() { awardsList.push(""); renderForms(); updateResumePreview(); }

window.addEducation = addEducation;
window.addExperience = addExperience;
window.addCertification = addCertification;
window.addProject = addProject;
window.addExtraCurricular = addExtraCurricular;
window.addSkill = addSkill;
window.addAward = addAward;

// ---------- LIVE RESUME PREVIEW (includes new sections) ----------
function updateResumePreview() {
  const name = document.getElementById('name').value || 'Your Name';
  const jobtitle = document.getElementById('jobtitle').value || 'Professional';
  const phone = document.getElementById('phone').value;
  const email = document.getElementById('email').value;
  const address = document.getElementById('address').value;
  const linkedin = document.getElementById('linkedin').value;
  const summaryText = document.getElementById('summary').value;

  // Right side photo
  const photoHtml = photoBase64 ? 
    `<div class="photo-right"><img class="profile-photo" src="${photoBase64}" alt="profile"></div>` :
    `<div class="photo-right"><div class="photo-placeholder">IMG</div></div>`;

  // Education HTML
  let eduHtml = '';
  educations.forEach(edu => {
    eduHtml += `
      <div class="edu-item">
        <div class="edu-title">${escapeHtml(edu.degree)}</div>
        <div class="edu-detail">${escapeHtml(edu.institution)} | ${escapeHtml(edu.year)} | ${escapeHtml(edu.score)}</div>
      </div>
    `;
  });

  // Experience HTML
  let expHtml = '';
  experiences.forEach(exp => {
    expHtml += `
      <div class="exp-item">
        <div class="exp-title">${escapeHtml(exp.title)} — ${escapeHtml(exp.company)} (${escapeHtml(exp.duration)})</div>
        <div class="exp-desc">${escapeHtml(exp.description).replace(/\n/g, '<br>')}</div>
      </div>
    `;
  });

  // Certifications HTML
  let certHtml = '';
  certifications.forEach(cert => {
    certHtml += `
      <div class="cert-item">
        <div class="cert-title">${escapeHtml(cert.name)}</div>
        <div class="cert-detail">${escapeHtml(cert.issuer)} | ${escapeHtml(cert.date)} | ${escapeHtml(cert.credential)}</div>
      </div>
    `;
  });

  // Projects HTML
  let projectHtml = '';
  projects.forEach(proj => {
    projectHtml += `
      <div class="project-item">
        <div class="project-title">${escapeHtml(proj.title)} — ${escapeHtml(proj.tech)} (${escapeHtml(proj.duration)})</div>
        <div class="project-desc">${escapeHtml(proj.description).replace(/\n/g, '<br>')}</div>
      </div>
    `;
  });

  // Extra-Curricular HTML
  let extraHtml = '';
  extraCurricular.forEach(extra => {
    extraHtml += `
      <div class="extra-item">
        <div class="extra-title">${escapeHtml(extra.activity)} — ${escapeHtml(extra.role)} (${escapeHtml(extra.year)})</div>
        <div class="extra-desc">${escapeHtml(extra.description).replace(/\n/g, '<br>')}</div>
      </div>
    `;
  });

  // Skills
  let skillsHtml = '<div class="skill-list">';
  skillsList.forEach(s => { if(s.trim()) skillsHtml += `<span class="skill-tag">${escapeHtml(s)}</span>`; });
  skillsHtml += '</div>';

  // Awards
  let awardsHtml = '';
  awardsList.forEach(a => { if(a.trim()) awardsHtml += `<div class="award-item">${escapeHtml(a)}</div>`; });

  // Contact line with social
  let contactLine = `<div class="contact-info"><span>${escapeHtml(address)}</span><span>${escapeHtml(phone)}</span><span>${escapeHtml(email)}</span>`;
  if(linkedin) contactLine += `<span>${escapeHtml(linkedin)}</span>`;
  contactLine += `</div>`;

  const finalResumeHtml = `
    <div class="resume-page">
      <div class="resume-header-row">
        <div class="left-title">
          <h1>${escapeHtml(name)}</h1>
          <div class="job-role">${escapeHtml(jobtitle)}</div>
          ${contactLine}
        </div>
        ${photoHtml}
      </div>

      <div class="section">
        <div class="section-title">PROFESSIONAL SUMMARY</div>
        <div class="summary-text">${escapeHtml(summaryText).replace(/\n/g, '<br>')}</div>
      </div>

      <div class="section">
        <div class="section-title">EDUCATION</div>
        ${eduHtml || '<div class="summary-text">No education added</div>'}
      </div>

      <div class="section">
        <div class="section-title">EXPERIENCE / INTERNSHIP</div>
        ${expHtml || '<div class="summary-text">No experience added</div>'}
      </div>

      <div class="section">
        <div class="section-title">CERTIFICATIONS</div>
        ${certHtml || '<div class="summary-text">No certifications added</div>'}
      </div>

      <div class="section">
        <div class="section-title">PROJECTS</div>
        ${projectHtml || '<div class="summary-text">No projects added</div>'}
      </div>

      <div class="section">
        <div class="section-title">EXTRA-CURRICULAR ACTIVITIES</div>
        ${extraHtml || '<div class="summary-text">No activities added</div>'}
      </div>

      <div class="section">
        <div class="section-title">TECHNICAL SKILLS</div>
        ${skillsHtml}
      </div>

      <div class="section">
        <div class="section-title">AWARDS & ACHIEVEMENTS</div>
        ${awardsHtml || '<div class="summary-text">No awards added</div>'}
      </div>
    </div>
  `;
  document.getElementById('resume-content').innerHTML = finalResumeHtml;
}

// ---------- OPTIMIZED PDF EXPORT (Under 1MB) ----------
async function downloadPerfectPDF() {
  const element = document.getElementById('resume-content');
  const btn = document.querySelector('.download-btn');
  const originalLabel = btn.innerHTML;
  btn.innerHTML = "Generating optimized PDF...";
  btn.disabled = true;

  try {
    await new Promise(r => setTimeout(r, 120));
    
    // OPTIMIZATION 1: Lower scale for smaller image size (2.0 instead of 2.8)
    const canvas = await html2canvas(element, {
      scale: 1.8,  // Reduced from 2.8 to 1.8 - still crisp but much smaller file
      useCORS: true,
      backgroundColor: '#ffffff',
      logging: false,
      windowWidth: element.scrollWidth,
      windowHeight: element.scrollHeight,
      imageTimeout: 0,
      allowTaint: false,
      foreignObjectRendering: false
    });
    
    // OPTIMIZATION 2: Compress the canvas image before adding to PDF
    const imgData = canvas.toDataURL('image/jpeg', 0.75);  // JPEG with 75% quality
    
    const { jsPDF } = window.jspdf;
    
    const imgWidth = 210;  // A4 width in mm
    const pageHeight = 297; // A4 height in mm
    const imgHeight = (canvas.height * imgWidth) / canvas.width;
    
    const pdf = new jsPDF({
      unit: 'mm',
      format: 'a4',
      orientation: 'portrait',
      hotfixes: ['px_scaling'],
      compress: true  // Enable PDF compression
    });
    
    // OPTIMIZATION 3: Add image with compression
    pdf.addImage(imgData, 'JPEG', 0, 0, imgWidth, imgHeight, undefined, 'FAST');
    
    if (imgHeight > pageHeight) {
      pdf.addPage();
      pdf.addImage(imgData, 'JPEG', 0, -pageHeight, imgWidth, imgHeight, undefined, 'FAST');
    }
    
    pdf.save('Professional_Resume_Pankaj.pdf');
    
  } catch (error) {
    console.error('PDF error:', error);
    alert('PDF generation failed: ' + error.message);
  } finally {
    btn.innerHTML = originalLabel;
    btn.disabled = false;
  }
}

// Attach live listeners for all input fields
const liveFields = ['name', 'jobtitle', 'phone', 'email', 'address', 'linkedin', 'summary'];
liveFields.forEach(id => {
  document.getElementById(id).addEventListener('input', () => updateResumePreview());
});

// Initial render
renderForms();
updateResumePreview();

