function main() {
    Clear-Host
    Write-Host @"
  _____  _    _ _   _   ______ _ _
 |  __ \| |  | | \ | | |  ____(_) |
 | |__) | |  | |  \| | | |__   _| | ___
 |  _  /| |  | | . ' | |  __| | | |/ _ \
 | | \ \| |__| | |\  | | |    | | |  __/
 |_|  \_\\____/|_| \_| |_|    |_|_|\___|


****************************************************************
* Copyright of Colin Heggli 2023                               *
* https://colin.heggli.dev                                     *
* https://github.com/M4rshe1                                   *
****************************************************************


"@

    Write-Host "Which RUN file do you want to run?"
    Write-Host "    All Tools           [all]"
    Write-Host "    Ping Tool           [ping]"
    Write-Host "    CTT Tool            [ctt]"
}

# Calling the main function
main

# Read user input and convert it to lowercase
$select = (Read-Host ">> ").ToLower()

# Using the switch statement to determine the action based on user input
switch ($select) {
    ("all") {
        Write-Host 'Starting All Tools...'
        irm 'https://example.com/all_tools.ps1' | iex
    }
    ("ping") {
        Write-Host "Starting Ping Tool..."
        irm 'https://example.com/ping_tool.ps1' | iex
    }
    ("ctt") {
        Write-Host "Starting CTT Tool..."
        irm 'https://example.com/ctt_tool.ps1' | iex
    }
    default {
        Write-Host "Invalid selection. Please choose 'all', 'ping', or 'ctt'."
    }
}
