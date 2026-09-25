/**
 * BLACKORANGE PORTFOLIO - MAIN CONTROLLER (DENNIS SHEM O. LIMO)
 */

document.addEventListener('DOMContentLoaded', () => {
  'use strict';

  // ==========================================================================
  // 1. NAVIGATION DRAWER
  // ==========================================================================
  const menuToggle = document.getElementById('menuToggle');
  const drawerBackdrop = document.getElementById('drawerBackdrop');
  const drawerCloseBtn = document.getElementById('drawerCloseBtn');
  const drawerNavLinks = document.querySelectorAll('.drawer-nav-link');

  function openDrawer() {
    drawerBackdrop.classList.add('active');
    document.documentElement.classList.add('no-scroll');
    document.body.classList.add('no-scroll');
  }

  function closeDrawer() {
    drawerBackdrop.classList.remove('active');
    document.documentElement.classList.remove('no-scroll');
    document.body.classList.remove('no-scroll');
  }

  if (menuToggle) menuToggle.addEventListener('click', openDrawer);
  if (drawerCloseBtn) drawerCloseBtn.addEventListener('click', closeDrawer);

  if (drawerBackdrop) {
    drawerBackdrop.addEventListener('click', (e) => {
      if (e.target === drawerBackdrop) closeDrawer();
    });
  }

  drawerNavLinks.forEach((link) => {
    link.addEventListener('click', (e) => {
      const targetId = link.getAttribute('href');
      if (targetId && targetId.startsWith('#')) {
        e.preventDefault();
        closeDrawer();
        setTimeout(() => {
          const targetEl = document.querySelector(targetId);
          if (targetEl) {
            const topOffset = targetEl.getBoundingClientRect().top + window.pageYOffset - 30;
            window.scrollTo({
              top: topOffset,
              behavior: 'smooth'
            });
          }
        }, 180);
      } else {
        closeDrawer();
      }
    });
  });

  // Close on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeDrawer();
      closeModal();
    }
  });

  // ==========================================================================
  // 2. SMOOTH SCROLLING
  // ==========================================================================
  const scrollIndicator = document.getElementById('scrollIndicator');
  if (scrollIndicator) {
    scrollIndicator.addEventListener('click', () => {
      const aboutSection = document.getElementById('about');
      if (aboutSection) {
        const topOffset = aboutSection.getBoundingClientRect().top + window.pageYOffset - 30;
        window.scrollTo({
          top: topOffset,
          behavior: 'smooth'
        });
      }
    });
  }

  // Universal smooth scroll for internal anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (!href || href === '#' || this.classList.contains('drawer-nav-link')) return;
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        const topOffset = target.getBoundingClientRect().top + window.pageYOffset - 30;
        window.scrollTo({
          top: topOffset,
          behavior: 'smooth'
        });
      }
    });
  });

  // ==========================================================================
  // 3. TOAST NOTIFICATIONS
  // ==========================================================================
  const toastContainer = document.getElementById('toastContainer');
  let toastTimeout;

  function showToast(message, icon = '✓') {
    if (!toastContainer) return;

    toastContainer.innerHTML = '';
    clearTimeout(toastTimeout);

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<span style="color: var(--primary-orange); font-size: 1.1rem; font-weight: bold;">${icon}</span> <span>${message}</span>`;
    
    toastContainer.appendChild(toast);

    requestAnimationFrame(() => {
      toast.classList.add('show');
    });

    toastTimeout = setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 400);
    }, 3500);
  }

  // ==========================================================================
  // 4. ABOUT PHOTO COLOR TOGGLE
  // ==========================================================================
  const aboutPhotoCard = document.getElementById('aboutPhotoCard');
  if (aboutPhotoCard) {
    aboutPhotoCard.addEventListener('click', () => {
      aboutPhotoCard.classList.toggle('color-mode');
      const isColor = aboutPhotoCard.classList.contains('color-mode');
      showToast(isColor ? 'Photo switched to Full Color mode' : 'Photo switched to Classic Monochrome', '📷');
    });
  }

  // ==========================================================================
  // 5. MODAL HANDLER
  // ==========================================================================
  const modalOverlay = document.getElementById('modalOverlay');
  const modalTitle = document.getElementById('modalTitle');
  const modalBody = document.getElementById('modalBody');
  const modalCloseBtn = document.getElementById('modalCloseBtn');

  function openModal(title, htmlContent) {
    if (!modalOverlay) return;
    modalTitle.textContent = title;
    modalBody.innerHTML = htmlContent;
    modalOverlay.classList.add('active');
    document.documentElement.classList.add('no-scroll');
    document.body.classList.add('no-scroll');
  }

  function closeModal() {
    if (!modalOverlay) return;
    modalOverlay.classList.remove('active');
    document.documentElement.classList.remove('no-scroll');
    document.body.classList.remove('no-scroll');
  }

  if (modalCloseBtn) modalCloseBtn.addEventListener('click', closeModal);
  if (modalOverlay) {
    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) closeModal();
    });
  }

  // ==========================================================================
  // 6. RESUME / CV MODAL
  // ==========================================================================
  const resumeModalBtn = document.getElementById('resumeModalBtn');
  if (resumeModalBtn) {
    resumeModalBtn.addEventListener('click', () => {
      const resumeContent = `
        <div style="display: flex; flex-direction: column; gap: 1.5rem; color: #e4e4e7;">
          <div style="border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 1rem;">
            <h4 style="font-size: 1.2rem; color: #fff; margin-bottom: 0.3rem;">Dennis Shem O. Limo</h4>
            <p style="color: var(--primary-orange); font-weight: 600; font-size: 0.95rem;">Data Analyst • Python Developer • Data Science</p>
            <p style="font-size: 0.85rem; color: #9c9ca8; margin-top: 0.3rem;">
              📍 Nairobi, Kenya (Remote-Ready) &nbsp;|&nbsp; ✉️ shemdennis5@gmail.com &nbsp;|&nbsp; 📞 +254 721 877 088
            </p>
          </div>

          <div>
            <h5 style="color: var(--primary-orange); font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Education & Certifications</h5>
            <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.5rem; font-size: 0.9rem;">
              <li><strong>Maseno University</strong> — Bachelor of Science in Computer Science (2016 – 2021)</li>
              <li><strong>Moringa School</strong> — Data Science & Artificial Intelligence Certification (2025)</li>
              <li><strong>Cisco Networking Academy</strong> — Cisco CCNA (Routing & Switching — Full Track) (2019 – 2020)</li>
              <li><strong>Cisco Networking Academy</strong> — Introduction to Cybersecurity (2026)</li>
            </ul>
          </div>

          <div>
            <h5 style="color: var(--primary-orange); font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Professional Experience</h5>
            <div style="display: flex; flex-direction: column; gap: 0.8rem; font-size: 0.88rem;">
              <div>
                <span style="font-weight: 700; color: #fff;">Freelance Data Analyst, Developer & Researcher</span> <span style="color: #9c9ca8;">(2019 – Present)</span>
                <p style="color: #a1a1aa; margin-top: 0.2rem;">End-to-end analytics, automated reporting pipelines, OCR workflows, and predictive ML models.</p>
              </div>
              <div>
                <span style="font-weight: 700; color: #fff;">IT Intern — Data & Systems Support</span> <span style="color: #9c9ca8;">(State Dept of Lands & Physical Planning)</span>
                <p style="color: #a1a1aa; margin-top: 0.2rem;">IFMIS quality assurance and validation, departmental hardware/software troubleshooting.</p>
              </div>
              <div>
                <span style="font-weight: 700; color: #fff;">Field Engineer Intern</span> <span style="color: #9c9ca8;">(Net Mtaani, 2023)</span>
                <p style="color: #a1a1aa; margin-top: 0.2rem;">Maintained network infrastructure and resolved connectivity bottlenecks, improving uptime by 15%.</p>
              </div>
              <div>
                <span style="font-weight: 700; color: #fff;">IT Attaché</span> <span style="color: #9c9ca8;">(County Government of Nandi, 2019)</span>
                <p style="color: #a1a1aa; margin-top: 0.2rem;">Digitized and organized land records using IFMIS databases, enhancing retrieval speed and data integrity.</p>
              </div>
            </div>
          </div>

          <div>
            <h5 style="color: var(--primary-orange); font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Languages & Availability</h5>
            <p style="font-size: 0.88rem; color: #a1a1aa;">
              <strong>Languages:</strong> English (Fluent), Swahili (Fluent)<br>
              <strong>Availability:</strong> Immediately available for full-time, contract, or remote engagements worldwide.
            </p>
          </div>

          <div style="display: flex; gap: 1rem; margin-top: 0.5rem;">
            <a href="mailto:shemdennis5@gmail.com" class="btn-primary" style="font-size: 0.88rem; padding: 0.6rem 1.4rem;">
              Contact Dennis ✉️
            </a>
            <a href="https://linkedin.com/in/dennis-limo" target="_blank" rel="noopener" style="padding: 0.6rem 1.4rem; background: #222228; color: #fff; border-radius: 8px; font-weight: 600; font-size: 0.88rem; display: inline-flex; align-items: center; gap: 0.4rem;">
              LinkedIn Profile ↗
            </a>
          </div>
        </div>
      `;
      openModal('Curriculum Vitae — Dennis Shem O. Limo', resumeContent);
    });
  }

  // ==========================================================================
  // 7. KEY PROJECTS & DYNAMIC CMS SYNC
  // ==========================================================================
  const projectsData = {
    orbitiq: {
      title: 'OrbitIQ — KCSE Results & University Placement Advisor',
      category: 'Solo Project • Deployed on Render',
      url: 'https://orbitiq-cic0.onrender.com',
      stack: ['Python', 'OCR Computer Vision', 'KUCCPS Calculation Engine', 'Jupyter', 'HTML/CSS', 'Render'],
      desc: `
        Engineered an end-to-end university advisory tool that streamlines student qualification evaluation:
        <ul style="margin: 0.8rem 0 0.8rem 1.2rem; display: flex; flex-direction: column; gap: 0.4rem; color: #d4d4d8;">
          <li>Automated OCR pipeline extracting subject grades from KCSE slip photos to populate student records seamlessly.</li>
          <li>Engineered KUCCPS cluster point calculation engine across diverse course categories based on extracted results.</li>
          <li>Built dynamic course-matching logic and automated PDF generation producing tailored student advisory reports.</li>
        </ul>
      `
    },
    loan: {
      title: 'Business Loan Application Platform',
      category: 'Commercial SaaS Target • Team Project',
      url: 'https://menace.pythonanywhere.com',
      stack: ['Python', 'RBAC Security', 'Session Management', 'Audit Logging', 'PythonAnywhere', 'HTML5'],
      desc: `
        Co-developed a secure microfinance loan management platform designed for commercial SaaS deployment:
        <ul style="margin: 0.8rem 0 0.8rem 1.2rem; display: flex; flex-direction: column; gap: 0.4rem; color: #d4d4d8;">
          <li>Architected role-based access control (RBAC) enabling Loan Officers to securely process client applications.</li>
          <li>Implemented strict session security protocols, including automated session reset on window/browser termination.</li>
          <li>Developed backend approval logic in Python with audit-ready action tracking alongside responsive interfaces.</li>
        </ul>
      `
    },
    ksu: {
      title: 'Koitalel Samoei University Portal',
      category: 'Freelance Project • Live Administrative System',
      url: 'https://ksu-5wmg.onrender.com',
      stack: ['Python Full-Stack', 'Admin CMS Engine', 'Dynamic RBAC', 'Render', 'Responsive Web'],
      desc: `
        Comprehensive institutional portal for Koitalel Samoei University:
        <ul style="margin: 0.8rem 0 0.8rem 1.2rem; display: flex; flex-direction: column; gap: 0.4rem; color: #d4d4d8;">
          <li>Developing both the public client-facing portal and administrative management system.</li>
          <li>Building dynamic admin panel capabilities for secure content editing, role management, and operational workflows.</li>
          <li>Ensuring high availability, mobile responsiveness, and intuitive navigation for staff and prospective students.</li>
        </ul>
      `
    },
    dengue: {
      title: 'Dengue Fever Clinical Data Analysis',
      category: 'Clinic Client Project • 1-Year Longitudinal Study',
      url: null,
      stack: ['Python', 'Pandas', 'Power BI', 'Seaborn', 'Statistical Modeling', 'Healthcare Analytics'],
      desc: `
        Led clinical data analysis on longitudinal healthcare datasets over a 1-year duration to assist medical decision-making:
        <ul style="margin: 0.8rem 0 0.8rem 1.2rem; display: flex; flex-direction: column; gap: 0.4rem; color: #d4d4d8;">
          <li>Tracked dengue fever case trends, seasonal infection patterns, and patient demographic risk profiles.</li>
          <li>Generated rigorous statistical reports and visual dashboards enabling medical staff to make informed, data-driven decisions.</li>
          <li>Cleaned and imputed large-scale clinical records to maintain high predictive data integrity.</li>
        </ul>
      `
    }
  };

  const dynamicProjectsMap = {};
  const dynamicBlogsMap = {};

  function bindProjectDetailButtons() {
    document.querySelectorAll('.btn-work-live[data-project]').forEach((btn) => {
      btn.onclick = () => {
        const key = btn.getAttribute('data-project');
        const project = dynamicProjectsMap[key] || projectsData[key];
        if (!project) return;

        const stackArray = Array.isArray(project.stack) ? project.stack : (project.stack_list || (project.tech_stack ? project.tech_stack.split(',') : []));

        const content = `
          <div style="display: flex; flex-direction: column; gap: 1.2rem;">
            <div style="font-size: 0.82rem; font-weight: 700; color: var(--primary-orange); text-transform: uppercase; letter-spacing: 0.05em;">
              ${escapeHtml(project.category || '')}
            </div>
            <div style="font-size: 0.95rem; color: #f4f4f6; line-height: 1.6;">${project.desc || escapeHtml(project.description || '')}</div>
            <div>
              <span style="font-size: 0.85rem; font-weight: 700; color: var(--primary-orange); text-transform: uppercase; letter-spacing: 0.05em;">Tech Stack</span>
              <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem;">
                ${stackArray.map(s => `<span style="background: rgba(255,87,34,0.15); color: #ff8a65; border: 1px solid rgba(255,87,34,0.3); padding: 4px 10px; border-radius: 999px; font-size: 0.8rem; font-weight: 600;">${escapeHtml(s.trim())}</span>`).join('')}
              </div>
            </div>
            <div style="margin-top: 1.2rem; display: flex; gap: 1rem; flex-wrap: wrap;">
              ${project.url || project.live_url ? `<a href="${escapeHtml(project.url || project.live_url)}" target="_blank" rel="noopener" class="btn-primary" style="font-size: 0.9rem; padding: 0.6rem 1.4rem;" onclick="logEvent('project_click', '${escapeHtml(project.url || project.live_url)}')">Launch Live System ↗</a>` : ''}
              <button onclick="closeModal()" style="padding: 0.6rem 1.4rem; background: #222228; color: #fff; border-radius: 8px; font-weight: 600; font-size: 0.9rem;">
                Close
              </button>
            </div>
          </div>
        `;

        openModal(project.title, content);
      };
    });
  }

  // Initial binding for pre-rendered projects
  bindProjectDetailButtons();

  // ==========================================================================
  // 8. BLOG POSTS READER & DYNAMIC BLOGS
  // ==========================================================================
  const blogPostsData = {
    ocr: {
      title: 'Engineering an Automated OCR Pipeline for Exam Slip Digitization',
      date: 'Technical Case Study',
      readTime: '6 min read',
      content: `
        <p style="color: #d4d4d8; line-height: 1.75; margin-bottom: 1.2rem;">
          In building <strong>OrbitIQ</strong>, our primary bottleneck was manual data entry: students typing dozens of individual KCSE grades led to frequent input errors and skewed university cluster calculations.
        </p>
        <p style="color: #d4d4d8; line-height: 1.75; margin-bottom: 1.2rem;">
          By architecting an automated <strong>Optical Character Recognition (OCR) pipeline</strong> using computer vision pre-processing (deskewing, adaptive thresholding, and ROI isolation), we automated grade extraction directly from photos taken with mobile phones.
        </p>
        <h4 style="color: var(--primary-orange); margin: 1.2rem 0 0.5rem 0;">Key Takeaway:</h4>
        <p style="color: #a1a1aa; line-height: 1.6;">
          Robust preprocessing (noise reduction and contrast enhancement) before feeding images into the OCR engine improved character confidence by over 38% on low-quality smartphone captures.
        </p>
      `
    },
    security: {
      title: 'Architecting RBAC and Strict Session Security for Commercial SaaS',
      date: 'Architecture & Security',
      readTime: '5 min read',
      content: `
        <p style="color: #d4d4d8; line-height: 1.75; margin-bottom: 1.2rem;">
          In financial microfinance platforms, user permission leaks represent catastrophic compliance risks. In the Business Loan Application Platform, we designed a zero-trust <strong>Role-Based Access Control (RBAC)</strong> model.
        </p>
        <p style="color: #d4d4d8; line-height: 1.75; margin-bottom: 1.2rem;">
          Every endpoint verifies granular permission tokens on the server rather than trusting client-side flags. Furthermore, we implemented aggressive session termination upon window close or tab defocus to protect sensitive borrower financial records.
        </p>
        <h4 style="color: var(--primary-orange); margin: 1.2rem 0 0.5rem 0;">Key Takeaway:</h4>
        <p style="color: #a1a1aa; line-height: 1.6;">
          Never rely on client-side state for authorization. Security in SaaS requires server-side permission trees combined with automated audit trails for every state change.
        </p>
      `
    },
    healthcare: {
      title: 'Tracking Clinical Infection Trends: Longitudinal Healthcare Analytics',
      date: 'Data Science & Health',
      readTime: '7 min read',
      content: `
        <p style="color: #d4d4d8; line-height: 1.75; margin-bottom: 1.2rem;">
          During our 1-year clinical study on Dengue fever infection dynamics, we synthesized longitudinal patient metrics to forecast outbreak peaks.
        </p>
        <p style="color: #d4d4d8; line-height: 1.75; margin-bottom: 1.2rem;">
          Using Python (Pandas and Seaborn) alongside interactive Power BI reporting dashboards, medical personnel could monitor infection clusters in real time, shifting resource allocation proactively ahead of epidemic spikes.
        </p>
        <h4 style="color: var(--primary-orange); margin: 1.2rem 0 0.5rem 0;">Key Takeaway:</h4>
        <p style="color: #a1a1aa; line-height: 1.6;">
          Data analysis in healthcare is only as valuable as its clinical interpretability. Visual dashboards designed with medical workflows in mind drove tangible improvements in early intervention response times.
        </p>
      `
    }
  };

  function bindBlogCardClicks() {
    document.querySelectorAll('.blog-card').forEach((card) => {
      card.onclick = (e) => {
        if (e.target.closest('.blog-card-share')) {
          e.stopPropagation();
          if (navigator.clipboard) {
            navigator.clipboard.writeText(window.location.href);
            showToast(`Article link copied to clipboard!`, '🔗');
          } else {
            showToast(`Link ready to share!`, '🔗');
          }
          return;
        }

        const postKey = card.getAttribute('data-blog');
        const post = dynamicBlogsMap[postKey] || blogPostsData[postKey];
        if (!post) return;

        let formattedContent = post.content || '';
        if (!formattedContent.includes('<p>') && !formattedContent.includes('<div>')) {
          formattedContent = formattedContent.split('\n\n').map(para => `<p style="color: #d4d4d8; line-height: 1.75; margin-bottom: 1.2rem;">${escapeHtml(para)}</p>`).join('');
        }

        const modalHtml = `
          <div style="display: flex; flex-direction: column; gap: 1rem;">
            <div style="display: flex; gap: 1rem; font-size: 0.82rem; color: var(--text-muted); margin-bottom: 0.5rem; flex-wrap: wrap;">
              <span>📅 ${escapeHtml(post.date || post.date_str || '')}</span>
              <span>⏱️ ${escapeHtml(post.readTime || post.read_time || '5 min read')}</span>
              ${post.category ? `<span style="color: var(--primary-orange); font-weight: 600;">🏷️ ${escapeHtml(post.category)}</span>` : ''}
            </div>
            ${post.image_url ? `<img src="${escapeHtml(post.image_url)}" style="width: 100%; max-height: 240px; object-fit: cover; border-radius: 8px; margin-bottom: 0.5rem;" alt="${escapeHtml(post.title)}">` : ''}
            <div>${formattedContent}</div>
          </div>
        `;

        openModal(post.title, modalHtml);
      };
    });
  }

  // Initial binding for pre-rendered blogs
  bindBlogCardClicks();

  // ==========================================================================
  // DYNAMIC CMS SYNC (FETCH FROM FLASK API)
  // ==========================================================================
  async function syncDynamicContent() {
    try {
      // 1. Projects
      const projRes = await fetch('/api/projects');
      if (projRes.ok) {
        const projData = await projRes.json();
        if (projData.success && projData.projects && projData.projects.length > 0) {
          const worksGrid = document.querySelector('.works-grid');
          if (worksGrid) {
            worksGrid.innerHTML = '';
            projData.projects.forEach(p => {
              const key = 'proj_' + p.id;
              dynamicProjectsMap[key] = p;

              const card = document.createElement('div');
              card.className = 'work-card';
              card.innerHTML = `
                <div class="work-card-content">
                  <div style="font-size: 0.76rem; font-weight: 700; color: var(--primary-orange); letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 0.4rem;">
                    ${escapeHtml(p.category || 'Featured Work')}
                  </div>
                  <h3 class="work-card-title">${escapeHtml(p.title)}</h3>
                  <p class="work-card-desc">${escapeHtml(p.subtitle || p.description.substring(0, 85) + '...')}</p>
                </div>
                <div style="display: flex; gap: 0.8rem; align-items: center; flex-wrap: wrap;">
                  <button class="btn-work-live" data-project="${key}">Details</button>
                  ${p.live_url ? `<a href="${escapeHtml(p.live_url)}" target="_blank" rel="noopener noreferrer" class="btn-work-live" style="background: transparent; border: 1px solid var(--primary-orange); color: var(--primary-orange-light);">Visit Site ↗</a>` : ''}
                </div>
              `;
              worksGrid.appendChild(card);
            });
            bindProjectDetailButtons();
          }
        }
      }

      // 2. Skills
      const skillRes = await fetch('/api/skills');
      if (skillRes.ok) {
        const skillData = await skillRes.json();
        if (skillData.success && skillData.skills && skillData.skills.length > 0) {
          const skillsGrid = document.querySelector('.skills-grid');
          if (skillsGrid) {
            skillsGrid.innerHTML = '';
            skillData.skills.forEach(s => {
              const item = document.createElement('div');
              item.className = 'skill-item';
              item.innerHTML = `
                <div class="skill-icon-box">
                  ${s.icon_svg || '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/></svg>'}
                </div>
                <span class="skill-name">${escapeHtml(s.name)}</span>
              `;
              skillsGrid.appendChild(item);
            });
          }
        }
      }

      // 3. Blogs
      const blogRes = await fetch('/api/blogs');
      if (blogRes.ok) {
        const blogData = await blogRes.json();
        if (blogData.success && blogData.blogs && blogData.blogs.length > 0) {
          const blogGrid = document.querySelector('.blog-grid');
          if (blogGrid) {
            blogGrid.innerHTML = '';
            blogData.blogs.forEach(b => {
              const key = 'blog_' + b.id;
              dynamicBlogsMap[key] = b;

              const article = document.createElement('article');
              article.className = 'blog-card';
              article.setAttribute('data-blog', key);
              article.innerHTML = `
                <img src="${escapeHtml(b.image_url || 'assets/images/blog-1.jpg')}" alt="${escapeHtml(b.title)}" class="blog-card-img" onerror="this.src='assets/images/blog-1.jpg'">
                <div class="blog-card-overlay"></div>
                <div class="blog-card-content">
                  <h3 class="blog-card-title">${escapeHtml(b.title)}</h3>
                  <div class="blog-card-meta">
                    <span class="blog-card-date">${escapeHtml(b.category || 'Insights')}</span>
                    <button class="blog-card-share" title="Share article" aria-label="Share article">
                      <svg viewBox="0 0 24 24"><path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92s2.92-1.31 2.92-2.92c0-1.61-1.31-2.92-2.92-2.92z"/></svg>
                    </button>
                  </div>
                </div>
              `;
              blogGrid.appendChild(article);
            });
            bindBlogCardClicks();
          }
        }
      }

      // 4. Profile
      const profRes = await fetch('/api/profile');
      if (profRes.ok) {
        const profData = await profRes.json();
        if (profData.success && profData.profile) {
          const prof = profData.profile;
          if (prof.full_name) {
            document.querySelectorAll('.hero-name, .about-info h2 .highlight-orange').forEach(el => {
              // keep brand stylings
            });
          }
        }
      }
    } catch (e) {
      console.warn('API sync fallback to static content:', e);
    }
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  // Trigger sync on load
  syncDynamicContent();

  // ==========================================================================
  // 9. GET IN TOUCH (BACKEND API INTEGRATION)
  // ==========================================================================
  const quoteForm = document.getElementById('quoteForm');
  const sendBtn = document.getElementById('sendBtn');

  if (quoteForm && sendBtn) {
    quoteForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const name = document.getElementById('contactName').value.trim();
      const email = document.getElementById('contactEmail').value.trim();
      const phone = document.getElementById('contactPhone').value.trim();
      const message = document.getElementById('contactMessage').value.trim();

      if (!name || !email || !message) {
        showToast('Please enter your name, email, and message.', '⚠️');
        return;
      }

      if (!email.includes('@') || !email.includes('.')) {
        showToast('Please provide a valid email address.', '⚠️');
        return;
      }

      const originalText = sendBtn.innerHTML;
      sendBtn.disabled = true;
      sendBtn.innerHTML = `<span class="spinner"></span> <span>Saving to database...</span>`;

      try {
        const response = await fetch('/api/contact', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ name, email, phone, message })
        });

        const result = await response.json();

        if (response.ok && result.success) {
          quoteForm.reset();
          showToast(result.message || `Thank you ${name}! Dennis has received your message.`, '✉️');
        } else {
          showToast(result.error || 'Failed to send message. Please try again.', '⚠️');
        }
      } catch (err) {
        console.error('Contact form submission error:', err);
        showToast('Connection issue. Please retry or email directly at shemdennis5@gmail.com', '⚠️');
      } finally {
        sendBtn.disabled = false;
        sendBtn.innerHTML = originalText;
      }
    });
  }

  // ==========================================================================
  // 10. VISITOR & PROJECT ANALYTICS LOGGING
  // ==========================================================================
  function logEvent(eventType, targetName = '') {
    try {
      fetch('/api/track', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ event_type: eventType, target_name: targetName })
      }).catch(() => {});
    } catch (e) {}
  }

  // Log page view
  logEvent('page_view', window.location.pathname);

  // Track project clicks
  document.querySelectorAll('a[href*="onrender.com"], a[href*="pythonanywhere.com"]').forEach((link) => {
    link.addEventListener('click', () => {
      logEvent('project_click', link.getAttribute('href'));
    });
  });

  // Track CV views
  if (resumeModalBtn) {
    resumeModalBtn.addEventListener('click', () => {
      logEvent('cv_view', 'Curriculum Vitae Modal');
    });
  }

});
