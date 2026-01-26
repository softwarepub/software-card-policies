/*
 * SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
 * SPDX-License-Identifier: CC-BY-4.0
 * SPDX-FileContributor: David Pape
 */

function orcidChecksumMatches($value, $orcid) {

    if (!$value.isURI()) {
        return false;
    }

    if (!/^https:\/\/orcid.org\/([0-9]{4}-){3}[0-9]{3}[0-9X]$/.test($value.uri)) {
        return false;
    }

    function f(t, x) {
        return 2 * (t + x);
    }

    const idString = $value.uri.slice(18).replace(/-/g, '');
    const providedChecksum = Number(idString.slice(15).replace('X', '10'));
    const digits = idString.slice(0, 15).split('').map(Number);
    const calculatedChecksum = (12 - digits.reduce(f, 0) % 11) % 11;

    return providedChecksum === calculatedChecksum;
}

