const express = require('express');
const axios = require('axios');
const validUrl = require('valid-url');
const apicache = require('apicache');
const cache = apicache.middleware;

const app = express();
const port = 5000; 

app.use(cache('5 ms'));
app.get('/get_api/numbers', async (req, res) => {
    const urls = Array.isArray(req.query.url) ? req.query.url : [req.query.url];
    let numbers = [];


    for (let url of urls) {
        if (validUrl.isUri(url)) {
            try {
                const response = await axios.get(url, { timeout: 500 });
                numbers = numbers.concat(response.data.numbers);
            } catch (error) {
                console.log(`Failed to fetch data from ${url}`);
            }
        }
    }


    numbers = [...new Set(numbers)].sort((a, b) => a - b);
    const numbersString = numbers.join(',');

    res.json({ numbers: numbersString });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
