/**
 * Player Search Autocomplete
 *
 * Converts text inputs with class 'player-search' into searchable fields
 * that query the /api/player_search endpoint with a 3-character minimum.
 *
 * Usage: <input type="text" name="target" class="player-search form-control"
 *               placeholder="Search player..." data-min-chars="3">
 */
(function () {
    'use strict';

    var debounceTimer;

    function debounce(fn, delay) {
        return function () {
            var args = arguments;
            var ctx = this;
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(function () {
                fn.apply(ctx, args);
            }, delay);
        };
    }

    function initPlayerSearch(input) {
        var minChars = parseInt(input.getAttribute('data-min-chars') || '3', 10);
        var wrapper = document.createElement('div');
        wrapper.className = 'player-search-wrapper';
        wrapper.style.position = 'relative';
        wrapper.style.display = 'inline-block';
        wrapper.style.width = input.style.width || '220px';
        input.parentNode.insertBefore(wrapper, input);
        wrapper.appendChild(input);
        input.style.width = '100%';
        input.setAttribute('autocomplete', 'off');

        var dropdown = document.createElement('div');
        dropdown.className = 'player-search-dropdown';
        dropdown.style.cssText =
            'display:none;position:absolute;top:100%;left:0;right:0;z-index:1000;' +
            'background:#1a1a2e;border:1px solid #444;max-height:200px;overflow-y:auto;';
        wrapper.appendChild(dropdown);

        var doSearch = debounce(function () {
            var q = input.value.trim();
            if (q.length < minChars) {
                dropdown.style.display = 'none';
                return;
            }
            fetch('/api/player_search?q=' + encodeURIComponent(q))
                .then(function (r) { return r.json(); })
                .then(function (results) {
                    dropdown.innerHTML = '';
                    if (results.length === 0) {
                        var noMatch = document.createElement('div');
                        noMatch.style.cssText = 'padding:6px 10px;color:#888;font-size:0.9em;';
                        noMatch.textContent = 'No matches found';
                        dropdown.appendChild(noMatch);
                        dropdown.style.display = 'block';
                        return;
                    }
                    results.forEach(function (p) {
                        var row = document.createElement('div');
                        row.style.cssText =
                            'padding:6px 10px;cursor:pointer;border-bottom:1px solid #333;font-size:0.9em;';
                        row.innerHTML =
                            '<span style="color:#d4a017;font-weight:bold;">' + escapeHtml(p.name) + '</span>' +
                            ' <span style="color:#888;">Lv' + p.level + ' ' + escapeHtml(p.race) +
                            ' ' + escapeHtml(p.player_class) +
                            (p.is_npc ? ' [NPC]' : '') +
                            ' (' + p.sex + ')</span>';
                        row.addEventListener('mousedown', function (e) {
                            e.preventDefault();
                            input.value = p.name;
                            dropdown.style.display = 'none';
                        });
                        row.addEventListener('mouseenter', function () {
                            row.style.background = '#2a2a4e';
                        });
                        row.addEventListener('mouseleave', function () {
                            row.style.background = '';
                        });
                        dropdown.appendChild(row);
                    });
                    dropdown.style.display = 'block';
                })
                .catch(function () {
                    dropdown.style.display = 'none';
                });
        }, 250);

        input.addEventListener('input', doSearch);
        input.addEventListener('focus', function () {
            if (input.value.trim().length >= minChars) {
                doSearch();
            }
        });
        input.addEventListener('blur', function () {
            setTimeout(function () { dropdown.style.display = 'none'; }, 200);
        });

        // Allow keyboard navigation
        input.addEventListener('keydown', function (e) {
            var items = dropdown.querySelectorAll('div[style*="cursor:pointer"]');
            if (!items.length) return;
            var active = dropdown.querySelector('.ps-active');
            var idx = -1;
            if (active) {
                for (var i = 0; i < items.length; i++) {
                    if (items[i] === active) { idx = i; break; }
                }
            }
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                if (active) active.classList.remove('ps-active');
                idx = (idx + 1) % items.length;
                items[idx].classList.add('ps-active');
                items[idx].style.background = '#2a2a4e';
                if (active) active.style.background = '';
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                if (active) active.classList.remove('ps-active');
                idx = idx <= 0 ? items.length - 1 : idx - 1;
                items[idx].classList.add('ps-active');
                items[idx].style.background = '#2a2a4e';
                if (active) active.style.background = '';
            } else if (e.key === 'Enter' && active) {
                e.preventDefault();
                active.dispatchEvent(new MouseEvent('mousedown'));
            }
        });
    }

    function escapeHtml(s) {
        var d = document.createElement('div');
        d.appendChild(document.createTextNode(s));
        return d.innerHTML;
    }

    // Initialize all player-search inputs on page load
    document.addEventListener('DOMContentLoaded', function () {
        var inputs = document.querySelectorAll('.player-search');
        for (var i = 0; i < inputs.length; i++) {
            initPlayerSearch(inputs[i]);
        }
    });
})();
