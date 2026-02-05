(function () {
    const CITY_COOKIE = "user_city";
    const RELOAD_FLAG = "geo_reloaded_once";

    function getCookie(name) {
        return document.cookie
            .split("; ")
            .find(row => row.startsWith(name + "="))
            ?.split("=")[1];
    }

    function isAboutPage() {
        return window.location.pathname.endsWith("/about/");
    }

    function alreadyOnCityAbout(city) {
        return window.location.pathname === `/${city}/about/`;
    }

    function reloadOnce() {
        if (!sessionStorage.getItem(RELOAD_FLAG)) {
            sessionStorage.setItem(RELOAD_FLAG, "true");
            window.location.reload();
        }
    }

    document.addEventListener("DOMContentLoaded", function () {

        const existingCity = getCookie(CITY_COOKIE);

        /* ===============================
           1️⃣ Cookie already exists
        =============================== */
        if (existingCity) {
            if (isAboutPage() && !alreadyOnCityAbout(existingCity)) {
                window.location.replace(`/${existingCity}/about/`);
                return;
            }
            return; // nothing else to do
        }

        /* ===============================
           2️⃣ Cookie missing → ask geo
        =============================== */
        if (!("geolocation" in navigator)) return;

        navigator.geolocation.getCurrentPosition(
            function (pos) {
                fetch("/set-location/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    body: JSON.stringify({
                        lat: pos.coords.latitude,
                        lng: pos.coords.longitude
                    })
                })
                .then(res => res.json())
                .then(data => {
                    if (!data.city) return;

                    // 🔁 Auto reload after location ACCEPTED
                    reloadOnce();

                    // About page handling
                    if (isAboutPage() && !alreadyOnCityAbout(data.city)) {
                        window.location.replace(`/${data.city}/about/`);
                    }
                });
            },
            function () {
                // Permission denied / location OFF → fallback
                fetch("/set-location/")
                    .then(res => res.json())
                    .then(data => {
                        if (!data.city) return;

                        reloadOnce();

                        if (isAboutPage() && !alreadyOnCityAbout(data.city)) {
                            window.location.replace(`/${data.city}/about/`);
                        }
                    });
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
    });

    /* ===============================
       Optional: clear location button
    =============================== */
    window.clearLocation = function () {
        document.cookie = `${CITY_COOKIE}=; path=/; max-age=0`;
        sessionStorage.removeItem(RELOAD_FLAG);
        window.location.reload();
    };

})();
