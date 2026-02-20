// Mock Data
const data = {
    audiobooks: [
        { id: 1, title: "Sariq devni minib", author: "Xudayberdi To'xtaboyev", cover: "https://images.unsplash.com/photo-1544947950-fa07a98d237f?q=80&w=200" },
        { id: 2, title: "O'tkan kunlar", author: "Abdulla Qodiriy", cover: "https://images.unsplash.com/photo-1512820790803-83ca734da794?q=80&w=200" },
        { id: 3, title: "Yulduzli tunlar", author: "Pirimqul Qodirov", cover: "https://images.unsplash.com/photo-1543004218-2bc691079bc3?q=80&w=200" }
    ],
    music: [
        { id: 1, title: "Lazgi", author: "Xorazm ansambli", cover: "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=200" },
        { id: 2, title: "Dutor navosi", author: "Milliy cholg'ular", cover: "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?q=80&w=200" }
    ]
};

let currentTab = 'audiobooks';

// DOM Elements
const itemList = document.getElementById('item-list');
const voiceBtn = document.getElementById('voice-btn');
const voiceOverlay = document.getElementById('voice-overlay');
const voiceText = document.getElementById('voice-text');
const miniPlayer = document.getElementById('mini-player');
const playerOverlay = document.getElementById('player-overlay');
const tabButtons = document.querySelectorAll('.tab-btn');

// Initialize
renderItems(currentTab);

// Tab Switching
tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        tabButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentTab = btn.dataset.tab;
        renderItems(currentTab);
    });
});

function renderItems(category) {
    itemList.innerHTML = '';
    data[category].forEach(item => {
        const card = document.createElement('div');
        card.className = 'item-card';
        card.innerHTML = `
            <img src="${item.cover}" alt="${item.title}" class="item-cover">
            <div class="item-info">
                <span class="item-title">${item.title}</span>
                <span class="item-desc">${item.author}</span>
            </div>
            <button class="play-small"><i data-lucide="play"></i></button>
        `;
        card.onclick = () => openPlayer(item);
        itemList.appendChild(card);
    });
    lucide.createIcons();
}

function openPlayer(item) {
    document.getElementById('current-title').textContent = item.title;
    document.getElementById('current-author').textContent = item.author;
    document.querySelector('.cover-art img').src = item.cover;

    playerOverlay.classList.add('open');

    // Show mini player for later
    miniPlayer.classList.remove('hidden');
    document.querySelector('.mini-subtitle').textContent = item.title;
    document.querySelector('.mini-cover').src = item.cover;
}

document.querySelector('.close-overlay').onclick = () => {
    playerOverlay.classList.remove('open');
};

miniPlayer.onclick = () => {
    playerOverlay.classList.add('open');
};

// Voice Command Simulation
voiceBtn.onclick = () => {
    toggleVoice();
};

function toggleVoice() {
    voiceOverlay.classList.remove('hidden');
    voiceText.textContent = "Eshityapman...";

    // Check for Web Speech API
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.lang = 'uz-UZ';
        recognition.start();

        recognition.onresult = (event) => {
            const command = event.results[0][0].transcript.toLowerCase();
            voiceText.textContent = `"${command}"`;
            handleCommand(command);

            setTimeout(() => {
                voiceOverlay.classList.add('hidden');
            }, 1500);
        };

        recognition.onerror = () => {
            voiceText.textContent = "Xatolik yuz berdi";
            setTimeout(() => {
                voiceOverlay.classList.add('hidden');
            }, 1000);
        };
    } else {
        voiceText.textContent = "Brauzer ovozli buyruqni qo'llab-quvvatlamaydi";
        setTimeout(() => {
            voiceOverlay.classList.add('hidden');
        }, 2000);
    }
}

function handleCommand(cmd) {
    if (cmd.includes('kitob')) {
        document.querySelector('[data-tab="audiobooks"]').click();
    } else if (cmd.includes('musiqa')) {
        document.querySelector('[data-tab="music"]').click();
    } else if (cmd.includes('qo\'y') || cmd.includes('eshitay')) {
        // Just play the first item as demo
        openPlayer(data[currentTab][0]);
    } else if (cmd.includes('to\'xta')) {
        playerOverlay.classList.remove('open');
    }
}

// Simple TTS for reading book
function speak(text) {
    const msg = new SpeechSynthesisUtterance();
    msg.text = text;
    msg.lang = 'uz-UZ';
    window.speechSynthesis.speak(msg);
}
