function main()
{
    Write-Host "
 _____  _    _ _   _   ______ _ _
 |  __ \| |  | | \ | | |  ____(_) |
 | |__) | |  | |  \| | | |__   _| | ___
 |  _  /| |  | | . ` | |  __| | | |/ _ \
 | | \ \| |__| | |\  | | |    | | |  __/
 |_|  \_\\____/|_| \_| |_|    |_|_|\___|



"
    Write-Host "Which RUN file do you want to run?"
    Write-Host "    All Tools           [all]"
    Write-Host "    Ping Tool           [ping]"
    Write-Host "    CTT Tool            [ctt]"
Write-Host '    All Tools as [all_tools ]'
Write-Host '    All Tools as [all_tools ]'
Write-Host '    All Tools as [all_tools ]'
#
}
$select = Read-Host ">> ".lower()

Switch ($select)
{
  ("All Tools") {
Write-Host 'Starting All Tools...'
irm api.heggli.dev/all_tools | iex
}   ("ping") {
        Write-Host "Starting Ping Tool..."
        irm api.heggli.dev/ping | iex
    }
    ("ctt") {
        Write-Host "Starting CTT Tool..."
        irm christitus.com/win | iex
    }
}