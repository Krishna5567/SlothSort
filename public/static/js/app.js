// SlothSort Frontend Controller

document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const targetDirInput = document.getElementById('target-dir-input');
    const btnPopulate = document.getElementById('btn-populate');
    const btnScan = document.getElementById('btn-scan');
    const btnProcess = document.getElementById('btn-process');
    const btnUndo = document.getElementById('btn-undo');
    const toggleLlm = document.getElementById('toggle-llm');
    const toggleTts = document.getElementById('toggle-tts');
    const toggleSlothPace = document.getElementById('toggle-sloth-pace');

    const slothMascot = document.getElementById('sloth-mascot');
    const slothTitle = document.getElementById('sloth-title');
    const slothDesc = document.getElementById('sloth-desc');
    const fileCountBadge = document.getElementById('file-count-badge');

    const filesTbody = document.getElementById('files-tbody');
    const manifestoTbody = document.getElementById('manifesto-tbody');
    const voiceMemosList = document.getElementById('voice-memos-list');
    const historyList = document.getElementById('history-list');

    // Tab buttons
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    // Tab Navigation
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            const target = btn.dataset.tab;
            const content = document.getElementById(target);
            if (content) content.classList.add('active');

            if (target === 'tab-history') {
                loadHistory();
            }
        });
    });

    // Initialize System Status
    async function loadStatus() {
        try {
            const res = await fetch('/api/status');
            const data = await res.json();
            if (data.cuda_available) {
                document.getElementById('device-text').textContent = `${data.device} (${data.vram_gb} GB VRAM)`;
            } else if (data.platform === "Vercel Serverless") {
                document.getElementById('device-text').textContent = "Vercel Cloud Showcase";
                const privacyBadge = document.getElementById('badge-privacy');
                if (privacyBadge) privacyBadge.textContent = "☁️ Cloud Interactive Demo";
            } else {
                document.getElementById('device-text').textContent = data.device || "Local CPU Inference";
            }
        } catch (err) {
            console.error("Failed to load status:", err);
        }
    }

    // Load Open Innovation Manifesto
    async function loadManifesto() {
        try {
            const res = await fetch('/api/open-innovation-stats');
            const data = await res.json();
            manifestoTbody.innerHTML = '';
            data.comparison.forEach(row => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><strong>${row.feature}</strong></td>
                    <td class="open-check">✓ ${row.open_source}</td>
                    <td class="closed-x">✗ ${row.closed_api}</td>
                `;
                manifestoTbody.appendChild(tr);
            });
        } catch (err) {
            console.error("Failed to load manifesto:", err);
        }
    }

    // Set Sloth Mascot State
    function setSlothState(state, messageTitle, messageDesc) {
        if (state === 'sleeping') {
            slothMascot.textContent = '💤';
            slothTitle.textContent = messageTitle || "Sloth Status: Deep in slow-and-steady processing...";
            slothTitle.style.color = '#38bdf8';
        } else if (state === 'happy') {
            slothMascot.textContent = '🦥';
            slothTitle.textContent = messageTitle || "Sloth Status: All done! 100% Zen restored.";
            slothTitle.style.color = '#10b981';
        } else {
            slothMascot.textContent = '🦥';
            slothTitle.textContent = messageTitle || "Sloth Status: Resting peacefully on the canopy branch";
            slothTitle.style.color = '#f59e0b';
        }
        slothDesc.textContent = messageDesc || "Everything is running offline with open-source AI.";
    }

    // Populate Sample Clutter
    btnPopulate.addEventListener('click', async () => {
        btnPopulate.disabled = true;
        setSlothState('sleeping', 'Creating messy sandbox clutter...', 'Synthesizing voice memos, mock invoices, and messy scripts.');
        try {
            const res = await fetch('/api/sandbox/populate', { method: 'POST' });
            const data = await res.json();
            if (data.success) {
                targetDirInput.value = data.sandbox_path;
                setSlothState('happy', 'Sample clutter generated!', `${data.file_count} sample messy files are ready in sandbox.`);
                await scanDirectory(data.sandbox_path);
            }
        } catch (err) {
            alert("Error populating sandbox: " + err);
        } finally {
            btnPopulate.disabled = false;
        }
    });

    // Scan Directory
    async function scanDirectory(path) {
        const dir = path !== undefined ? path : targetDirInput.value.trim();
        filesTbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding: 2rem;">Scanning directory...</td></tr>`;

        try {
            const res = await fetch('/api/scan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ directory: dir || null })
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || 'Scan failed');
            }

            const data = await res.json();
            targetDirInput.value = data.target_dir;
            fileCountBadge.textContent = `(${data.file_count})`;

            if (data.files.length === 0) {
                filesTbody.innerHTML = `
                    <tr><td colspan="6">
                        <div class="empty-state">
                            <div class="empty-icon">🍃</div>
                            <h3>Directory is squeaky clean!</h3>
                            <p>No messy files found. Click "Populate Sample Clutter" to try the demo.</p>
                        </div>
                    </td></tr>
                `;
                return;
            }

            filesTbody.innerHTML = '';
            data.files.forEach(f => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><span style="color: #94a3b8;">⏳ Pending</span></td>
                    <td><strong>${f.name}</strong></td>
                    <td style="color: var(--text-muted); font-style: italic;">Will be generated</td>
                    <td><span class="badge" style="background: #1e293b; color: #94a3b8;">Uncategorized</span></td>
                    <td style="color: var(--text-secondary); font-size: 0.8rem;">Ready for local analysis</td>
                    <td>${formatBytes(f.size_bytes)}</td>
                `;
                filesTbody.appendChild(tr);
            });

            setSlothState('chill', `Found ${data.file_count} files waiting for lazy sorting`, 'Click "Hibernate & Sort" to let open-source AI do all the work.');

        } catch (err) {
            filesTbody.innerHTML = `<tr><td colspan="6" style="color: #ef4444; padding: 2rem; text-align: center;">Error: ${err.message}</td></tr>`;
        }
    }

    btnScan.addEventListener('click', () => scanDirectory());

    // Process / Hibernate & Sort
    btnProcess.addEventListener('click', async () => {
        const dir = targetDirInput.value.trim();
        btnProcess.disabled = true;
        setSlothState('sleeping', 'Zzz... Sloth is steadily sorting and transcribing...', 'Running Whisper on GPU for voice memos and SmolLM2 for intelligent categorization.');

        try {
            const res = await fetch('/api/process', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    directory: dir || null,
                    enable_llm: toggleLlm.checked,
                    enable_tts: toggleTts.checked,
                    sloth_mode: toggleSlothPace.checked
                })
            });

            const data = await res.json();
            if (!data.success) {
                alert(data.message || "Failed to process files.");
                return;
            }

            // Render Results in Table
            filesTbody.innerHTML = '';
            fileCountBadge.textContent = `(${data.items.length})`;

            data.items.forEach(item => {
                const tr = document.createElement('tr');
                const badgeClass = getBadgeClass(item.category);

                tr.innerHTML = `
                    <td><span style="color: #10b981; font-weight: bold;">✓ Sorted</span></td>
                    <td style="color: #94a3b8; text-decoration: line-through;">${item.original_name}</td>
                    <td><strong style="color: #38bdf8;">${item.new_name}</strong></td>
                    <td><span class="badge ${badgeClass}">${item.category}</span></td>
                    <td style="max-width: 320px; font-size: 0.82rem; color: #cbd5e1;">${item.summary || item.snippet}</td>
                    <td>${formatBytes(item.size_bytes)}</td>
                `;
                filesTbody.appendChild(tr);
            });

            // Update Morning Digest Tab
            document.getElementById('digest-greeting-text').textContent = data.digest.greeting;
            document.getElementById('digest-body-text').textContent = data.digest.briefing;
            document.getElementById('stat-files').textContent = data.total_files;
            document.getElementById('stat-memos').textContent = data.voice_memos;
            document.getElementById('stat-energy').textContent = data.digest.energy_saved_pct;
            document.getElementById('stat-zen').textContent = data.digest.sloth_zen_rating;

            // Audio Player & Speech synthesis
            const audioBox = document.getElementById('digest-audio-box');
            const audioElem = document.getElementById('digest-audio');
            audioBox.style.display = 'flex';
            if (data.audio_url) {
                audioElem.src = data.audio_url;
                audioElem.style.display = 'block';
            } else {
                audioElem.style.display = 'none';
            }

            // Update Voice Memos Tab
            renderVoiceMemos(data.items);

            setSlothState('happy', 'Sorting complete! 🦥 100% human energy conserved.', 'Files organized into neat folders. Check out your Morning Digest tab!');

        } catch (err) {
            alert("Processing error: " + err);
        } finally {
            btnProcess.disabled = false;
        }
    });

    // Render Voice Memos
    function renderVoiceMemos(items) {
        const audioItems = items.filter(it => it.is_audio);
        if (audioItems.length === 0) {
            voiceMemosList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">🎙️</div>
                    <h3>No audio voice memos were found in this batch.</h3>
                </div>
            `;
            return;
        }

        voiceMemosList.innerHTML = '';
        audioItems.forEach(item => {
            const card = document.createElement('div');
            card.style.cssText = 'background: #0d1527; border: 1px solid #1e293b; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem;';
            card.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <div>
                        <strong style="color: #c084fc;">🎙️ ${item.new_name}</strong>
                        <span style="font-size: 0.8rem; color: #94a3b8; margin-left: 10px;">(Original: ${item.original_name})</span>
                    </div>
                    <span class="badge badge-voice">Whisper base (CUDA)</span>
                </div>
                <div style="background: #131d33; padding: 12px; border-radius: 8px; font-family: monospace; font-size: 0.85rem; color: #f1f5f9; line-height: 1.5; margin-bottom: 10px;">
                    "${item.transcript || 'No transcript generated'}"
                </div>
                <div style="font-size: 0.8rem; color: #10b981;">
                    ✓ Companion transcript file saved as <code>${item.new_name.replace(/\.[^/.]+$/, "")}_transcript.txt</code>
                </div>
            `;
            voiceMemosList.appendChild(card);
        });
    }

    // 1-Click Undo
    btnUndo.addEventListener('click', async () => {
        if (!confirm("Are you sure you want to undo the last organizing run and move files back?")) {
            return;
        }
        btnUndo.disabled = true;
        try {
            const res = await fetch('/api/undo', { method: 'POST' });
            const data = await res.json();
            if (data.success) {
                alert(`Undo successful! Restored ${data.restored_count} files back to original locations.`);
                await scanDirectory();
                setSlothState('chill', 'Rollback completed', 'All files have been restored safely.');
            } else {
                alert("Undo notice: " + (data.error || "No run to undo."));
            }
        } catch (err) {
            alert("Undo failed: " + err);
        } finally {
            btnUndo.disabled = false;
        }
    });

    // Load History
    async function loadHistory() {
        try {
            const res = await fetch('/api/history');
            const data = await res.json();
            if (data.length === 0) {
                historyList.innerHTML = `<div class="empty-state"><div class="empty-icon">⏳</div><h3>No past transactions found</h3></div>`;
                return;
            }

            historyList.innerHTML = '';
            data.forEach(item => {
                const dateStr = new Date(item.timestamp * 1000).toLocaleString();
                const card = document.createElement('div');
                card.style.cssText = 'background: #0d1527; border: 1px solid #1e293b; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center;';
                card.innerHTML = `
                    <div>
                        <strong style="color: var(--text-primary);">${item.run_id}</strong>
                        <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 4px;">Date: ${dateStr} | Folder: <code>${item.target_dir}</code></div>
                    </div>
                    <div>
                        <span class="badge ${item.is_undone ? 'badge-media' : 'badge-finance'}">
                            ${item.is_undone ? 'Undone / Rolled Back' : `${item.file_count} Files Sorted`}
                        </span>
                    </div>
                `;
                historyList.appendChild(card);
            });
        } catch (err) {
            console.error("Failed to load history:", err);
        }
    }

    // Helpers
    function formatBytes(bytes, decimals = 2) {
        if (!+bytes) return '0 B';
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
    }

    function getBadgeClass(cat) {
        if (!cat) return '';
        const c = cat.toLowerCase();
        if (c.includes('voice') || c.includes('audio')) return 'badge-voice';
        if (c.includes('finance') || c.includes('receipt')) return 'badge-finance';
        if (c.includes('code') || c.includes('script')) return 'badge-code';
        if (c.includes('doc') || c.includes('note')) return 'badge-doc';
        if (c.includes('media') || c.includes('graphic')) return 'badge-media';
        if (c.includes('data') || c.includes('sheet')) return 'badge-data';
        return '';
    }

    // Browser Speech Synthesis for Morning Digest
    const btnSpeakBrowser = document.getElementById('btn-speak-browser');
    if (btnSpeakBrowser) {
        btnSpeakBrowser.addEventListener('click', () => {
            const greeting = document.getElementById('digest-greeting-text').textContent;
            const text = document.getElementById('digest-body-text').textContent;
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(`${greeting}. ${text}`);
                utterance.rate = 0.9;
                utterance.pitch = 1.0;
                window.speechSynthesis.speak(utterance);
            } else {
                alert("Speech Synthesis is not supported in this browser.");
            }
        });
    }

    // Run initial loads
    loadStatus();
    loadManifesto();
});
