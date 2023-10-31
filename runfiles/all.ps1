function main()
{
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
    Write-Host "    PWSH Profile        [pwsh]"
    Write-Host '    Device Info as      [info]'
}

# Calling the main function
main

# Read user input and convert it to lowercase
$select = (Read-Host ">> ").ToLower()

# Using the switch statement to determine the action based on user input
switch ($select)
{
    ("all") {
        Clear-Host
        Write-Host 'Starting All Tools...'
        Invoke-RestMethod 'api.heggli.dev/run/all' | Invoke-Expression
    }
    ("ping") {
        Clear-Host
        Write-Host "Starting Ping Tool..."
        Invoke-RestMethod 'api.heggli.dev/run/ping' | Invoke-Expression
    }
    ("ctt") {
        Clear-Host
        Write-Host "Starting CTT Tool..."
        Invoke-RestMethod 'christitus.com/win' | Invoke-Expression
    }
    ("pwsh") {
        Clear-Host
        Write-Host "Starting CTT Tool..."
        Invoke-RestMethod 'api.heggli.dev/run/pwsh' | Invoke-Expression
    }
    ("info") {
        Clear-Host
        Write-Host "Starting Device Info..."
        Invoke-RestMethod 'api.heggli.dev/run/info' | Invoke-Expression
    }
    default {
        Write-Host "Invalid selection. Please choose 'all', 'ping', or 'pwsh'...."
    }
}
