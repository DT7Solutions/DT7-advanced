/**
 * DT7 Solutions - Sequential 2-Step Anti-Spam Security Verification Script
 * Step 1: Security Question (Math Calculation) -> Once solved...
 * Step 2: Visual Security CAPTCHA Code -> Unlocks & verifies -> Enables Submit
 */
(function () {
    function generateCaptchaCode(length) {
        var chars = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"; // exclude easily confused characters (0, O, 1, I)
        var code = "";
        for (var i = 0; i < length; i++) {
            code += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return code;
    }

    function resetSecurityChallenge(container) {
        // Generate Step 1 Math
        var num1 = Math.floor(Math.random() * 12) + 2; // 2 to 13
        var num2 = Math.floor(Math.random() * 9) + 1;  // 1 to 9
        var sum = num1 + num2;
        container.setAttribute("data-expected-sum", sum);

        // Generate Step 2 CAPTCHA
        var captchaCode = generateCaptchaCode(5);
        container.setAttribute("data-expected-captcha", captchaCode);

        // Reset state
        container.setAttribute("data-step1-passed", "false");
        container.setAttribute("data-step2-passed", "false");

        // Elements
        var num1Input = container.querySelector('.math-num1-input');
        var num2Input = container.querySelector('.math-num2-input');
        var mathQuestionText = container.querySelector('.math-question-text');
        var mathAnswerInput = container.querySelector('.math-answer-input');

        var captchaCodeText = container.querySelector('.captcha-code-text');
        var captchaInput = container.querySelector('.captcha-input-field');
        var captchaExpectedInput = container.querySelector('.captcha-expected-input');

        var step1Badge = container.querySelector('.step1-status-badge');
        var step2Badge = container.querySelector('.step2-status-badge');
        var step2Box = container.querySelector('.step2-box');
        var successAlert = container.querySelector('.anti-spam-success-msg');
        var errorMsg = container.querySelector('.anti-spam-error-msg');

        if (num1Input) num1Input.value = num1;
        if (num2Input) num2Input.value = num2;
        if (mathQuestionText) mathQuestionText.textContent = "What is " + num1 + " + " + num2 + " = ?";
        if (mathAnswerInput) {
            mathAnswerInput.value = "";
            mathAnswerInput.disabled = false;
            mathAnswerInput.style.borderColor = "";
        }

        if (captchaCodeText) captchaCodeText.textContent = captchaCode.split('').join(' ');
        if (captchaExpectedInput) captchaExpectedInput.value = captchaCode;
        if (captchaInput) {
            captchaInput.value = "";
            captchaInput.style.borderColor = "";
        }

        // Hide Step 2 initially until Step 1 is done
        if (step2Box) step2Box.style.display = "none";
        if (step1Badge) {
            step1Badge.className = "badge bg-primary me-2";
            step1Badge.textContent = "Step 1 of 2";
            step1Badge.style.cssText = "background:#0284c7!important; color:#ffffff;";
        }
        if (step2Badge) {
            step2Badge.className = "badge bg-secondary me-2";
            step2Badge.textContent = "Step 2 of 2";
        }

        if (successAlert) successAlert.style.display = "none";
        if (errorMsg) errorMsg.style.display = "none";

        // Lock form submit button until both steps are done
        var form = container.closest('form');
        if (form) {
            var submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.style.opacity = "0.5";
                submitBtn.style.cursor = "not-allowed";
                submitBtn.title = "Complete 2-step security verification first";
            }
        }
    }

    function checkStep1(container) {
        var expectedSum = parseInt(container.getAttribute("data-expected-sum"), 10);
        var mathAnswerInput = container.querySelector('.math-answer-input');
        var val = mathAnswerInput ? parseInt(mathAnswerInput.value.trim(), 10) : NaN;

        var step1Badge = container.querySelector('.step1-status-badge');
        var step2Box = container.querySelector('.step2-box');
        var captchaInput = container.querySelector('.captcha-input-field');
        var errorMsg = container.querySelector('.anti-spam-error-msg');

        if (!isNaN(val) && val === expectedSum) {
            container.setAttribute("data-step1-passed", "true");
            if (step1Badge) {
                step1Badge.className = "badge bg-success me-2";
                step1Badge.textContent = "✔ Step 1 Passed";
                step1Badge.style.cssText = "background:#16a34a!important; color:#ffffff;";
            }
            if (mathAnswerInput) mathAnswerInput.style.borderColor = "#16a34a";
            if (errorMsg) errorMsg.style.display = "none";

            // Reveal Step 2 dynamically ("once done then asking second verification")
            if (step2Box && step2Box.style.display === "none") {
                step2Box.style.display = "block";
                step2Box.style.opacity = "0";
                setTimeout(function () {
                    step2Box.style.transition = "opacity 0.3s ease-in-out";
                    step2Box.style.opacity = "1";
                    if (captchaInput) captchaInput.focus();
                }, 50);
            }
            return true;
        } else {
            container.setAttribute("data-step1-passed", "false");
            if (step1Badge) {
                step1Badge.className = "badge bg-primary me-2";
                step1Badge.textContent = "Step 1 of 2";
                step1Badge.style.cssText = "background:#0284c7!important; color:#ffffff;";
            }
            if (step2Box) step2Box.style.display = "none";
            return false;
        }
    }

    function checkStep2(container) {
        var expectedCaptcha = (container.getAttribute("data-expected-captcha") || "").toUpperCase();
        var captchaInput = container.querySelector('.captcha-input-field');
        var val = captchaInput ? captchaInput.value.trim().toUpperCase() : "";

        var step2Badge = container.querySelector('.step2-status-badge');
        var successAlert = container.querySelector('.anti-spam-success-msg');
        var errorMsg = container.querySelector('.anti-spam-error-msg');
        var form = container.closest('form');
        var submitBtn = form ? form.querySelector('button[type="submit"], input[type="submit"]') : null;

        if (val.length === 5 && val === expectedCaptcha) {
            container.setAttribute("data-step2-passed", "true");
            if (step2Badge) {
                step2Badge.className = "badge bg-success me-2";
                step2Badge.textContent = "✔ Step 2 Verified!";
                step2Badge.style.cssText = "background:#16a34a!important; color:#ffffff;";
            }
            if (captchaInput) captchaInput.style.borderColor = "#16a34a";
            if (successAlert) successAlert.style.display = "block";
            if (errorMsg) errorMsg.style.display = "none";

            // Unlock Submit Button!
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.style.opacity = "1";
                submitBtn.style.cursor = "pointer";
                submitBtn.title = "Submit Form";
            }
            return true;
        } else {
            container.setAttribute("data-step2-passed", "false");
            if (step2Badge) {
                step2Badge.className = "badge bg-secondary me-2";
                step2Badge.textContent = "Step 2 of 2";
            }
            if (successAlert) successAlert.style.display = "none";
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.style.opacity = "0.5";
                submitBtn.style.cursor = "not-allowed";
            }
            return false;
        }
    }

    function initAntiSpamProtection() {
        var renderTime = (Date.now() / 1000).toString();
        var forms = document.querySelectorAll("form");

        forms.forEach(function (form) {
            if (form.getAttribute("role") === "search" || form.classList.contains("search-popup__form")) return;

            // 1. Inject Hidden Render Timestamp
            if (!form.querySelector('input[name="form_render_ts"]')) {
                var tsInput = document.createElement("input");
                tsInput.type = "hidden";
                tsInput.name = "form_render_ts";
                tsInput.value = renderTime;
                form.appendChild(tsInput);
            }

            // 2. Inject Invisible Honeypot Field
            if (!form.querySelector('input[name="hp_website_url"]')) {
                var hpInput = document.createElement("input");
                hpInput.type = "text";
                hpInput.name = "hp_website_url";
                hpInput.tabIndex = -1;
                hpInput.autocomplete = "off";
                hpInput.setAttribute("aria-hidden", "true");
                hpInput.style.cssText = "position:absolute!important;left:-9999px!important;top:-9999px!important;opacity:0!important;height:0!important;width:0!important;z-index:-1!important;";
                form.appendChild(hpInput);
            }

            // 3. Inject 2-Step Security Challenge Container
            var securityBox = form.querySelector('.anti-spam-security-container');
            if (!securityBox) {
                var submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
                if (submitBtn) {
                    securityBox = document.createElement("div");
                    securityBox.className = "anti-spam-security-container p-3 border rounded bg-light mb-3";
                    securityBox.style.cssText = "background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; margin-bottom:15px; text-align:left;";
                    securityBox.innerHTML = 
                        '<div class="d-flex align-items-center justify-content-between mb-2 pb-2 border-bottom" style="border-color:#e2e8f0!important;">' +
                            '<span class="font-weight-bold text-dark" style="font-size:13px; font-weight:700; color:#0f172a;">' +
                                '<i class="fas fa-shield-alt text-primary me-1" style="color:#0284c7;"></i> 2-Step Security Verification' +
                            '</span>' +
                            '<button type="button" class="btn btn-sm btn-link text-decoration-none p-0 refresh-all-btn" title="Refresh Security Verification" style="font-size:12px; color:#64748b;">' +
                                '<i class="fas fa-sync-alt me-1"></i> Reset' +
                            '</button>' +
                        '</div>' +

                        '<!-- Step 1: Security Question (Math Problem) -->' +
                        '<div class="step1-box mb-2 p-2 rounded" style="background:#ffffff; border:1px solid #e2e8f0;">' +
                            '<div class="d-flex align-items-center mb-1">' +
                                '<span class="step1-status-badge badge bg-primary me-2" style="background:#0284c7!important; color:#ffffff; font-size:11px; padding:4px 8px;">Step 1 of 2</span>' +
                                '<label class="form-label mb-0 font-weight-bold" style="font-size:12px; color:#1e293b; font-weight:600;">' +
                                    'Security Question: <span class="math-question-text text-danger font-weight-bold" style="color:#e11d48; font-weight:700;"></span>' +
                                '</label>' +
                            '</div>' +
                            '<input type="number" name="math_answer" class="form-control math-answer-input mt-1" placeholder="Enter calculation answer" required autocomplete="off" style="font-size:13px; height:36px; border-radius:6px;">' +
                            '<input type="hidden" name="math_num1" class="math-num1-input">' +
                            '<input type="hidden" name="math_num2" class="math-num2-input">' +
                        '</div>' +

                        '<!-- Step 2: Visual Security Code CAPTCHA (Unlocked after Step 1) -->' +
                        '<div class="step2-box mb-2 p-2 rounded" style="display:none; background:#ffffff; border:1px solid #e2e8f0;">' +
                            '<div class="d-flex align-items-center mb-2">' +
                                '<span class="step2-status-badge badge bg-secondary me-2" style="font-size:11px; padding:4px 8px;">Step 2 of 2</span>' +
                                '<label class="form-label mb-0 font-weight-bold" style="font-size:12px; color:#1e293b; font-weight:600;">' +
                                    'Enter Security Code Below:' +
                                '</label>' +
                            '</div>' +
                            '<div class="d-flex align-items-center justify-content-between mb-2 p-2 rounded" style="background:#0f172a; border:1px solid #334155;">' +
                                '<span class="captcha-code-text" style="color:#38bdf8; font-weight:800; font-family:monospace; letter-spacing:4px; font-size:18px; user-select:none;"></span>' +
                                '<span class="text-muted" style="font-size:11px; color:#94a3b8!important;">Case-Insensitive</span>' +
                            '</div>' +
                            '<input type="text" name="captcha_input" class="form-control captcha-input-field" placeholder="Type 5-character code" required autocomplete="off" style="font-size:13px; height:36px; border-radius:6px; text-transform:uppercase; letter-spacing:1px;">' +
                            '<input type="hidden" name="captcha_expected" class="captcha-expected-input">' +
                        '</div>' +

                        '<div class="anti-spam-success-msg text-success mt-2 font-weight-bold" style="display:none; font-size:12px; color:#16a34a;">' +
                            '<i class="fas fa-check-circle me-1"></i> Both security verifications passed! Submit button unlocked.' +
                        '</div>' +

                        '<div class="anti-spam-error-msg text-danger mt-2 font-weight-bold" style="display:none; font-size:12px; color:#dc2626;">' +
                            '<i class="fas fa-exclamation-circle me-1"></i> <span class="error-text">Verification failed.</span>' +
                        '</div>';

                    submitBtn.parentNode.insertBefore(securityBox, submitBtn);
                }
            }

            if (securityBox) {
                resetSecurityChallenge(securityBox);

                var refreshBtn = securityBox.querySelector('.refresh-all-btn');
                if (refreshBtn) {
                    refreshBtn.addEventListener("click", function (e) {
                        e.preventDefault();
                        resetSecurityChallenge(securityBox);
                    });
                }

                // Step 1 Input Listener -> Auto-checks & unlocks Step 2 once solved!
                var mathAnswerInput = securityBox.querySelector('.math-answer-input');
                if (mathAnswerInput) {
                    mathAnswerInput.addEventListener("input", function () {
                        checkStep1(securityBox);
                    });
                }

                // Step 2 Input Listener -> Auto-checks & unlocks Submit once matched!
                var captchaInput = securityBox.querySelector('.captcha-input-field');
                if (captchaInput) {
                    captchaInput.addEventListener("input", function () {
                        checkStep2(securityBox);
                    });
                }

                // Form Submit Safeguard
                if (!form.dataset.antiSpamInitialized) {
                    form.dataset.antiSpamInitialized = "true";
                    form.addEventListener("submit", function (e) {
                        var step1Passed = checkStep1(securityBox);
                        var step2Passed = checkStep2(securityBox);

                        if (!step1Passed || !step2Passed) {
                            e.preventDefault();
                            e.stopPropagation();

                            var errorMsg = securityBox.querySelector('.anti-spam-error-msg');
                            var errorText = securityBox.querySelector('.error-text');

                            if (errorMsg && errorText) {
                                errorMsg.style.display = "block";
                                if (!step1Passed) {
                                    errorText.textContent = "Please solve Step 1 (Security Question) first.";
                                    if (mathAnswerInput) mathAnswerInput.focus();
                                } else {
                                    errorText.textContent = "Please enter Step 2 (Security CAPTCHA Code).";
                                    if (captchaInput) captchaInput.focus();
                                }
                            }
                            return false;
                        }
                    }, true);
                }
            }
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initAntiSpamProtection);
    } else {
        initAntiSpamProtection();
    }
})();
