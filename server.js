const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();

const IMAGES_ROOT_DIR = path.join(__dirname, 'images');
const DISPLAY_IMAGES_DIR = path.join(IMAGES_ROOT_DIR, 'display');

app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

app.use('/images', express.static(IMAGES_ROOT_DIR));
app.use('/images/display', express.static(DISPLAY_IMAGES_DIR));

const getFilesRecursive = (directory) => {
    let results = [];
    const files = fs.readdirSync(directory);

    for (const file of files) {
        const filePath = path.join(directory, file);
        const stat = fs.statSync(filePath);

        if (stat && stat.isDirectory()) {
            results = results.concat(getFilesRecursive(filePath));
        } else if (['.jpeg', '.jpg', '.png', '.gif'].includes(path.extname(file).toLowerCase())) {
            results.push(path.relative(DISPLAY_IMAGES_DIR, filePath));
        }
    }

    return results;
};

app.get('/get-images', (req, res) => {
    try {
        const imageFiles = getFilesRecursive(DISPLAY_IMAGES_DIR);
        res.json(imageFiles);
    } catch (err) {
        console.error('Error reading image files:', err);
        return res.status(500).send('Server error');
    }
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public/contact.html'));
});

app.post('/submit-message', (req, res) => {
    const { name, email, message } = req.body;

    const messageToSave = `
----------------------------------------
Name: ${name}
Email: ${email}
Message: 
${message}
----------------------------------------
    `;

    fs.appendFile(path.join(__dirname, 'messages.txt'), messageToSave, (err) => {
        if (err) {
            console.error("Error saving message:", err);
            return res.status(500).send('Failed to save message. Try again later.');
        }

        res.send('Message sent successfully!');
    });
});

app.listen(3000, () => {
    console.log('Server started on http://localhost:3000');
});

