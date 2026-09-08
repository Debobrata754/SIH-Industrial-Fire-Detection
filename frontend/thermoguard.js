/* =========================================================
   THERMOGUARD — NTRO MONITORING DASHBOARD
   Plain vanilla JavaScript (no frameworks, no build step)
   ========================================================= */

document.addEventListener('DOMContentLoaded', function () {

    /* ---------------------------------------------------------
       0. MAP INITIALIZATION — Leaflet + hotspot markers
       --------------------------------------------------------- */

    // Create the map, centered roughly over India, inside the
    // #map-canvas div from your HTML.
    const map = L.map('map-canvas').setView([22.5, 78.9], 5);

    // Esri World Street Map tiles — free, no API key, English labels
    // everywhere (state/country names stay in English regardless of region)
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri',
        maxZoom: 19
    }).addTo(map);

    // Sample hotspot data — replace this array with your real
    // FIRMS/VIIRS data later. Each object = one dot on the map.
    const hotspots = [
        {
            facility: 'Jamnagar Refinery Complex',
            lat: 22.2394,
            lng: 70.0335,
            type: 'critical',   // critical | persistent | agri | wildfire
            frp: 142,
            confidence: 96
        },
        {
            facility: 'Tata Steel Plant',
            lat: 22.8046,
            lng: 86.2029,
            type: 'persistent',
            frp: 35,
            confidence: 89
        },
        {
            facility: 'Simlipal Forest',
            lat: 21.6,
            lng: 86.3,
            type: 'wildfire',
            frp: 12,
            confidence: 70
        },
        {
            facility: 'IOCL Panipat Refinery',
            lat: 29.39,
            lng: 76.97,
            type: 'critical',
            frp: 128,
            confidence: 94.2
        }
    ];

    // Colors matching your legend in the CSS
    const hotspotColors = {
        critical: '#DC2626',
        persistent: '#EA580C',
        agri: '#CA8A04',
        wildfire: '#4ADE80'
    };

    hotspots.forEach(function (spot) {
        const marker = L.circleMarker([spot.lat, spot.lng], {
            radius: 8,
            color: hotspotColors[spot.type],
            fillColor: hotspotColors[spot.type],
            fillOpacity: 0.8,
            weight: 2
        }).addTo(map);

        // Popup shown when clicking the dot on the map
        marker.bindPopup(
            '<strong>' + spot.facility + '</strong><br>' +
            'FRP: ' + spot.frp + ' MW<br>' +
            'Confidence: ' + spot.confidence + '%'
        );

        // Clicking a map dot also opens your inspector panel
        marker.on('click', function () {
            const inspector = document.getElementById('incident-inspector');
            inspector.querySelector('.inspector-facility').textContent = spot.facility;
            inspector.hidden = false;
        });
    });

    // Leaflet needs to recalculate its size once the map's container
    // is actually visible and at its final size — important now that
    // the map panel can be hidden behind a mobile tab at load time.
    setTimeout(function () {
        map.invalidateSize();
    }, 200);

    /* ---------------------------------------------------------
       1. CONFIDENCE SLIDER — update label live
       --------------------------------------------------------- */
    const confidenceSlider = document.getElementById('confidence-slider');
    const confidenceLabel = confidenceSlider.previousElementSibling; // the <label>

    confidenceSlider.addEventListener('input', function () {
        confidenceLabel.textContent = 'Minimum Confidence: ' + confidenceSlider.value + '%';
    });

    /* ---------------------------------------------------------
       2. FRP THRESHOLD SLIDER — update label live
       --------------------------------------------------------- */
    const frpSlider = document.getElementById('frp-slider');
    const frpLabel = frpSlider.previousElementSibling;

    frpSlider.addEventListener('input', function () {
        frpLabel.textContent = 'Minimum FRP: ' + frpSlider.value + ' MW';
    });

    /* ---------------------------------------------------------
       3. CLASSIFICATION CHECKBOXES — filter incident cards
       --------------------------------------------------------- */
    const classificationCheckboxes = document.querySelectorAll(
        '.filter-group input[name^="class-"]'
    );
    const incidentCardEls = document.querySelectorAll('.incident-card[data-classification]');

    classificationCheckboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', filterIncidents);
    });

    function filterIncidents() {
        // Which classes are currently checked
        const activeClasses = [];
        classificationCheckboxes.forEach(function (checkbox) {
            if (checkbox.checked) {
                activeClasses.push(checkbox.name);
            }
        });

        // Actually hide/show each incident card based on its
        // data-classification attribute, instead of just logging.
        incidentCardEls.forEach(function (card) {
            const cardClass = card.getAttribute('data-classification');
            const shouldShow = activeClasses.indexOf(cardClass) !== -1;
            card.classList.toggle('is-hidden', !shouldShow);
        });
    }

    /* ---------------------------------------------------------
       4. INCIDENT CARDS — click to open the inspector panel
       --------------------------------------------------------- */
    const incidentCards = document.querySelectorAll('.incident-card');
    const inspector = document.getElementById('incident-inspector');

    incidentCards.forEach(function (card) {
        card.addEventListener('click', function () {
            const facilityName = card.querySelector('.incident-facility').textContent;

            // Fill inspector with this card's info
            inspector.querySelector('.inspector-facility').textContent = facilityName;

            // Show the inspector panel
            inspector.hidden = false;

            // Scroll it into view (useful on smaller screens)
            inspector.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        });
    });

    /* ---------------------------------------------------------
       5. DATE RANGE DROPDOWN — react to selection
       --------------------------------------------------------- */
    const dateRangeSelect = document.querySelector('select[name="date-range"]');

    dateRangeSelect.addEventListener('change', function () {
        console.log('Date range changed to:', dateRangeSelect.value);
        // Hook this up later to re-fetch / re-filter hotspot data
    });

    /* ---------------------------------------------------------
       6. TIMELINE PLAYBACK BAR — play / pause / rewind / forward
       --------------------------------------------------------- */
    const timelineSlider = document.getElementById('timeline-slider');
    const btnPlay = document.getElementById('btn-play');
    const btnRewind = document.getElementById('btn-rewind');
    const btnForward = document.getElementById('btn-forward');
    const playbackDateLabel = document.getElementById('playback-date-label');

    // The scrubber represents the range from "Jan 2026" to "today".
    // This maps its 0–100 value onto that many actual days, purely
    // for the date readout — it doesn't (yet) fetch different data
    // per date. Wire that in once you have a historical FIRMS feed.
    const timelineStart = new Date(2026, 0, 1);
    const timelineEnd = new Date();
    const timelineDayCount = Math.max(
        1,
        Math.round((timelineEnd - timelineStart) / (1000 * 60 * 60 * 24))
    );

    function updatePlaybackLabel() {
        const percent = parseInt(timelineSlider.value, 10) / parseInt(timelineSlider.max, 10);
        const dayOffset = Math.round(percent * timelineDayCount);
        const currentDate = new Date(timelineStart.getTime() + dayOffset * 24 * 60 * 60 * 1000);
        playbackDateLabel.textContent = currentDate.toLocaleDateString('en-US', {
            month: 'short',
            year: 'numeric'
        });
    }

    let isPlaying = false;
    let playInterval = null;

    btnPlay.addEventListener('click', function () {
        isPlaying = !isPlaying;

        if (isPlaying) {
            btnPlay.innerHTML = '&#10074;&#10074;'; // pause icon
            btnPlay.setAttribute('aria-label', 'Pause historical timeline');
            playInterval = setInterval(function () {
                let value = parseInt(timelineSlider.value, 10);
                if (value >= parseInt(timelineSlider.max, 10)) {
                    value = 0; // loop back to start
                } else {
                    value += 1;
                }
                timelineSlider.value = value;
                updatePlaybackLabel();
            }, 200); // moves every 200ms — adjust speed here
        } else {
            btnPlay.innerHTML = '&#9654;'; // play icon
            btnPlay.setAttribute('aria-label', 'Play historical timeline');
            clearInterval(playInterval);
        }
    });

    btnRewind.addEventListener('click', function () {
        let value = parseInt(timelineSlider.value, 10);
        timelineSlider.value = Math.max(0, value - 10);
        updatePlaybackLabel();
    });

    btnForward.addEventListener('click', function () {
        let value = parseInt(timelineSlider.value, 10);
        const max = parseInt(timelineSlider.max, 10);
        timelineSlider.value = Math.min(max, value + 10);
        updatePlaybackLabel();
    });

    timelineSlider.addEventListener('input', updatePlaybackLabel);
    updatePlaybackLabel();

    /* ---------------------------------------------------------
       7. EXPORT REPORT BUTTON
       --------------------------------------------------------- */
    const exportButton = document.querySelector('.btn-export');

    exportButton.addEventListener('click', function () {
        alert('Export triggered — hook this up to your PDF/GeoJSON export logic.');
    });

    /* ---------------------------------------------------------
       8. MOBILE TAB NAV — switch which panel is visible
       --------------------------------------------------------- */
    const mobileTabs = document.querySelectorAll('.mobile-tab');

    mobileTabs.forEach(function (tab) {
        tab.addEventListener('click', function () {
            const targetId = tab.getAttribute('data-target');

            mobileTabs.forEach(function (t) {
                t.classList.toggle('is-active', t === tab);
            });

            document.querySelectorAll('.dashboard-body > .panel').forEach(function (panel) {
                panel.classList.toggle('is-active-mobile', panel.id === targetId);
            });

            // The map needs a nudge to redraw correctly the first time
            // its container becomes visible again.
            if (targetId === 'panel-map') {
                setTimeout(function () {
                    map.invalidateSize();
                }, 50);
            }
        });
    });

});