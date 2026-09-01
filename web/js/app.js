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
        loadFlyingStars(2024);
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
    const year = parseInt(document.getElementById('guaYearInput').value) || 1988;
    const gender = document.getElementById('guaGenderInput').value;
    const resultBox = document.getElementById('guaResult');

    resultBox.innerHTML = "កំពុងគណនា...";
    try {
        const res = await fetch('/api/calculate/gua', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ birth_year: year, gender: gender })
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

// 4. Load Flying Stars Grid
async function loadFlyingStars(year) {
    const gridEl = document.getElementById('flyingStarGrid');
    gridEl.innerHTML = "កំពុងផ្ទុកតារាហោះ...";

    try {
        const res = await fetch('/api/calculate/flying-stars', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ year: year })
        });
        const json = await res.json();
        if (json.success) {
            const grid = json.data.grid;
            const layout = ["SE", "S", "SW", "E", "CENTER", "W", "NE", "N", "NW"];
            let html = "";
            layout.forEach(pos => {
                const cell = grid[pos];
                const isCenter = pos === "CENTER";
                html += `
                    <div class="star-cell ${isCenter ? 'center-cell' : ''}">
                        <div class="star-palace">${pos}</div>
                        <div class="star-number">${cell.star_number}</div>
                        <div class="star-title">${cell.details.name || ''}</div>
                    </div>
                `;
            });
            gridEl.innerHTML = html;
        }
    } catch (e) {
        gridEl.innerHTML = `កំហុស៖ ${e.message}`;
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
                <div class="pillar-card"><div class="pillar-name">សសរស្តម្ភឆ្នាំ</div><div class="pillar-ganzhi">${p.year.ganzhi}</div></div>
                <div class="pillar-card"><div class="pillar-name">សសរស្តម្ភខែ</div><div class="pillar-ganzhi">${p.month.ganzhi}</div></div>
                <div class="pillar-card"><div class="pillar-name">សសរស្តម្ភថ្ងៃ</div><div class="pillar-ganzhi">${p.day.ganzhi}</div></div>
                <div class="pillar-card"><div class="pillar-name">សសរស្តម្ភម៉ោង</div><div class="pillar-ganzhi">${p.time.ganzhi}</div></div>
            `;
            dmBox.innerHTML = `
                <div class="advice-card">
                    <strong>Day Master (អត្តសញ្ញាណ):</strong> ${baziJson.data.day_master.element} (${baziJson.data.day_master.nature})<br>
                    <strong>តុល្យភាពធាតុ៖</strong> ${baziJson.data.recommendation}
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

// Initial Setup
document.addEventListener('DOMContentLoaded', () => {
    updateCompass(180);
    updateMemoryTelemetry();
    setInterval(updateMemoryTelemetry, 10000);
});
