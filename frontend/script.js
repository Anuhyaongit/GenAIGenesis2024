// Debounce function to limit how often a function can run
function debounce(func, wait, immediate) {
    var timeout;
    return function() {
        var context = this, args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        }, wait);
        if (immediate && !timeout) func.apply(context, args);
    };
};

// Function to call the backend with language
function callBackendWithLanguage(language) {
    fetch('/generate_language', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ language: language }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // Handle the response as needed
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// Listen for input on the language field and submit after user stops typing
document.getElementById('languageInput').addEventListener('input', debounce(function() {
    const language = document.getElementById('languageInput').value;
    // Call backend with the language
    callBackendWithLanguage(language);
}, 500)); // Adjust the debounce time as necessary

// Function to call the backend with language and paragraph
function callBackend(language, paragraph) {
    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ language: language, paragraph: paragraph }),
    })
    .then(response => response.json())
    .then(data => {
        // Assuming you want to display the response somewhere
        document.getElementById('output_translation').value = data.response;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

document.getElementById('translateForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);

    // Fetch call to /generate for translation
    fetch('/generate', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('output_sentence').value = data.response; // Update the translation content
        // After handling the translation, proceed to fetch emotion analysis
        return fetch('/generate_emo', {
            method: 'POST',
            body: formData, // Assuming formData contains necessary data for emotion analysis
        });
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('output_emo').value = data.response; // Update the emotion analysis content
    })
    .catch(error => console.error('Error:', error));
});

// Clear Button event listener
document.getElementById('clearButton').addEventListener('click', function() {
    document.getElementById('translateForm').reset();
    document.getElementById('output_sentence').value = '';
    document.getElementById('output_emo').value = '';
});
