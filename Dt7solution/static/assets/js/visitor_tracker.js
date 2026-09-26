(function () {
    function getCookie(name) {
        var value = "; " + document.cookie;
        var parts = value.split("; " + name + "=");
        if (parts.length === 2) return parts.pop().split(";").shift();
        return null;
    }

    function setCookie(name, value, days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        document.cookie = name + "=" + value + ";expires=" + date.toUTCString() + ";path=/";
    }

    function getVisitorId() {
        var vid = getCookie("visitor_id");
        if (!vid) {
            vid = 'v_' + Math.random().toString(36).substring(2, 11) + '_' + Date.now();
            setCookie("visitor_id", vid, 365);
        }
        return vid;
    }

    var maxScrollDepth = 0;
    var startTime = Date.now();
    var currentHistoryId = null;

    function calculateScrollDepth() {
        var winHeight = window.innerHeight || document.documentElement.clientHeight;
        var docHeight = Math.max(
            document.body.scrollHeight, document.documentElement.scrollHeight,
            document.body.offsetHeight, document.documentElement.offsetHeight,
            document.body.clientHeight, document.documentElement.clientHeight
        );
        var scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;
        if (docHeight <= winHeight) return 100;
        var depth = Math.round(((scrollTop + winHeight) / docHeight) * 100);
        return Math.min(Math.max(depth, 0), 100);
    }

    function sendTrackingPayload(isFinal) {
        var visitorId = getVisitorId();
        var currentPage = window.location.pathname + window.location.search;
        var pageTitle = document.title || "";
        var timeSpent = Math.floor((Date.now() - startTime) / 1000);
        var currentDepth = calculateScrollDepth();
        if (currentDepth > maxScrollDepth) {
            maxScrollDepth = currentDepth;
        }

        var payload = {
            visitor_id: visitorId,
            current_page: currentPage,
            page_title: pageTitle,
            scroll_depth: maxScrollDepth,
            time_spent: timeSpent,
            history_id: currentHistoryId,
            referrer: document.referrer || ""
        };

        var url = "/api/track-visitor/";

        if (isFinal && navigator.sendBeacon) {
            var blob = new Blob([JSON.stringify(payload)], { type: 'application/json' });
            navigator.sendBeacon(url, blob);
        } else {
            fetch(url, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
                keepalive: true
            })
            .then(function (res) { return res.json(); })
            .then(function (data) {
                if (data && data.history_id) {
                    currentHistoryId = data.history_id;
                }
            })
            .catch(function () {});
        }
    }


    document.addEventListener("DOMContentLoaded", function () {
        var cookieConsent = getCookie("cookieConsent");
        var modalOverlay = document.getElementById("cookieConsentModalOverlay");
        var submitBtn = document.getElementById("submitCookiePreferencesBtn");
        var acceptAllBtn = document.getElementById("acceptAllCookiesBtn");
        var declineAllBtn = document.getElementById("declineAllCookiesBtn");
        var closeXBtn = document.getElementById("closeCookieModalBtn");

        var functionalToggle = document.getElementById("functionalCookiesToggle");
        var advertisingToggle = document.getElementById("advertisingCookiesToggle");

        // Load saved preferences if available
        var savedPref = getCookie("cookiePreferences");
        if (savedPref) {
            try {
                var prefObj = JSON.parse(decodeURIComponent(savedPref));
                if (functionalToggle) functionalToggle.checked = !!prefObj.functional;
                if (advertisingToggle) advertisingToggle.checked = !!prefObj.advertising;
            } catch (e) {}
        }

        if (cookieConsent === "true") {
            // User accepted cookies previously -> Track visitor if functional enabled
            var isFunctional = true;
            if (savedPref) {
                try { isFunctional = !!JSON.parse(decodeURIComponent(savedPref)).functional; } catch(e){}
            }
            if (isFunctional) {
                sendTrackingPayload(false);
            }
        } else if (cookieConsent === "false") {
            // Declined -> Keep modal closed
            if (modalOverlay) modalOverlay.style.display = "none";
        } else {
            // Show Cookie Consent Modal Overlay for new visitors
            if (modalOverlay) modalOverlay.style.display = "flex";
        }

        // 1. Submit Preferences
        if (submitBtn) {
            submitBtn.addEventListener("click", function () {
                var funcVal = functionalToggle ? functionalToggle.checked : true;
                var advVal = advertisingToggle ? advertisingToggle.checked : true;

                var pref = { functional: funcVal, advertising: advVal };
                setCookie("cookiePreferences", encodeURIComponent(JSON.stringify(pref)), 365);
                setCookie("cookieConsent", "true", 365);

                if (modalOverlay) modalOverlay.style.display = "none";

                if (funcVal) {
                    sendTrackingPayload(false);
                }
            });
        }

        // 2. Accept All
        if (acceptAllBtn) {
            acceptAllBtn.addEventListener("click", function () {
                if (functionalToggle) functionalToggle.checked = true;
                if (advertisingToggle) advertisingToggle.checked = true;

                var pref = { functional: true, advertising: true };
                setCookie("cookiePreferences", encodeURIComponent(JSON.stringify(pref)), 365);
                setCookie("cookieConsent", "true", 365);

                if (modalOverlay) modalOverlay.style.display = "none";
                sendTrackingPayload(false);
            });
        }

        // 3. Decline All
        if (declineAllBtn) {
            declineAllBtn.addEventListener("click", function () {
                if (functionalToggle) functionalToggle.checked = false;
                if (advertisingToggle) advertisingToggle.checked = false;

                var pref = { functional: false, advertising: false };
                setCookie("cookiePreferences", encodeURIComponent(JSON.stringify(pref)), 30);
                setCookie("cookieConsent", "false", 30);

                if (modalOverlay) modalOverlay.style.display = "none";
            });
        }

        // 4. Close X Button
        if (closeXBtn) {
            closeXBtn.addEventListener("click", function () {
                if (modalOverlay) modalOverlay.style.display = "none";
            });
        }

        // Track max scroll depth if functional cookie enabled
        window.addEventListener("scroll", function () {
            if (getCookie("cookieConsent") === "true") {
                var depth = calculateScrollDepth();
                if (depth > maxScrollDepth) {
                    maxScrollDepth = depth;
                }
            }
        }, { passive: true });

        // Final payload on page unload
        window.addEventListener("visibilitychange", function () {
            if (document.visibilityState === "hidden" && getCookie("cookieConsent") === "true") {
                sendTrackingPayload(true);
            }
        });
    });
})();
