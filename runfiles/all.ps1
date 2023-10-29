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
}

# Calling the main function
main

# Read user input and convert it to lowercase
$select = (Read-Host ">> ").ToLower()

# Using the switch statement to determine the action based on user input
switch ($select)
{
    ("all") {
        Write-Host 'Starting All Tools...'
        Invoke-RestMethod 'api.heggli.dev/run/all' | Invoke-Expression
    }
    ("ping") {
        Write-Host "Starting Ping Tool..."
        Invoke-RestMethod 'api.heggli.dev/run/ping' | Invoke-Expression
    }
    ("ctt") {
        Write-Host "Starting CTT Tool..."
        Invoke-RestMethod 'irm christitus.com/win | iex' | Invoke-Expression
    }
    ("pwsh") {
        Write-Host "Starting CTT Tool..."
        Invoke-RestMethod 'api.heggli.dev/run/pwsh' | Invoke-Expression
    }
    default {
        Write-Host "Invalid selection. Please choose 'all', 'ping', or 'pwsh'...."
    }
}
