#!/bin/sh
# SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

# Install this hook using:
# ln -s "$PWD/pre-commit.sh" "$PWD/.git/hooks/pre-commit"

set -e

finalize () {
    rc="$?"
    if [ "$rc" -ne 0 ]; then
        echo "pre-commit hook failed" >&2
        exit "$rc"
    fi
}

trap "finalize" INT TERM EXIT

ruff check --silent .
ruff format --silent --check .
reuse lint --quiet
