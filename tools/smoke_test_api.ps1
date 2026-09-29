# End to end smoke test of the BankFlow API.
#
#   powershell -ExecutionPolicy Bypass -File tools\smoke_test_api.ps1
#   powershell -ExecutionPolicy Bypass -File tools\smoke_test_api.ps1 -BaseUrl http://127.0.0.1:8001/api
#
# It registers one throwaway demo customer, exercises every customer and employee endpoint,
# and prints a PASS or FAIL line for each check. The loan lifecycle runs on the throwaway
# account so the documented demo customer stays exactly as seeded.
# Run "python manage.py seed_demo --flush" afterwards to remove the throwaway accounts.
param(
    [string]$BaseUrl = "http://127.0.0.1:8000/api",
    [string]$CustomerEmail = "mohammed@bankflow.com",
    [string]$CustomerPassword = "Demo@12345",
    [string]$AdminEmail = "admin@bankflow.com",
    [string]$AdminPassword = "Admin@12345"
)

$ErrorActionPreference = "Stop"
$script:passed = 0
$script:failed = 0

function Check {
    param([string]$Name, [scriptblock]$Action)
    try {
        $result = & $Action
        if ($result) {
            Write-Output ("PASS  " + $Name)
            $script:passed++
        } else {
            Write-Output ("FAIL  " + $Name)
            $script:failed++
        }
    } catch {
        Write-Output ("FAIL  " + $Name + "  -> " + $_.Exception.Message)
        $script:failed++
    }
}

function Status {
    param([scriptblock]$Action)
    try { & $Action | Out-Null; return 200 } catch { return [int]$_.Exception.Response.StatusCode.value__ }
}

Write-Output "BankFlow API smoke test against $BaseUrl"
Write-Output ("-" * 62)

# ------------------------------------------------------------------ anonymous
Check "register creates a demo customer" {
    $email = "verify+" + (Get-Date -Format "yyyyMMddHHmmss") + "@bankflow.com"
    $body = @{
        name = "Verification Customer"; email = $email; phone = "+91 90000 00001"
        password = "Verify@12345"; confirm_password = "Verify@12345"
    } | ConvertTo-Json
    $response = Invoke-RestMethod -Method Post -Uri "$BaseUrl/auth/register/" -ContentType "application/json" -Body $body
    $script:newUserEmail = $email
    $script:newUserPassword = "Verify@12345"
    $login = Invoke-RestMethod -Method Post -Uri "$BaseUrl/auth/login/" -ContentType "application/json" `
        -Body (@{ email = $email; password = "Verify@12345" } | ConvertTo-Json)
    $script:newUserHeaders = @{ Authorization = "Bearer $($login.access)" }
    $response.user.email -eq $email
}

Check "new account cannot open the dashboard without a token" {
    (Status { Invoke-RestMethod -Uri "$BaseUrl/dashboard/" }) -eq 401
}

Check "login returns access and refresh tokens" {
    $response = Invoke-RestMethod -Method Post -Uri "$BaseUrl/auth/login/" -ContentType "application/json" `
        -Body (@{ email = $CustomerEmail; password = $CustomerPassword } | ConvertTo-Json)
    $script:customerHeaders = @{ Authorization = "Bearer $($response.access)" }
    $script:refresh = $response.refresh
    [bool]$response.access -and [bool]$response.refresh
}

Check "refresh exchanges a refresh token" {
    $response = Invoke-RestMethod -Method Post -Uri "$BaseUrl/auth/refresh/" -ContentType "application/json" `
        -Body (@{ refresh = $script:refresh } | ConvertTo-Json)
    [bool]$response.access
}

Check "wrong password is rejected" {
    (Status {
        Invoke-RestMethod -Method Post -Uri "$BaseUrl/auth/login/" -ContentType "application/json" `
            -Body (@{ email = $CustomerEmail; password = "not-the-password" } | ConvertTo-Json)
    }) -eq 401
}

# ------------------------------------------------------- customer endpoints
Check "profile reads and updates" {
    $profile = Invoke-RestMethod -Uri "$BaseUrl/profile/" -Headers $script:customerHeaders
    $updated = Invoke-RestMethod -Method Put -Uri "$BaseUrl/profile/" -Headers $script:customerHeaders `
        -ContentType "application/json" -Body (@{ name = "Mohammed Adnan"; phone = "+91 98765 43210" } | ConvertTo-Json)
    $profile.user.email -eq $CustomerEmail -and $updated.user.name -eq "Mohammed Adnan"
}

Check "account details are masked" {
    $account = Invoke-RestMethod -Uri "$BaseUrl/account/" -Headers $script:customerHeaders
    $account.masked_account_number -like "XXXX XXXX *" -and $account.balance -eq 85450
}

Check "dashboard returns the documented demo numbers" {
    $dashboard = Invoke-RestMethod -Uri "$BaseUrl/dashboard/" -Headers $script:customerHeaders
    $script:dashboard = $dashboard
    $dashboard.balance -eq 85450 -and $dashboard.monthly_income -eq 45000 -and
        $dashboard.monthly_expenses -eq 18450 -and $dashboard.active_loans -eq 2 -and
        $dashboard.top_category.category -eq "Shopping" -and $dashboard.top_category.amount -eq 7200
}

Check "dashboard includes the six month trend and daily spending" {
    $script:dashboard.monthly_trend.Count -eq 6 -and $script:dashboard.daily_spending.Count -eq 14
}

Check "transactions list paginates" {
    $page = Invoke-RestMethod -Uri "$BaseUrl/transactions/" -Headers $script:customerHeaders
    $page.count -ge 20 -and $page.results.Count -eq 10 -and [bool]$page.next
}

Check "transaction search, category and type filters work" {
    $search = Invoke-RestMethod -Uri "$BaseUrl/transactions/?search=Swiggy" -Headers $script:customerHeaders
    $food = Invoke-RestMethod -Uri "$BaseUrl/transactions/?category=Food" -Headers $script:customerHeaders
    $credits = Invoke-RestMethod -Uri "$BaseUrl/transactions/?type=CREDIT" -Headers $script:customerHeaders
    $allFoodReturned = (@($food.results).Count -eq $food.count)
    $search.count -eq 1 -and $food.count -ge 2 -and $credits.count -ge 3 -and $allFoodReturned
}

Check "transaction detail loads" {
    $list = Invoke-RestMethod -Uri "$BaseUrl/transactions/?category=Shopping" -Headers $script:customerHeaders
    $detail = Invoke-RestMethod -Uri "$BaseUrl/transactions/$($list.results[0].id)/" -Headers $script:customerHeaders
    $detail.id -eq $list.results[0].id -and $detail.transaction_id -eq $list.results[0].transaction_id
}

Check "CSV export returns a file with a header" {
    $csv = Invoke-WebRequest -Uri "$BaseUrl/transactions/export/?category=Shopping" -Headers $script:customerHeaders -UseBasicParsing
    $lines = $csv.Content.Trim().Split("`n")
    $csv.Headers["Content-Type"] -like "text/csv*" -and $lines.Count -eq 5 -and $lines[0] -like "*Transaction ID*"
}

Check "loans list returns the seeded loans" {
    $loans = Invoke-RestMethod -Uri "$BaseUrl/loans/" -Headers $script:customerHeaders
    $loans.count -eq 2 -and $loans.results[0].loan_id -like "LOAN*"
}

Check "a new customer starts with no loans" {
    $loans = Invoke-RestMethod -Uri "$BaseUrl/loans/" -Headers $script:newUserHeaders
    $loans.count -eq 0
}

Check "a demo loan application is accepted and priced" {
    $body = @{
        loan_type = "PERSONAL"; amount = 200000; interest_rate = 10.5; tenure_months = 24
        purpose = "Smoke test loan"; monthly_income = 60000; employment_type = "SALARIED"
    } | ConvertTo-Json
    $loan = Invoke-RestMethod -Method Post -Uri "$BaseUrl/loans/" -Headers $script:newUserHeaders -ContentType "application/json" -Body $body
    $script:newLoanId = $loan.id
    $loan.status -eq "PENDING" -and $loan.emi -gt 0 -and $loan.remaining_amount -eq 200000
}

Check "loan detail loads" {
    $loan = Invoke-RestMethod -Uri "$BaseUrl/loans/$($script:newLoanId)/" -Headers $script:newUserHeaders
    $loan.id -eq $script:newLoanId
}

Check "EMI endpoint matches the standard formula" {
    $emi = Invoke-RestMethod -Method Post -Uri "$BaseUrl/emi/" -Headers $script:customerHeaders -ContentType "application/json" `
        -Body (@{ loan_amount = 500000; interest_rate = 9; tenure_months = 60 } | ConvertTo-Json)
    [math]::Abs($emi.monthly_emi - 10379.18) -lt 1 -and $emi.total_interest -gt 0
}

Check "notifications list, mark one read, mark all read" {
    $list = Invoke-RestMethod -Uri "$BaseUrl/notifications/" -Headers $script:newUserHeaders
    $first = $list[0]
    $one = Invoke-RestMethod -Method Put -Uri "$BaseUrl/notifications/$($first.id)/" -Headers $script:newUserHeaders `
        -ContentType "application/json" -Body (@{ is_read = $true } | ConvertTo-Json)
    $all = Invoke-RestMethod -Method Post -Uri "$BaseUrl/notifications/read-all/" -Headers $script:newUserHeaders
    $list.Count -ge 2 -and $one.is_read -eq $true -and $all.updated -ge 0
}

Check "assistant answers a balance question" {
    $chat = Invoke-RestMethod -Method Post -Uri "$BaseUrl/assistant/chat/" -Headers $script:customerHeaders `
        -ContentType "application/json" -Body (@{ message = "What is my current balance?" } | ConvertTo-Json)
    $chat.type -eq "account_balance" -and $chat.response -like "*85,450*"
}

Check "assistant answers a spending question" {
    $chat = Invoke-RestMethod -Method Post -Uri "$BaseUrl/assistant/chat/" -Headers $script:customerHeaders `
        -ContentType "application/json" -Body (@{ message = "How much did I spend this month?" } | ConvertTo-Json)
    $chat.type -eq "expense_summary" -and $chat.response -like "*18,450*"
}

Check "assistant explains a banking term" {
    $chat = Invoke-RestMethod -Method Post -Uri "$BaseUrl/assistant/chat/" -Headers $script:customerHeaders `
        -ContentType "application/json" -Body (@{ message = "Explain EMI" } | ConvertTo-Json)
    $chat.type -eq "banking_knowledge" -and $chat.response -like "*Equated Monthly Instalment*"
}

Check "assistant history is stored" {
    $history = Invoke-RestMethod -Uri "$BaseUrl/assistant/history/" -Headers $script:customerHeaders
    $history.count -ge 3 -and $history.suggestions.Count -gt 5
}

Check "change password rejects a wrong current password" {
    (Status {
        Invoke-RestMethod -Method Post -Uri "$BaseUrl/auth/change-password/" -Headers $script:customerHeaders `
            -ContentType "application/json" `
            -Body (@{ current_password = "wrong"; new_password = "Brand@New2026"; confirm_password = "Brand@New2026" } | ConvertTo-Json)
    }) -eq 400
}

Check "change password works for the throwaway account" {
    $login = Invoke-RestMethod -Method Post -Uri "$BaseUrl/auth/login/" -ContentType "application/json" `
        -Body (@{ email = $script:newUserEmail; password = "Verify@12345" } | ConvertTo-Json)
    $headers = @{ Authorization = "Bearer $($login.access)" }
    $result = Invoke-RestMethod -Method Post -Uri "$BaseUrl/auth/change-password/" -Headers $headers `
        -ContentType "application/json" `
        -Body (@{ current_password = "Verify@12345"; new_password = "Verify@98765"; confirm_password = "Verify@98765" } | ConvertTo-Json)
    $relogin = Invoke-RestMethod -Method Post -Uri "$BaseUrl/auth/login/" -ContentType "application/json" `
        -Body (@{ email = $script:newUserEmail; password = "Verify@98765" } | ConvertTo-Json)
    [bool]$result.message -and [bool]$relogin.access
}

# ------------------------------------------------------------ role boundary
Check "a customer cannot open employee endpoints" {
    (Status { Invoke-RestMethod -Uri "$BaseUrl/admin/analytics/" -Headers $script:customerHeaders }) -eq 403
}

Check "a customer cannot read the assistant monitor" {
    (Status { Invoke-RestMethod -Uri "$BaseUrl/assistant/monitor/" -Headers $script:customerHeaders }) -eq 403
}

# --------------------------------------------------------- employee endpoints
Check "employee login works" {
    $login = Invoke-RestMethod -Method Post -Uri "$BaseUrl/auth/login/" -ContentType "application/json" `
        -Body (@{ email = $AdminEmail; password = $AdminPassword } | ConvertTo-Json)
    $script:adminHeaders = @{ Authorization = "Bearer $($login.access)" }
    [bool]$login.access
}

Check "admin analytics returns totals and every chart" {
    $analytics = Invoke-RestMethod -Uri "$BaseUrl/admin/analytics/" -Headers $script:adminHeaders
    $analytics.totals.customers -ge 3 -and $analytics.totals.transactions -gt 20 -and
        $analytics.monthly_trend.Count -eq 6 -and $analytics.category_breakdown.Count -ge 4 -and
        $analytics.loan_status_breakdown.Count -eq 5
}

Check "admin overview returns the six KPI numbers" {
    $overview = Invoke-RestMethod -Uri "$BaseUrl/admin/analytics/overview/" -Headers $script:adminHeaders
    $overview.total_customers -ge 3 -and $overview.total_accounts -ge 3 -and $overview.total_loans -ge 6
}

Check "admin customer table and 360 view load" {
    $customers = Invoke-RestMethod -Uri "$BaseUrl/admin/customers/" -Headers $script:adminHeaders
    $first = $customers.results | Where-Object { $_.email -eq $CustomerEmail }
    $detail = Invoke-RestMethod -Uri "$BaseUrl/admin/customers/$($first.id)/" -Headers $script:adminHeaders
    $customers.count -ge 3 -and $detail.customer.email -eq $CustomerEmail -and $detail.accounts.Count -ge 1
}

Check "admin transaction table filters" {
    $all = Invoke-RestMethod -Uri "$BaseUrl/admin/transactions/" -Headers $script:adminHeaders
    $food = Invoke-RestMethod -Uri "$BaseUrl/admin/transactions/?category=Food" -Headers $script:adminHeaders
    $all.count -gt 20 -and $food.count -ge 1
}

Check "admin loan table filters" {
    $pending = Invoke-RestMethod -Uri "$BaseUrl/admin/loans/?status=PENDING" -Headers $script:adminHeaders
    $pending.count -ge 1
}

Check "an employee can decide a loan and the customer is notified" {
    $loan = Invoke-RestMethod -Method Patch -Uri "$BaseUrl/admin/loans/$($script:newLoanId)/" -Headers $script:adminHeaders `
        -ContentType "application/json" -Body (@{ status = "APPROVED" } | ConvertTo-Json)
    $notifications = Invoke-RestMethod -Uri "$BaseUrl/notifications/" -Headers $script:newUserHeaders
    $matches = @($notifications | Where-Object { $_.title -like "*$($loan.loan_id)*" })
    ($loan.status -eq "APPROVED") -and ($matches.Count -ge 1)
}

Check "an invalid loan status is rejected" {
    (Status {
        Invoke-RestMethod -Method Patch -Uri "$BaseUrl/admin/loans/$($script:newLoanId)/" -Headers $script:adminHeaders `
            -ContentType "application/json" -Body (@{ status = "NONSENSE" } | ConvertTo-Json)
    }) -eq 400
}

Check "admin user table loads" {
    $users = Invoke-RestMethod -Uri "$BaseUrl/admin/users/" -Headers $script:adminHeaders
    $admins = @($users.results | Where-Object { $_.role -eq "ADMIN" })
    ($users.count -ge 4) -and ($admins.Count -ge 1) -and (@($users.results).Count -eq $users.count)
}

Check "assistant monitor shows the conversations" {
    $monitor = Invoke-RestMethod -Uri "$BaseUrl/assistant/monitor/" -Headers $script:adminHeaders
    $monitor.total_messages -ge 3 -and $monitor.intent_breakdown.Count -ge 2
}

Write-Output ("-" * 62)
Write-Output "passed: $script:passed   failed: $script:failed"
if ($script:failed -gt 0) { exit 1 }
