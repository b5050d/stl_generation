const canvas = document.getElementById('pasteCanvas');
const ctx = canvas.getContext('2d');
const thresholdInput = document.getElementById('threshold');
const applyBtn = document.getElementById('applyBtn');
const invertBtn = document.getElementById('invertBtn');
const upBtn = document.getElementById('upBtn');
const downBtn = document.getElementById('downBtn');
const leftBtn = document.getElementById('leftBtn');
const rightBtn = document.getElementById('rightBtn');
const shrinkHBtn = document.getElementById('shrinkHBtn');
const stretchHBtn = document.getElementById('stretchHBtn');
const shrinkVBtn = document.getElementById('shrinkVBtn');
const stretchVBtn = document.getElementById('stretchVBtn');
const sendBtn = document.getElementById('sendBtn');

// Offscreen canvas holds the current grayscale/processed image
const grayCanvas = document.createElement('canvas');
grayCanvas.width = 300;
grayCanvas.height = 300;
const grayCtx = grayCanvas.getContext('2d');

// Initialize visible canvas with a light-gray background
ctx.fillStyle = '#ececec';
ctx.fillRect(0, 0, 300, 300);

function updateVisible() {
ctx.clearRect(0, 0, 300, 300);
ctx.drawImage(grayCanvas, 0, 0);
}

// === Paste Handler ===
window.addEventListener('paste', function(e) {
e.preventDefault();
const items = e.clipboardData && e.clipboardData.items;
if (!items) return;

for (let item of items) {
    if (item.kind === 'file' && item.type.startsWith('image/')) {
    const file = item.getAsFile();
    const reader = new FileReader();
    reader.onload = function(event) {
        const img = new Image();
        img.onload = function() {
        // 1) Draw and scale the pasted image into the gray offscreen canvas
        grayCtx.clearRect(0, 0, 300, 300);
        grayCtx.drawImage(img, 0, 0, 300, 300);

        // 2) Convert to grayscale
        const imageData = grayCtx.getImageData(0, 0, 300, 300);
        const data = imageData.data;
        for (let i = 0; i < data.length; i += 4) {
            const r = data[i], g = data[i + 1], b = data[i + 2];
            const gray = 0.299 * r + 0.587 * g + 0.114 * b;
            data[i] = data[i + 1] = data[i + 2] = gray;
        }
        grayCtx.putImageData(imageData, 0, 0);

        // 3) Draw the grayscale result onto the visible canvas
        updateVisible();
        };
        img.onerror = function() {
        console.error('Failed to load pasted image.');
        };
        img.src = event.target.result;
    };
    reader.readAsDataURL(file);
    break;
    }
}
});

// === Apply Threshold ===
applyBtn.addEventListener('click', () => {
const imageData = grayCtx.getImageData(0, 0, 300, 300);
const data = imageData.data;
let thresh = parseInt(thresholdInput.value, 10);
if (isNaN(thresh) || thresh < 0) thresh = 0;
if (thresh > 255) thresh = 255;

for (let i = 0; i < data.length; i += 4) {
    const gray = data[i];
    const bw = gray >= thresh ? 255 : 0;
    data[i] = data[i + 1] = data[i + 2] = bw;
}
grayCtx.putImageData(imageData, 0, 0);
updateVisible();
});

// === Invert Colors ===
invertBtn.addEventListener('click', () => {
const imageData = grayCtx.getImageData(0, 0, 300, 300);
const data = imageData.data;
for (let i = 0; i < data.length; i += 4) {
    const val = data[i];
    const inverted = 255 - val;
    data[i] = data[i + 1] = data[i + 2] = inverted;
}
grayCtx.putImageData(imageData, 0, 0);
updateVisible();
});

// === Translate Image (mode border fill) ===
function translateImage(direction) {
const w = 300, h = 300;
const src = grayCtx.getImageData(0, 0, w, h).data;
const dstData = grayCtx.createImageData(w, h);
const dst = dstData.data;

function modeBorderPixels(getIdx) {
    const counts = {};
    const countsA = {};
    const count = (direction === 'left' || direction === 'right') ? h : w;
    for (let i = 0; i < count; i++) {
    const idx = getIdx(i) * 4;
    const gray = src[idx];
    const alpha = src[idx + 3];
    counts[gray] = (counts[gray] || 0) + 1;
    countsA[alpha] = (countsA[alpha] || 0) + 1;
    }
    let modeGray = 0, modeA = 255, maxG = -1, maxA = -1;
    for (let key in counts) {
    if (counts[key] > maxG) {
        maxG = counts[key];
        modeGray = parseInt(key);
    }
    }
    for (let key in countsA) {
    if (countsA[key] > maxA) {
        maxA = countsA[key];
        modeA = parseInt(key);
    }
    }
    return { gray: modeGray, alpha: modeA };
}

let border = { gray: 0, alpha: 255 };

if (direction === 'left') {
    border = modeBorderPixels(y => (w - 1) + y * w);
    for (let y = 0; y < h; y++) {
    for (let x = 1; x < w; x++) {
        const sIdx = (x + y * w) * 4;
        const dIdx = ((x - 1) + y * w) * 4;
        dst[dIdx]     = src[sIdx];
        dst[dIdx + 1] = src[sIdx + 1];
        dst[dIdx + 2] = src[sIdx + 2];
        dst[dIdx + 3] = src[sIdx + 3];
    }
    const fillIdx = ((w - 1) + y * w) * 4;
    dst[fillIdx]     = border.gray;
    dst[fillIdx + 1] = border.gray;
    dst[fillIdx + 2] = border.gray;
    dst[fillIdx + 3] = border.alpha;
    }
} else if (direction === 'right') {
    border = modeBorderPixels(y => 0 + y * w);
    for (let y = 0; y < h; y++) {
    for (let x = 0; x < w - 1; x++) {
        const sIdx = (x + y * w) * 4;
        const dIdx = ((x + 1) + y * w) * 4;
        dst[dIdx]     = src[sIdx];
        dst[dIdx + 1] = src[sIdx + 1];
        dst[dIdx + 2] = src[sIdx + 2];
        dst[dIdx + 3] = src[sIdx + 3];
    }
    const fillIdx = (0 + y * w) * 4;
    dst[fillIdx]     = border.gray;
    dst[fillIdx + 1] = border.gray;
    dst[fillIdx + 2] = border.gray;
    dst[fillIdx + 3] = border.alpha;
    }
} else if (direction === 'up') {
    border = modeBorderPixels(x => x + (h - 1) * w);
    for (let y = 1; y < h; y++) {
    for (let x = 0; x < w; x++) {
        const sIdx = (x + y * w) * 4;
        const dIdx = (x + (y - 1) * w) * 4;
        dst[dIdx]     = src[sIdx];
        dst[dIdx + 1] = src[sIdx + 1];
        dst[dIdx + 2] = src[sIdx + 2];
        dst[dIdx + 3] = src[sIdx + 3];
    }
    }
    for (let x = 0; x < w; x++) {
    const fillIdx = (x + (h - 1) * w) * 4;
    dst[fillIdx]     = border.gray;
    dst[fillIdx + 1] = border.gray;
    dst[fillIdx + 2] = border.gray;
    dst[fillIdx + 3] = border.alpha;
    }
} else if (direction === 'down') {
    border = modeBorderPixels(x => x + 0 * w);
    for (let y = 0; y < h - 1; y++) {
    for (let x = 0; x < w; x++) {
        const sIdx = (x + y * w) * 4;
        const dIdx = (x + (y + 1) * w) * 4;
        dst[dIdx]     = src[sIdx];
        dst[dIdx + 1] = src[sIdx + 1];
        dst[dIdx + 2] = src[sIdx + 2];
        dst[dIdx + 3] = src[sIdx + 3];
    }
    }
    for (let x = 0; x < w; x++) {
    const fillIdx = (x + 0 * w) * 4;
    dst[fillIdx]     = border.gray;
    dst[fillIdx + 1] = border.gray;
    dst[fillIdx + 2] = border.gray;
    dst[fillIdx + 3] = border.alpha;
    }
}

grayCtx.putImageData(dstData, 0, 0);
updateVisible();
}

// === Shrink / Stretch Horizontally ===
function shrinkHorizontal() {
const w = 300, h = 300;
const shrinkBy = 5;
const newW = w - shrinkBy;
const offsetX = (w - newW) / 2;
const temp = document.createElement('canvas');
temp.width = w; temp.height = h;
const tCtx = temp.getContext('2d');
tCtx.drawImage(grayCanvas, 0, 0);

// Left border column data
const leftCol = tCtx.getImageData(0, 0, 1, h).data;
const countsL = {};
const countsAL = {};
for (let y = 0; y < h; y++) {
    const gray = leftCol[y * 4];
    const alpha = leftCol[y * 4 + 3];
    countsL[gray] = (countsL[gray] || 0) + 1;
    countsAL[alpha] = (countsAL[alpha] || 0) + 1;
}
let modeLeft = 0, modeAlphaL = 255, maxL = -1, maxAL = -1;
for (let key in countsL) {
    if (countsL[key] > maxL) {
    maxL = countsL[key];
    modeLeft = parseInt(key);
    }
}
for (let key in countsAL) {
    if (countsAL[key] > maxAL) {
    maxAL = countsAL[key];
    modeAlphaL = parseInt(key);
    }
}

// Right border column data
const rightCol = tCtx.getImageData(w - 1, 0, 1, h).data;
const countsR = {};
const countsAR = {};
for (let y = 0; y < h; y++) {
    const gray = rightCol[y * 4];
    const alpha = rightCol[y * 4 + 3];
    countsR[gray] = (countsR[gray] || 0) + 1;
    countsAR[alpha] = (countsAR[alpha] || 0) + 1;
}
let modeRight = 0, modeAlphaR = 255, maxR = -1, maxAR = -1;
for (let key in countsR) {
    if (countsR[key] > maxR) {
    maxR = countsR[key];
    modeRight = parseInt(key);
    }
}
for (let key in countsAR) {
    if (countsAR[key] > maxAR) {
    maxAR = countsAR[key];
    modeAlphaR = parseInt(key);
    }
}

grayCtx.clearRect(0, 0, w, h);
grayCtx.drawImage(temp, 0, 0, w, h, offsetX, 0, newW, h);

// Fill left band
grayCtx.fillStyle = `rgba(${modeLeft},${modeLeft},${modeLeft},${modeAlphaL / 255})`;
grayCtx.fillRect(0, 0, offsetX, h);

// Fill right band
const rightX = offsetX + newW;
grayCtx.fillStyle = `rgba(${modeRight},${modeRight},${modeRight},${modeAlphaR / 255})`;
grayCtx.fillRect(rightX, 0, offsetX, h);

updateVisible();
}

function stretchHorizontal() {
const w = 300, h = 300;
const expandBy = 5;
const newW = w + expandBy;
const offsetX = (w - newW) / 2;
const temp = document.createElement('canvas');
temp.width = w; temp.height = h;
const tCtx = temp.getContext('2d');
tCtx.drawImage(grayCanvas, 0, 0);

grayCtx.clearRect(0, 0, w, h);
grayCtx.drawImage(temp, 0, 0, w, h, offsetX, 0, newW, h);
updateVisible();
}

// === Shrink / Stretch Vertically ===
function shrinkVertical() {
const w = 300, h = 300;
const shrinkBy = 5;
const newH = h - shrinkBy;
const offsetY = (h - newH) / 2;
const temp = document.createElement('canvas');
temp.width = w; temp.height = h;
const tCtx = temp.getContext('2d');
tCtx.drawImage(grayCanvas, 0, 0);

// Top border row data
const topRow = tCtx.getImageData(0, 0, w, 1).data;
const countsT = {};
const countsAT = {};
for (let x = 0; x < w; x++) {
    const gray = topRow[x * 4];
    const alpha = topRow[x * 4 + 3];
    countsT[gray] = (countsT[gray] || 0) + 1;
    countsAT[alpha] = (countsAT[alpha] || 0) + 1;
}
let modeTop = 0, modeAlphaT = 255, maxT = -1, maxAT = -1;
for (let key in countsT) {
    if (countsT[key] > maxT) {
    maxT = countsT[key];
    modeTop = parseInt(key);
    }
}
for (let key in countsAT) {
    if (countsAT[key] > maxAT) {
    maxAT = countsAT[key];
    modeAlphaT = parseInt(key);
    }
}

// Bottom border row data
const bottomRow = tCtx.getImageData(0, h - 1, w, 1).data;
const countsB = {};
const countsAB = {};
for (let x = 0; x < w; x++) {
    const gray = bottomRow[x * 4];
    const alpha = bottomRow[x * 4 + 3];
    countsB[gray] = (countsB[gray] || 0) + 1;
    countsAB[alpha] = (countsAB[alpha] || 0) + 1;
}
let modeBottom = 0, modeAlphaB = 255, maxB = -1, maxAB = -1;
for (let key in countsB) {
    if (countsB[key] > maxB) {
    maxB = countsB[key];
    modeBottom = parseInt(key);
    }
}
for (let key in countsAB) {
    if (countsAB[key] > maxAB) {
    maxAB = countsAB[key];
    modeAlphaB = parseInt(key);
    }
}

grayCtx.clearRect(0, 0, w, h);
grayCtx.drawImage(temp, 0, 0, w, h, 0, offsetY, w, newH);

// Fill top band
grayCtx.fillStyle = `rgba(${modeTop},${modeTop},${modeTop},${modeAlphaT / 255})`;
grayCtx.fillRect(0, 0, w, offsetY);

// Fill bottom band
const bottomY = offsetY + newH;
grayCtx.fillStyle = `rgba(${modeBottom},${modeBottom},${modeBottom},${modeAlphaB / 255})`;
grayCtx.fillRect(0, bottomY, w, offsetY);

updateVisible();
}

function stretchVertical() {
const w = 300, h = 300;
const expandBy = 5;
const newH = h + expandBy;
const offsetY = (h - newH) / 2;
const temp = document.createElement('canvas');
temp.width = w; temp.height = h;
const tCtx = temp.getContext('2d');
tCtx.drawImage(grayCanvas, 0, 0);

grayCtx.clearRect(0, 0, w, h);
grayCtx.drawImage(temp, 0, 0, w, h, 0, offsetY, w, newH);
updateVisible();
}

// === Event Listeners ===
leftBtn.addEventListener('click', () => translateImage('left'));
rightBtn.addEventListener('click', () => translateImage('right'));
upBtn.addEventListener('click', () => translateImage('up'));
downBtn.addEventListener('click', () => translateImage('down'));

shrinkHBtn.addEventListener('click', shrinkHorizontal);
stretchHBtn.addEventListener('click', stretchHorizontal);
shrinkVBtn.addEventListener('click', shrinkVertical);
stretchVBtn.addEventListener('click', stretchVertical);

// === Send to Python ===
sendBtn.addEventListener('click', () => {
const dataURL = canvas.toDataURL('image/png');
const base64Data = dataURL.split(',')[1];

fetch('/upload_image', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image_data: base64Data })
})
.then(async (res) => {
    if (!res.ok) {
        const txt = await res.text();
        throw new Error(`Server error: ${res.status} ${txt}`);
    }
    // Get filename
    const disposition = res.headers.get('Content-Disposition');
    let filename = 'cookie_cutter.stl';
    if (disposition && disposition.includes('filename=')) {
        filename = disposition.split('filename=')[1].split(';')[0].replace(/["']/g, '');
    }
    return res.blob().then((blob) => ({ blob, filename }));
})
.then(({ blob, filename }) => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
})
.catch((err) => {
    console.error('Error sending image to Python:', err);
});
});