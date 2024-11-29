const express = require('express');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const port = 80;

let pythonProcess; // Variable to store the Python process

// Serve the index.html file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Define a route to start the Python script
app.get('/startScript', (req, res) => {
    // Check if Python script is already running
    if (pythonProcess) {
        res.status(400).send('Python script is already running!');
        return;
    }
    
    // Start the Python script
    pythonProcess = spawn('python3', ['main.py']);

    pythonProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`Python script exited with code ${code}`);
        pythonProcess = null; // Reset the Python process variable
    });

    res.send('Python script has started!');
});

// Define a route to stop the Python script
app.get('/stopScript', (req, res) => {
    // Check if Python script is running
    if (!pythonProcess) {
        res.status(400).send('Python script is not running!');
        return;
    }
    
    // Send SIGINT signal to gracefully terminate the Python process
    pythonProcess.kill('SIGINT');

    // Reset the Python process variable
    pythonProcess = null;

    res.send('Python script has been stopped!');
});

// Start the server
app.listen(port, () => {
    console.log(`Server is listening at http://localhost:${port}`);
});