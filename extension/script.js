const p1Input = document.getElementById('product1url');
const p2Input = document.getElementById('product2url');
const compareButton = document.getElementById('compare-button');
const p1Button = document.getElementById('p1');
const p2Button = document.getElementById('p2');
const closeButton = document.getElementById('close-button');
const message = document.getElementById('compare-message');

function enableCompareButtonIfBothFieldsAreFilled() {
    try {
        // Enable the compare button if both fields are filled
        if (p1Input.value != '' && p2Input.value != '') {
            console.log('Fields are filled!');    
            compareButton.disabled = false;
            compareButton.classList.replace('bg-gray-200', 'bg-black');
            compareButton.classList.add('hover:bg-indigo-500');
        } else {
            console.log('Fields are empty!');    
            compareButton.disabled = true;
            compareButton.classList.replace('bg-black', 'bg-gray-200');
            compareButton.classList.remove('hover:bg-indigo-500');
        }
    } catch (error) {
        console.log(error);
    }
}

function getProducturl(index, url){
    try {
        // Store the URL in the appropriate input field
        if (index === 1){
            p1Input.value = url;
            storeData(1, url);
        } else if (index === 2){
            p2Input.value = url;
            storeData(2, url);
        }
        enableCompareButtonIfBothFieldsAreFilled();
    } catch (error) {
        console.log(error);
    }
}

async function getTab(index) {
    let [tab] = await chrome.tabs.query({active: true, currentWindow: true});
    chrome.scripting.executeScript({
        // Target the current tab
        target: {tabId: tab.id},
        function: getProducturl(index, tab.url),
        args: [index]
    });
}

function storeData(index, value) {
    console.log('Storing data');
    // Store the data in the local storage
    if (index === 1){
        chrome.storage.local.set({'product1url': value});
    } else if (index === 2){
        chrome.storage.local.set({'product2url': value});
    }
    enableCompareButtonIfBothFieldsAreFilled();
}

function loadStoredData() {
    // Load the stored data if available on page load
    chrome.storage.local.get(['product1url', 'product2url', 'message'], 
        (result) => {
            p1Input.value = result.product1url === undefined ? '' : result.product1url;
            p2Input.value = result.product2url === undefined ? '' : result.product2url;
            message.classList.add('text-green-500');
            message.textContent = result.message === undefined ? '' : result.message;
            enableCompareButtonIfBothFieldsAreFilled();
        });
}

async function fetchComparisonData(){
    const product1url = p1Input.value;
    const product2url = p2Input.value;

    message.textContent = 'Comparing...';
    message.classList.add('text-blue-500');

    // Fetch data from the API
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/compare?product1url=${product1url}&product2url=${product2url}`,
            {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        console.log(data.message);

        chrome.storage.local.set({'message': data.message});

    } catch (error) {
        console.error('Error fetching data:', error);
        message.textContent = 'Error fetching data';
    }
}

// Event Listener for submitting the form
document.getElementById('compare-form').addEventListener('submit', fetchComparisonData);

// Event Listeners for auto-filling the product URLs
p1Button.addEventListener('click', () => getTab(1));
p2Button.addEventListener('click', () => getTab(2));

// Event Listeners for storing the data
p1Input.addEventListener('input', () => storeData(1, p1Input.value));
p2Input.addEventListener('input', () => storeData(2, p2Input.value));


// Close window and clear data
closeButton.addEventListener('click', () => { 
    chrome.storage.local.clear();
    p1Input.value = '';
    p2Input.value = '';
    window.close();
});

// Run these functions when the extension is opened/clicked


loadStoredData();