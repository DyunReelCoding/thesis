function extractWebsiteFeatures() {
    // Extract website features
    let websiteFeatures = {
        ransomware: {
            fileDownloadBehavior: getFileDownloadBehavior(),
            encryptionPatterns: getEncryptionPatterns(),
            networkProtocols: getNetworkProtocols(),
            fileSystemActivities: getFileSystemActivities()
        },
        phishing: {
            urlStructure: extractURLStructure(),
            domainReputation: checkDomainReputation(),
            htmlContent: analyzeHTMLContent(),
            sslCertificates: checkSSLCertificates(),
            phishingKeywords: checkPhishingKeywords()
        },
        trojan: {
            networkTrafficAnomalies: analyzeNetworkTraffic(),
            systemCallPatterns: analyzeSystemCalls(),
            fileSystemModifications: checkFileSystemModifications(),
            processBehavior: analyzeProcessBehavior(),
            registryChanges: checkRegistryChanges()
        }
    };

    return websiteFeatures;
}


// Load the trained models
let rfModel = loadRandomForestModel(); // Load random forest model
let lgbmModel = loadLGBMModel(); // Load LGBM model
let xgBoostModel = loadXGBoostModel(); // Load XGBoost model

// Function to display a warning message with options to continue or go back
function displayWarning(message, continueCallback) {
    // Create a modal overlay
    let overlay = document.createElement("div");
    overlay.classList.add("overlay");

    // Create a dialog box
    let dialog = document.createElement("div");
    dialog.classList.add("dialog");

    // Create a message element
    let messageElement = document.createElement("p");
    messageElement.textContent = message;

    // Create "Continue" button
    let continueButton = document.createElement("button");
    continueButton.textContent = "Continue";
    continueButton.onclick = function() {
        // Remove the overlay and dialog box
        overlay.remove();
        dialog.remove();
        // Execute the callback function to continue
        continueCallback();
    };

    // Create "Go Back" button
    let goBackButton = document.createElement("button");
    goBackButton.textContent = "Go Back";
    goBackButton.onclick = function() {
        // Remove the overlay and dialog box
        overlay.remove();
        dialog.remove();
        // Go back to the previous page
        history.back();
    };

    // Append elements to the dialog box
    dialog.appendChild(messageElement);
    dialog.appendChild(continueButton);
    dialog.appendChild(goBackButton);

    // Append the dialog box to the overlay
    overlay.appendChild(dialog);

    // Append the overlay to the body
    document.body.appendChild(overlay);
}
// Function to validate website features against the models
function validateWebsiteFeatures(websiteFeatures) {
    // Use the trained models to validate website features
    let ransomwarePrediction = rfModel.predict(websiteFeatures.ransomware);
    let phishingPrediction = lgbmModel.predict(websiteFeatures.phishing);
    let trojanPrediction = xgBoostModel.predict(websiteFeatures.trojan);

    // Display the matched result
    if (ransomwarePrediction === 1) {
        alert("The website matches ransomware detection.");
    } else if (phishingPrediction === 1) {
        alert("The website matches phishing detection.");
    } else if (trojanPrediction === 1) {
        alert("The website matches trojan detection.");
    } else {
        alert("The website does not match any detection criteria.");
    }
}

// Execute the function to extract website features and validate against the models when the page loads
window.onload = function() {
    let websiteFeatures = extractWebsiteFeatures();
    validateWebsiteFeatures(websiteFeatures);
};
