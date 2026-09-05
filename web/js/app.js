/**
 * Supreme Feng Shui AGI System - Web UI Controller
 */

// Tab Navigation
function switchTab(tabId) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

    event.currentTarget.classList.add('active');
    const target = document.getElementById(tabId);
    if (target) {
        target.classList.add('active');
    }

    if (tabId === 'starsTab') {
        loadFlyingStars();
    } else if (tabId === 'baziTab') {
        loadBaziAndFortune();
    }
}

// 1. Submit Full Consultation
async function submitConsultation() {
    const btn = document.getElementById('btnConsult');
    const query = document.getElementById('consultQuery').value.trim() || "តើខ្ញុំគួររៀបចំគេហដ្ឋាន និងការិយាល័យយ៉ាងណាដើម្បីស្រូបយកលាភសំណាងក្នុងយុគទី ៩?";
    const birthDate = document.getElementById('profileBirthDate').value;
    const birthTime = document.getElementById('profileBirthTime').value;
    const gender = document.getElementById('profileGender').value;
    const houseDegree = parseFloat(document.getElementById('houseDegree').value) || 180.0;
    const complexReasoning = document.getElementById('enableReasoning').checked;

    const chatOutput = document.getElementById('chatOutput');

    // Append User Message
    const userMsgDiv = document.createElement('div');
    userMsgDiv.className = 'ai-msg';
    userMsgDiv.innerHTML = `
        <div class="ai-avatar" style="background:#0984e3;"><i class="fa-solid fa-user"></i></div>
        <div class="ai-bubble" style="background:rgba(9, 132, 227, 0.15); border-color:#0984e3;">
            <strong>សំណួររបស់អ្នក៖</strong><br>${query}
        </div>
    `;
    chatOutput.appendChild(userMsgDiv);
    chatOutput.scrollTop = chatOutput.scrollHeight;

    // Loading State
    btn.disabled = true;
    btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> កំពុងគណនា និងវិភាគជាមួយ MoE...`;

    try {
        const res = await fetch('/api/consult', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: query,
                birth_date: birthDate,
                birth_time: birthTime,
                gender: gender,
                house_degree: houseDegree,
                complex_reasoning: complexReasoning
            })
        });

        const data = await res.json();
        const modelBadge = document.getElementById('modelUsedBadge');
        if (modelBadge && data.model_used) {
            modelBadge.innerText = data.model_used;
        }

        // Format AI Response
        const aiMsgDiv = document.createElement('div');
        aiMsgDiv.className = 'ai-msg';
        aiMsgDiv.innerHTML = `
            <div class="ai-avatar"><i class="fa-solid fa-yin-yang"></i></div>
            <div class="ai-bubble">
                <div style="white-space: pre-wrap;">${data.synthesis || 'មិនអាចបង្កើតចម្លើយបានទេ។'}</div>
            </div>
        `;
        chatOutput.appendChild(aiMsgDiv);
        chatOutput.scrollTop = chatOutput.scrollHeight;

    } catch (err) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'ai-msg';
        errorDiv.innerHTML = `
            <div class="ai-avatar" style="background:#ff4757;"><i class="fa-solid fa-triangle-exclamation"></i></div>
            <div class="ai-bubble" style="border-color:#ff4757;">
                មានបញ្ហាក្នុងការតភ្ជាប់ API៖ ${err.message}
            </div>
        `;
        chatOutput.appendChild(errorDiv);
    } finally {
        btn.disabled = false;
        btn.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> វិភាគជាមួយ FS-Supreme-Master`;
    }
}

// 2. Direct Gua Calculation
async function calculateGuaDirect() {
    const dateInput = document.getElementById('guaDateInput');
    const birthDate = dateInput ? dateInput.value : (document.getElementById('profileBirthDate')?.value || "1988-05-15");
    const gender = document.getElementById('guaGenderInput').value;
    const resultBox = document.getElementById('guaResult');

    resultBox.innerHTML = "កំពុងគណនា...";
    try {
        const res = await fetch('/api/calculate/gua', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ birth_date: birthDate, gender: gender })
        });
        const json = await res.json();
        if (json.success) {
            const d = json.data;
            let luckyHtml = d.lucky_directions.map(i => `<li><b>${i.direction}</b> (${i.type}): ${i.meaning}</li>`).join('');
            let unluckyHtml = d.unlucky_directions.map(i => `<li><b>${i.direction}</b> (${i.type}): ${i.meaning}</li>`).join('');

            resultBox.innerHTML = `
                <div class="advice-card" style="margin-top:10px;">
                    <h4>លទ្ធផល Life Gua លេខ៖ ${d.gua_number} (${d.trigram_name}) - ${d.group}</h4>
                    <p><b>ធាតុ៖</b> ${d.element}</p>
                    ${d.li_chun_note ? `<p style="margin-top:4px; color:var(--gold);"><b>ℹ️ កំណត់សម្គាល់លីឈុន៖</b> ${d.li_chun_note}</p>` : ''}
                    <p style="margin-top:8px; color:var(--jade);"><b>✨ ទិសល្អទាំង ៤៖</b></p>
                    <ul style="padding-left:18px;">${luckyHtml}</ul>
                    <p style="margin-top:8px; color:var(--crimson);"><b>⚠️ ទិសគួរជៀសវាង៖</b></p>
                    <ul style="padding-left:18px;">${unluckyHtml}</ul>
                </div>
            `;
        }
    } catch (e) {
        resultBox.innerHTML = `<span style="color:var(--crimson);">កំហុស៖ ${e.message}</span>`;
    }
}

// 3. Compass Needle Update
function updateCompass(val) {
    const needle = document.querySelector('.needle');
    if (needle) {
        needle.style.transform = `rotate(${val}deg)`;
    }
    const info = document.getElementById('mountainInfo');
    if (info) {
        let dirName = "ខាងជើង (North)";
        if (val >= 337.5 || val < 22.5) dirName = "壬/子/癸 (ខាងជើង ធាតុទឹក)";
        else if (val >= 22.5 && val < 67.5) dirName = "丑/艮/寅 (ឦសាន ធាតុដី)";
        else if (val >= 67.5 && val < 112.5) dirName = "甲/卯/乙 (ខាងកើត ធាតុឈើ)";
        else if (val >= 112.5 && val < 157.5) dirName = "辰/巽/巳 (អាគ្នេយ៍ ធាតុឈើ)";
        else if (val >= 157.5 && val < 202.5) dirName = "丙/午/丁 (ខាងត្បូង ធាតុភ្លើង)";
        else if (val >= 202.5 && val < 247.5) dirName = "未/坤/申 (និរតី ធាតុដី)";
        else if (val >= 247.5 && val < 292.5) dirName = "庚/酉/辛 (ខាងលិច ធាតុមាស)";
        else dirName = "戌/乾/亥 (ពាយ័ព្យ ធាតុមាស)";

        info.innerText = `ទិសបច្ចុប្បន្ន៖ ${val}° - ${dirName}`;
    }
}

let selectedFlyingStarsYear = 2026;

function setFlyingStarsYear(year, btn) {
    selectedFlyingStarsYear = year;
    if (btn) {
        document.querySelectorAll('.year-selector .chip-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    }
    loadFlyingStars();
}

// 4. Load Complete Xuan Kong 24 Mountains House Natal Chart
async function loadFlyingStars() {
    const gridEl = document.getElementById('flyingStarGrid');
    const badgeEl = document.getElementById('chartMetaBadge');
    const castleBox = document.getElementById('castleGateBox');
    const adviceBox = document.getElementById('starAdviceBox');

    if (!gridEl) return;
    gridEl.innerHTML = "<div style='grid-column: 1 / -1; text-align:center; padding:20px; color:var(--gold);'>កំពុងគណនាតារាងជោគជតាភូមិគ្រឹះ ស្វៀនខុង...</div>";

    const degreeInput = document.getElementById('houseNatalDegree');
    const periodInput = document.getElementById('houseNatalPeriod');
    const facingDegree = degreeInput ? parseFloat(degreeInput.value || 180) : 180;
    const period = periodInput ? parseInt(periodInput.value || 9) : 9;
    const year = selectedFlyingStarsYear || 2026;

    try {
        const res = await fetch('/api/calculate/house-flying-stars', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                facing_degree: facingDegree,
                period: period,
                year: year
            })
        });
        const json = await res.json();
        if (json.success) {
            const data = json.data;
            const natal = data.natal_chart;

            // Update Badge
            if (badgeEl) {
                badgeEl.style.display = "block";
                const formName = data.formations && data.formations.length > 0 ? data.formations[0].name_kh : "ទម្រង់ធម្មតា";
                badgeEl.innerHTML = `
                    <strong>ទម្រង់ហុងស៊ុយ៖</strong> ${formName} •
                    <strong>អង្គុយ/បែរ៖</strong> 坐 ${data.sitting.mountain} (${data.sitting.degree}°) 向 ${data.facing.mountain} (${data.facing.degree}°) •
                    <strong>ប្រភេទប្លង់៖</strong> ${data.chart_mode}
                `;
            }

            // Render 3x3 Lo Shu layout: SE, S, SW, E, CENTER, W, NE, N, NW
            const layout = ["SE", "S", "SW", "E", "CENTER", "W", "NE", "N", "NW"];
            let html = "";
            layout.forEach(pos => {
                const cell = natal[pos];
                const isCenter = pos === "CENTER";
                const isFacing = cell.is_facing_palace ? "border: 2px solid #ff7675;" : "";
                const isSitting = cell.is_sitting_palace ? "border: 2px solid #00cec9;" : "";
                const tag = cell.is_facing_palace ? "<span style='color:#ff7675;'>[ទិសមុខ]</span> " : (cell.is_sitting_palace ? "<span style='color:#00cec9;'>[ទិសអង្គុយ]</span> " : "");

                html += `
                    <div class="star-cell ${isCenter ? 'center-cell' : ''}" style="${isFacing || isSitting}">
                        <div class="star-palace">${tag}${pos} (${cell.palace_kh.split(' ')[0]})</div>
                        <div class="natal-star-box">
                            <span class="natal-m-star" title="ផ្កាយភ្នំ Mountain Star (សុខភាព/មនុស្ស)">${cell.mountain_star}</span>
                            <span class="natal-w-star" title="ផ្កាយទឹក Water Star (ទ្រព្យសម្បត្តិ/លុយកាក់)">${cell.water_star}</span>
                        </div>
                        <div class="natal-p-star" title="ផ្កាយយុគ Period Star">${cell.period_star}</div>
                        <div class="natal-a-badge" title="ផ្កាយប្រចាំឆ្នាំ Annual Star">${year}: ${cell.annual_star}</div>
                        <div class="star-title" style="font-size:0.7rem; margin-top:4px;">${cell.cure_advice.split('៖')[0]}</div>
                    </div>
                `;
            });
            gridEl.innerHTML = html;

            // Castle Gates & Ling Shen guidance box
            if (castleBox && data.castle_gates) {
                castleBox.style.display = "block";
                const cg = data.castle_gates;
                const zs = data.ling_shen_zheng_shen;
                castleBox.innerHTML = `
                    <h4>🏰 ក្បួនទ្វារបន្ទាយ (Castle Gate Formula) & វិញ្ញាណសូន្យ (Ling Shen Period 9)</h4>
                    <p><strong>ទ្វារបន្ទាយឆ្វេង (${cg.left_castle_gate.palace})៖</strong> ${cg.left_castle_gate.status_kh} - ${cg.left_castle_gate.advice}</p>
                    <p><strong>ទ្វារបន្ទាយស្តាំ (${cg.right_castle_gate.palace})៖</strong> ${cg.right_castle_gate.status_kh} - ${cg.right_castle_gate.advice}</p>
                    <p style="margin-top:6px; border-top:1px dashed rgba(255,255,255,0.15); padding-top:6px;">
                        <strong>${zs.period}៖</strong><br>
                        • ${zs.ling_shen_rule}<br>
                        • ${zs.zheng_shen_rule}
                    </p>
                `;
            }

            if (adviceBox && data.practical_advice) {
                adviceBox.innerHTML = `
                    <h4>💡 ការវិភាគលម្អិត និងដំបូន្មានហុងស៊ុយគេហដ្ឋាន</h4>
                    <p>${data.practical_advice}</p>
                `;
            }
        }
    } catch (e) {
        gridEl.innerHTML = `<div style='grid-column: 1 / -1; color:#ff7675;'>កំហុសក្នុងការគណនាតារាហោះ៖ ${e.message}</div>`;
    }
}

// 5. Load BaZi and Fortune
async function loadBaziAndFortune() {
    const birthDate = document.getElementById('profileBirthDate').value || "1988-05-15";
    const birthTime = document.getElementById('profileBirthTime').value || "10:30";

    const baziGrid = document.getElementById('baziPillars');
    const dmBox = document.getElementById('dayMasterBox');
    const remedyBox = document.getElementById('dailyRemedyBox');

    try {
        // BaZi Call
        const baziRes = await fetch('/api/calculate/bazi', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ birth_date: birthDate, birth_time: birthTime })
        });
        const baziJson = await baziRes.json();
        if (baziJson.success) {
            const p = baziJson.data.pillars;
            baziGrid.innerHTML = `
                <div class="pillar-card">
                    <div class="pillar-name">សសរស្តម្ភឆ្នាំ</div>
                    <div class="pillar-ganzhi">${p.year.ganzhi}</div>
                    <div style="font-size:0.75rem; color:var(--text-muted); margin-top:4px;">藏干: ${p.year.hidden_stems ? p.year.hidden_stems.join(' ') : ''}</div>
                </div>
                <div class="pillar-card">
                    <div class="pillar-name">សសរស្តម្ភខែ</div>
                    <div class="pillar-ganzhi">${p.month.ganzhi}</div>
                    <div style="font-size:0.75rem; color:var(--text-muted); margin-top:4px;">藏干: ${p.month.hidden_stems ? p.month.hidden_stems.join(' ') : ''}</div>
                </div>
                <div class="pillar-card">
                    <div class="pillar-name">សសរស្តម្ភថ្ងៃ (Day Master)</div>
                    <div class="pillar-ganzhi" style="color:var(--gold); font-weight:800;">${p.day.ganzhi}</div>
                    <div style="font-size:0.75rem; color:var(--text-muted); margin-top:4px;">藏干: ${p.day.hidden_stems ? p.day.hidden_stems.join(' ') : ''}</div>
                </div>
                <div class="pillar-card">
                    <div class="pillar-name">សសរស្តម្ភម៉ោង</div>
                    <div class="pillar-ganzhi">${p.time.ganzhi}</div>
                    <div style="font-size:0.75rem; color:var(--text-muted); margin-top:4px;">藏干: ${p.time.hidden_stems ? p.time.hidden_stems.join(' ') : ''}</div>
                </div>
            `;
            dmBox.innerHTML = `
                <div class="advice-card">
                    <strong>សង្ក្រាន្តសូរ្យគតិ (Jie Qi):</strong> ${baziJson.data.solar_term || 'សង្ក្រាន្តទូទៅ'}<br>
                    <strong>Day Master (អត្តសញ្ញាណ):</strong> ${baziJson.data.day_master.element} (${baziJson.data.day_master.nature})<br>
                    <strong>តុល្យភាព និងឱសថធាតុ (Yong Shen):</strong> ${baziJson.data.recommendation}
                </div>
            `;
        }

        // Fortune Call
        const predRes = await fetch('/api/predict/fortune', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ birth_date: birthDate, birth_time: birthTime })
        });
        const predJson = await predRes.json();
        if (predJson.success) {
            const d = predJson.data;
            document.getElementById('luckOverallVal').innerText = `${d.overall_luck.score}% (${d.overall_luck.level})`;
            document.getElementById('luckOverallBar').style.width = `${d.overall_luck.score}%`;

            document.getElementById('luckWealthVal').innerText = `${d.wealth_luck.score}%`;
            document.getElementById('luckWealthBar').style.width = `${d.wealth_luck.score}%`;

            document.getElementById('luckCareerVal').innerText = `${d.career_luck.score}%`;
            document.getElementById('luckCareerBar').style.width = `${d.career_luck.score}%`;

            document.getElementById('luckLoveVal').innerText = `${d.love_luck.score}%`;
            document.getElementById('luckLoveBar').style.width = `${d.love_luck.score}%`;

            document.getElementById('luckHealthVal').innerText = `${d.health_luck.score}%`;
            document.getElementById('luckHealthBar').style.width = `${d.health_luck.score}%`;

            remedyBox.innerHTML = `
                <h4>⏰ ម៉ោងល្អប្រចាំថ្ងៃ៖</h4>
                <p>${d.auspicious_hours.join(' • ')}</p>
                <h4 style="margin-top:8px;">💡 ដំបូន្មានកែតម្រូវ៖</h4>
                <p>${d.daily_remedy}</p>
            `;
        }
    } catch (e) {
        console.error("Error loading BaZi:", e);
    }
}

// 6. Super Smart Hybrid Memory Telemetry Poller
async function updateMemoryTelemetry() {
    const statusText = document.getElementById('systemStatusText');
    if (!statusText) return;

    try {
        const res = await fetch('/health');
        if (res.ok) {
            const data = await res.json();
            const ramMb = data.process_ram_used_mb || 48;
            const swapTotal = data.swap_total_mb || 4096;
            statusText.innerHTML = `⚡ Hybrid RAM: ${ramMb}MB used / ~${Math.round(data.effective_total_ram_mb || 5120)}MB (zRAM+Swap)`;
        }
    } catch (e) {
        statusText.innerText = "⚡ MoE Active • Super Smart RAM";
    }
}

// 7. Curriculum Center Logic (100 Topics & 1,000 Lessons)
let currentCategory = 'CAT1';
let currentLessonId = 1;
let allTopics = [];

async function loadCurriculumTopics(categoryId) {
    currentCategory = categoryId;
    const listEl = document.getElementById('curriculumTopicsList');
    if (!listEl) return;

    listEl.innerHTML = '<div style="color:var(--text-muted); padding:10px;">⏳ កំពុងផ្ទុកប្រធានបទ...</div>';

    try {
        const res = await fetch(`/api/curriculum/topics?category_id=${categoryId}`);
        const json = await res.json();
        if (json.success) {
            allTopics = json.data;
            renderTopicsList(allTopics);
        }
    } catch (e) {
        listEl.innerHTML = `<div style="color:#ff4757;">❌ បរាជ័យក្នុងការផ្ទុកប្រធានបទ៖ ${e.message}</div>`;
    }
}

function selectCurriculumCategory(catId) {
    document.querySelectorAll('.cat-chip').forEach(chip => {
        chip.classList.toggle('active', chip.getAttribute('onclick').includes(catId));
    });
    loadCurriculumTopics(catId);
}

function renderTopicsList(topics) {
    const listEl = document.getElementById('curriculumTopicsList');
    if (!listEl) return;

    if (topics.length === 0) {
        listEl.innerHTML = '<div style="color:var(--text-muted); padding:10px;">រកមិនឃើញប្រធានបទ។</div>';
        return;
    }

    listEl.innerHTML = topics.map(t => `
        <div class="topic-item" id="topic_item_${t.topic_id}">
            <div class="topic-item-header" onclick="toggleTopicLessons(${t.topic_id})">
                <span>📌 ប្រធានបទ ${t.topic_id}: ${t.name_kh}</span>
                <span style="font-size:0.75rem; color:var(--gold);">មេរៀន ${t.lesson_start}-${t.lesson_end}</span>
            </div>
            <div class="topic-item-desc">${t.summary}</div>
            <div class="lesson-sub-list" id="sub_list_${t.topic_id}" style="display:none;"></div>
        </div>
    `).join('');
}

async function toggleTopicLessons(topicId) {
    const subList = document.getElementById(`sub_list_${topicId}`);
    if (!subList) return;

    if (subList.style.display === 'flex') {
        subList.style.display = 'none';
        return;
    }

    subList.style.display = 'flex';
    subList.innerHTML = '<div style="font-size:0.75rem; color:var(--text-muted);">⏳ កំពុងទាញមេរៀន...</div>';

    try {
        const res = await fetch(`/api/curriculum/topic/${topicId}`);
        const json = await res.json();
        if (json.success && json.data.lessons) {
            subList.innerHTML = json.data.lessons.map(les => `
                <div class="lesson-sub-item ${les.lesson_id === currentLessonId ? 'active' : ''}" 
                     onclick="event.stopPropagation(); loadLessonDetails(${les.lesson_id});">
                    📖 មេរៀន ${les.lesson_id}: ${les.sub_topic_kh}
                </div>
            `).join('');
        }
    } catch (e) {
        subList.innerHTML = `<div style="color:#ff4757; font-size:0.75rem;">កំហុស៖ ${e.message}</div>`;
    }
}

function filterTopics(query) {
    if (!query) {
        renderTopicsList(allTopics);
        return;
    }
    const q = query.toLowerCase().trim();
    const num = parseInt(q);
    if (!isNaN(num) && num >= 1 && num <= 1000) {
        loadLessonDetails(num);
    }

    const filtered = allTopics.filter(t => 
        t.name_kh.toLowerCase().includes(q) ||
        t.name_en.toLowerCase().includes(q) ||
        t.summary.toLowerCase().includes(q) ||
        (num >= t.lesson_start && num <= t.lesson_end)
    );
    renderTopicsList(filtered);
}

async function loadLessonDetails(lessonId) {
    currentLessonId = lessonId;
    const titleEl = document.getElementById('lessonTitleHeader');
    const badgeEl = document.getElementById('lessonNumberBadge');
    const catBadge = document.getElementById('lessonCatBadge');
    const topicBadge = document.getElementById('lessonTopicBadge');
    const ruleEl = document.getElementById('lessonClassicalRule');
    const formulaEl = document.getElementById('lessonFormula');
    const remedyEl = document.getElementById('lessonRemedy');
    const expBox = document.getElementById('aiExplanationBox');
    const prevBtn = document.getElementById('btnPrevLesson');
    const nextBtn = document.getElementById('btnNextLesson');

    if (expBox) expBox.style.display = 'none';

    try {
        const res = await fetch(`/api/curriculum/lesson/${lessonId}`);
        const json = await res.json();
        if (json.success) {
            const pillarBadge = document.getElementById('lessonPillarBadge');
            const pGeo = document.getElementById('pillarGeo');
            const pQi = document.getElementById('pillarQi');
            const pTime = document.getElementById('pillarTime');
            const pBaZi = document.getElementById('pillarBaZi');
            const tabooEl = document.getElementById('lessonTaboo');

            if (titleEl) titleEl.innerText = les.title_kh;
            if (badgeEl) badgeEl.innerText = `មេរៀន ${les.lesson_id}/1000`;
            if (catBadge) catBadge.innerText = `${les.category_icon} ${les.category_name}`;
            if (topicBadge) topicBadge.innerText = `ប្រធានបទទី ${les.topic_id}: ${les.topic_title_kh}`;
            if (pillarBadge) pillarBadge.innerText = les.active_pillar || "🏛️ 7 Pillars Core";
            if (ruleEl) ruleEl.innerText = les.classical_rule;
            if (formulaEl) formulaEl.innerText = les.formula;
            if (remedyEl) remedyEl.innerText = les.practical_remedy;
            if (pGeo) pGeo.innerText = les.geo_analysis || "ស្របតាមរាងទ្រង់ដី និងជញ្ជាំងអគារ";
            if (pQi) pQi.innerText = les.qi_analysis || "លំហូរខ្យល់ដង្ហើម Sheng Qi វិជ្ជមាន";
            if (pTime) pTime.innerText = les.time_analysis || "យុគទី ៩ (2024-2043) Li Fire";
            if (pBaZi) pBaZi.innerText = les.bazi_synergy || "ទ្រទ្រង់ធាតុ Yong Shen នៃម្ចាស់ជោគជតា";
            if (tabooEl) tabooEl.innerText = les.taboo_warning || "ជៀសវាងការប៉ះទង្គិចធាតុ";

            if (prevBtn) prevBtn.disabled = !les.prev_lesson_id;
            if (nextBtn) nextBtn.disabled = !les.next_lesson_id;

            // Highlight active lesson in sidebar
            document.querySelectorAll('.lesson-sub-item').forEach(item => {
                item.classList.toggle('active', item.innerText.includes(`មេរៀន ${lessonId}:`));
            });
        }
    } catch (e) {
        console.error("Error loading lesson:", e);
    }
}

function navigateLesson(direction) {
    const targetId = currentLessonId + direction;
    if (targetId >= 1 && targetId <= 1000) {
        loadLessonDetails(targetId);
    }
}

async function requestDeepAIExplanation() {
    const btn = document.getElementById('btnDeepExplain');
    const expBox = document.getElementById('aiExplanationBox');
    const expContent = document.getElementById('aiExpContent');

    if (!expBox || !expContent) return;

    btn.disabled = true;
    btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> កំពុងដំណើរការ AI Master...`;
    expBox.style.display = 'block';
    expContent.innerHTML = `<div style="color:var(--gold);">⏳ ម៉ូដែល FS-Supreme-Master កំពុងសំយោគក្បួនមេរៀនទី ${currentLessonId}...</div>`;

    try {
        const res = await fetch(`/api/curriculum/lesson/${currentLessonId}/explain`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const json = await res.json();
        if (json.success) {
            expContent.innerText = json.deep_explanation;
        } else {
            expContent.innerText = `❌ កំហុស៖ ${json.error || 'មិនអាចបង្កើតបាន'}`;
        }
    } catch (e) {
        expContent.innerText = `❌ កំហុសតភ្ជាប់ API៖ ${e.message}`;
    } finally {
        btn.disabled = false;
        btn.innerHTML = `<i class="fa-solid fa-brain"></i> ពន្យល់លម្អិតជាមួយ AI Master`;
    }
}

// Initial Setup
document.addEventListener('DOMContentLoaded', () => {
    updateCompass(180);
    updateMemoryTelemetry();
    loadCurriculumTopics('CAT1');
    loadLessonDetails(1);
    setInterval(updateMemoryTelemetry, 10000);
});
