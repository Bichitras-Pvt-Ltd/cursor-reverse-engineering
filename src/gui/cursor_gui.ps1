Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Load settings
$settingsPath = Join-Path $PSScriptRoot "..\..\config\settings.json"
$settings = Get-Content $settingsPath | ConvertFrom-Json

# Create the main form
$form = New-Object System.Windows.Forms.Form
$form.Text = 'Cursor Temp Mail Creator'
$form.Size = New-Object System.Drawing.Size(600,500)
$form.StartPosition = 'CenterScreen'
$form.BackColor = [System.Drawing.Color]::FromArgb(30, 30, 30)
$form.ForeColor = [System.Drawing.Color]::White

# Create First Name Label and TextBox
$firstNameLabel = New-Object System.Windows.Forms.Label
$firstNameLabel.Location = New-Object System.Drawing.Point(20,30)
$firstNameLabel.Size = New-Object System.Drawing.Size(120,20)
$firstNameLabel.Text = 'First Name:'
$firstNameLabel.ForeColor = [System.Drawing.Color]::White
$form.Controls.Add($firstNameLabel)

$firstNameBox = New-Object System.Windows.Forms.TextBox
$firstNameBox.Location = New-Object System.Drawing.Point(150,30)
$firstNameBox.Size = New-Object System.Drawing.Size(200,20)
$firstNameBox.Text = $settings.credentials.first_name
$firstNameBox.BackColor = [System.Drawing.Color]::FromArgb(45, 45, 45)
$firstNameBox.ForeColor = [System.Drawing.Color]::White
$form.Controls.Add($firstNameBox)

# Create Last Name Label and TextBox
$lastNameLabel = New-Object System.Windows.Forms.Label
$lastNameLabel.Location = New-Object System.Drawing.Point(20,70)
$lastNameLabel.Size = New-Object System.Drawing.Size(120,20)
$lastNameLabel.Text = 'Last Name:'
$lastNameLabel.ForeColor = [System.Drawing.Color]::White
$form.Controls.Add($lastNameLabel)

$lastNameBox = New-Object System.Windows.Forms.TextBox
$lastNameBox.Location = New-Object System.Drawing.Point(150,70)
$lastNameBox.Size = New-Object System.Drawing.Size(200,20)
$lastNameBox.Text = $settings.credentials.last_name
$lastNameBox.BackColor = [System.Drawing.Color]::FromArgb(45, 45, 45)
$lastNameBox.ForeColor = [System.Drawing.Color]::White
$form.Controls.Add($lastNameBox)

# Create Password Label and TextBox
$passwordLabel = New-Object System.Windows.Forms.Label
$passwordLabel.Location = New-Object System.Drawing.Point(20,110)
$passwordLabel.Size = New-Object System.Drawing.Size(120,20)
$passwordLabel.Text = 'Password:'
$passwordLabel.ForeColor = [System.Drawing.Color]::White
$form.Controls.Add($passwordLabel)

$passwordBox = New-Object System.Windows.Forms.TextBox
$passwordBox.Location = New-Object System.Drawing.Point(150,110)
$passwordBox.Size = New-Object System.Drawing.Size(200,20)
$passwordBox.Text = $settings.credentials.password
$passwordBox.BackColor = [System.Drawing.Color]::FromArgb(45, 45, 45)
$passwordBox.ForeColor = [System.Drawing.Color]::White
$form.Controls.Add($passwordBox)

# Create Output TextBox
$outputBox = New-Object System.Windows.Forms.TextBox
$outputBox.Location = New-Object System.Drawing.Point(20,200)
$outputBox.Size = New-Object System.Drawing.Size(540,200)
$outputBox.Multiline = $true
$outputBox.ScrollBars = 'Vertical'
$outputBox.ReadOnly = $true
$outputBox.BackColor = [System.Drawing.Color]::FromArgb(20, 20, 20)
$outputBox.ForeColor = [System.Drawing.Color]::LightGreen
$form.Controls.Add($outputBox)

# Create Generate Button
$generateButton = New-Object System.Windows.Forms.Button
$generateButton.Location = New-Object System.Drawing.Point(150,150)
$generateButton.Size = New-Object System.Drawing.Size(200,30)
$generateButton.Text = 'Generate Temp Mail'
$generateButton.BackColor = [System.Drawing.Color]::FromArgb(0, 122, 204)
$generateButton.ForeColor = [System.Drawing.Color]::White
$form.Controls.Add($generateButton)

# Create Copy Button
$copyButton = New-Object System.Windows.Forms.Button
$copyButton.Location = New-Object System.Drawing.Point(20,410)
$copyButton.Size = New-Object System.Drawing.Size(540,30)
$copyButton.Text = 'Copy to Clipboard'
$copyButton.BackColor = [System.Drawing.Color]::FromArgb(0, 122, 204)
$copyButton.ForeColor = [System.Drawing.Color]::White
$form.Controls.Add($copyButton)

# Button click event handler
$generateButton.Add_Click({
    $outputBox.Clear()
    $outputBox.AppendText("Generating temp mail...`r`n")
    
    try {
        # Run the Python script
        $pythonScript = Join-Path $PSScriptRoot "..\bot\cursor_bot.py"
        $process = Start-Process python -ArgumentList $pythonScript -NoNewWindow -PassThru -Wait
        
        # Read the credentials file
        $accountsFile = $settings.paths.accounts_file
        if (Test-Path $accountsFile) {
            $credentials = Get-Content $accountsFile -Raw
            $outputBox.AppendText("`r`nCredentials generated successfully:`r`n")
            $outputBox.AppendText($credentials)
        } else {
            $outputBox.AppendText("Error: Credentials file not found.`r`n")
        }
    }
    catch {
        $outputBox.AppendText("Error: $_`r`n")
    }
})

# Copy button click event handler
$copyButton.Add_Click({
    if ($outputBox.Text) {
        [System.Windows.Forms.Clipboard]::SetText($outputBox.Text)
        [System.Windows.Forms.MessageBox]::Show("Content copied to clipboard!", "Success", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information)
    }
})

# Show the form
$form.ShowDialog() 