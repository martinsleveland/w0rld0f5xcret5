Write-Host "----------------------------- "
Write-Host "| Welcome to the Main Menu! |"
Write-Host "----------------------------- "
Write-Host "Pick a number from the list below:"
Write-Host "----------------------------- "
Write-Host "1. | System information"
Write-Host "2. | Network configuration"
Write-Host "3. | File management"
Write-Host "4. | Others"
Write-Host "5. | Secure information"
Write-Host "0. | Exit" 
Write-Host "----------------------------- "


# functions or scripts for each option

function fetchSystemInfo {
    Write-Host "Fetching system information..."
}

function fetchNetworkConf {
    Write-Host "Fetching system information..."
}

function fetchFiles {
    Write-Host "Fetching files..."
}

function others {
    Write-Host "Fetching Wi-Fi profiles..."
    
    # Get all Wi-Fi profiles
    $profiles = netsh wlan show profiles | Select-String "All User Profile" | ForEach-Object { $_.ToString().Split(':')[1].Trim() }
    
    # Display available profiles
    Write-Host "Available Wi-Fi profiles:"
    for ($i = 0; $i -lt $profiles.Count; $i++) {
        Write-Host "$($i + 1). $($profiles[$i])"
    }
    
    # Ask user to choose a profile
    $choice = Read-Host "Enter the number of the profile you want to see the key for (or 0 to go back)"
    
    if ($choice -eq '0') {
        return
    }
    
    $choiceIndex = [int]$choice - 1
    if ($choiceIndex -ge 0 -and $choiceIndex -lt $profiles.Count) {
        $selectedProfile = $profiles[$choiceIndex]
        Write-Host "Fetching key for profile: $selectedProfile"
        
        # Fetch and display the key for the selected profile
        $key = netsh wlan show profile name="$selectedProfile" key=clear | Select-String "Key Content"
        if ($key) {
            Write-Host $key
        } else {
            Write-Host "Unable to retrieve key for this profile."
        }
    } else {
        Write-Host "Invalid choice. Please try again."
    }
    
    Read-Host "Press Enter to continue..."
}

function secureInformation {
    Write-Host "Securing information..."
    $fromEmail = Read-Host "Enter the sedning email address: "
    $toEmail = Read-Host "Enter the reciving email address: "
    $password = Read-Host "Enter your password" -AsSecureString
    $fullCredential = New-Object System.Management.Automation.PSCredential($email, $password)

    if ($fullCredential -ne $null) {
        Write-Host "Credentials stored successfully."
        Write-Host "How would you like to proceed?"
        $choice = Read-Host "1. Email me the credentials`n2. Dropbox`n3. Exit"
        switch ($choice) {
            1 {
                Send-MailMessage `
                -From "$fromEmail" `
                -To "$toEmail" `
                -Subject "What's up?" `
                -Body "Hey, just testing some PowerShell magic. ✨" `
                -SmtpServer "smtp.yourprovider.com"

    } else {
        Write-Host "Failed to store credentials."
    }
}

$choice = Read-Host "You: "
switch ($choice) {
    1 {
        Write-Host "You chose 'System information'."
        Start-Process msinfo32
    }
    2 {
        Write-Host "You chose 'Network configuration'."
        Write-Host "Fetching network information..."
        
        # Get IP configuration
        Get-NetIPConfiguration | Format-Table InterfaceAlias, InterfaceDescription, IPv4Address, IPv6Address

        # Get network adapters
        Get-NetAdapter | Format-Table Name, InterfaceDescription, Status, LinkSpeed

        # Get DNS client server addresses
        Get-DnsClientServerAddress | Format-Table InterfaceAlias, ServerAddresses

        # Pause to allow user to read the information
        Read-Host "Press Enter to continue..."
    }
    3 {
        Write-Host "You chose 'File management'."
    }
    4 {
        Write-Host "You chose 'Others'."
        others
    }
    5 {
        Write-Host "You chose 'Secure information'."
        others
    }
    0 {
        Write-Host "Exitting the program. Goodbye!"
        exit
    }
    default {
        Write-Host "invalid choice, please try again."
    }
}
