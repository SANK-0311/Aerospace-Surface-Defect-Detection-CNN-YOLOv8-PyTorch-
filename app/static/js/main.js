// DOM Elements
const uploadForm = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const fileName = document.getElementById('fileName');
const uploadBtn = document.getElementById('uploadBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');

// Update file name display
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        fileName.textContent = e.target.files[0].name;
    } else {
        fileName.textContent = 'No file selected';
    }
});

// Handle form submission
uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Hide previous results/errors
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    
    // Get file
    const file = fileInput.files[0];
    if (!file) {
        showError('Please select an image file');
        return;
    }
    
    // Validate file type
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/bmp'];
    if (!validTypes.includes(file.type)) {
        showError('Invalid file type. Please upload JPG, PNG, or BMP image');
        return;
    }
    
    // Show loading
    loadingSpinner.style.display = 'block';
    uploadBtn.disabled = true;
    
    // Prepare form data
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        // Send request
        const response = await fetch('/api/predict', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Prediction failed');
        }
        
        // Display results
        displayResults(data);
        
    } catch (error) {
        showError(error.message);
    } finally {
        loadingSpinner.style.display = 'none';
        uploadBtn.disabled = false;
    }
});

function displayResults(data) {
    // Show results section
    resultsSection.style.display = 'block';
    
    // Update stats
    document.getElementById('totalDefects').textContent = data.total_detections;
    document.getElementById('inferenceTime').textContent = `${data.inference_time}s`;
    
    // Display annotated image
    const resultImage = document.getElementById('resultImage');
    resultImage.src = data.image_url;
    resultImage.alt = `Annotated: ${data.image_name}`;
    
    // Display detections table
    const detectionsBody = document.getElementById('detectionsBody');
    const noDetections = document.getElementById('noDetections');
    const detectionsTable = document.getElementById('detectionsTable');
    
    if (data.detections.length === 0) {
        detectionsTable.style.display = 'none';
        noDetections.style.display = 'block';
    } else {
        detectionsTable.style.display = 'table';
        noDetections.style.display = 'none';
        
        detectionsBody.innerHTML = '';
        
        data.detections.forEach((detection, index) => {
            const row = document.createElement('tr');
            
            const bbox = detection.bounding_box;
            const location = `(${bbox.x1.toFixed(1)}, ${bbox.y1.toFixed(1)}, ${bbox.x2.toFixed(1)}, ${bbox.y2.toFixed(1)})`;
            
            row.innerHTML = `
                <td>${index + 1}</td>
                <td><strong>${detection.class_name}</strong></td>
                <td>${(detection.confidence * 100).toFixed(2)}%</td>
                <td>${location}</td>
            `;
            
            detectionsBody.appendChild(row);
        });
    }
}

function showError(message) {
    errorSection.style.display = 'block';
    document.getElementById('errorMessage').textContent = `Error: ${message}`;
}